# Merchandising: Price Matching & Competitor Intel Agent

**Domain:** Merchandising · **Gemini Enterprise display name:** Merchandising: Price Matching & Competitor Intel

---

## Why This Agent Matters

### Business Problem
Omnichannel retailers lose customer trust when prices exceed key market competitors (Amazon, Walmart, Target), but blind price matching severely erodes gross margin. Crucially, retailers should not lower prices if competitors are out of stock. This agent links competitor price scraping feeds, stock availability alerts, and POS price-match claims to optimize price matching rules.

### Target Personas
- **Director of Pricing & Competitive Strategy**: Oversee market price index parity (100 baseline) and competitor price gap rules.
- **Store Operations VP**: Monitor store POS price match policy claims ($) and manager override frequency.
- **Category Merchandisers**: Identify competitor out-of-stock holding margin opportunities ($).

---

## Key Metrics Tracked

| Metric / KPI | Definition & Formula | Business Target / Impact |
| :--- | :--- | :--- |
| **Price Index vs Market** | `(our_category_price / market_avg_price) * 100` | Target 98 - 102 (Parity range with primary competitors) |
| **Competitor Price Gap %** | `((our_price - competitor_price) / our_price) * 100` | Flags SKUs with >5% price premium vs market |
| **POS Price Match Claims ($)** | Total dollar discounts granted at POS for customer price matches | Controls margin erosion from policy claims |
| **Holding Margin Opportunity ($)** | Revenue/margin saved by holding price when competitor is out of stock | Prevents unnecessary price discounting |

---

## What It Answers

Routed to **Data Insights**:
- Competitor price feeds, category price index parity, POS price match claims $, manager override counts, and competitor out-of-stock holding margin alerts.

Routed to **Market Context**:
- Competitor price matching policy trends, dynamic pricing strategies, and competitor price tracking industry best practices.

---

## Sample Q&A Showcase

The following three responses are captured from live post-deploy smoke tests of this agent:

### 1. Internal Data Analytics (Data Insights / BigQuery)

> **User Prompt:** "Which product categories have a price index above 105 compared to market competitors?"

**Sub-Agent Routed:** Data Insights (`sub_agents/data_insights.yaml`)  
**Authorized Table Queried:** `merc_pmci_price_index_summary`

**Agent Response:**
> Electronics Accessories (112.5) and Footwear (106.5) both have price indices above 105, placing them in the Premium / High Gap tier. Apparel is at 104.2, while Home Decor is at 98.5 (Competitive).

---

### 2. External Market Grounding (Market Context / Google Search)

> **User Prompt:** "How do major omnichannel retailers handle price-matching policies when competitors are out of stock?"

**Sub-Agent Routed:** Market Context (`sub_agents/market_context.yaml`)  
**Grounding Tool:** `google_search`

**Agent Response:**
> Major retailers (including Target, Best Buy, and Home Depot) explicitly require that the competitor item be **currently in stock** at the time of match request, preventing margin erosion on items competitors cannot deliver.

---

### 3. Visual Analytics & Chart Generation (`render_chart`)

> **User Prompt:** "Plot our price index versus market parity (100) across product categories."

**Sub-Agent Routed:** Data Insights (`sub_agents/data_insights.yaml`)  
**Custom Tool Invoked:** `render_chart` (`tools/chart_generator.py`)

**Agent Response:**
> I have rendered the bar chart comparing our category price index against market parity (100 baseline).

**Generated Artifact:**  
![Sample Chart](sample_chart.png)

---

## Data

All tables live in the shared `retail_ent_agents` BigQuery dataset, prefixed `merc_pmci_` (see `_shared/table_registry.yaml`).

| Table | Columns | Holds |
| :--- | :--- | :--- |
| `merc_pmci_competitor_price_feed` | `sku, category, our_price_dollars, amazon_price, walmart_price, target_price, competitor_price_gap_pct` | SKU-level competitor price comparisons and gap % |
| `merc_pmci_price_index_summary` | `category, price_index_vs_market, pricing_position_tier, tracked_skus_count` | Category price index vs market parity (100 baseline) |
| `merc_pmci_pos_price_match_claims` | `store_id, fiscal_month, claim_count, price_match_dollars_claimed, manager_override_count` | Store POS price match policy claims and discount dollars $ |
| `merc_pmci_competitor_stock_alerts` | `sku, competitor_name, competitor_stock_status, holding_margin_opportunity_dollars` | Competitor stock availability alerts and holding margin opportunity $ |

---

## Example Questions

Verified against this agent's `eval/agent.evalset.json`:

- "Which product categories have a price index above 105 compared to market competitors?"
- "What was the total POS price match dollars claimed in July 2026?"
- "How do major omnichannel retailers handle price-matching policies when competitors are out of stock?"

---

## Tools

- **`ask_data_insights`, `forecast`, `analyze_contribution`, `detect_anomalies`** (ADK's `BigQueryToolset`, via `tools/bigquery_ca.py`) — scoped to the four tables above.
- **`render_chart`** (`tools/chart_generator.py`) — custom tool for chart/visualization requests.
- **`google_search`** — used only by the Market Context sub-agent.

---

## Run It Locally

```bash
uv run adk run domains/merchandising/agents/price_matching_competitor_intel
```

---

## Files

```
price_matching_competitor_intel/
  root_agent.yaml                 # orchestrator — routing instructions
  sub_agents/
    data_insights.yaml             # BigQuery Conversational Analytics sub-agent
    market_context.yaml            # Google Search grounding sub-agent
  tools/
    bigquery_ca.py                  # BigQueryToolset factory
    chart_generator.py               # render_chart custom tool
    callbacks.py                      # current-date / BigQuery project injection
  data/                             # seed CSVs + generate_seed_data.py
  eval/agent.evalset.json          # ADK quality evals
  tests/{unit,integration}/         # mocked vs. real-BigQuery tests
  sample_chart.png                  # visual chart artifact captured from live smoke test
```
