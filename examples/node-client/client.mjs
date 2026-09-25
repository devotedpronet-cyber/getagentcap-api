// Node.js client for GET /ledger — no dependencies, uses global fetch (Node 18+).
// Usage: GETAGENTCAP_API_KEY=sk_... node client.mjs [--agent_id=...] [--since=2026-09-01T00:00:00Z]

const BASE_URL = "https://getagentcap.com/api/v1";

async function getLedger({ apiKey, limit = 50, since, agentId } = {}) {
  const url = new URL(`${BASE_URL}/ledger`);
  if (limit) url.searchParams.set("limit", limit);
  if (since) url.searchParams.set("since", since);
  if (agentId) url.searchParams.set("agent_id", agentId);

  const res = await fetch(url, {
    headers: { Authorization: `Bearer ${apiKey}` },
  });

  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(`GetAgentCap API ${res.status}: ${body.error ?? res.statusText}`);
  }

  return res.json();
}

async function main() {
  const apiKey = process.env.GETAGENTCAP_API_KEY;
  if (!apiKey) {
    console.error("Set GETAGENTCAP_API_KEY first.");
    process.exit(1);
  }

  const args = Object.fromEntries(
    process.argv.slice(2).map((a) => a.replace(/^--/, "").split("="))
  );

  const { payments } = await getLedger({
    apiKey,
    since: args.since,
    agentId: args.agent_id,
  });

  for (const p of payments) {
    console.log(`${p.occurred_at}  ${p.amount_usdc} USDC  ${p.agents?.name ?? p.agent_id}  ${p.tx_hash}`);
  }
}

main().catch((err) => {
  console.error(err.message);
  process.exit(1);
});
