# Examples

Minimal reference clients for the GetAgentCap Ledger API. Set `GETAGENTCAP_API_KEY`
to a key from the dashboard (Settings → API keys) before running either.

- [`node-client/`](node-client/) — fetch recent payments with plain `fetch`, no dependencies.
- [`python-webhook/`](python-webhook/) — poll the ledger and forward new payments to a webhook, FastAPI.
