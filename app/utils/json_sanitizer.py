import math


def sanitize_json(obj):
    """
    Recursively sanitize JSON objects before inserting into PostgreSQL.

    Fixes:
    - Removes NULL bytes (\x00)
    - Converts NaN / Infinity to None
    """

    if isinstance(obj, dict):
        return {
            key: sanitize_json(value)
            for key, value in obj.items()
        }

    if isinstance(obj, list):
        return [
            sanitize_json(item)
            for item in obj
        ]

    if isinstance(obj, str):
        return obj.replace("\x00", "")

    if isinstance(obj, float):
        if math.isnan(obj) or math.isinf(obj):
            return None

    return obj