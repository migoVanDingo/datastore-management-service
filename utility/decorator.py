from functools import wraps
from flask import jsonify

def unavailable(message="This endpoint is currently unavailable", status_code=503):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return jsonify({"error": message}), status_code
        return wrapper
    return decorator