from functools import wraps
from flask import current_app, g, jsonify
from flask import request, jsonify
from functools import wraps
from jwt import decode, ExpiredSignatureError, InvalidTokenError
import requests

from utility.constant import Constant
from utility.refresh_access_token import refresh_access_token


def unavailable(message="This endpoint is currently unavailable", status_code=503):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return jsonify({"error": message}), status_code
        return wrapper
    return decorator


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        refresh_token = request.cookies.get('refresh_token')  # Get refresh token from the cookies
        # Check the 'Authorization' header for the access token
        if "Authorization" in request.headers:
            auth_header = request.headers["Authorization"]
            if auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]
        
        if not token:
            current_app.logger.error(f"Token is missing for {g.request_id}")
            return jsonify({"message": "Token is missing!"}), 401

        current_app.logger.info(f"Token: {token}")
        try:
            # Try decoding the access token
            decoded_token = requests.post(Constant.base_url + Constant.user_port + Constant.decode_token_endpoint, json={"token": token})

            current_app.logger.info(f"Decoded token: {decoded_token}")
            # You can access user info from decoded_token["sub"], etc.
        except ExpiredSignatureError:
            # Token expired, try to refresh it using the refresh token from the cookie
            current_app.logger.info(f"Token expired, refreshing: {g.request_id}")
            if refresh_token:
                new_access_token = refresh_access_token(refresh_token)
                if new_access_token:
                    g.access_token = new_access_token  # Attach the new access token to the request
                    current_app.logger.info(f"Token refreshed successfully for {g.request_id}")
                else:
                    current_app.logger.error(f"Failed to refresh token for {g.request_id}")
                    return jsonify({"message": "Failed to refresh token!"}), 401
            else:
                current_app.logger.error(f"Token expired, but refresh token is missing for {g.request_id}")
                return jsonify({"message": "Token expired, but refresh token is missing!"}), 401
        except InvalidTokenError:
            current_app.logger.error(f"Invalid token for {g.request_id}")
            return jsonify({"message": "Invalid token!"}), 401

        # Pass the decoded token or new access token to the route
        g.access_token = token  # Attach valid access token to the request for further processing
        return f(*args, **kwargs)

    return decorated