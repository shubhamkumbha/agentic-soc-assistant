from dataclasses import dataclass, field


@dataclass
class QueryPlan:
    """
    Represents the execution plan produced after
    analyzing a natural language query.
    """

    intent: str

    tools: list[str] = field(default_factory=list)

    parameters: dict = field(default_factory=dict)

    confidence: float = 1.0