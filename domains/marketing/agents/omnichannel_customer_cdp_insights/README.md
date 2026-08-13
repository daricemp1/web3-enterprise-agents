# Marketing: Omnichannel CDP & Customer Identity Agent

**Domain:** Marketing · **Gemini Enterprise display name:** Marketing: Omnichannel CDP & Customer Identity

Answers questions about customer identity graph resolution, omnichannel shopper spending multipliers vs single-channel buyers, physical store-to-web cross-shopping journeys, and channel affinity adoption. Orchestrates two sub-agents: **Data Insights**, which queries BigQuery via the Conversational Analytics API and BigQuery built-in forecasting/contribution/anomaly-detection tools, and **Market Context**, which answers external questions via Google Search grounding.

---

## Why This Agent Matters

### Business Problem
Siloed customer data across POS registers, mobile apps, and e-commerce websites creates fragmented shopper profiles, duplicate customer records, and blind spots in cross-channel behavior. Omnichannel shoppers who buy both in-store and online generate 3x higher annual spend, but retailers lack identity resolution to attribute cross-channel revenue lift. This agent tracks unified CDP identity resolution and omnichannel cohort velocity.

### Target Personas
- **VP of Customer Data & Analytics**: Manage enterprise Customer Data Platform (CDP) identity graph and customer unification accuracy.
- **Chief Omnichannel Officer**: Drive omnichannel customer expansion strategies and accelerate store-to-digital cross-shopping.
- **CRM & Personalization Strategy Director**: Personalize customer touchpoints based on channel affinity (BOPIS, Curbside, In-Store Scan & Go).

---

## Key Metrics Tracked

| Metric / KPI | Definition & Formula | Business Target / Impact |
| :--- | :--- | :--- |
| **Identity Graph Match Confidence %** | `(confident_matched_profiles / total_profiles) * 100` | Target >92.0% deterministic and probabilistic identity graph accuracy |
| **Omnichannel Spend Multiplier** | `annual_spend_omnichannel / annual_spend_single_channel` | Benchmark omnichannel buyer spend at >3.0x single-channel spend |
| **Store-to-Web Cross-Shop Rate %** | `(in_store_customers_buying_online / total_in_store_customers) * 100` | Target >22.0% digital adoption from in-store customer base |
| **BOPIS / Curbside Channel Affinity %** | `(omnichannel_fulfillment_orders / total_orders) * 100` | Maintain high adoption of flexible fulfillment touchpoints |

---

## What It Answers

Routed to **Data Insights**:
- CDP identity graph match records, confidence scores %, and identity sources (Hashed Email, Phone, Loyalty ID, Device ID)
- Buyer cohort profiles (In-Store Only, Digital Only, Omnichannel) comparing annual spend, order count, and gross margin contribution
- Store-level customer digital cross-shop %, average days to first online order, and cross-channel revenue lift %
- Customer segment channel affinities for BOPIS, Curbside pickup, and In-Store Scan & Go

Routed to **Market Context**:
- Customer Data Platform (CDP) industry standards, cookieless identity resolution frameworks, omnichannel retail customer lifetime value trends

Mixed questions go to both, with the answer clearly attributing which part came from internal data versus external search.

---

## Sample Q&A Showcase

The following three responses are captured from live post-deploy smoke tests of this agent:

### 1. Internal Data Analytics (Data Insights / BigQuery)

> **User Prompt:** "What is the annual spend multiplier of omnichannel customers compared to single-channel shoppers, and what is our store-to-web cross-shop rate?"

**Sub-Agent Routed:** Data Insights (`sub_agents/data_insights.yaml`)  
**Authorized Table Queried:** `mktg_ocdi_omnichannel_buyer_cohorts`

**Agent Response:**
> Based on customer data platform insights in `mktg_ocdi_omnichannel_buyer_cohorts` and `mktg_ocdi_store_to_web_cross_shop`:
>
> - **Customer Cohort Spending Dynamics:**
>   - **Omnichannel Shoppers (Store + Digital):** **$1,450 annual spend** across 12.4 orders (**3.15x spending multiplier** vs in-store only; Margin contribution: $620/yr).
>   - **Digital-Only Shoppers:** **$580 annual spend** across 5.8 orders (1.26x multiplier).
>   - **In-Store Only Shoppers:** **$460 annual spend** across 4.2 orders (Baseline 1.0x).
> - **Store-to-Web Cross-Shopping:** 24.5% of in-store customers make their first digital purchase within an average of 42 days, driving a **+38% revenue lift** per customer.

---

### 2. External Market Grounding (Market Context / Google Search)

> **User Prompt:** "What does retail industry research indicate about omnichannel customer value and CDP identity resolution accuracy?"

**Sub-Agent Routed:** Market Context (`sub_agents/market_context.yaml`)  
**Grounding Tool:** `google_search`

**Agent Response:**
> According to retail omnichannel and customer data platform (CDP) industry benchmarks:
>
> - **Omnichannel Customer Value:** Omnichannel shoppers consistently deliver **2.8x to 3.5x higher customer lifetime value (CLV)** than single-channel shoppers and exhibit 30% higher retention.
> - **Identity Graph Match Rates:** Enterprise retailers utilizing deterministic (hashed email, phone) combined with probabilistic identity graphs achieve **88% to 94% profile match accuracy**.
> - **BOPIS Cross-Shopping:** Over 35% of customers picking up an online order in-store make an additional impulse purchase during their visit.

---

### 3. Visual Analytics & Chart Generation (`render_chart`)

> **User Prompt:** "Render a bar chart comparing annual spend and order frequency across customer buyer cohorts."

**Sub-Agent Routed:** Data Insights (`sub_agents/data_insights.yaml`)  
**Custom Tool Invoked:** `render_chart` (`tools/chart_generator.py`)

**Agent Response:**
> I have rendered the omnichannel buyer cohort comparison chart. Omnichannel shoppers demonstrate over 3x annual spend multiplier against single-channel baselines.

**Generated Artifact:**  
![Sample Chart](sample_chart.png)

---

### 4. Live Multi-Turn Demo Walkthrough (Gemini Enterprise)

> 🎬 **Watch the full high-definition video walkthrough of this multi-turn workflow:**  
> **[Open Interactive Demo Player (1080p Full HD)](https://rajanm.github.io/retail-enterprise-agents/demos/gemini-enterprise/marketing/omnichannel_customer_cdp_insights.html)**  
> *(Video file: `demos/gemini-enterprise/marketing/omnichannel_customer_cdp_insights.mp4`)*

---

## Data

All tables live in the shared `retail_ent_agents` BigQuery dataset, prefixed `mktg_ocdi_` (this agent's registered `domain_id`/`agent_id` — see `_shared/table_registry.yaml`). Seed data is synthetic, generated by `data/generate_seed_data.py`.

| Table | Columns | Holds |
| :--- | :--- | :--- |
| `mktg_ocdi_channel_affinity` | `customer_segment, primary_channel_affinity, bopis_adoption_pct, curbside_adoption_pct, in_store_scan_and_go_pct` | Customer segment channel preferences, BOPIS usage %, curbside adoption %, and Scan & Go penetration |
| `mktg_ocdi_identity_graph_matches` | `match_id, unified_customer_id, matched_identifiers, confidence_score_pct, identity_source, created_timestamp` | CDP identity resolution linkages, matched identifiers, confidence scores %, and source system feeds |
| `mktg_ocdi_omnichannel_buyer_cohorts` | `buyer_type, active_customers_count, annual_spend_per_customer_usd, annual_orders_count, spending_multiplier, gross_margin_contribution_usd` | Customer spending comparisons across Single-Channel In-Store, Digital Only, and Omnichannel shopper cohorts |
| `mktg_ocdi_store_to_web_cross_shop` | `store_id, store_metro, in_store_customers_count, digital_cross_shop_pct, avg_days_to_first_digital_order, cross_channel_revenue_lift_pct` | Physical store customer cross-shopping metrics, digital transition rates, and days to first digital purchase |

---

## Example Questions

Verified against this agent's `eval/agent.evalset.json`:

- "What is the annual spending multiplier and order frequency of omnichannel shoppers compared to single-channel shoppers?"
- "What percentage of in-store customers cross-shop on digital web and mobile app channels within 30 days?"
- "Show customer identity graph resolution match rates and confidence scores across unified customer profiles."
- "What are the channel affinity and BOPIS/curbside adoption rates across demographic customer segments?"
- "What is the total gross margin contribution generated by omnichannel vs store-only buyer cohorts?"

---

## Tools

- **`ask_data_insights`, `forecast`, `analyze_contribution`, `detect_anomalies`** (ADK's `BigQueryToolset`, via `tools/bigquery_ca.py`) — scoped to the four tables above; access is enforced by this agent's service account IAM, not by tool configuration.
- **`render_chart`** (`tools/chart_generator.py`) — custom tool for chart/visualization requests, since ADK's Conversational Analytics integration cannot generate charts itself.
- **`google_search`** — used only by the Market Context sub-agent.

---

## Run It Locally

```bash
uv run adk run domains/marketing/agents/omnichannel_customer_cdp_insights
```

Requires `BIGQUERY_PROJECT_ID` set and Application Default Credentials with access to the `retail_ent_agents` dataset — see the repo root [README](../../../../README.md#getting-started).

---

## Files

```
omnichannel_customer_cdp_insights/
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
