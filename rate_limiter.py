import time
from collections import defaultdict
from fastapi import HTTPException

# Simple in-memory rate limiter
request_counts = defaultdict(list)
RATE_LIMIT = 10        # max requests
WINDOW_SECONDS = 60    # per minute

def check_rate_limit(api_key: str):
    now = time.time()
    window_start = now - WINDOW_SECONDS
    
    # Remove old requests outside window
    request_counts[api_key] = [
        t for t in request_counts[api_key] if t > window_start
    ]
    
    if len(request_counts[api_key]) >= RATE_LIMIT:
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded. Max {RATE_LIMIT} requests per minute."
        )
    
    request_counts[api_key].append(now)
    remaining = RATE_LIMIT - len(request_counts[api_key])
    return remaining
