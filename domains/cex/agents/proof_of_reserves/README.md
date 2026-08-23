# CEX: Proof of Reserves & Solvency

**Domain:** CEX · **Gemini Enterprise display name:** CEX: Proof of Reserves & Solvency

Audits on-chain wallet reserve assets versus exchange customer liability balances, verifying collateralization ratios and solvency margins. Orchestrates two sub-agents: **Data Insights** (BigQuery Conversational Analytics API, forecasting, anomalies) and **Market Context** (Google Search grounding).

---

## Why This Agent Matters

### Business Problem
Web3 protocols, trading desks, and node operators require real-time on-chain analytics and quantitative verification without manual indexer scraping or slow manual SQL authoring.

### Target Personas
- **Protocol Founders & Core Devs**: Monitor liquidity health, gas consumption, and network throughput.
- **Risk Officers & Quant Traders**: Track order book slippage, liquidation risks, and whale movements.

---

## Example Questions Answered

- **Q:** What is the current proof-of-reserves ratio for BTC and ETH in the August 1, 2026 audit?
  **A:** In the August 1, 2026 audit, BTC has a reserve ratio of 104.98% (48,500 BTC reserve vs 46,200 BTC liabilities) and ETH has a reserve ratio of 105.48% (385,000 ETH reserve vs 365,000 ETH liabilities).
- **Q:** How much of total BTC reserves are held in cold storage?
  **A:** 94.5% of total BTC reserves are held in BitGo cold storage custody.
