import re

# --------------------------------------------------
# Dataset Mapping
# --------------------------------------------------

DATASET_KEYWORDS = {
    "ssh": "ssh_logs",
    "ftp": "ftp_logs",
    "https": "https_logs",
    "http": "https_logs",
    "rdp": "rdp_logs",
    "sql injection": "sqli_logs",
    "sqli": "sqli_logs",
    "octopus": "octopus_logs",
}

# --------------------------------------------------
# Protocol Mapping
# --------------------------------------------------

PROTOCOL_KEYWORDS = {
    "ssh": "SSH",
    "ftp": "FTP",
    "https": "HTTP/s",
    "http": "HTTP/s",
    "rdp": "RDP",
    "sip": "SipSession",
    "octopus": "SipSession",
}

# --------------------------------------------------
# Common Usernames
# --------------------------------------------------

COMMON_USERNAMES = [
    "root",
    "administrator",
    "admin",
    "anonymous",
    "guest",
    "ubuntu",
    "oracle",
    "postgres",
    "mysql",
]

# --------------------------------------------------
# Status Mapping
# --------------------------------------------------

STATUS_KEYWORDS = {
    "failed": "failure",
    "failure": "failure",
    "successful": "success",
    "success": "success",
    "completed": "completed",
}

# --------------------------------------------------
# Attack Types
# --------------------------------------------------

ATTACK_TYPES = {
    "sql injection": "SQL Injection",
    "sqli": "SQL Injection",
    "brute force": "Brute Force Attack",
    "recon": "Reconnaissance",
    "reconnaissance": "Reconnaissance",
}

# --------------------------------------------------
# Highest Keywords
# --------------------------------------------------

HIGHEST_KEYWORDS = [
    "highest",
    "most",
    "largest",
    "maximum",
    "top",
]


def extract_entities(query: str) -> dict:
    """
    Extract structured entities from a natural-language query.

    Returns a dictionary containing only detected entities.
    """

    query = query.lower().strip()

    entities = {}

    # --------------------------------------------------
    # IP Address
    # --------------------------------------------------

    ip_match = re.search(
        r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
        query,
    )

    if ip_match:
        entities["ip"] = ip_match.group()

    # --------------------------------------------------
    # Result Limit
    # --------------------------------------------------

    limit_match = re.search(
        r"\b(?:top|first|last|show)\s+(\d+)\b",
        query,
    )

    if limit_match:
        entities["limit"] = int(limit_match.group(1))

    else:
        entities["limit"] = 50

    # --------------------------------------------------
    # Dataset
    # --------------------------------------------------

    for keyword, dataset in DATASET_KEYWORDS.items():

        if keyword in query:
            entities["dataset"] = dataset
            break

    # --------------------------------------------------
    # Protocol
    # --------------------------------------------------

    for keyword, protocol in PROTOCOL_KEYWORDS.items():

        if keyword in query:
            entities["protocol"] = protocol
            break

    # --------------------------------------------------
    # Username
    # --------------------------------------------------

    for username in COMMON_USERNAMES:

        pattern = rf"\b{re.escape(username)}\b"

        if re.search(pattern, query):
            entities["username"] = username
            break

    # --------------------------------------------------
    # Status
    # --------------------------------------------------

    for keyword, status in STATUS_KEYWORDS.items():

        if keyword in query:
            entities["status"] = status
            break

    # --------------------------------------------------
    # Attack Type
    # --------------------------------------------------

    for keyword, attack_type in ATTACK_TYPES.items():

        if keyword in query:
            entities["event_type"] = attack_type
            break

    # --------------------------------------------------
    # Highest Only
    # --------------------------------------------------

    if any(word in query for word in HIGHEST_KEYWORDS):

        if (
            "event" in query
            or "dataset" in query
            or "protocol" in query
        ):
            entities["highest_only"] = True

    return entities