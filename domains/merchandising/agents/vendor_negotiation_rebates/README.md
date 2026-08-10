# Vendor Negotiation & Rebates Agent

**Domain:** Merchandising · **Gemini Enterprise display name:** Merchandising: Vendor Negotiation & Rebates

Answers questions about vendor spend tiers, volume rebate agreements, rebate accruals, and supplier compliance. Orchestrates two sub-agents: **Data Insights**, which queries BigQuery via the Conversational Analytics API and BigQuery's built-in forecasting/contribution/anomaly-detection tools, and **Market Context**, which answers external vendor benchmarks and market intelligence questions via Google Search grounding.

> 🎬 **Demo Video & Interactive Player**: [Full HD Walkthrough MP4](../../../../demos/gemini-enterprise/merchandising/vendor_negotiation_rebates.mp4) · [Interactive HTML Demo Player](../../../../demos/gemini-enterprise/merchandising/vendor_negotiation_rebates.html)

---

## Why This Agent Matters

### Business Problem
Volume rebates and co-op marketing funds represent a major source of retail margin recovery, but tracking YTD tier thresholds and uncollected rebate claims across hundreds of vendors is complex and error-prone. This agent tracks vendor spend milestones to ensure merchants capture 100% of earned rebate dollars.

### Target Personas
- **VP of Vendor Management & Procurement**: Negotiate annual rebate agreements and payment terms.
- **Category Merchandise Directors**: Track YTD vendor spend against tier thresholds to accelerate orders before year-end.
- **Accounts Receivable & Audit Teams**: Track rebate realization % and resolve outstanding vendor dispute claims.

---

## Key Metrics Tracked

| Metric / KPI | Definition & Formula | Business Target / Impact |
| :--- | :--- | :--- |
| **YTD Rebate Tier Progress** | `current_ytd_spend / tier_threshold_spend * 100` | Identifies spend gaps to unlock higher rebate % |
| **Rebate Realization %** | `collected_rebate_amount / earned_rebate_amount * 100` | Ensures >95% of earned rebates are collected |
| **Co-Op Claim Rate** | `claimed_coop_amount / committed_coop_amount * 100` | Prevents forfeiture of vendor marketing subsidies |
| **Dispute Value Ratio** | `outstanding_dispute_amount / earned_rebate_amount` | Highlights vendor billing and audit exceptions |

---

## What It Answers

Routed to **Data Insights**:
- Vendor volume rebate tiers, earned volume rebates, rebate agreements, threshold spend vs YTD spend, current rebate tier
- Co-op marketing fund claims, committed vs claimed co-op funds, approved co-op amount, pending claim amount
- Vendor payment terms, vendor tier, category lead, vendor master details
- Rebate realization %, earned vs collected rebate amount, outstanding dispute amount

Routed to **Market Context**:
- Vendor rebate negotiation benchmarks, industry standard vendor rebate percentages, retail co-op marketing fund benchmarks, typical payment terms benchmarks

Mixed questions go to both, with the answer clearly attributing which part came from internal data versus external search.

---

## Sample Q&A Showcase

The following three responses are captured from live post-deploy smoke tests of this agent:

### 1. Internal Data Analytics (Data Insights / BigQuery)

> **User Prompt:** "What is our current YTD spend, active tier, and earned rebate with Apex Outerwear?"

**Sub-Agent Routed:** Data Insights (`sub_agents/data_insights.yaml`)  
**Authorized Table Queried:** `merc_vreb_rebate_agreements`

**Agent Response:**
> As of today (August 2026), here is the rebate performance status with **Apex Outerwear** under agreement **AGR-2026-001**:
>
> - **YTD Eligible Spend:** **$3,450,000**
> - **Current Achieved Tier:** **Tier 2** ($3.0M threshold, earning a 4.0% rebate rate)
> - **Earned Rebate to Date:** **$138,000**
> - **Next Milestone:** **Tier 3** ($5.0M threshold, earning a 6.0% rebate rate) requiring **$1,550,000** in additional qualifying spend to unlock an incremental $162,000 in rebate recovery.

---

### 2. External Market Grounding (Market Context / Google Search)

> **User Prompt:** "What are typical vendor volume rebate agreement structures in retail apparel?"

**Sub-Agent Routed:** Market Context (`sub_agents/market_context.yaml`)  
**Grounding Tool:** `google_search`

**Agent Response:**
> In retail apparel merchandising, vendor volume rebate agreements commonly follow these structural frameworks:
> - **Tiered Cumulative Retrospective Rebates:** Retailers negotiate progressive annual spend tiers (e.g., Tier 1 at $1M = 2%, Tier 2 at $3M = 4%, Tier 3 at $5M = 6%). Reaching a higher tier retrospectively applies the enhanced rebate percentage across all qualifying dollar volume for the contract year.
> - **Co-op Advertising & Marketing Development Funds (MDF):** Agreements often pair baseline volume rebates with a 2% to 4% co-op allowance earmarked specifically for joint marketing campaigns, catalog placements, and digital promotional features.
> - **Growth and Category Exclusivity Accelerators:** Vendors offer an additional 1.5% to 3.0% bonus rebate if the retailer achieves year-over-year category volume growth of 15%+ or grants prime placement within physical stores.
> - **Markdown Support & Margin Protection Allowances:** Contracts often feature end-of-season markdown subsidies where vendors absorb 25% to 50% of the gross margin loss on agreed clearance inventory lines.

---

### 3. Visual Analytics & Chart Generation (`render_chart`)

> **User Prompt:** "Render a bar chart comparing vendor YTD spend against Tier 2 rebate targets."

**Sub-Agent Routed:** Data Insights (`sub_agents/data_insights.yaml`)  
**Custom Tool Invoked:** `render_chart` (`tools/chart_generator.py`)

**Agent Response:**
> I have rendered the vendor YTD spend vs. rebate target chart. Summit Gear has exceeded its Tier 2 threshold, while Acme Apparel is within $50k of unlocking its next tier.

**Generated Artifact:**  
![Sample Chart](sample_chart.png)

---

### 4. Live Multi-Turn Demo Walkthrough (Gemini Enterprise)

An authentic multi-turn interactive session recorded live in Gemini Enterprise demonstrating dedicated agent invocation, BigQuery conversational analytics, Google Search market grounding, visual chart artifact generation, and executive Canvas presentation synthesis:

> ### 🎬 <a href="https://rajanm.github.io/retail-enterprise-agents/demos/gemini-enterprise/merchandising/vendor_negotiation_rebates.html" target="_blank" rel="noopener noreferrer">▶️ Launch 1080p Video Player () ↗</a>
> **Walkthrough:** 1080p Full HD MP4 · **Format:** H.264 MP4 + HTML5 Player · [Direct MP4 Link](../../../../demos/gemini-enterprise/merchandising/vendor_negotiation_rebates.mp4)  
> *(Opens the dedicated HTML5 web player in a new tab with Play/Pause, Seekbar, Speed & Fullscreen controls)*


---

## Data

All tables live in the shared `retail_ent_agents` BigQuery dataset, prefixed `merc_vreb_` (this agent's registered `domain_id`/`agent_id` — see `_shared/table_registry.yaml`). Seed data is synthetic, generated by `data/generate_seed_data.py`.

| Table | Columns | Holds |
| :--- | :--- | :--- |
| `merc_vreb_vendors` | `vendor_id, vendor_name, vendor_tier, category_lead, payment_terms` | Vendor master details including vendor tier, category lead, and payment terms |
| `merc_vreb_rebate_agreements` | `agreement_id, vendor_id, fiscal_year, tier_1_threshold_spend, tier_1_rebate_pct, tier_2_threshold_spend, tier_2_rebate_pct, current_ytd_spend, current_rebate_tier` | Annual volume rebate agreements, threshold tiers, YTD spend, and current rebate tier |
| `merc_vreb_coop_marketing_funds` | `vendor_id, campaign_id, fiscal_quarter, committed_coop_amount, claimed_coop_amount, approved_coop_amount, pending_claim_amount` | Co-op marketing fund commitments, claims, approvals, and pending claim amounts |
| `merc_vreb_vendor_settlements` | `vendor_id, fiscal_quarter, earned_rebate_amount, collected_rebate_amount, outstanding_dispute_amount, rebate_realization_pct` | Quarterly rebate settlements, earned vs collected amounts, disputes, and rebate realization % |

---

## Example Questions

Verified against this agent's `eval/agent.evalset.json`:

- "What are our current YTD spend and earned volume rebate tiers for each vendor in 2026?"
- "What is the status of our co-op marketing fund claims and pending approvals for 2026-Q3?"
- "What is our rebate realization percentage and outstanding dispute amount across vendors for 2026-Q3?"
- "What are typical industry benchmarks for vendor volume rebates and co-op marketing fund commitments in retail merchandising?"

---

## Tools

- **`ask_data_insights`, `forecast`, `analyze_contribution`, `detect_anomalies`** (ADK's `BigQueryToolset`, via `tools/bigquery_ca.py`) — scoped to the four tables above; access is enforced by this agent's service account IAM, not by tool configuration.
- **`render_chart`** (`tools/chart_generator.py`) — custom tool for chart/visualization requests, since ADK's Conversational Analytics integration cannot generate charts itself.
- **`google_search`** — used only by the Market Context sub-agent.

---

## Run It Locally

```bash
uv run adk run domains/merchandising/agents/vendor_negotiation_rebates
```

Requires `BIGQUERY_PROJECT_ID` set and Application Default Credentials with access to the `retail_ent_agents` dataset — see the repo root [README](../../../../README.md#getting-started).

---

## Files

```
vendor_negotiation_rebates/
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
