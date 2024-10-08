import requests
from fastapi import HTTPException

USER_SERVICE_URL = 'http://127.0.0.1:8081'

def validate_token(token: dict):
    response = requests.get(f"{USER_SERVICE_URL}/validate_token", headers={"Authorization": f"Bearer {token}"})
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token."
        )