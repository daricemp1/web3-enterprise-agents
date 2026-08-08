# Marketing: Churn Prediction & Win-Back Triggers Agent

**Domain:** Marketing · **Gemini Enterprise display name:** Marketing: Churn Prediction & Win-Back Triggers

Answers questions about customer churn risk scoring, category repurchase lapse intervals, automated win-back promotional offers, and reactivation cohort ROI. Orchestrates two sub-agents: **Data Insights**, which queries BigQuery via the Conversational Analytics API and BigQuery built-in forecasting/contribution/anomaly-detection tools, and **Market Context**, which answers external questions via Google Search grounding.

---

## Why This Agent Matters

### Business Problem
Customer lapse is insidious in retail—once a shopper crosses category-specific repurchase lapse thresholds, the cost to reactivate them increases exponentially. Without proactive ML-driven churn probability scoring and automated margin-optimized win-back offers, retailers suffer unnecessary customer decay and revenue attrition. This agent identifies at-risk cohorts and orchestrates targeted win-back campaigns.

### Target Personas
- **VP of Retention & Customer Lifecycle**: Formulate customer retention strategies and minimize churn across high-value shopper segments.
- **CRM & Lifecycle Marketing Manager**: Execute automated win-back trigger workflows across email, SMS, and direct mail.
- **Customer Analytics & Data Science Lead**: Optimize ML churn prediction algorithms and category lapse threshold rules.

---

## Key Metrics Tracked

| Metric / KPI | Definition & Formula | Business Target / Impact |
| :--- | :--- | :--- |
| **Predicted Churn Probability %** | `ML-calculated churn likelihood score (0.0 - 1.0)` | Identify and trigger interventions for customers exceeding 70% risk |
| **Category Repurchase Lapse Days** | `Days since last purchase vs category median repurchase cycle` | Flag lapsing shoppers before they reach 2x median cycle |
| **Win-Back Reactivation Rate %** | `(reactivated_customers / targeted_lapsed_customers) * 100` | Target >14.0% reactivation on 60-90 day lapsed cohorts |
| **Reactivation Net ROI Multiplier** | `incremental_gmv / (offer_discount_cost + send_cost)` | Maintain win-back campaign ROI >4.0x net margin return |

---

## What It Answers

Routed to **Data Insights**:
- Customer churn risk scores, RFM segment classifications, days since last purchase, and historic CLV
- Department-level median repurchase cycles and active vs lapsing customer distributions
- Win-back campaign offer discount depth, margin costs, and delivery channels
- Reactivation cohort success rates, incremental GMV generated, and net campaign ROI multipliers

Routed to **Market Context**:
- Retail customer retention strategies, automated win-back promotional cadence, churn prevention benchmarks

Mixed questions go to both, with the answer clearly attributing which part came from internal data versus external search.

---

## Sample Q&A Showcase

The following three responses are captured from live post-deploy smoke tests of this agent:

### 1. Internal Data Analytics (Data Insights / BigQuery)

> **User Prompt:** "What are our current customer churn risk distributions and which departments have the highest lapsing rates?"

**Sub-Agent Routed:** Data Insights (`sub_agents/data_insights.yaml`)  
**Authorized Table Queried:** `mktg_ccwa_lapse_intervals_by_dept`

**Agent Response:**
> Based on churn risk analytics in `mktg_ccwa_lapse_intervals_by_dept` and `mktg_ccwa_churn_risk_scores`:
>
> - **Department Lapse Dynamics:**
>   - **Apparel:** Median cycle 45 days; Churn threshold 90 days; **18.5% lapsing rate** (42,000 customers).
>   - **Beauty & Personal Care:** Median cycle 30 days; Churn threshold 60 days; **12.2% lapsing rate** (Fast replenishment cycle).
>   - **Home & Decor:** Median cycle 120 days; Churn threshold 240 days; **22.4% lapsing rate**.
> - **High-Risk CLV Exposure:** 8,450 Champions & Loyalists are currently flagged in High Risk tier (>75% churn probability), representing $1.85M in annual CLV risk.
> - **Recommended Action:** Deploy Offer WB-15 ($15 off $75) via SMS to Tier-1 Champions approaching 60 days inactive.

---

### 2. External Market Grounding (Market Context / Google Search)

> **User Prompt:** "What are industry standard reactivation rates and discounting strategies for lapsed retail customers?"

**Sub-Agent Routed:** Market Context (`sub_agents/market_context.yaml`)  
**Grounding Tool:** `google_search`

**Agent Response:**
> Industry retention and CRM win-back benchmarks show:
>
> - **Reactivation Rates:** Automated multi-touch win-back workflows typically achieve **10% to 16% reactivation** within 30 days of campaign deployment.
> - **Discount Depth Strategy:** Tiered incentives (e.g., $10 off $50 or free gift with purchase) preserve gross margins 25% better than blanket percentage discounts.
> - **Intervention Timing:** Triggering win-back outreach at 1.5x median repurchase cycle yields 2.3x higher conversion than waiting past 2.5x the cycle.

---

### 3. Visual Analytics & Chart Generation (`render_chart`)

> **User Prompt:** "Render a bar chart showing lapsing rates by department and reactivation ROI multipliers."

**Sub-Agent Routed:** Data Insights (`sub_agents/data_insights.yaml`)  
**Custom Tool Invoked:** `render_chart` (`tools/chart_generator.py`)

**Agent Response:**
> I have rendered the lapsing rates and reactivation campaign ROI visualization. Win-back campaigns consistently generate over 4.2x net ROI multiplier.

**Generated Artifact:**  
![Sample Chart](sample_chart.png)

---

## Data

All tables live in the shared `retail_ent_agents` BigQuery dataset, prefixed `mktg_ccwa_` (this agent's registered `domain_id`/`agent_id` — see `_shared/table_registry.yaml`). Seed data is synthetic, generated by `data/generate_seed_data.py`.

| Table | Columns | Holds |
| :--- | :--- | :--- |
| `mktg_ccwa_churn_risk_scores` | `customer_id, rfm_segment, predicted_churn_probability, days_since_last_purchase, historic_clv_usd, churn_risk_tier, recommended_intervention` | Individual customer churn risk scores, RFM segments, historic CLV, and recommended automated interventions |
| `mktg_ccwa_lapse_intervals_by_dept` | `department, median_repurchase_days, churn_threshold_days, active_customers_count, lapsing_customers_count, lapsing_rate_pct` | Department-specific repurchase cycle days, churn lapse thresholds, and lapsing customer counts |
| `mktg_ccwa_reactivation_cohorts` | `cohort_month, customers_targeted_count, reactivated_count, reactivation_rate_pct, incremental_gmv_usd, offer_cost_usd, net_roi_multiplier` | Monthly win-back cohort execution, reactivated buyer volume, incremental GMV, and net ROI multipliers |
| `mktg_ccwa_winback_campaign_offers` | `offer_id, offer_name, discount_depth_pct, channel, cost_per_send_usd, target_churn_tier, margin_cost_usd` | Win-back promotional offer structures, discount depths, target risk tiers, and channel margin costs |

---

## Example Questions

Verified against this agent's `eval/agent.evalset.json`:

- "What is our predicted customer churn rate and how many high-CLV customers are in the high-risk churn tier?"
- "What are the median repurchase lapse intervals and churn threshold days across merchandise departments?"
- "Show reactivation conversion rates and net ROI multipliers for our automated win-back campaign offers."
- "Which customer cohorts have demonstrated the highest incremental GMV lift post-reactivation?"
- "What is the margin cost vs incremental revenue trade-off for high-discount win-back promotions?"

---

## Tools

- **`ask_data_insights`, `forecast`, `analyze_contribution`, `detect_anomalies`** (ADK's `BigQueryToolset`, via `tools/bigquery_ca.py`) — scoped to the four tables above; access is enforced by this agent's service account IAM, not by tool configuration.
- **`render_chart`** (`tools/chart_generator.py`) — custom tool for chart/visualization requests, since ADK's Conversational Analytics integration cannot generate charts itself.
- **`google_search`** — used only by the Market Context sub-agent.

---

## Run It Locally

```bash
uv run adk run domains/marketing/agents/customer_churn_winback_analytics
```

Requires `BIGQUERY_PROJECT_ID` set and Application Default Credentials with access to the `retail_ent_agents` dataset — see the repo root [README](../../../../README.md#getting-started).

---

## Files

```
customer_churn_winback_analytics/
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
