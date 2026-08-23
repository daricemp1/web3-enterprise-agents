# CEX: Order Book Depth & Spread Analytics

**Domain:** CEX · **Gemini Enterprise display name:** CEX: Order Book Depth & Spread Analytics

Analyzes bid-ask spread efficiency, top-of-book depth, order book imbalance, and slippage across major spot and perpetual trading pairs. Orchestrates two sub-agents: **Data Insights** (BigQuery Conversational Analytics API, forecasting, anomalies) and **Market Context** (Google Search grounding).

---

## Why This Agent Matters

### Business Problem
Web3 protocols, trading desks, and node operators require real-time on-chain analytics and quantitative verification without manual indexer scraping or slow manual SQL authoring.

### Target Personas
- **Protocol Founders & Core Devs**: Monitor liquidity health, gas consumption, and network throughput.
- **Risk Officers & Quant Traders**: Track order book slippage, liquidation risks, and whale movements.

---

## Example Questions Answered

- **Q:** Which exchange and pair offered the highest 2% bid depth on August 2, 2026?
  **A:** On August 2, 2026, Binance BTC/USDT had the highest 2% bid depth at $15,100,000 USD (with an ask depth of $14,900,000 USD and a tight spread of 0.42 bps).
- **Q:** What was the recorded slippage on the $1.2M BTC/USDT trade on August 2?
  **A:** The $1,200,000 USD sell trade on Binance BTC/USDT incurred a slippage of 2.30 bps at an executed price of $65,135.00.
