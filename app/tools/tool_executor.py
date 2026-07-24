from sqlalchemy.orm import Session

from app.tools.tool_registry import TOOL_REGISTRY


def execute_tool(
    tool_name: str,
    db: Session,
    parameters: dict,
):
    """
    Executes a registered SOC tool.

    The orchestrator delegates all tool execution here.
    """

    if tool_name not in TOOL_REGISTRY:
        raise ValueError(f"Unknown tool: {tool_name}")

    tool = TOOL_REGISTRY[tool_name]

    # --------------------------------------------------
    # get_top_attackers
    # --------------------------------------------------

    if tool_name == "get_top_attackers":

        return tool(
            db=db,
            limit=parameters.get("limit", 5),
        )

    # --------------------------------------------------
    # investigate_ip
    # --------------------------------------------------

    if tool_name == "investigate_ip":

        return tool(
            db=db,
            ip_address=parameters["ip"],
        )

    # --------------------------------------------------
    # get_protocol_summary
    # --------------------------------------------------

    if tool_name == "get_protocol_summary":

        return tool(db)

    # --------------------------------------------------
    # search_security_events
    # --------------------------------------------------

    if tool_name == "search_security_events":

        return tool(
            db=db,
            filters=parameters,
            limit=parameters.get("limit", 50),
        )

    raise ValueError(f"Tool not implemented: {tool_name}")