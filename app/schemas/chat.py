from pydantic import BaseModel, Field
from typing import Any

class ChatRequest(BaseModel):
    """Natural language query from a SOC analyst."""

    query: str = Field(
        min_length=1,
        max_length=1000,
    )


class ChatResponse(BaseModel):
    """Standard response returned by the agent."""

    status: str

    intent: str

    tools_used: list[str]

    summary: str

    data: Any

    limitations: list[str] = []