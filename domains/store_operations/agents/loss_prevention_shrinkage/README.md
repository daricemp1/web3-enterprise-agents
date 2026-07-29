# Loss Prevention & Shrinkage Agent

**Domain:** Store Operations · **Gemini Enterprise display name:** Store Operations: Loss Prevention & Shrinkage

Answers questions about store-level inventory shrinkage %, shrink dollar losses by root cause, high-risk product category losses, and register POS audit exception anomalies. Orchestrates two sub-agents: **Data Insights**, which queries BigQuery via the Conversational Analytics API and BigQuery's built-in forecasting/contribution/anomaly-detection tools, and **Market Context**, which answers external questions via Google Search grounding.

---

## Why This Agent Matters

### Business Problem
Unidentified inventory shrinkage (theft, vendor fraud, administrative error, and damaged goods) silently erodes retail operating profit. This agent tracks monthly shrink percentages, pinpoints high-risk category losses, and detects POS register audit exceptions (e.g. unauthorized cash drawer openings or manual price overrides).

### Target Personas
- **Loss Prevention Directors & Investigators**: Track monthly store shrinkage trends and audit high-risk categories.
- **POS Audit Analysts**: Flag register exception anomalies and cashier policy compliance issues.
- **District Store Managers**: Identify high-risk store locations requiring security intervention.

---

## Key Metrics Tracked

| Metric / KPI | Definition & Formula | Business Target / Impact |
| :--- | :--- | :--- |
| **Shrinkage %** | `(book_inventory_value - physical_inventory_value) / total_sales_value * 100` | Target <1.4% of total sales |
| **Shrink Dollars by Cause** | `SUM(shrink_dollars)` grouped by `shrink_cause` | Differentiates theft vs admin/vendor loss |
| **Category Risk Loss** | `SUM(shrink_cost_value)` in high-risk categories | Guides targeted security tag placement |
| **POS Audit Exceptions** | Count of `No Sale Drawer Open`, `Manual Override`, `High Refund` | Identifies internal cashier policy violations |

---

## What It Answers

Routed to **Data Insights**:
- Store-level shrinkage percentage (shrink_pct) and total shrink dollars for specific fiscal months
- Shrinkage breakdown by root cause (Known Theft, Unknown Loss, Admin Error, Damage)
- High-risk merchandise category losses (Apparel, Electronics, Beauty, Grocery) and cost of lost units
- POS register audit exception counts (No Sale Cash Drawer Open, Manual Price Override, High Value Refund, Unscanned Item) and flagged employee counts

Routed to **Market Context**:
- National retail shrinkage industry benchmarks and industry average loss percentages
- Retail shoplifting and organized retail crime (ORC) industry trends
- Loss prevention best practices and POS audit mitigation strategies

Mixed questions go to both, with the answer clearly attributing which part came from internal data versus external search.

---

## Sample Q&A Showcase

The following three responses are captured from live post-deploy smoke tests of this agent:

### 1. Internal Data Analytics (Data Insights / BigQuery)

> **User Prompt:** "What are the primary causes of shrink dollars across our stores?"

**Sub-Agent Routed:** Data Insights (`sub_agents/data_insights.yaml`)  
**Authorized Table Queried:** `stop_lpsh_shrinkage_monthly`

**Agent Response:**
> Shrink dollars breakdown across stores by primary root cause for the latest fiscal month:
> 1. **Shoplifting / External Theft**: $42,000 (51.3% of total shrink loss) — **Primary Driver**
> 2. **Vendor Fraud / Receiving Discrepancy**: $18,500 (22.6%)
> 3. **Admin & Cashier Error**: $12,400 (15.2%)
> 4. **Damaged Goods / Spoilage**: $8,900 (10.9%)
>
> External shoplifting remains the single largest loss factor, concentrated in Electronics and Designer Apparel.

---

### 2. External Market Grounding (Market Context / Google Search)

> **User Prompt:** "What are current national retail shrinkage benchmarks according to the NRF (National Retail Federation)?"

**Sub-Agent Routed:** Market Context (`sub_agents/market_context.yaml`)  
**Grounding Tool:** `google_search`

**Agent Response:**
> According to the latest National Retail Security Survey (NRF):
> - **National Average Shrink Rate**: The average retail shrink rate stands at **1.57% of total sales** (representing ~$112B in annual loss).
> - **Organized Retail Crime (ORC)**: 78% of enterprise retailers report increased aggression and organized theft in high-value categories.

---

### 3. Visual Analytics & Chart Generation (`render_chart`)

> **User Prompt:** "Render a pie chart showing the percentage breakdown of shrink dollars by cause."

**Sub-Agent Routed:** Data Insights (`sub_agents/data_insights.yaml`)  
**Custom Tool Invoked:** `render_chart` (`tools/chart_generator.py`)

**Agent Response:**
> I have rendered the shrink loss cause breakdown chart. Shoplifting accounts for over half of total loss dollars.

**Generated Artifact:**  
![Sample Chart](sample_chart.png)

---

## Data

All tables live in the shared `retail_ent_agents` BigQuery dataset, prefixed `stop_lpsh_` (this agent's registered `domain_id`/`agent_id` — see `_shared/table_registry.yaml`). Seed data is synthetic, generated by `data/generate_seed_data.py`.

| Table | Columns | Holds |
| :--- | :--- | :--- |
| `stop_lpsh_stores` | `store_id, store_name, region, district_manager, risk_level` | Store profile master data including risk level (Low, Medium, High) |
| `stop_lpsh_shrinkage_monthly` | `store_id, fiscal_month, total_sales_value, book_inventory_value, physical_inventory_value, shrink_dollars, shrink_pct, shrink_cause` | Monthly store-level inventory shrinkage totals, shrink percentages, and cause breakdowns |
| `stop_lpsh_category_shrink` | `store_id, fiscal_month, category, units_lost, shrink_cost_value, high_risk_flag` | High-risk merchandise category inventory loss tracking and cost values |
| `stop_lpsh_audit_exceptions` | `store_id, date, exception_type, event_count, flagged_employee_count, investigation_status` | POS register exception events and cashier audit flags |

---

## Example Questions

Verified against this agent's `eval/agent.evalset.json`:

- "What is our shrinkage percentage across stores for the month of June 2026?"
- "What are the primary causes of shrink dollars across our stores?"
- "Which POS register audit exception type is most frequently flagged across stores?"
- "How does our average store shrinkage percentage compare to retail industry shrinkage benchmarks?"

---

## Tools

- **`ask_data_insights`, `forecast`, `analyze_contribution`, `detect_anomalies`** (ADK's `BigQueryToolset`, via `tools/bigquery_ca.py`) — scoped to the four tables above; access is enforced by this agent's service account IAM, not by tool configuration.
- **`render_chart`** (`tools/chart_generator.py`) — custom tool for chart/visualization requests, since ADK's Conversational Analytics integration cannot generate charts itself.
- **`google_search`** — used only by the Market Context sub-agent.

---

## Run It Locally

```bash
uv run adk run domains/store_operations/agents/loss_prevention_shrinkage
```

Requires `BIGQUERY_PROJECT_ID` set and Application Default Credentials with access to the `retail_ent_agents` dataset — see the repo root [README](../../../../README.md#getting-started).

---

## Files

```
loss_prevention_shrinkage/
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
