import json

SAFE_GLOBALS = {"__builtins__": None}


class JsonQueryError(Exception):
    """Custom exception for json-query errors."""


def parse_json(source):
    try:
        return json.load(source)
    except json.JSONDecodeError as e:
        raise JsonQueryError(f"Invalid JSON: {e}")


def evaluate_query(data, query):
    try:
        return eval(query, SAFE_GLOBALS, {"x": data})
    except Exception as e:
        raise JsonQueryError(f"Query evaluation failed: {e}")
