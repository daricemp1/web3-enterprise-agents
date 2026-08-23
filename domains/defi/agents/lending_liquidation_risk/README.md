# DEFI: Lending Health & Liquidation Risk

**Domain:** DEFI · **Gemini Enterprise display name:** DEFI: Lending Health & Liquidation Risk

Monitors money market borrowing utilization, collateral health factor distributions, and identifies collateral positions approaching liquidation thresholds. Orchestrates two sub-agents: **Data Insights** (BigQuery Conversational Analytics API, forecasting, anomalies) and **Market Context** (Google Search grounding).

---

## Why This Agent Matters

### Business Problem
Web3 protocols, trading desks, and node operators require real-time on-chain analytics and quantitative verification without manual indexer scraping or slow manual SQL authoring.

### Target Personas
- **Protocol Founders & Core Devs**: Monitor liquidity health, gas consumption, and network throughput.
- **Risk Officers & Quant Traders**: Track order book slippage, liquidation risks, and whale movements.

---

## Example Questions Answered

- **Q:** Which position is closest to liquidation and what is its health factor?
  **A:** Position POS-8901 on Aave v3 is highest risk with a health factor of 1.09 ($18.5M wstETH collateral against $14.2M USDC debt), liquidating if ETH falls to $3,120.00.
- **Q:** How much volume was liquidated across Aave v3 on August 1?
  **A:** $3,450,000.00 USD was successfully liquidated on Aave v3 with zero bad debt incurred and $172,500.00 in liquidator bonuses.
