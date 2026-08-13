# Marketing: Brand Health & Social Sentiment Agent

**Domain:** Marketing · **Gemini Enterprise display name:** Marketing: Brand Health & Social Sentiment

Answers questions about Net Brand Sentiment Score (NBSS), social listening Share of Voice (SOV) vs competitors, topic sentiment drivers across social platforms, customer brand advocacy, and public sentiment recovery. Orchestrates two sub-agents: **Data Insights**, which queries BigQuery via the Conversational Analytics API and BigQuery built-in forecasting/contribution/anomaly-detection tools, and **Market Context**, which answers external questions via Google Search grounding.

---

## Why This Agent Matters

### Business Problem
Brand equity and customer trust directly drive long-term organic retention and customer lifetime value. However, negative sentiment crises, viral social criticism, or competitor narrative shifts can rapidly erode brand perception before quarterly brand tracker surveys detect them. This agent delivers unified real-time social listening, Net Brand Sentiment Score (NBSS), competitive Share of Voice (SOV), and brand advocacy metrics.

### Target Personas
- **VP of Brand Marketing & Communications**: Monitor enterprise brand health, corporate reputation, and campaign sentiment lift.
- **Social Media & Community Director**: Track platform-specific sentiment drivers (TikTok, Instagram, Reddit, X) and manage community engagement.
- **PR & Crisis Management Lead**: Detect viral complaint spikes in real time and monitor post-incident sentiment recovery.

---

## Key Metrics Tracked

| Metric / KPI | Definition & Formula | Business Target / Impact |
| :--- | :--- | :--- |
| **Net Brand Sentiment Score (NBSS)** | `positive_sentiment_pct - negative_sentiment_pct` | Maintain NBSS > +50 across all organic social channels |
| **Social Share of Voice % (SOV)** | `(brand_mentions / total_market_mentions) * 100` | Target >30.0% share of voice against primary retail competitors |
| **Brand NPS Index** | `Index score (0-100) combining NPS and brand advocacy` | Benchmark brand health above 75.0 index rating |
| **Customer Trust & Value Score** | `Score out of 10.0 from verified customer sentiment cohorts` | Maintain brand trust >8.5 and value perception >8.0 |

---

## What It Answers

Routed to **Data Insights**:
- Net Brand Sentiment Score (NBSS) and Brand NPS trends over time across months
- Competitive social listening Share of Voice (SOV) and earned media rankings
- Platform-level topic drivers and reach/engagement volumes across TikTok, Reddit, Instagram, and X
- Customer advocacy, sustainability perception, and value-for-money scores across customer cohorts

Routed to **Market Context**:
- Industry social listening benchmarks, viral PR crisis response frameworks, retail brand reputation index trends

Mixed questions go to both, with the answer clearly attributing which part came from internal data versus external search.

---

## Sample Q&A Showcase

The following three responses are captured from live post-deploy smoke tests of this agent:

### 1. Internal Data Analytics (Data Insights / BigQuery)

> **User Prompt:** "What is our current Net Brand Sentiment Score (NBSS) and Brand NPS trend over the past 4 months?"

**Sub-Agent Routed:** Data Insights (`sub_agents/data_insights.yaml`)  
**Authorized Table Queried:** `mktg_bhss_brand_sentiment_tracker`

**Agent Response:**
> Based on recent sentiment tracking data in `mktg_bhss_brand_sentiment_tracker`:
>
> - **Net Brand Sentiment Score (NBSS):** Improved steadily from **+42.0** in May to **+58.5** in August.
> - **Positive Sentiment:** Increased from **62.0%** to **73.5%** driven by summer promotional satisfaction.
> - **Negative Sentiment:** Decreased from **20.0%** to **15.0%** following customer service response improvements.
> - **Brand NPS Index:** Currently sits at a healthy **78.2**, exceeding the 75.0 target benchmark.

---

### 2. External Market Grounding (Market Context / Google Search)

> **User Prompt:** "What are current industry benchmarks for retail brand social sentiment and Share of Voice tracking?"

**Sub-Agent Routed:** Market Context (`sub_agents/market_context.yaml`)  
**Grounding Tool:** `google_search`

**Agent Response:**
> According to retail brand health and social listening intelligence benchmarks:
>
> - **Net Brand Sentiment Score (NBSS):** Leading omnichannel apparel and department store retailers maintain an NBSS between **+45 and +60** during non-promotional periods.
> - **Share of Voice (SOV):** Top-tier enterprise retailers typically capture **25% to 35%** SOV within their category segment.
> - **Platform Drivers:** Video-first channels (TikTok, Instagram Reels) generate 4x higher brand advocacy engagement compared to text-based platforms.

---

### 3. Visual Analytics & Chart Generation (`render_chart`)

> **User Prompt:** "Render a bar chart comparing our monthly Net Brand Sentiment Score and Brand NPS index."

**Sub-Agent Routed:** Data Insights (`sub_agents/data_insights.yaml`)  
**Custom Tool Invoked:** `render_chart` (`tools/chart_generator.py`)

**Agent Response:**
> I have rendered the brand sentiment and NPS index progression chart. Both metrics show sustained upward momentum over the 4-month tracking window.

**Generated Artifact:**  
![Sample Chart](sample_chart.png)

---

### 4. Live Multi-Turn Demo Walkthrough (Gemini Enterprise)

> 🎬 **Watch the full high-definition video walkthrough of this multi-turn workflow:**  
> **[Open Interactive Demo Player (1080p Full HD)](https://rajanm.github.io/retail-enterprise-agents/demos/gemini-enterprise/marketing/brand_health_social_sentiment.html)**  
> *(Video file: `demos/gemini-enterprise/marketing/brand_health_social_sentiment.mp4`)*

---

## Data

All tables live in the shared `retail_ent_agents` BigQuery dataset, prefixed `mktg_bhss_` (this agent's registered `domain_id`/`agent_id` — see `_shared/table_registry.yaml`). Seed data is synthetic, generated by `data/generate_seed_data.py`.

| Table | Columns | Holds |
| :--- | :--- | :--- |
| `mktg_bhss_brand_advocacy_scores` | `customer_cohort, advocacy_tier, brand_trust_score_10, sustainability_perception_10, value_for_money_score_10, recommendation_intent_pct` | Customer brand advocacy ratings, trust scores, sustainability perceptions, and recommendation intent % |
| `mktg_bhss_brand_sentiment_tracker` | `tracking_month, positive_sentiment_pct, neutral_sentiment_pct, negative_sentiment_pct, net_brand_sentiment_score, brand_nps_index` | Monthly social sentiment distribution, Net Brand Sentiment Score (NBSS), and overall Brand NPS index |
| `mktg_bhss_share_of_voice_competitors` | `retailer_brand, month, total_social_mentions, share_of_voice_pct, sentiment_leader_rank, earned_media_mentions` | Competitive social mention volumes, share of voice % (SOV), and sentiment leader rankings |
| `mktg_bhss_social_listening_mentions` | `mention_id, platform, topic_category, sentiment, reach_impressions, engagement_count, timestamp` | Granular social listening posts, platform reach, topic categories (shipping, customer service, pricing), and sentiment |

---

## Example Questions

Verified against this agent's `eval/agent.evalset.json`:

- "What is our current Net Brand Sentiment Score (NBSS) and Brand NPS trend over the past 4 months?"
- "What is our Share of Voice (SOV) percentage compared to primary retail competitors in social mentions?"
- "Show top positive and negative social listening topic drivers across TikTok, X/Twitter, and Reddit."
- "What are our brand trust, sustainability perception, and value-for-money scores across customer tiers?"
- "How did recent operational improvements in checkout speed impact customer social sentiment scores?"

---

## Tools

- **`ask_data_insights`, `forecast`, `analyze_contribution`, `detect_anomalies`** (ADK's `BigQueryToolset`, via `tools/bigquery_ca.py`) — scoped to the four tables above; access is enforced by this agent's service account IAM, not by tool configuration.
- **`render_chart`** (`tools/chart_generator.py`) — custom tool for chart/visualization requests, since ADK's Conversational Analytics integration cannot generate charts itself.
- **`google_search`** — used only by the Market Context sub-agent.

---

## Run It Locally

```bash
uv run adk run domains/marketing/agents/brand_health_social_sentiment
```

Requires `BIGQUERY_PROJECT_ID` set and Application Default Credentials with access to the `retail_ent_agents` dataset — see the repo root [README](../../../../README.md#getting-started).

---

## Files

```
brand_health_social_sentiment/
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
