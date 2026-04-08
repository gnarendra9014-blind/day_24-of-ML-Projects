import json
import os
from datetime import datetime

LOG_FILE = "api_requests.json"

def log_request(endpoint: str, model: str, prompt: str,
                response: str, latency_ms: float,
                tokens: int, api_key: str, status: int):
    logs = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE) as f:
            logs = json.load(f)
    
    logs.append({
        "timestamp": datetime.now().isoformat(),
        "endpoint": endpoint,
        "model": model,
        "prompt_preview": prompt[:80],
        "response_preview": response[:80],
        "latency_ms": round(latency_ms, 2),
        "tokens": tokens,
        "api_key_prefix": api_key[:8] + "...",
        "status_code": status,
    })
    
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)
