from dataclasses import dataclass
from enum import Enum

from app.agents.entity_extractor import extract_entities


class Intent(str, Enum):
    TOP_ATTACKERS = "get_top_attackers"
    INVESTIGATE_IP = "investigate_ip"
    PROTOCOL_SUMMARY = "get_protocol_summary"
    EVENT_SEARCH = "search_security_events"
    UNKNOWN = "unknown"


@dataclass
class ClassificationResult:
    """
    Output of the Intent Classifier.
    """

    intent: Intent
    parameters: dict


# --------------------------------------------------
# Keyword Groups
# --------------------------------------------------

TOP_ATTACKER_WORDS = [
    "top attacker",
    "top attackers",
    "most active attacker",
    "most active attackers",
    "attacking ip",
    "attacking ips",
    "attacking ip address",
    "attacking ip addresses",
    "top attacking",
    "source ip",
    "source ips",
]

INVESTIGATION_WORDS = [
    "investigate",
    "investigation",
    "lookup",
    "trace",
    "details",
    "information",
]

SUMMARY_WORDS = [
    "protocol summary",
    "dataset summary",
    "summary",
]

EVENT_SEARCH_WORDS = [
    "events",
    "event",
    "logs",
    "log",
    "activity",
    "activities",
    "search",
]


def classify_intent(query: str) -> ClassificationResult:
    """
    Rule-based intent classification.

    Priority:

    1. Multi-step workflow
    2. Investigate IP
    3. Top Attackers
    4. Protocol Summary
    5. Event Search
    """

    query = query.lower().strip()

    entities = extract_entities(query)

    # --------------------------------------------------
    # 1. MULTI STEP WORKFLOW
    # --------------------------------------------------

    if (
        "most active attacker" in query
        and "investigate" in query
    ):

        return ClassificationResult(
            intent=Intent.TOP_ATTACKERS,
            parameters=entities,
        )

    # --------------------------------------------------
    # 2. INVESTIGATE IP
    # --------------------------------------------------

    if entities.get("ip"):

        if (
            any(word in query for word in INVESTIGATION_WORDS)
            or (
                "activity" not in query
                and "events" not in query
                and "logs" not in query
            )
        ):

            return ClassificationResult(
                intent=Intent.INVESTIGATE_IP,
                parameters=entities,
            )

    # --------------------------------------------------
    # 3. TOP ATTACKERS
    # --------------------------------------------------

    if any(word in query for word in TOP_ATTACKER_WORDS):

        return ClassificationResult(
            intent=Intent.TOP_ATTACKERS,
            parameters=entities,
        )

    if (
        "attacker" in query
        or "attackers" in query
    ):

        return ClassificationResult(
            intent=Intent.TOP_ATTACKERS,
            parameters=entities,
        )

    # --------------------------------------------------
    # 4. PROTOCOL SUMMARY
    # --------------------------------------------------

    if entities.get("highest_only"):

        return ClassificationResult(
            intent=Intent.PROTOCOL_SUMMARY,
            parameters=entities,
        )

    if any(word in query for word in SUMMARY_WORDS):

        return ClassificationResult(
            intent=Intent.PROTOCOL_SUMMARY,
            parameters=entities,
        )

    # --------------------------------------------------
    # 5. EVENT SEARCH
    # --------------------------------------------------

    if any(
        key in entities
        for key in (
            "dataset",
            "protocol",
            "username",
            "status",
            "event_type",
        )
    ):

        return ClassificationResult(
            intent=Intent.EVENT_SEARCH,
            parameters=entities,
        )

    if any(word in query for word in EVENT_SEARCH_WORDS):

        return ClassificationResult(
            intent=Intent.EVENT_SEARCH,
            parameters=entities,
        )

    # --------------------------------------------------
    # UNKNOWN
    # --------------------------------------------------

    return ClassificationResult(
        intent=Intent.UNKNOWN,
        parameters=entities,
    )