# INFRA: RPC Latency & Validator Health

**Domain:** INFRA · **Gemini Enterprise display name:** INFRA: RPC Latency & Validator Health

Tracks distributed RPC node endpoint latencies, validator uptime, attestation rates, and consensus slash risk events. Orchestrates two sub-agents: **Data Insights** (BigQuery Conversational Analytics API, forecasting, anomalies) and **Market Context** (Google Search grounding).

---

## Why This Agent Matters

### Business Problem
Web3 protocols, trading desks, and node operators require real-time on-chain analytics and quantitative verification without manual indexer scraping or slow manual SQL authoring.

### Target Personas
- **Protocol Founders & Core Devs**: Monitor liquidity health, gas consumption, and network throughput.
- **Risk Officers & Quant Traders**: Track order book slippage, liquidation risks, and whale movements.

---

## Example Questions Answered

- **Q:** Which RPC provider had the lowest latency in us-east-1 on August 1, 2026?
  **A:** Alchemy had the lowest average latency in us-east-1 at 28.5 ms (p99 of 85.0 ms and 0.02% error rate).
- **Q:** Were any validator groups flagged with elevated slashing or missed block risk?
  **A:** Solo-Stakers-Group-B was flagged with ELEVATED risk due to 3 missed blocks and a sub-optimal attestation rate of 96.40%.
