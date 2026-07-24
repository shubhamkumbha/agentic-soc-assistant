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


def get_protocol_summary(db):
    """
    Return event counts grouped by dataset.
    """

    summary = []

    for table in LOG_TABLES:

        count = db.query(table).count()

        summary.append(
            {
                "dataset": table.__tablename__,
                "event_count": count,
            }
        )

    summary.sort(
        key=lambda item: item["event_count"],
        reverse=True,
    )

    if not summary:
        return {
            "data": [],
            "limitations": [
                "Protocol summary information is unavailable in the supplied dataset.",
            ],
        }

    return {
        "data": summary,
        "limitations": [],
    }