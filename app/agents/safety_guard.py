from dataclasses import dataclass


@dataclass
class SafetyResult:
    allowed: bool
    reason: str | None = None


UNSAFE_KEYWORDS = [
    "delete",
    "drop",
    "truncate",
    "remove",
    "erase",
    "destroy",
    "update",
    "insert",
    "create user",
    "grant",
    "revoke",
    "alter",
    "shutdown",
]


def validate_query(query: str) -> SafetyResult:
    """
    Reject destructive or administrative database requests.

    The SOC Assistant is strictly read-only.
    """

    query = query.lower()

    for keyword in UNSAFE_KEYWORDS:
        if keyword in query:
            return SafetyResult(
                allowed=False,
                reason=(
                    "The assistant has read-only access and cannot perform "
                    "destructive or administrative database operations."
                ),
            )

    return SafetyResult(allowed=True)