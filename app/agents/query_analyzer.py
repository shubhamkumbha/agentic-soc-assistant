from app.agents.intent_classifier import (
    Intent,
    classify_intent,
)
from app.schemas.query_plan import (
    QueryPlan,
    ToolStep,
)


def analyze_query(query: str) -> QueryPlan:
    """
    Analyze the user's natural language query and
    build an execution plan.

    The execution plan contains the ordered list
    of tools the orchestrator should execute.
    """

    classification = classify_intent(query)

    intent = classification.intent
    params = classification.parameters

    query_lower = query.lower()

    # --------------------------------------------------
    # Multi-step workflow
    # --------------------------------------------------

    if (
        "most active attacker" in query_lower
        or (
            "top attacker" in query_lower
            and "investigate" in query_lower
        )
    ):

        return QueryPlan(
            intent="investigate_top_attacker",
            multi_step=True,
            confidence=1.0,
            steps=[
                ToolStep(
                    tool="get_top_attackers",
                    parameters={
                        "limit": 1,
                    },
                ),
                ToolStep(
                    tool="investigate_ip",
                    parameters={},
                ),
            ],
        )

    # --------------------------------------------------
    # Single-step plans
    # --------------------------------------------------

    if intent == Intent.TOP_ATTACKERS:

        return QueryPlan(
            intent=intent.value,
            confidence=1.0,
            steps=[
                ToolStep(
                    tool="get_top_attackers",
                    parameters={
                        "limit": params.get("limit", 5),
                    },
                )
            ],
        )

    if intent == Intent.INVESTIGATE_IP:

        return QueryPlan(
            intent=intent.value,
            confidence=1.0,
            steps=[
                ToolStep(
                    tool="investigate_ip",
                    parameters={
                        "ip": params.get("ip"),
                    },
                )
            ],
        )

    if intent == Intent.PROTOCOL_SUMMARY:

        return QueryPlan(
            intent=intent.value,
            confidence=1.0,
            steps=[
                ToolStep(
                    tool="get_protocol_summary",
                    parameters={
                        "highest_only": params.get(
                            "highest_only",
                            False,
                        ),
                    },
                )
            ],
        )

    if intent == Intent.EVENT_SEARCH:

        return QueryPlan(
            intent=intent.value,
            confidence=1.0,
            steps=[
                ToolStep(
                    tool="search_security_events",
                    parameters=params,
                )
            ],
        )

    return QueryPlan(
        intent=Intent.UNKNOWN.value,
        confidence=0.0,
        steps=[],
    )