# DEFI: Cross-Chain Bridge & Outflow Monitor

**Domain:** DEFI · **Gemini Enterprise display name:** DEFI: Cross-Chain Bridge & Outflow Monitor

Tracks cross-chain bridge transfer velocity, lock-and-mint vs burn liquidity imbalances, and alerts on anomalous multi-chain capital flight. Orchestrates two sub-agents: **Data Insights** (BigQuery Conversational Analytics API, forecasting, anomalies) and **Market Context** (Google Search grounding).

---

## Why This Agent Matters

### Business Problem
Web3 protocols, trading desks, and node operators require real-time on-chain analytics and quantitative verification without manual indexer scraping or slow manual SQL authoring.

### Target Personas
- **Protocol Founders & Core Devs**: Monitor liquidity health, gas consumption, and network throughput.
- **Risk Officers & Quant Traders**: Track order book slippage, liquidation risks, and whale movements.

---

## Example Questions Answered

- **Q:** Which bridge recorded the highest volume to Arbitrum on August 2, 2026?
  **A:** Across Protocol processed $46,800,000 USD (1,980 transfers) from Ethereum to Arbitrum on August 2, 2026.
- **Q:** What is the current liquidity utilization of Stargate on Base?
  **A:** Stargate has a 79.17% pool utilization on Base with $48,000,000 USD available liquidity in normal status.
