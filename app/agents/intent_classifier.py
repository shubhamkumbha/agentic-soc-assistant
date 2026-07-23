from enum import Enum


class Intent(str, Enum):
    TOP_ATTACKERS = "get_top_attackers"
    INVESTIGATE_IP = "investigate_ip"
    PROTOCOL_SUMMARY = "get_protocol_summary"
    EVENT_SEARCH = "search_security_events"
    UNKNOWN = "unknown"


TOP_ATTACKERS_KEYWORDS = [
    "top attacker",
    "top attackers",
    "top ip",
    "top ips",
    "top attacking",
    "most active",
    "most attacks",
    "highest attacks",
]

INVESTIGATE_IP_KEYWORDS = [
    "investigate",
    "lookup",
    "details",
    "trace",
]

PROTOCOL_SUMMARY_KEYWORDS = [
    "protocol",
    "summary",
    "protocol summary",
    "dataset summary",
]

EVENT_SEARCH_KEYWORDS = [
    "search",
    "find",
    "event",
    "events",
]


def contains_any(text: str, keywords: list[str]) -> bool:
    return any(keyword in text for keyword in keywords)


def classify_intent(query: str) -> Intent:
    """
    Rule-based intent classifier.
    """

    query = query.lower().strip()

    # -----------------------------
    # Top Attackers
    # -----------------------------
    if (
        contains_any(query, TOP_ATTACKERS_KEYWORDS)
        or (
            "top" in query
            and (
                "attacker" in query
                or "attackers" in query
                or "ip" in query
                or "ips" in query
            )
        )
    ):
        return Intent.TOP_ATTACKERS

    # -----------------------------
    # Investigate IP
    # -----------------------------
    if (
        contains_any(query, INVESTIGATE_IP_KEYWORDS)
        and ("ip" in query)
    ):
        return Intent.INVESTIGATE_IP

    # -----------------------------
    # Protocol Summary
    # -----------------------------
    if contains_any(query, PROTOCOL_SUMMARY_KEYWORDS):
        return Intent.PROTOCOL_SUMMARY

    # -----------------------------
    # Event Search
    # -----------------------------
    if contains_any(query, EVENT_SEARCH_KEYWORDS):
        return Intent.EVENT_SEARCH

    return Intent.UNKNOWN