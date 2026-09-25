"""Poll GET /ledger for new payments and forward each to a local webhook.

The Ledger API has no push/webhook of its own — this polls `since` the last
seen payment and re-emits each one as a webhook POST, so downstream systems
can treat it like a push feed.

Usage:
    export GETAGENTCAP_API_KEY=sk_...
    uvicorn main:app --reload
    # in another shell:
    curl -X POST http://localhost:8000/poll
"""

import os
from datetime import datetime, timezone

import httpx
from fastapi import FastAPI, HTTPException

BASE_URL = "https://getagentcap.com/api/v1"
WEBHOOK_URL = os.environ.get("WEBHOOK_URL", "http://localhost:8000/webhook")

app = FastAPI()
_state = {"since": None}


def _api_key() -> str:
    key = os.environ.get("GETAGENTCAP_API_KEY")
    if not key:
        raise HTTPException(500, "GETAGENTCAP_API_KEY not set")
    return key


@app.post("/poll")
async def poll():
    """Fetch payments since the last poll and forward each to WEBHOOK_URL."""
    params = {"limit": 500}
    if _state["since"]:
        params["since"] = _state["since"]

    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{BASE_URL}/ledger",
            params=params,
            headers={"Authorization": f"Bearer {_api_key()}"},
        )
        resp.raise_for_status()
        payments = resp.json()["payments"]

        for payment in reversed(payments):  # oldest first
            await client.post(WEBHOOK_URL, json=payment)

    if payments:
        _state["since"] = payments[0]["occurred_at"]

    return {"forwarded": len(payments)}


@app.post("/webhook")
async def webhook(payment: dict):
    """Example receiver — replace with your own handling."""
    print(f"[{datetime.now(timezone.utc).isoformat()}] payment: {payment}")
    return {"ok": True}
