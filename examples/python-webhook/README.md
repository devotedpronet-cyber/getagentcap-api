# Python FastAPI webhook receiver

The Ledger API is pull-only. This wraps it in a tiny poll → webhook bridge so
you can treat new payments as push events.

```bash
pip install -r requirements.txt
export GETAGENTCAP_API_KEY=sk_...
uvicorn main:app --reload
```

Then trigger a poll (cron this, or call it from your own scheduler):

```bash
curl -X POST http://localhost:8000/poll
```

Each new payment since the last poll is POSTed to `WEBHOOK_URL` (default
`http://localhost:8000/webhook`, a stub receiver included for reference —
point it at your own endpoint instead).
