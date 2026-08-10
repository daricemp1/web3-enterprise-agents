# Merchandising: Markdown & Clearance Optimization Agent

**Domain:** Merchandising · **Gemini Enterprise display name:** Merchandising: Markdown & Clearance Optimization

> 🎬 **Demo Video & Interactive Player**: [Full HD Walkthrough MP4](../../../../demos/gemini-enterprise/merchandising/markdown_clearance_optimization.mp4) · [Interactive HTML Demo Player](../../../../demos/gemini-enterprise/merchandising/markdown_clearance_optimization.html)

---

## Why This Agent Matters

### Business Problem
End-of-season and terminal merchandise clearance represents one of the largest margin erosion risks in retail. Late or overly aggressive markdowns destroy gross margin, while delayed markdowns leave seasonal inventory stranded past season end. Optimizing clearance discount ladders (25% → 40% → 60% → Salvage) balances inventory velocity with gross margin protection.

### Target Personas
- **Director of Clearance & Markdown Planning**: Oversee category clearance velocity, discount ladder progression, and markdown dollar budget allocation.
- **Category Merchandisers**: Monitor SKU clearance sell-through % vs target curves and execute salvage/jobber liquidation sales.
- **Merchandise Financial Planners**: Track cumulative gross margin erosion dollars ($) and salvage recovery writeoff avoidance.

---

## Key Metrics Tracked

| Metric / KPI | Definition & Formula | Business Target / Impact |
| :--- | :--- | :--- |
| **Clearance Sell-Through %** | `(clearance_units_sold / total_clearance_inventory) * 100` | Target 85%+ clearance sell-through before season end |
| **Discount Depth %** | `((original_price - current_price) / original_price) * 100` | Maximizes velocity at lowest viable discount depth |
| **Markdown Budget Spend ($)** | Cumulative markdown price reduction dollars expended | Keeps markdown dollar erosion within fiscal budget |
| **Salvage Recovery ($)** | Total dollars recovered from terminal jobber/salvage sales | Minimizes total inventory writeoff losses |

---

## What It Answers

Routed to **Data Insights**:
- Clearance catalog markdown stages, discount depth %, planned markdown discount ladders, weekly sell-through velocity curves, gross margin erosion $, and liquidation salvage recovery $.

Routed to **Market Context**:
- Industry clearance timing benchmarks, end-of-season liquidation strategies, and markdown depth progression best practices.

---

## Sample Q&A Showcase

The following three responses are captured from live post-deploy smoke tests of this agent:

### 1. Internal Data Analytics (Data Insights / BigQuery)

### 1. Internal Data Analytics (Data Insights / BigQuery)

> **User Prompt:** "What is our current markdown budget spend and clearance sell-through velocity?"

**Sub-Agent Routed:** Data Insights (`sub_agents/data_insights.yaml`)  
**Authorized Table Queried:** `merc_mcle_clearance_velocity_weekly`, `merc_mcle_markdown_budget_spend`

**Agent Response:**
> Based on current clearance tracking data:
> - **Markdown Budget Utilization:** **$142,500** spent out of a allocated **$200,000** seasonal clearance budget (**71.25% budget utilization**).
> - **Weekly Clearance Velocity:** Clearance SKUs are currently turning at an average velocity of **6.8% per week**.
> - **Inventory Recovery Realization:** Clearance sales have generated **$385,200 in gross liquidation recovery**, delivering an average salvage recovery rate of **58.4% of original retail price**.

---

### 2. External Market Grounding (Market Context / Google Search)

> **User Prompt:** "What are best practices for retail end-of-season markdown discount ladders?"

**Sub-Agent Routed:** Market Context (`sub_agents/market_context.yaml`)  
**Grounding Tool:** `google_search`

**Agent Response:**
> Industry best practices for retail end-of-season markdown ladders include:
> - **Cadenced Step-Down Schedule:** Establishing structured 2-to-3 week review cycles with defined discount steps (e.g., First Drop at 20–25% off, Second Drop at 40–50% off, Final Clearance at 60–70% off) rather than immediate deep price cuts.
> - **Velocity-Triggered Dynamic Transitions:** Transitioning SKUs down the ladder based strictly on weekly sell-through velocity thresholds (e.g., maintaining 25% discount if weekly velocity exceeds 7%, stepping to 40% if velocity falls below 4%).
> - **Salvage & Secondary Channel Thresholds:** Setting a firm cut-off point (typically 60–90 days on clearance) where remaining inventory transitions to factory outlets or third-party liquidators to protect brand equity and reclaim warehouse holding space.

---

### 3. Visual Analytics & Chart Generation (`render_chart`)

> **User Prompt:** "Plot our cumulative clearance velocity curve versus target sell-through percentage."

**Sub-Agent Routed:** Data Insights (`sub_agents/data_insights.yaml`)  
**Custom Tool Invoked:** `render_chart` (`tools/chart_generator.py`)

**Agent Response:**
> I have rendered the chart showing our cumulative clearance sell-through velocity versus target curve across markdown stages.

**Generated Artifact:**  
![Sample Chart](sample_chart.png)

---

### 4. Live Multi-Turn Demo Walkthrough (Gemini Enterprise)

An authentic multi-turn interactive session recorded live in Gemini Enterprise demonstrating dedicated agent invocation, BigQuery conversational analytics, Google Search market grounding, visual chart artifact generation, and executive Canvas presentation synthesis:

> ### 🎬 <a href="https://rajanm.github.io/retail-enterprise-agents/demos/gemini-enterprise/merchandising/markdown_clearance_optimization.html" target="_blank" rel="noopener noreferrer">▶️ Launch 1080p Video Player () ↗</a>
> **Walkthrough:** 1080p Full HD MP4 · **Format:** H.264 MP4 + HTML5 Player · [Direct MP4 Link](../../../../demos/gemini-enterprise/merchandising/markdown_clearance_optimization.mp4)  
> *(Opens the dedicated HTML5 web player in a new tab with Play/Pause, Seekbar, Speed & Fullscreen controls)*


---

## Data

All tables live in the shared `retail_ent_agents` BigQuery dataset, prefixed `merc_mcle_` (see `_shared/table_registry.yaml`).

| Table | Columns | Holds |
| :--- | :--- | :--- |
| `merc_mcle_clearance_catalog` | `sku, category, original_retail_price, current_clearance_price, markdown_stage, units_in_clearance` | Clearance catalog SKU master, pricing, and markdown stage |
| `merc_mcle_markdown_ladders` | `category, planned_stage_week, target_discount_pct, target_sell_through_pct, max_markdown_budget_dollars` | Planned category markdown discount ladders and budget caps |
| `merc_mcle_clearance_velocity_weekly` | `sku, fiscal_week, discount_depth_pct, units_sold, remaining_units, gross_margin_erosion_dollars` | Weekly clearance sales velocity, units sold, and margin erosion |
| `merc_mcle_salvage_liquidation_recovery` | `category, terminal_units_salvaged, jobber_sale_price_dollars, recovered_dollars, writeoff_avoidance_pct` | Terminal inventory jobber liquidation sales and salvage recovery $ |

---

## Example Questions

Verified against this agent's `eval/agent.evalset.json`:

- "What is the clearance sell-through rate and markdown dollar spend for Apparel SKUs in July 2026?"
- "What is our terminal salvage recovery dollar value for Home Decor?"
- "What are retail industry best practices for end-of-season apparel clearance markdown timing?"

---

## Tools

- **`ask_data_insights`, `forecast`, `analyze_contribution`, `detect_anomalies`** (ADK's `BigQueryToolset`, via `tools/bigquery_ca.py`) — scoped to the four tables above.
- **`render_chart`** (`tools/chart_generator.py`) — custom tool for chart/visualization requests.
- **`google_search`** — used only by the Market Context sub-agent.

---

## Run It Locally

```bash
uv run adk run domains/merchandising/agents/markdown_clearance_optimization
```

---

## Files

```
markdown_clearance_optimization/
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
