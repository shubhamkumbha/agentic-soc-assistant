from sqlalchemy.orm import Session

from app.agents.intent_classifier import (
    Intent,
    classify_intent,
)
from app.tools.ip_investigation import investigate_ip
from app.tools.top_attackers import get_top_attackers


def process_query(
    query: str,
    db: Session,
):
    """
    Main entry point for the SOC Agent.
    """

    intent = classify_intent(query)

    # -------------------------------------------------
    # Tool 1 - Top Attackers
    # -------------------------------------------------

    if intent == Intent.TOP_ATTACKERS:

        data = get_top_attackers(db)

        return {
            "status": "success",
            "intent": intent.value,
            "tools_used": [
                "get_top_attackers",
            ],
            "summary": "Top attacking IP addresses retrieved successfully.",
            "data": data,
            "limitations": [],
        }

    # -------------------------------------------------
    # Tool 2 - Investigate IP
    # -------------------------------------------------

    if intent == Intent.INVESTIGATE_IP:

        ip_address = None

        for word in query.split():

            word = word.strip(",.?!")

            # Very simple IPv4 detection
            if word.count(".") == 3:
                ip_address = word
                break

        if not ip_address:

            return {
                "status": "error",
                "intent": intent.value,
                "tools_used": [],
                "summary": "No IP address found in the query.",
                "data": [],
                "limitations": [
                    "Please provide a valid IP address.",
                ],
            }

        result = investigate_ip(
            db=db,
            ip_address=ip_address,
        )

        return {
            "status": "success",
            "intent": intent.value,
            "tools_used": [
                "investigate_ip",
            ],
            "summary": f"Investigation completed for {ip_address}.",
            "data": result,
            "limitations": [],
        }

    # -------------------------------------------------
    # Unknown Intent
    # -------------------------------------------------

    return {
        "status": "success",
        "intent": intent.value,
        "tools_used": [],
        "summary": "Intent not implemented yet.",
        "data": [],
        "limitations": [
            "This intent will be implemented in a later step.",
        ],
    }