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


def matches_filters(event: dict, filters: dict) -> bool:
    """
    Check whether a normalized event satisfies all requested filters.
    """

    # -----------------------------
    # Dataset
    # -----------------------------

    dataset = filters.get("dataset")

    if dataset and event["dataset"] != dataset:
        return False

    # -----------------------------
    # Source IP
    # -----------------------------

    ip = filters.get("ip")

    if ip and event["source_ip"] != ip:
        return False

    # -----------------------------
    # Username
    # -----------------------------

    username = filters.get("username")

    if username:

        if not event["username"]:
            return False

        if event["username"].lower() != username.lower():
            return False

    # -----------------------------
    # Protocol
    # -----------------------------

    protocol = filters.get("protocol")

    if protocol:

        if not event["protocol"]:
            return False

        if protocol.lower() not in event["protocol"].lower():
            return False

    return True


def search_security_events(
    db: Session,
    filters: dict,
    limit: int = 50,
):
    """
    Search normalized security events using structured filters.
    """

    results = []

    for table in LOG_TABLES:

        rows = (
            db.query(table.document)
            .all()
        )

        for (document,) in rows:

            event = normalize_log(
                document=document,
                dataset=table.__tablename__,
            )

            if not matches_filters(event, filters):
                continue

            results.append(event)

            if len(results) >= limit:
                return results

    return results