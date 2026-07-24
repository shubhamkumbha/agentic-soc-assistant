from sqlalchemy.orm import Session

from app.agents.intent_classifier import Intent
from app.agents.query_analyzer import analyze_query
from app.tools.ip_investigation import investigate_ip
from app.tools.protocol_summary import get_protocol_summary
from app.tools.search_security_events import search_security_events
from app.tools.top_attackers import get_top_attackers


def process_query(
    query: str,
    db: Session,
):
    """
    Main entry point for the SOC Agent.

    Responsibilities:
    - Receive a QueryPlan from the Query Analyzer
    - Execute the required tool(s)
    - Build a standardized API response
    """

    # --------------------------------------------
    # Analyze the natural language query
    # --------------------------------------------

    plan = analyze_query(query)

    intent = Intent(plan.intent)
    params = plan.parameters

    # --------------------------------------------
    # Top Attackers
    # --------------------------------------------

    if intent == Intent.TOP_ATTACKERS:

        limit = params.get("limit", 5)

        data = get_top_attackers(
            db=db,
            limit=limit,
        )

        return {
            "status": "success",
            "intent": intent.value,
            "tools_used": plan.tools,
            "summary": f"Top {len(data)} attacking IP addresses identified.",
            "data": data,
            "limitations": [],
        }

    # --------------------------------------------
    # Investigate IP
    # --------------------------------------------

    if intent == Intent.INVESTIGATE_IP:

        ip = params.get("ip")

        if not ip:
            return {
                "status": "failed",
                "intent": intent.value,
                "tools_used": [],
                "summary": "No IP address was found in the query.",
                "data": {},
                "limitations": [
                    "Please provide a valid IP address."
                ],
            }

        data = investigate_ip(
            db=db,
            ip_address=ip,
        )

        return {
            "status": "success",
            "intent": intent.value,
            "tools_used": plan.tools,
            "summary": f"Investigation completed for {ip}.",
            "data": data,
            "limitations": [],
        }

    # --------------------------------------------
    # Protocol Summary
    # --------------------------------------------

    if intent == Intent.PROTOCOL_SUMMARY:

        data = get_protocol_summary(db)

        highest_only = params.get(
            "highest_only",
            False,
        )

        if highest_only and data:

            highest_count = max(
                item["event_count"]
                for item in data
            )

            data = [
                item
                for item in data
                if item["event_count"] == highest_count
            ]

            summary = (
                f"{len(data)} dataset(s) contain the highest number of events."
            )

        else:

            summary = (
                "Protocol and dataset summary retrieved successfully."
            )

        return {
            "status": "success",
            "intent": intent.value,
            "tools_used": plan.tools,
            "summary": summary,
            "data": data,
            "limitations": [],
        }

    # --------------------------------------------
    # Search Security Events
    # --------------------------------------------

    if intent == Intent.EVENT_SEARCH:

        data = search_security_events(
            db=db,
            filters=params,
            limit=params.get("limit", 50),
        )

        return {
            "status": "success",
            "intent": intent.value,
            "tools_used": plan.tools,
            "summary": f"Found {len(data)} matching security event(s).",
            "data": data,
            "limitations": [],
        }

    # --------------------------------------------
    # Unknown
    # --------------------------------------------

    return {
        "status": "success",
        "intent": intent.value,
        "tools_used": [],
        "summary": "Unable to determine the user's intent.",
        "data": [],
        "limitations": [
            "Try rephrasing your query."
        ],
    }