import os
from dotenv import load_dotenv
from fastapi import HTTPException, Header
from typing import Optional

load_dotenv()
API_SECRET_KEY = os.getenv("API_SECRET_KEY", "my-secret-key")

def verify_api_key(x_api_key: Optional[str] = Header(None)):
    if not x_api_key:
        raise HTTPException(status_code=401, detail="API key missing. Add X-API-Key header.")
    if x_api_key != API_SECRET_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key.")
    return x_api_key
