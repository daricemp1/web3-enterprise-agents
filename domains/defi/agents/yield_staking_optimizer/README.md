# DEFI: Liquid Staking & Yield Optimizer

**Domain:** DEFI · **Gemini Enterprise display name:** DEFI: Liquid Staking & Yield Optimizer

Compares liquid staking token (LST) yields, reward distribution APRs, and optimizes risk-adjusted capital deployment across yield vaults. Orchestrates two sub-agents: **Data Insights** (BigQuery Conversational Analytics API, forecasting, anomalies) and **Market Context** (Google Search grounding).

---

## Why This Agent Matters

### Business Problem
Web3 protocols, trading desks, and node operators require real-time on-chain analytics and quantitative verification without manual indexer scraping or slow manual SQL authoring.

### Target Personas
- **Protocol Founders & Core Devs**: Monitor liquidity health, gas consumption, and network throughput.
- **Risk Officers & Quant Traders**: Track order book slippage, liquidation risks, and whale movements.

---

## Example Questions Answered

- **Q:** What is the highest yielding stablecoin vault with over $100M TVL?
  **A:** The Curve sUSDe/USDC Pool offers the highest yield at 17.30% Net APY (13.10% base + 4.20% rewards) on $120M TVL.
- **Q:** What is the current annual staking reward rate for Lido stETH?
  **A:** Lido stETH yields 3.42% annual staking rewards with 9,850,000 ETH staked and a tight peg discount of 2.0 bps.
