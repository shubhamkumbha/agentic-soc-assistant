from typing import Any


def normalize_log(
    document: dict,
    dataset: str,
) -> dict[str, Any]:
    """
    Normalize heterogeneous log documents into a common structure.

    Every tool in the SOC Assistant should operate on this structure
    instead of raw dataset-specific documents.
    """

    public = document.get("public", {})
    private = document.get("private", {})

    source_ip = None
    destination_ip = None

    # --------------------------------------------------
    # Public Source / Destination
    # --------------------------------------------------

    if isinstance(public, dict):

        source = public.get("source", {})

        if isinstance(source, dict):
            source_ip = source.get("ip")

        destination = public.get("destination", {})

        if isinstance(destination, dict):
            destination_ip = destination.get("ip")

    # --------------------------------------------------
    # Private Source / Destination (RDP)
    # --------------------------------------------------

    if source_ip is None and isinstance(private, dict):

        source = private.get("source", {})

        if isinstance(source, dict):
            source_ip = source.get("ip")

        destination = private.get("destination", {})

        if isinstance(destination, dict):
            destination_ip = destination.get("ip")

    # --------------------------------------------------
    # Timestamp
    # --------------------------------------------------

    timestamp = None

    ts = document.get("timestamp")

    if isinstance(ts, dict):
        timestamp = ts.get("$date")
    else:
        timestamp = ts

    # --------------------------------------------------
    # Path / Payload
    # --------------------------------------------------

    path = (
        document.get("ftp_path")
        or document.get("payload")
    )

    # --------------------------------------------------
    # Return Normalized Structure
    # --------------------------------------------------

    return {
        "dataset": dataset,
        "source_ip": source_ip,
        "destination_ip": destination_ip,
        "timestamp": timestamp,
        "protocol": document.get("protocol"),
        "username": document.get("username"),
        "status": document.get("status"),
        "connection_status": document.get("connection_status"),
        "event_type": (
            document.get("mitre", {})
            .get("attack_type")
            if isinstance(document.get("mitre"), dict)
            else None
        ),
        "command": document.get("command"),
        "path": path,
        "payload": document.get("payload"),
        "trace_id": document.get("trace_id"),
        "raw": document,
    }