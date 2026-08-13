# Marketing: Geotargeted & Local Store Marketing Agent

**Domain:** Marketing · **Gemini Enterprise display name:** Marketing: Geotargeted & Local Store Marketing

Answers questions about local store trade area demographics, geofenced mobile advertising campaigns, physical store foot-traffic lift, and localized promo code redemptions. Orchestrates two sub-agents: **Data Insights**, which queries BigQuery via the Conversational Analytics API and BigQuery built-in forecasting/contribution/anomaly-detection tools, and **Market Context**, which answers external questions via Google Search grounding.

---

## Why This Agent Matters

### Business Problem
Physical brick-and-mortar stores require localized digital marketing to drive in-store foot traffic, promote grand openings, and clear local overstock. Blanket national ad campaigns waste budget in under-penetrated markets. This agent analyzes store trade area demographics, geofenced mobile ad effectiveness, and in-store foot traffic lift from local digital campaigns.

### Target Personas
- **Director of Field & Local Store Marketing**: Align localized ad spend to store-level sales goals and foot-traffic targets.
- **Regional Retail Marketing Managers**: Track store trade area campaign performance, geotargeted promo redemptions, and store visit lift.
- **Omnichannel Growth Lead**: Optimize digital-to-physical store drive campaigns using geofencing and mobile location signals.

---

## Key Metrics Tracked

| Metric / KPI | Definition & Formula | Business Target / Impact |
| :--- | :--- | :--- |
| **Store Foot Traffic Lift %** | `((exposed_daily_traffic - baseline_daily_traffic) / baseline_daily_traffic) * 100` | Target >12.0% incremental foot traffic lift during active local campaigns |
| **Cost per Store Visit ($)** | `local_ad_spend / incremental_store_visitors` | Maintain cost per incremental store visit under $4.50 |
| **In-Store Promo Redemption GMV ($)** | `Total in-store sales attributed to local promo codes` | Drive >$50,000 incremental sales per store district |
| **Geofenced Ad CTR %** | `(ad_clicks / ad_impressions) * 100` | Target >1.8% CTR on mobile radius geotargeted ads |

---

## What It Answers

Routed to **Data Insights**:
- Store trade area population demographics, median household income, and retail density index
- Geofenced local campaign spend, impressions, clicks, and CTR across channels (Google Local, Meta, TikTok)
- Daily store foot traffic baseline vs exposed visitors and calculated cost per store visit ($)
- Local in-store promotional code redemptions, in-store sales GMV, and new local customer acquisition %

Routed to **Market Context**:
- Geofencing mobile marketing benchmarks, location-based advertising foot traffic conversion rates, local retail marketing trends

Mixed questions go to both, with the answer clearly attributing which part came from internal data versus external search.

---

## Sample Q&A Showcase

The following three responses are captured from live post-deploy smoke tests of this agent:

### 1. Internal Data Analytics (Data Insights / BigQuery)

> **User Prompt:** "What is our foot traffic lift and cost per store visit across local store digital campaigns, and which stores saw the highest promo redemptions?"

**Sub-Agent Routed:** Data Insights (`sub_agents/data_insights.yaml`)  
**Authorized Table Queried:** `mktg_gtlm_store_foot_traffic_lift`

**Agent Response:**
> Based on local geotargeting analytics in `mktg_gtlm_store_foot_traffic_lift` and `mktg_gtlm_geo_promo_conversions`:
>
> - **Foot Traffic Lift by Store:**
>   - **Store 101 (Downtown Flagship):** **+18.4% traffic lift** (1,450 daily exposed vs 1,225 baseline; Cost per visit: **$3.15**).
>   - **Store 104 (Suburban Center):** **+14.2% traffic lift** (820 daily exposed vs 718 baseline; Cost per visit: **$3.80**).
>   - **Store 108 (Metro Mall):** **+9.5% traffic lift** (Cost per visit: **$4.90**).
> - **Local Promo Redemptions:** Promo `LOCAL20` drove $68,400 in-store sales with a $78.50 AOV, acquiring 34% first-time local shoppers.

---

### 2. External Market Grounding (Market Context / Google Search)

> **User Prompt:** "What are industry benchmarks for local mobile geofencing campaigns driving retail store foot traffic?"

**Sub-Agent Routed:** Market Context (`sub_agents/market_context.yaml`)  
**Grounding Tool:** `google_search`

**Agent Response:**
> According to location-based marketing and retail foot traffic studies:
>
> - **Foot Traffic Lift:** 3-to-5 mile mobile geofencing campaigns average between **8% and 15% incremental foot traffic lift** for specialty and department retail.
> - **Cost per Store Visit (CPV):** Industry CPV benchmarks range from **$2.50 to $5.50** depending on market metro density.
> - **Drive-to-Store Formats:** Dynamic map pins and real-time inventory display ads boost local CTR by 2.2x over static promotional banners.

---

### 3. Visual Analytics & Chart Generation (`render_chart`)

> **User Prompt:** "Render a bar chart comparing foot traffic lift % and cost per visit across store campaigns."

**Sub-Agent Routed:** Data Insights (`sub_agents/data_insights.yaml`)  
**Custom Tool Invoked:** `render_chart` (`tools/chart_generator.py`)

**Agent Response:**
> I have rendered the local store foot traffic lift and cost per visit visualization. Downtown and suburban stores demonstrate high foot traffic conversion at low CPVs.

**Generated Artifact:**  
![Sample Chart](sample_chart.png)

---

### 4. Live Multi-Turn Demo Walkthrough (Gemini Enterprise)

> 🎬 **Watch the full high-definition video walkthrough of this multi-turn workflow:**  
> **[Open Interactive Demo Player (1080p Full HD)](https://rajanm.github.io/retail-enterprise-agents/demos/gemini-enterprise/marketing/geotargeted_local_marketing.html)**  
> *(Video file: `demos/gemini-enterprise/marketing/geotargeted_local_marketing.mp4`)*

---

## Data

All tables live in the shared `retail_ent_agents` BigQuery dataset, prefixed `mktg_gtlm_` (this agent's registered `domain_id`/`agent_id` — see `_shared/table_registry.yaml`). Seed data is synthetic, generated by `data/generate_seed_data.py`.

| Table | Columns | Holds |
| :--- | :--- | :--- |
| `mktg_gtlm_geo_promo_conversions` | `promo_code, store_id, promo_type, redemptions_in_store, in_store_sales_usd, aov_usd, new_local_customers_pct` | Local store promo code redemptions, in-store sales GMV, basket AOV, and new local customer share % |
| `mktg_gtlm_local_digital_campaigns` | `campaign_id, store_id, channel, ad_type, geofence_radius_miles, impressions, clicks, ctr_pct, ad_spend_usd` | Localized store digital campaigns, geofence radius in miles, impressions, clicks, CTR %, and ad spend |
| `mktg_gtlm_store_foot_traffic_lift` | `store_id, campaign_id, baseline_daily_traffic, exposed_daily_traffic, incremental_visitors_count, foot_traffic_lift_pct, cost_per_store_visit_usd` | Store-level daily visitor traffic lift, incremental visitors, foot traffic lift %, and cost per store visit ($) |
| `mktg_gtlm_store_trade_areas` | `store_id, trade_area_type, radius_miles, household_population, median_household_income_usd, retail_density_index` | Store trade area definitions, radius distances, surrounding population, median income, and retail density |

---

## Example Questions

Verified against this agent's `eval/agent.evalset.json`:

- "What is our incremental store foot-traffic lift percentage and cost per store visit from local geofenced advertising?"
- "Which local digital advertising channels (Google Local Inventory Ads, Meta Geofence, Maps) delivered the highest CTR?"
- "Show in-store redemption volume and gross revenue generated from localized digital promo coupons."
- "What are the household demographics and retail density characteristics across primary store trade areas?"
- "What percentage of customers visiting stores through local campaigns are new local customers?"

---

## Tools

- **`ask_data_insights`, `forecast`, `analyze_contribution`, `detect_anomalies`** (ADK's `BigQueryToolset`, via `tools/bigquery_ca.py`) — scoped to the four tables above; access is enforced by this agent's service account IAM, not by tool configuration.
- **`render_chart`** (`tools/chart_generator.py`) — custom tool for chart/visualization requests, since ADK's Conversational Analytics integration cannot generate charts itself.
- **`google_search`** — used only by the Market Context sub-agent.

---

## Run It Locally

```bash
uv run adk run domains/marketing/agents/geotargeted_local_marketing
```

Requires `BIGQUERY_PROJECT_ID` set and Application Default Credentials with access to the `retail_ent_agents` dataset — see the repo root [README](../../../../README.md#getting-started).

---

## Files

```
geotargeted_local_marketing/
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
