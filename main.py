import os
import time
import json
from datetime import datetime
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from groq import Groq
from dotenv import load_dotenv
from auth import verify_api_key
from rate_limiter import check_rate_limit
from logger import log_request

load_dotenv()
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

app = FastAPI(
    title="My LLM API",
    description="A production-ready LLM API with auth, rate limiting and logging",
    version="1.0.0"
)

# Request/Response models
class CompletionRequest(BaseModel):
    prompt: str
    model: Optional[str] = "llama-3.3-70b-versatile"
    max_tokens: Optional[int] = 300
    temperature: Optional[float] = 0.7

class CompletionResponse(BaseModel):
    response: str
    model: str
    tokens_used: int
    latency_ms: float

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: list[ChatMessage]
    model: Optional[str] = "llama-3.3-70b-versatile"
    max_tokens: Optional[int] = 300

# Routes
@app.get("/")
def root():
    return {
        "name": "My LLM API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": ["/complete", "/chat", "/models", "/health", "/logs"]
    }

@app.get("/health")
def health():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/models")
def list_models(api_key: str = Depends(verify_api_key)):
    return {
        "models": [
            {"id": "llama-3.3-70b-versatile", "description": "Best quality"},
            {"id": "llama-3.1-8b-instant", "description": "Fastest"},
            {"id": "llama-3.2-11b-vision-preview", "description": "Vision capable"},
        ]
    }

@app.post("/complete", response_model=CompletionResponse)
def complete(request: CompletionRequest, api_key: str = Depends(verify_api_key)):
    remaining = check_rate_limit(api_key)
    start = time.perf_counter()
    
    try:
        res = groq_client.chat.completions.create(
            model=request.model,
            messages=[{"role": "user", "content": request.prompt}],
            max_tokens=request.max_tokens,
            temperature=request.temperature,
        )
        response_text = res.choices[0].message.content
        tokens = res.usage.total_tokens
        latency = (time.perf_counter() - start) * 1000
        
        log_request("/complete", request.model, request.prompt,
                   response_text, latency, tokens, api_key, 200)
        
        return CompletionResponse(
            response=response_text,
            model=request.model,
            tokens_used=tokens,
            latency_ms=round(latency, 2)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
def chat(request: ChatRequest, api_key: str = Depends(verify_api_key)):
    check_rate_limit(api_key)
    start = time.perf_counter()
    
    try:
        messages = [{"role": m.role, "content": m.content} for m in request.messages]
        res = groq_client.chat.completions.create(
            model=request.model,
            messages=messages,
            max_tokens=request.max_tokens,
        )
        response_text = res.choices[0].message.content
        latency = (time.perf_counter() - start) * 1000
        
        log_request("/chat", request.model,
                   messages[-1]["content"], response_text,
                   latency, res.usage.total_tokens, api_key, 200)
        
        return {
            "response": response_text,
            "model": request.model,
            "tokens_used": res.usage.total_tokens,
            "latency_ms": round(latency, 2)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/logs")
def get_logs(api_key: str = Depends(verify_api_key)):
    if not os.path.exists("api_requests.json"):
        return {"logs": [], "total": 0}
    with open("api_requests.json") as f:
        logs = json.load(f)
    return {"logs": logs[-20:], "total": len(logs)}
