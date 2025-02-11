from flask import current_app, g
import requests
from utility.constant import Constant

def refresh_access_token(refresh_token):
    """Refresh the access token using the refresh token."""
    REFRESH_TOKEN_URL = Constant.base_url + Constant.user_port + Constant.refresh_token_endpoint 

    current_app.logger.info(f"Sending request to refresh token: {g.request_id}")
    response = requests.post(REFRESH_TOKEN_URL, data={
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    })

    if response.status_code == 200:
        data = response.json()
        new_access_token = data['access_token']
        return new_access_token
    else:
        return None 