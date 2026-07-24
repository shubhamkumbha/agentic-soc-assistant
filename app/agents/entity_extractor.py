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
# Usernames
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

TOP_WORDS = {
    "top",
    "highest",
    "largest",
    "maximum",
    "most",
}


def extract_entities(query: str) -> dict:
    """
    Extract structured entities from natural language.
    """

    query = query.lower().strip()

    entities = {}

    # ---------------- IP ----------------

    ip = re.search(
        r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
        query,
    )

    if ip:
        entities["ip"] = ip.group()

    # ---------------- LIMIT ----------------

    limit = re.search(
        r"\b(?:top|first|last|show)\s+(\d+)\b",
        query,
    )

    entities["limit"] = int(limit.group(1)) if limit else 5

    # ---------------- DATASET ----------------

    for keyword, dataset in DATASET_KEYWORDS.items():
        if keyword in query:
            entities["dataset"] = dataset
            break

    # ---------------- PROTOCOL ----------------

    for keyword, protocol in PROTOCOL_KEYWORDS.items():
        if keyword in query:
            entities["protocol"] = protocol
            break

    # ---------------- USERNAME ----------------

    for username in COMMON_USERNAMES:
        if re.search(rf"\b{username}\b", query):
            entities["username"] = username
            break

    # ---------------- STATUS ----------------

    for keyword, value in STATUS_KEYWORDS.items():
        if keyword in query:
            entities["status"] = value
            break

    # ---------------- EVENT TYPE ----------------

    for keyword, attack in ATTACK_TYPES.items():
        if keyword in query:
            entities["event_type"] = attack
            break

    # ---------------- Dataset Summary ----------------

    entities["highest_only"] = (
        any(word in query for word in TOP_WORDS)
        and (
            "dataset" in query
            or "datasets" in query
            or "protocol" in query
            or "protocols" in query
            or "event count" in query
            or "number of events" in query
            or "events" in query
        )
    )

    return entities