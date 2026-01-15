import hmac
import hashlib
import time
from fastapi import FastAPI, Request, HTTPException, Query
from pydantic import BaseModel, StringConstraints
from datetime import datetime
from typing import Optional, Annotated

from app.config import WEBHOOK_SECRET
from app.models import init_db
from app.storage import insert_message, get_messages, get_stats
from app.logging_utils import log_request

app = FastAPI()

@app.on_event("startup")
def startup():
    init_db()

class WebhookPayload(BaseModel):
    message_id: str
    from_: Annotated[str, StringConstraints(pattern=r"^\+\d+$")]
    to: Annotated[str, StringConstraints(pattern=r"^\+\d+$")]
    ts: datetime
    text: Optional[Annotated[str, StringConstraints(max_length=4096)]] = None

@app.get("/health/live")
def health_live():
    return {"status": "alive"}

@app.get("/health/ready")
def health_ready():
    if not WEBHOOK_SECRET:
        raise HTTPException(status_code=503, detail="WEBHOOK_SECRET not set")
    return {"status": "ready"}

@app.post("/webhook")
async def webhook(request: Request):
    start_time = time.time()
    body = await request.body()

    signature = request.headers.get("X-Signature")
    if not signature:
        raise HTTPException(status_code=401, detail="invalid signature")

    computed = hmac.new(
        WEBHOOK_SECRET.encode(),
        body,
        hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(computed, signature):
        raise HTTPException(status_code=401, detail="invalid signature")

    payload = await request.json()
    result = insert_message(payload)

    latency = int((time.time() - start_time) * 1000)
    log_request(
        "POST", "/webhook", 200, latency,
        {"message_id": payload.get("message_id"), "dup": result == "duplicate", "result": result}
    )

    return {"status": "ok"}

@app.get("/messages")
def list_messages(
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    from_: Optional[str] = Query(None, alias="from"),
    since: Optional[str] = None,
    q: Optional[str] = None
):
    total, data = get_messages(limit, offset, from_, since, q)
    return {
        "data": data,
        "total": total,
        "limit": limit,
        "offset": offset
    }

@app.get("/stats")
def stats():
    return get_stats()