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
    Result returned by the intent classifier.
    """

    intent: Intent
    parameters: dict


def classify_intent(query: str) -> ClassificationResult:
    """
    Classify the user's intent.

    Entity extraction is performed first.
    Intent classification then uses both the
    extracted entities and the original query.
    """

    query = query.lower().strip()

    entities = extract_entities(query)

    # --------------------------------------------------
    # Top Attackers
    # --------------------------------------------------

    if (
        "attacker" in query
        or "attackers" in query
        or "top ip" in query
        or "top ips" in query
    ):
        return ClassificationResult(
            intent=Intent.TOP_ATTACKERS,
            parameters=entities,
        )

    # --------------------------------------------------
    # Investigate IP
    # --------------------------------------------------

    if (
        "investigate" in query
        or "lookup" in query
        or "trace" in query
        or (
            "ip" in entities
            and "activity" not in query
            and "events" not in query
            and "logs" not in query
        )
    ):
        return ClassificationResult(
            intent=Intent.INVESTIGATE_IP,
            parameters=entities,
        )

    # --------------------------------------------------
    # Protocol Summary
    # --------------------------------------------------

    if entities.get("highest_only"):

        return ClassificationResult(
            intent=Intent.PROTOCOL_SUMMARY,
            parameters=entities,
        )

    if (
        "protocol summary" in query
        or "dataset summary" in query
        or "summary" == query
    ):

        return ClassificationResult(
            intent=Intent.PROTOCOL_SUMMARY,
            parameters=entities,
        )

    # --------------------------------------------------
    # Event Search
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

    if (
        "activity" in query
        or "events" in query
        or "logs" in query
        or "search" in query
    ):

        return ClassificationResult(
            intent=Intent.EVENT_SEARCH,
            parameters=entities,
        )

    # --------------------------------------------------
    # Unknown
    # --------------------------------------------------

    return ClassificationResult(
        intent=Intent.UNKNOWN,
        parameters=entities,
    )