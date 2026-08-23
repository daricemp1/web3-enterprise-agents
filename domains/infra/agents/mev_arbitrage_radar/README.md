# INFRA: MEV & Sandwich Attack Radar

**Domain:** INFRA · **Gemini Enterprise display name:** INFRA: MEV & Sandwich Attack Radar

Detects maximal extractable value (MEV) activities including sandwich trades, cross-DEX spatial arbitrage, and private mempool bundle volumes. Orchestrates two sub-agents: **Data Insights** (BigQuery Conversational Analytics API, forecasting, anomalies) and **Market Context** (Google Search grounding).

---

## Why This Agent Matters

### Business Problem
Web3 protocols, trading desks, and node operators require real-time on-chain analytics and quantitative verification without manual indexer scraping or slow manual SQL authoring.

### Target Personas
- **Protocol Founders & Core Devs**: Monitor liquidity health, gas consumption, and network throughput.
- **Risk Officers & Quant Traders**: Track order book slippage, liquidation risks, and whale movements.

---

## Example Questions Answered

- **Q:** What was the highest profit MEV bundle extracted in recent blocks?
  **A:** A sandwich bundle in block 20450145 extracted $8,920.00 USD in profit via titan builder, paying a 1.20 ETH builder bribe.
- **Q:** What was the victim loss on the Uniswap v3 sandwich attack on August 1?
  **A:** The victim incurred $840.50 USD in slippage loss on the Uniswap v3 WETH/USDC 0.05% pool, yielding $710.20 USD net attacker profit.
