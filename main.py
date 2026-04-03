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


def _utc_today():
    return datetime.now(timezone.utc).date()


@app.get("/date")
def server_date() -> dict[str, str]:
    """Календарная дата сервера в UTC (ISO 8601 date)."""
    d = _utc_today()
    return {
        "iso": d.isoformat(),
        "year": str(d.year),
        "month": str(d.month),
        "day": str(d.day),
    }


@app.get("/date/iso")
def server_date_iso() -> dict[str, str]:
    """Только дата в формате YYYY-MM-DD (UTC)."""
    return {"date": _utc_today().isoformat()}


@app.get("/date/ru")
def server_date_ru() -> dict[str, str]:
    """Дата в формате ДД.ММ.ГГГГ (UTC)."""
    d = _utc_today()
    return {"dmy": f"{d.day:02d}.{d.month:02d}.{d.year}"}


if __name__ == "__main__":
    import uvicorn

    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("main:app", host=host, port=port, reload=True)
