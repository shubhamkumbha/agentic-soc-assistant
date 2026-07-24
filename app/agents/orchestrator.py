from sqlalchemy.orm import Session

from app.agents.query_analyzer import analyze_query
from app.agents.safety_guard import validate_query

from app.tools.top_attackers import get_top_attackers
from app.tools.ip_investigation import investigate_ip
from app.tools.protocol_summary import get_protocol_summary
from app.tools.search_security_events import search_security_events


def process_query(query: str, db: Session):
    """
    Main entry point for the SOC Assistant.

    Flow:

    User Query
        ↓
    Safety Guard
        ↓
    Query Analyzer
        ↓
    Execute Tool(s)
        ↓
    Return Standard Response
    """

    # ==========================================================
    # Safety Guard
    # ==========================================================

    safety = validate_query(query)

    if not safety.allowed:
        return {
            "status": "rejected",
            "intent": "unsafe_request",
            "tools_used": [],
            "summary": safety.reason,
            "data": {},
            "limitations": [
                "The assistant operates with read-only database access."
            ],
        }

    # ==========================================================
    # Build Execution Plan
    # ==========================================================

    plan = analyze_query(query)

    result = None
    tools_used = []

    # ==========================================================
    # Execute Plan
    # ==========================================================

    for step in plan.steps:

        tool = step.tool
        params = step.parameters

        tools_used.append(tool)

        # ------------------------------------------------------
        # Top Attackers
        # ------------------------------------------------------

        if tool == "get_top_attackers":

            result = get_top_attackers(
                db=db,
                limit=params.get("limit", 5),
            )

        # ------------------------------------------------------
        # Investigate IP
        # ------------------------------------------------------

        elif tool == "investigate_ip":

            ip = params.get("ip")

            # Multi-step workflow
            if not ip:

                if (
                    isinstance(result, list)
                    and len(result) > 0
                ):
                    ip = result[0]["source_ip"]

            if not ip:

                return {
                    "status": "failed",
                    "intent": plan.intent,
                    "tools_used": tools_used,
                    "summary": "No IP address available for investigation.",
                    "data": {},
                    "limitations": [
                        "Please provide a valid IP address."
                    ],
                }

            result = investigate_ip(
                db=db,
                ip_address=ip,
            )

        # ------------------------------------------------------
        # Protocol Summary
        # ------------------------------------------------------

        elif tool == "get_protocol_summary":

            protocol_data = get_protocol_summary(db)

            if params.get("highest_only"):

                highest = max(
                    item["event_count"]
                    for item in protocol_data
                )

                protocol_data = [
                    item
                    for item in protocol_data
                    if item["event_count"] == highest
                ]

            result = protocol_data

        # ------------------------------------------------------
        # Search Events
        # ------------------------------------------------------

        elif tool == "search_security_events":

            result = search_security_events(
                db=db,
                filters=params,
                limit=params.get("limit", 50),
            )

    # ==========================================================
    # Build Summary
    # ==========================================================

    if plan.multi_step:

        summary = (
            "The most active attacker was identified and "
            "automatically investigated successfully."
        )

    elif plan.intent == "get_top_attackers":

        summary = (
            f"Top {len(result)} attacking IP address(es) "
            "were identified across all monitored datasets."
        )

    elif plan.intent == "investigate_ip":

        summary = (
            "IP investigation completed successfully."
        )

    elif plan.intent == "get_protocol_summary":

        if (
            len(plan.steps) > 0
            and plan.steps[0].parameters.get("highest_only")
        ):

            summary = (
                "The dataset(s) with the highest number of "
                "security events were identified."
            )

        else:

            summary = (
                "Protocol statistics were generated successfully."
            )

    elif plan.intent == "search_security_events":

        summary = (
            f"Found {len(result)} matching security event(s)."
        )

    else:

        summary = "Query executed successfully."

    # ==========================================================
    # Final Response
    # ==========================================================

    return {
        "status": "success",
        "intent": plan.intent,
        "tools_used": tools_used,
        "summary": summary,
        "data": result,
        "limitations": [],
    }