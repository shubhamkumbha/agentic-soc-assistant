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
    Extract the source IP from different log formats.

    Supports both nested and flat JSON structures.
    """

    # ---------- Nested structure ----------
    public = document.get("public", {})

    if isinstance(public, dict):
        source = public.get("source", {})

        if isinstance(source, dict):
            ip = source.get("ip")
            if ip:
                return ip

    # ---------- Flat structure ----------
    for key in [
        "src_ip",
        "source_ip",
        "ip",
        "client_ip",
        "remote_ip",
    ]:
        ip = document.get(key)

        if ip:
            return ip

    return None


def get_top_attackers(
    db: Session,
    limit: int = 5,
):
    """
    Return the most active attacking IP addresses
    across all supported log datasets.
    """

    ip_counts: dict[str, int] = {}

    for table in LOG_TABLES:

        rows = db.query(table.document).all()

        for (document,) in rows:

            ip = extract_source_ip(document)

            if not ip:
                continue

            ip_counts[ip] = (
                ip_counts.get(ip, 0) + 1
            )

    ranked = sorted(
        ip_counts.items(),
        key=lambda item: item[1],
        reverse=True,
    )

    return [
        {
            "source_ip": ip,
            "event_count": count,
        }
        for ip, count in ranked[:limit]
    ]