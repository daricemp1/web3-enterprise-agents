# CEX: Whale Inflows & Custody Transfers

**Domain:** CEX · **Gemini Enterprise display name:** CEX: Whale Inflows & Custody Transfers

Tracks large on-chain deposit/withdrawal flows, hot and cold storage rebalancing, and exchange reserve drawdowns across major assets. Orchestrates two sub-agents: **Data Insights** (BigQuery Conversational Analytics API, forecasting, anomalies) and **Market Context** (Google Search grounding).

---

## Why This Agent Matters

### Business Problem
Web3 protocols, trading desks, and node operators require real-time on-chain analytics and quantitative verification without manual indexer scraping or slow manual SQL authoring.

### Target Personas
- **Protocol Founders & Core Devs**: Monitor liquidity health, gas consumption, and network throughput.
- **Risk Officers & Quant Traders**: Track order book slippage, liquidation risks, and whale movements.

---

## Example Questions Answered

- **Q:** What was the largest whale deposit recorded on August 1, 2026?
  **A:** The largest whale deposit on August 1, 2026 was 1,500 BTC ($96,375,000 USD) deposited to Coinbase by Institutional Fund A.
- **Q:** How much BTC was swept from hot to cold storage on August 1?
  **A:** 3,000 BTC was rebalanced from Hot-Wallet-01 to Cold-Vault-03, keeping hot wallet ratio at 5.5%.
