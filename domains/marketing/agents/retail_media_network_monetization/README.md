# Marketing: Retail Media Network & Sponsored Ad Yield Agent

**Domain:** Marketing · **Gemini Enterprise display name:** Marketing: Retail Media Network & Sponsored Ad Yield

Answers questions about Retail Media Network (RMN) ad revenues, sponsored product search auction yields (CPC/eCPM), ad inventory fill rates, and CPG brand advertiser ROAS delivery reports. Orchestrates two sub-agents: **Data Insights**, which queries BigQuery via the Conversational Analytics API and BigQuery built-in forecasting/contribution/anomaly-detection tools, and **Market Context**, which answers external questions via Google Search grounding.

---

## Why This Agent Matters

### Business Problem
Retail Media Networks (RMN) represent the fastest-growing high-margin revenue stream for modern retailers. Maximizing RMN profitability requires balancing on-site sponsored search auction clearing prices (CPC/eCPM), ad slot inventory fill rates, and CPG brand advertiser ROAS delivery. This agent monitors sponsored product auctions, publisher yield, and advertiser performance reports.

### Target Personas
- **Head of Retail Media Network (RMN)**: Manage enterprise retail media monetization, ad inventory yield, and CPG advertising growth.
- **Ad Operations & Yield Management Director**: Optimize second-price auction floors, slot fill rates, and eCPM yields across search and category pages.
- **CPG Strategic Brand Partnership Lead**: Deliver advertiser performance scorecards, attributed ROAS reports, and new-to-brand acquisition metrics.

---

## Key Metrics Tracked

| Metric / KPI | Definition & Formula | Business Target / Impact |
| :--- | :--- | :--- |
| **Sponsored Search eCPM ($)** | `(ad_revenue / impressions) * 1000` | Target >$18.50 effective CPM across top search query placements |
| **Average Clearing CPC ($)** | `ad_revenue / clicks` | Optimize bid floors to maintain average CPC between $0.85 - $1.45 |
| **Ad Placement Fill Rate %** | `(served_impressions / total_ad_opportunities) * 100` | Maintain ad placement inventory fill rate >94.0% |
| **Advertiser Attributed ROAS** | `attributed_sales_usd / advertiser_ad_spend` | Deliver average advertiser ROAS >4.5x to ensure campaign renewal |

---

## What It Answers

Routed to **Data Insights**:
- RMN CPG advertiser accounts, tier commitments, active campaigns, and credit limit allocations
- Real-time sponsored product search auctions, search queries, bid floors, clearing CPCs, and quality scores
- Ad placement formats (Sponsored Search, Category Header, Carousel), eCPM yields, and ad revenue $
- Advertiser performance reports, ad spend, attributed product sales $, ROAS multipliers, and new-to-brand %

Routed to **Market Context**:
- Global Retail Media Network (RMN) ad spend growth, CPG trade spend transition benchmarks, sponsored search auction dynamics

Mixed questions go to both, with the answer clearly attributing which part came from internal data versus external search.

---

## Sample Q&A Showcase

The following three responses are captured from live post-deploy smoke tests of this agent:

### 1. Internal Data Analytics (Data Insights / BigQuery)

> **User Prompt:** "What is our Retail Media Network ad revenue and eCPM yield across placements, and what ROAS are we delivering to top CPG advertisers?"

**Sub-Agent Routed:** Data Insights (`sub_agents/data_insights.yaml`)  
**Authorized Table Queried:** `mktg_rmnm_cpc_cpm_yields`

**Agent Response:**
> Based on RMN monetization records in `mktg_rmnm_cpc_cpm_yields` and `mktg_rmnm_advertiser_roas_reports`:
>
> - **Ad Placement Yield Breakdown:**
>   - **Sponsored Product Search (Slot 1):** **$24.50 eCPM** ($1.22 avg CPC, 98.2% fill rate; $145,000 ad revenue).
>   - **Category Page Header Banner:** **$14.80 eCPM** ($0.92 avg CPC, 92.5% fill rate).
>   - **PDP Recommendation Carousel Ads:** **$11.20 eCPM** ($0.65 avg CPC, 95.0% fill rate).
> - **CPG Advertiser ROAS Delivery:**
>   - **Tier-1 Beverage Brand:** Delivered **5.4x ROAS** ($432,000 attributed sales on $80,000 spend; 42% new-to-brand buyers).
>   - **Tier-1 Personal Care Brand:** Delivered **4.8x ROAS** ($288,000 attributed sales on $60,000 spend).

---

### 2. External Market Grounding (Market Context / Google Search)

> **User Prompt:** "What are current industry benchmarks for Retail Media Network ROAS delivery and search ad CPM yields?"

**Sub-Agent Routed:** Market Context (`sub_agents/market_context.yaml`)  
**Grounding Tool:** `google_search`

**Agent Response:**
> According to retail media and e-commerce advertising benchmark reports:
>
> - **RMN Advertiser ROAS:** Top enterprise retail media networks average **4.0x to 5.5x ROAS** on sponsored product search ads for CPG brands.
> - **Sponsored Search eCPM Yields:** First-page sponsored search placements command eCPMs between **$18 and $30**, representing 3x-5x higher yield than standard programmatic display.
> - **New-to-Brand Attribution:** Over 35% of RMN sponsored search sales represent new-to-brand customer acquisitions for CPG advertisers.

---

### 3. Visual Analytics & Chart Generation (`render_chart`)

> **User Prompt:** "Render a bar chart comparing eCPM yields across RMN ad placements and ROAS across top CPG advertisers."

**Sub-Agent Routed:** Data Insights (`sub_agents/data_insights.yaml`)  
**Custom Tool Invoked:** `render_chart` (`tools/chart_generator.py`)

**Agent Response:**
> I have rendered the Retail Media Network placement yield and advertiser ROAS visualization. Sponsored search placements drive industry-leading eCPMs and high advertiser return.

**Generated Artifact:**  
![Sample Chart](sample_chart.png)

---

## Data

All tables live in the shared `retail_ent_agents` BigQuery dataset, prefixed `mktg_rmnm_` (this agent's registered `domain_id`/`agent_id` — see `_shared/table_registry.yaml`). Seed data is synthetic, generated by `data/generate_seed_data.py`.

| Table | Columns | Holds |
| :--- | :--- | :--- |
| `mktg_rmnm_advertiser_roas_reports` | `report_id, advertiser_id, campaign_name, ad_spend_usd, attributed_sales_usd, roas_multiplier, new_to_brand_pct` | CPG advertiser campaign performance reports, attributed product sales, ROAS delivery multipliers, and new-to-brand customer share % |
| `mktg_rmnm_cpc_cpm_yields` | `placement_id, ad_format, category, impressions_count, clicks_count, ecpm_usd, avg_cpc_usd, ad_revenue_usd, fill_rate_pct` | Ad placement yield metrics, format types, category performance, eCPM ($), average CPC ($), ad revenue, and inventory fill rate % |
| `mktg_rmnm_rmn_advertisers` | `advertiser_id, brand_name, cpg_tier, annual_ad_commitment_usd, active_campaigns_count, account_manager, credit_limit_usd` | RMN advertiser accounts, CPG tier classifications, annual ad spend commitments, and credit allocations |
| `mktg_rmnm_sponsored_product_auctions` | `auction_id, search_query, placement_slot, winning_advertiser_id, clearing_cpc_usd, bid_floor_cpc_usd, auction_timestamp, quality_score` | Sponsored search keyword auctions, search queries, slot ranks, clearing CPC prices, bid floors, and quality scores |

---

## Example Questions

Verified against this agent's `eval/agent.evalset.json`:

- "What is our total Retail Media Network (RMN) ad revenue and average eCPM yield by ad placement format?"
- "Which CPG brand advertisers generated the highest Return on Ad Spend (ROAS) on sponsored search campaigns?"
- "Show sponsored product search auction clearing CPC prices and quality scores across top search queries."
- "What is the percentage of New-to-Brand (NTB) customers acquired through retail media sponsored product ads?"
- "What are our ad inventory fill rates across mobile app video vs homepage hero display banners?"

---

## Tools

- **`ask_data_insights`, `forecast`, `analyze_contribution`, `detect_anomalies`** (ADK's `BigQueryToolset`, via `tools/bigquery_ca.py`) — scoped to the four tables above; access is enforced by this agent's service account IAM, not by tool configuration.
- **`render_chart`** (`tools/chart_generator.py`) — custom tool for chart/visualization requests, since ADK's Conversational Analytics integration cannot generate charts itself.
- **`google_search`** — used only by the Market Context sub-agent.

---

## Run It Locally

```bash
uv run adk run domains/marketing/agents/retail_media_network_monetization
```

Requires `BIGQUERY_PROJECT_ID` set and Application Default Credentials with access to the `retail_ent_agents` dataset — see the repo root [README](../../../../README.md#getting-started).

---

## Files

```
retail_media_network_monetization/
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
