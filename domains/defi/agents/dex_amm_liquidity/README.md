# DEFI: AMM Liquidity & Impermanent Loss

**Domain:** DEFI · **Gemini Enterprise display name:** DEFI: AMM Liquidity & Impermanent Loss

Analyzes automated market maker (AMM) pool depths, 24-hour volume-to-TVL ratios, fee generation, and historical impermanent loss. Orchestrates two sub-agents: **Data Insights** (BigQuery Conversational Analytics API, forecasting, anomalies) and **Market Context** (Google Search grounding).

---

## Why This Agent Matters

### Business Problem
Web3 protocols, trading desks, and node operators require real-time on-chain analytics and quantitative verification without manual indexer scraping or slow manual SQL authoring.

### Target Personas
- **Protocol Founders & Core Devs**: Monitor liquidity health, gas consumption, and network throughput.
- **Risk Officers & Quant Traders**: Track order book slippage, liquidation risks, and whale movements.

---

## Example Questions Answered

- **Q:** Which liquidity pool demonstrates the highest capital efficiency and fee APY?
  **A:** Uniswap v3 ETH/USDC 0.05% has the highest capital efficiency at 1.45 ($210M 24h volume on $145M TVL) generating a 26.4% fee APY.
- **Q:** What were the total trading fees collected by the ETH/USDC 0.05% pool on August 2, 2026?
  **A:** On August 2, 2026, the pool generated $112,500.00 USD in LP fees on $225,000,000 USD in daily volume.
