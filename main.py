import os
from datetime import datetime, timezone

from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()

app = FastAPI(title="Test backend", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/time")
def server_time() -> dict[str, str]:
    """Текущее время сервера в UTC (ISO 8601)."""
    now = datetime.now(timezone.utc)
    return {
        "utc_iso": now.isoformat().replace("+00:00", "Z"),
        "unix": str(int(now.timestamp())),
    }


if __name__ == "__main__":
    import uvicorn

    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("main:app", host=host, port=port, reload=True)
