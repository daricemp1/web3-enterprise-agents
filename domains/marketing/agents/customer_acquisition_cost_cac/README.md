# Marketing: CAC Payback Velocity & Unit Economics Agent

**Domain:** Marketing · **Gemini Enterprise display name:** Marketing: CAC Payback Velocity & Unit Economics

Answers questions about paid and blended Customer Acquisition Cost (CAC) by channel, CAC payback velocity (months), new customer cohort repeat rates, and unit economics margin recovery. Orchestrates two sub-agents: **Data Insights**, which queries BigQuery via the Conversational Analytics API and BigQuery built-in forecasting/contribution/anomaly-detection tools, and **Market Context**, which answers external questions via Google Search grounding.

---

## Why This Agent Matters

### Business Problem
Escalating digital customer acquisition costs (CAC) across paid search and social channels threaten e-commerce unit economics. Without granular cohort margin recovery tracking and payback period calculation, retailers overspend on unprofitable acquisition channels and underfund channels with high first-order AOV and fast repeat acceleration. This agent monitors blended vs paid CAC, cohort gross margin recovery, and payback velocity.

### Target Personas
- **Chief Marketing Officer & Head of Growth**: Evaluate customer acquisition efficiency and balance paid vs blended CAC targets.
- **Performance Marketing & Media Director**: Manage channel-level CAC ceilings and reallocate ad spend toward fast-payback channels.
- **FP&A & Commercial Finance Lead**: Track customer cohort margin recovery curves and validate CAC payback horizons.

---

## Key Metrics Tracked

| Metric / KPI | Definition & Formula | Business Target / Impact |
| :--- | :--- | :--- |
| **Paid CAC ($)** | `channel_ad_spend / paid_new_customers_acquired` | Keep paid acquisition cost below target ceiling ($45.00) |
| **Blended CAC ($)** | `total_marketing_spend / total_new_customers_acquired` | Target blended CAC <$28.00 across omnichannel acquisition |
| **CAC Payback Period (Months)** | `Months required for cohort gross margin to equal initial CAC` | Target payback horizon <4.5 months |
| **60-Day Repeat Order Rate %** | `(cohort_repeat_buyers_60d / total_cohort_buyers) * 100` | Target >28.0% repeat purchase rate within 60 days of acquisition |

---

## What It Answers

Routed to **Data Insights**:
- Paid vs blended CAC by acquisition channel (Paid Search, Meta Ads, TikTok, Affiliate, Influencer)
- New customer cohort acquisition volume, first-order AOV, and 60-day repeat order velocity
- Cohort gross margin recovery curves across months 1, 3, and 6 vs initial CAC
- Channel ad spend, impression volume, click traffic, and Cost per Click (CPC)

Routed to **Market Context**:
- Retail e-commerce CAC benchmarks by channel, privacy attribution shifts (iOS ATT, Privacy Sandbox), LTV:CAC industry ratios

Mixed questions go to both, with the answer clearly attributing which part came from internal data versus external search.

---

## Sample Q&A Showcase

The following three responses are captured from live post-deploy smoke tests of this agent:

### 1. Internal Data Analytics (Data Insights / BigQuery)

> **User Prompt:** "What is our paid vs blended Customer Acquisition Cost (CAC) by channel and which channels have the fastest payback period?"

**Sub-Agent Routed:** Data Insights (`sub_agents/data_insights.yaml`)  
**Authorized Table Queried:** `mktg_cacc_cac_by_channel`

**Agent Response:**
> Based on acquisition performance in `mktg_cacc_cac_by_channel` and `mktg_cacc_payback_period_months`:
>
> - **Paid Search:** Paid CAC **$34.50** (Target ceiling $40.00); Payback period: **3.2 months** (Fastest recovery, 32.5% 60-day repeat rate).
> - **Affiliate Marketing:** Paid CAC **$22.00**; Payback period: **2.8 months** (Lowest CAC, high profitability).
> - **Meta/Social Ads:** Paid CAC **$44.80** (Near ceiling $45.00); Payback period: **4.8 months** (High volume, requires email nurturing).
> - **Blended Omnichannel CAC:** Overall blended CAC is **$26.40**, well within the $28.00 target ceiling.

---

### 2. External Market Grounding (Market Context / Google Search)

> **User Prompt:** "What are current industry standards for e-commerce CAC payback periods and LTV:CAC ratios?"

**Sub-Agent Routed:** Market Context (`sub_agents/market_context.yaml`)  
**Grounding Tool:** `google_search`

**Agent Response:**
> According to retail performance marketing and direct-to-consumer finance benchmarks:
>
> - **CAC Payback Period:** Healthy retail e-commerce brands target a payback window of **3 to 6 months** on first-party repeat purchases.
> - **LTV:CAC Ratio:** A sustainable benchmark ratio is **3.0x to 4.5x** over a 12-month customer lifetime horizon.
> - **Repeat Rate Acceleration:** Converting a first-time buyer to a second order within 60 days increases 12-month retention by over 60%.

---

### 3. Visual Analytics & Chart Generation (`render_chart`)

> **User Prompt:** "Render a bar chart comparing Paid CAC vs Target Ceiling and CAC Payback Period across channels."

**Sub-Agent Routed:** Data Insights (`sub_agents/data_insights.yaml`)  
**Custom Tool Invoked:** `render_chart` (`tools/chart_generator.py`)

**Agent Response:**
> I have rendered the CAC and payback period comparison chart. Affiliate and Paid Search deliver the fastest margin payback below 3.5 months.

**Generated Artifact:**  
![Sample Chart](sample_chart.png)

---

### 4. Live Multi-Turn Demo Walkthrough (Gemini Enterprise)

> 🎬 **Watch the full high-definition video walkthrough of this multi-turn workflow:**  
> **[Open Interactive Demo Player (1080p Full HD)](https://rajanm.github.io/retail-enterprise-agents/demos/gemini-enterprise/marketing/customer_acquisition_cost_cac.html)**  
> *(Video file: `demos/gemini-enterprise/marketing/customer_acquisition_cost_cac.mp4`)*

---

## Data

All tables live in the shared `retail_ent_agents` BigQuery dataset, prefixed `mktg_cacc_` (this agent's registered `domain_id`/`agent_id` — see `_shared/table_registry.yaml`). Seed data is synthetic, generated by `data/generate_seed_data.py`.

| Table | Columns | Holds |
| :--- | :--- | :--- |
| `mktg_cacc_cac_by_channel` | `channel, month, total_spend_usd, new_customers_count, paid_cac_usd, blended_cac_usd, target_cac_ceiling_usd` | Monthly channel acquisition spend, new customer counts, paid CAC vs blended CAC, and target CAC ceilings |
| `mktg_cacc_new_customer_cohorts` | `acquisition_channel, cohort_month, new_customers_acquired, first_order_gmv_usd, first_order_aov_usd, repeat_order_60d_pct` | New customer acquisition cohorts, initial order GMV, first-order AOV, and 60-day repeat purchase rate % |
| `mktg_cacc_paid_marketing_spend` | `channel, month, ad_spend_usd, clicks_count, cpc_usd, impressions_count` | Granular channel advertising spend, traffic clicks, cost per click (CPC), and total impression reach |
| `mktg_cacc_payback_period_months` | `cohort_month, channel, initial_cac_usd, gross_margin_pct, month_1_margin_recovery, month_3_margin_recovery, month_6_margin_recovery, payback_period_months` | Cohort gross margin recovery milestones at 1/3/6 months and calculated CAC payback period in months |

---

## Example Questions

Verified against this agent's `eval/agent.evalset.json`:

- "What is our Customer Acquisition Cost (CAC) by marketing channel and how does it compare to target ceilings?"
- "What is the average CAC payback period in months across paid search, paid social, and affiliate cohorts?"
- "Show first-order Average Order Value (AOV) and 60-day repeat purchase rate by customer acquisition channel."
- "What is our blended CAC vs paid CAC across retail acquisition funnels in 2026 YTD?"
- "Which acquisition channels deliver the fastest cumulative gross margin recovery and highest LTV:CAC ratios?"

---

## Tools

- **`ask_data_insights`, `forecast`, `analyze_contribution`, `detect_anomalies`** (ADK's `BigQueryToolset`, via `tools/bigquery_ca.py`) — scoped to the four tables above; access is enforced by this agent's service account IAM, not by tool configuration.
- **`render_chart`** (`tools/chart_generator.py`) — custom tool for chart/visualization requests, since ADK's Conversational Analytics integration cannot generate charts itself.
- **`google_search`** — used only by the Market Context sub-agent.

---

## Run It Locally

```bash
uv run adk run domains/marketing/agents/customer_acquisition_cost_cac
```

Requires `BIGQUERY_PROJECT_ID` set and Application Default Credentials with access to the `retail_ent_agents` dataset — see the repo root [README](../../../../README.md#getting-started).

---

## Files

```
customer_acquisition_cost_cac/
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
