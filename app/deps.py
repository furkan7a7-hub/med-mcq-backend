import os
from fastapi import Header, HTTPException, status

ADMIN_KEY = os.getenv("API_KEY", "change_me_admin_key")

def require_admin(x_api_key: str = Header(None)):
    if x_api_key != ADMIN_KEY:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing x-api-key")
