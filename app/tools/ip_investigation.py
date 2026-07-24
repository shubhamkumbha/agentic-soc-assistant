from sqlalchemy.orm import Session

from app.models.log_models import (
    FTPLog,
    HTTPSLog,
    OctopusLog,
    RDPLog,
    SQLILog,
    SSHLog,
)
from app.utils.log_normalizer import normalize_log

LOG_TABLES = [
    FTPLog,
    HTTPSLog,
    OctopusLog,
    RDPLog,
    SQLILog,
    SSHLog,
]


def investigate_ip(
    db: Session,
    ip_address: str,
):
    """
    Investigate an IP across every supported dataset.
    Uses normalized log events instead of dataset-specific parsing.
    """

    total_events = 0

    first_seen = None
    last_seen = None

    datasets = set()
    protocols = set()
    usernames = set()
    paths = set()
    commands = set()
    payloads = set()

    for table in LOG_TABLES:

        rows = db.query(table.document).all()

        for (document,) in rows:

            event = normalize_log(
                document=document,
                dataset=table.__tablename__,
            )

            if event["source_ip"] != ip_address:
                continue

            total_events += 1

            datasets.add(event["dataset"])

            if event["protocol"]:
                protocols.add(event["protocol"])

            if event["username"]:
                usernames.add(event["username"])

            if event["path"]:
                paths.add(event["path"])

            if event["command"]:
                commands.add(event["command"])

            if event["payload"]:
                payloads.add(event["payload"])

            timestamp = event["timestamp"]

            if timestamp:

                if first_seen is None or timestamp < first_seen:
                    first_seen = timestamp

                if last_seen is None or timestamp > last_seen:
                    last_seen = timestamp

    return {
        "source_ip": ip_address,
        "event_count": total_events,
        "first_seen": first_seen,
        "last_seen": last_seen,
        "datasets": sorted(datasets),
        "protocols": sorted(protocols),
        "usernames": sorted(usernames),
        "paths": sorted(paths),
        "commands": sorted(commands),
        "payloads": sorted(payloads),
    }