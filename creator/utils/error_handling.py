import traceback

def error_to_dict(err: Exception | None) -> dict:
    if err is None:
        return {}
    return {
        "type": type(err).__name__,
        "message": str(err),
        "traceback": traceback.format_exc()
    }