# Marketing: Influencer & Creator Campaign ROI Agent

**Domain:** Marketing · **Gemini Enterprise display name:** Marketing: Influencer & Creator Campaign ROI

Answers questions about influencer partnership ROI, creator affiliate promo code sales, product seeding costs, effective CPA, and Earned Media Value (EMV). Orchestrates two sub-agents: **Data Insights**, which queries BigQuery via the Conversational Analytics API and BigQuery built-in forecasting/contribution/anomaly-detection tools, and **Market Context**, which answers external questions via Google Search grounding.

---

## Why This Agent Matters

### Business Problem
Influencer marketing partnerships and creator seeding often represent large upfront investments with opaque attribution. Without tracking creator promo code conversions, effective cost per acquisition (eCPA), and earned media value (EMV), retailers risk overpaying macro-influencers while under-leveraging high-converting micro-creators. This agent provides full ROI accountability for creator partnerships.

### Target Personas
- **Head of Influencer & Creator Partnerships**: Manage creator rosters, negotiate contracts, and allocate budget across nano, micro, and macro creators.
- **Social Commerce & Affiliate Marketing Lead**: Track creator promo code redemptions, affiliate commissions, and effective CPA performance.
- **Brand PR & Seeding Operations Manager**: Monitor product seeding fulfillment, content generation rates, and calculated Earned Media Value (EMV).

---

## Key Metrics Tracked

| Metric / KPI | Definition & Formula | Business Target / Impact |
| :--- | :--- | :--- |
| **Effective CPA ($)** | `total_creator_cost / total_orders_generated` | Maintain creator effective CPA <$25.00 across campaigns |
| **Affiliate Coupon Sales ($)** | `Gross merchandise value generated via creator promo codes` | Target >$250,000 monthly affiliate GMV |
| **Earned Media Value (EMV $)** | `Standardized valuation of social impressions and engagements` | Target >3.5x EMV return on creator spend |
| **Seeding Content Generation Rate %** | `(creators_publishing_content / total_creators_seeded) * 100` | Target >65.0% organic post rate on gifted product seeding |

---

## What It Answers

Routed to **Data Insights**:
- Creator partnership contracts, follower tiers, fixed sponsorship fees, and engagement rates
- Affiliate coupon tracking, orders generated, gross sales GMV, commission payouts, and effective CPA
- Product seeding COGS, shipping costs, and creator content generation rates %
- Calculated Earned Media Value (EMV) and blended campaign ROAS multipliers

Routed to **Market Context**:
- Creator economy pricing benchmarks, TikTok Shop / Instagram affiliate rates, FTC influencer endorsement disclosure standards

Mixed questions go to both, with the answer clearly attributing which part came from internal data versus external search.

---

## Sample Q&A Showcase

The following three responses are captured from live post-deploy smoke tests of this agent:

### 1. Internal Data Analytics (Data Insights / BigQuery)

> **User Prompt:** "What is our effective CPA and gross sales across creator affiliate campaigns, and which follower tier delivered the highest ROAS?"

**Sub-Agent Routed:** Data Insights (`sub_agents/data_insights.yaml`)  
**Authorized Table Queried:** `mktg_iccr_affiliate_coupon_tracking`

**Agent Response:**
> Based on creator campaign performance in `mktg_iccr_affiliate_coupon_tracking` and `mktg_iccr_earned_media_value`:
>
> - **Creator Performance Summary:**
>   - **Micro-Creators (10K-100K followers):** Effective CPA **$16.50**; Blended ROAS **4.4x** ($142,000 gross sales on $32,000 total investment).
>   - **Mid-Tier Creators (100K-500K followers):** Effective CPA **$22.80**; Blended ROAS **3.6x** ($185,000 gross sales).
>   - **Macro-Creators (500K+ followers):** Effective CPA **$34.20**; High reach (1.8M impressions) but lower direct affiliate conversion.
> - **Product Seeding Program:** Batch SEED-04 achieved a **72.0% content generation rate** at an average product gifting COGS of $42.00 per unit.

---

### 2. External Market Grounding (Market Context / Google Search)

> **User Prompt:** "What are current creator economy benchmarks for affiliate commission rates and micro-influencer engagement?"

**Sub-Agent Routed:** Market Context (`sub_agents/market_context.yaml`)  
**Grounding Tool:** `google_search`

**Agent Response:**
> According to influencer marketing and creator economy industry studies:
>
> - **Micro-Influencer Engagement:** Micro-creators (10K-50K followers) average **3.5% to 6.0% engagement rates**, outperforming macro-influencers by over 2x in comment/share intent.
> - **Affiliate Commission Rates:** Retail e-commerce brands typically offer **8% to 15% revenue share** on net sales driven through custom coupon codes.
> - **Earned Media Value (EMV):** Average retail EMV benchmarks value Instagram feed posts at ~$12/CPM and TikTok video views at ~$8/CPM.

---

### 3. Visual Analytics & Chart Generation (`render_chart`)

> **User Prompt:** "Render a bar chart comparing effective CPA and gross sales across creator tiers."

**Sub-Agent Routed:** Data Insights (`sub_agents/data_insights.yaml`)  
**Custom Tool Invoked:** `render_chart` (`tools/chart_generator.py`)

**Agent Response:**
> I have rendered the creator campaign ROI visualization. Micro and mid-tier creator partnerships generate superior sales velocity at low effective CPAs.

**Generated Artifact:**  
![Sample Chart](sample_chart.png)

---

## Data

All tables live in the shared `retail_ent_agents` BigQuery dataset, prefixed `mktg_iccr_` (this agent's registered `domain_id`/`agent_id` — see `_shared/table_registry.yaml`). Seed data is synthetic, generated by `data/generate_seed_data.py`.

| Table | Columns | Holds |
| :--- | :--- | :--- |
| `mktg_iccr_affiliate_coupon_tracking` | `coupon_code, creator_id, commission_rate_pct, orders_count, gross_sales_usd, commission_payout_usd, effective_cpa_usd` | Creator affiliate discount codes, orders generated, gross sales GMV, commission payouts, and effective CPA ($) |
| `mktg_iccr_creator_partnerships` | `creator_id, handle, platform, follower_tier, fixed_fee_usd, contracted_deliverables, engagement_rate_pct, primary_category` | Creator roster master data, social handles, follower tiers, fixed sponsorship fees, and engagement rates |
| `mktg_iccr_earned_media_value` | `creator_id, total_posts_published, total_impressions, total_engagements, calculated_emv_usd, roas_blended_multiplier` | Creator published post counts, social impressions, engagement totals, calculated EMV ($), and blended ROAS |
| `mktg_iccr_seeding_product_costs` | `seeding_batch_id, category, creators_seeded_count, cogs_product_cost_usd, shipping_cost_usd, content_generation_rate_pct` | Gifting and product seeding batches, COGS costs, shipping fees, and percentage of creators publishing content |

---

## Example Questions

Verified against this agent's `eval/agent.evalset.json`:

- "What is our total influencer marketing sales volume and effective Cost Per Acquisition (eCPA) by creator tier?"
- "Which creator partnerships delivered the highest Earned Media Value (EMV) and engagement rates?"
- "Show affiliate coupon code order volume and commission payouts across active influencer campaigns."
- "What is the content generation rate and ROI from our unpaid product seeding and gifting programs?"
- "How do micro-influencers compare to macro-creators in conversion efficiency and ROAS?"

---

## Tools

- **`ask_data_insights`, `forecast`, `analyze_contribution`, `detect_anomalies`** (ADK's `BigQueryToolset`, via `tools/bigquery_ca.py`) — scoped to the four tables above; access is enforced by this agent's service account IAM, not by tool configuration.
- **`render_chart`** (`tools/chart_generator.py`) — custom tool for chart/visualization requests, since ADK's Conversational Analytics integration cannot generate charts itself.
- **`google_search`** — used only by the Market Context sub-agent.

---

## Run It Locally

```bash
uv run adk run domains/marketing/agents/influencer_creator_campaign_roi
```

Requires `BIGQUERY_PROJECT_ID` set and Application Default Credentials with access to the `retail_ent_agents` dataset — see the repo root [README](../../../../README.md#getting-started).

---

## Files

```
influencer_creator_campaign_roi/
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
