from app.agents.entity_extractor import extract_entities
from app.agents.intent_classifier import classify_intent
from app.schemas.query_plan import QueryPlan


def normalize_query(query: str) -> str:
    """
    Normalize a natural language query.
    """

    return " ".join(
        query.lower().strip().split()
    )


def enrich_entities(
    query: str,
    entities: dict,
) -> dict:
    """
    Add additional information inferred
    from the natural language query.
    """

    query = query.lower()

    # --------------------------
    # SSH
    # --------------------------

    if "ssh" in query:
        entities["dataset"] = "ssh_logs"

    # --------------------------
    # FTP
    # --------------------------

    elif "ftp" in query:
        entities["dataset"] = "ftp_logs"

    # --------------------------
    # HTTPS
    # --------------------------

    elif "https" in query:
        entities["dataset"] = "https_logs"

    # --------------------------
    # SQL Injection
    # --------------------------

    elif (
        "sql injection" in query
        or "sqli" in query
    ):
        entities["dataset"] = "sqli_logs"

    # --------------------------
    # RDP
    # --------------------------

    elif "rdp" in query:
        entities["dataset"] = "rdp_logs"

    # --------------------------
    # Octopus
    # --------------------------

    elif "octopus" in query:
        entities["dataset"] = "octopus_logs"

    # --------------------------
    # Highest Only
    # --------------------------

    if (
        "highest" in query
        or "most events" in query
    ):
        entities["highest_only"] = True

    else:
        entities["highest_only"] = False

    return entities


def validate_entities(
    entities: dict,
):
    """
    Validate extracted entities.
    """

    limit = entities.get("limit")

    if limit is not None:

        if limit < 1:
            entities["limit"] = 1

        elif limit > 100:
            entities["limit"] = 100

    return entities


def analyze_query(
    query: str,
) -> QueryPlan:
    """
    Analyze a natural language query.
    """

    normalized = normalize_query(query)

    entities = extract_entities(normalized)

    entities = enrich_entities(
        normalized,
        entities,
    )

    entities = validate_entities(
        entities,
    )

    classification = classify_intent(
        normalized,
    )

    return QueryPlan(
        intent=classification.intent.value,
        tools=[
            classification.intent.value
        ],
        parameters=entities,
        confidence=1.0,
    )