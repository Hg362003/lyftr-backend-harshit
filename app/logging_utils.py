import json
import time
import uuid
from datetime import datetime


def log_request(method, path, status, latency_ms, extra=None):
    log = {
        "ts": datetime.utcnow().isoformat() + "Z",
        "level": "INFO",
        "request_id": str(uuid.uuid4()),
        "method": method,
        "path": path,
        "status": status,
        "latency_ms": latency_ms
    }

    if extra:
        log.update(extra)

    print(json.dumps(log))