from sqlalchemy.orm import Session

from app.models.log_models import (
    FTPLog,
    HTTPSLog,
    OctopusLog,
    RDPLog,
    SQLILog,
    SSHLog,
)

LOG_TABLES = [
    FTPLog,
    HTTPSLog,
    OctopusLog,
    RDPLog,
    SQLILog,
    SSHLog,
]


def extract_source_ip(document: dict) -> str | None:
    """
    Extract source IP from different log formats.
    """

    public = document.get("public", {})

    if isinstance(public, dict):
        source = public.get("source", {})

        if isinstance(source, dict):
            ip = source.get("ip")

            if ip:
                return ip

    for key in (
        "src_ip",
        "source_ip",
        "ip",
        "client_ip",
        "remote_ip",
    ):
        ip = document.get(key)

        if ip:
            return ip

    return None


def investigate_ip(
    db: Session,
    ip_address: str,
):
    """
    Investigate an IP address across all available log datasets.
    """

    total_events = 0
    datasets = []

    for table in LOG_TABLES:

        rows = db.query(table.document).all()

        table_count = 0

        for (document,) in rows:

            source_ip = extract_source_ip(document)

            if source_ip != ip_address:
                continue

            table_count += 1

        if table_count > 0:

            datasets.append(table.__tablename__)

            total_events += table_count

    return {
        "source_ip": ip_address,
        "event_count": total_events,
        "first_seen": None,
        "last_seen": None,
        "datasets": datasets,
        "protocols": [],
        "usernames": [],
        "paths": [],
        "commands": [],
        "payloads": [],
    }