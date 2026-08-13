# Marketing: CRM, Email & SMS Campaign Orchestration Agent

**Domain:** Marketing · **Gemini Enterprise display name:** Marketing: CRM, Email & SMS Campaign Orchestration

Answers questions about CRM campaign engagement, email and SMS automated lifecycle journeys, revenue per recipient, unsubscribe and bounce rates, and domain deliverability. Orchestrates two sub-agents: **Data Insights**, which queries BigQuery via the Conversational Analytics API and BigQuery built-in forecasting/contribution/anomaly-detection tools, and **Market Context**, which answers external questions via Google Search grounding.

---

## Why This Agent Matters

### Business Problem
Direct-to-consumer messaging (Email & SMS) delivers the highest ROI of any retail marketing channel, but excessive dispatch frequency leads to subscriber fatigue, high unsubscribe rates, and domain deliverability penalties. This agent optimizes CRM lifecycle journeys, evaluates revenue per send, and monitors inbox deliverability health across email and SMS.

### Target Personas
- **Director of Lifecycle & CRM Marketing**: Oversee omnichannel subscriber engagement and maximize CRM attributed revenue.
- **Email & SMS Marketing Operations Lead**: Monitor campaign open rates, click-through rates, deliverability metrics, and send cadences.
- **Customer Engagement & Retention Strategist**: Optimize automated trigger flows (Welcome, Browse Abandon, Cart Abandon, Post-Purchase).

---

## Key Metrics Tracked

| Metric / KPI | Definition & Formula | Business Target / Impact |
| :--- | :--- | :--- |
| **Revenue per Recipient ($)** | `gross_campaign_revenue / total_delivered_recipients` | Target >$0.45 per email send and >$1.80 per SMS send |
| **Automated Journey Conversion %** | `(journey_conversions / journey_entries) * 100` | Maintain abandoned cart journey conversion >8.5% |
| **Email Deliverability Rate %** | `(delivered_emails / total_dispatched) * 100` | Target >99.2% inbox placement and deliverability |
| **Unsubscribe & Spam Rate %** | `(unsubscribes / delivered_sends) * 100` | Keep email unsubscribe <0.25% and spam complaints <0.04% |

---

## What It Answers

Routed to **Data Insights**:
- Campaign-level send volume, open rates, CTR %, and conversion rates by channel
- Automated lifecycle journey step conversions, delay hours, and attributed revenue (Welcome, Cart Abandon, Win-back)
- Audience segment revenue per send and Average Order Value (AOV)
- Monthly channel deliverability %, bounce rates, unsubscribe rates, and spam complaints

Routed to **Market Context**:
- Apple Mail Privacy Protection (MPP) open rate shifts, SMS 10DLC carrier compliance regulations, retail email/SMS benchmarks

Mixed questions go to both, with the answer clearly attributing which part came from internal data versus external search.

---

## Sample Q&A Showcase

The following three responses are captured from live post-deploy smoke tests of this agent:

### 1. Internal Data Analytics (Data Insights / BigQuery)

> **User Prompt:** "What is our revenue per recipient across email and SMS campaigns, and how are automated cart abandonment flows performing?"

**Sub-Agent Routed:** Data Insights (`sub_agents/data_insights.yaml`)  
**Authorized Table Queried:** `mktg_esco_revenue_per_recipient`

**Agent Response:**
> Based on CRM performance records in `mktg_esco_revenue_per_recipient` and `mktg_esco_lifecycle_journey_steps`:
>
> - **Revenue per Recipient Performance:**
>   - **SMS VIP Flash Sale:** **$2.15** per recipient ($107,500 revenue / 50,000 recipients; AOV $86.00).
>   - **Email Weekly Promotional:** **$0.52** per recipient ($260,000 revenue / 500,000 recipients; AOV $65.00).
>   - **Email Loyalty Exclusive:** **$0.88** per recipient ($88,000 revenue / 100,000 recipients).
> - **Automated Cart Abandonment Flow:**
>   - Step 1 (SMS 1-hour delay): **11.4% conversion** ($48,200 attributed revenue).
>   - Step 2 (Email 24-hour delay): **6.2% conversion** ($31,500 attributed revenue).
> - **Deliverability Health:** Email deliverability remains strong at **99.4%** with a 0.18% unsubscribe rate.

---

### 2. External Market Grounding (Market Context / Google Search)

> **User Prompt:** "What are current retail benchmarks for SMS marketing CTR and email deliverability compliance?"

**Sub-Agent Routed:** Market Context (`sub_agents/market_context.yaml`)  
**Grounding Tool:** `google_search`

**Agent Response:**
> According to direct marketing and CRM deliverability benchmarks:
>
> - **SMS CTR & Conversion:** Retail promotional SMS campaigns average **8% to 12% CTR** with conversion rates between **3% and 5%**.
> - **Email Deliverability Standards:** Gmail and Yahoo sender guidelines mandate spam complaint rates strictly below **0.10%** (with hard blocks above 0.30%).
> - **Automated Triggers:** Automated behavioral trigger emails generate over **300% higher revenue per recipient** compared to standard batch marketing blasts.

---

### 3. Visual Analytics & Chart Generation (`render_chart`)

> **User Prompt:** "Render a bar chart comparing revenue per recipient and conversion rates across CRM channels and journeys."

**Sub-Agent Routed:** Data Insights (`sub_agents/data_insights.yaml`)  
**Custom Tool Invoked:** `render_chart` (`tools/chart_generator.py`)

**Agent Response:**
> I have rendered the CRM performance visualization. SMS and automated behavioral workflows lead in revenue generation per recipient.

**Generated Artifact:**  
![Sample Chart](sample_chart.png)

---

### 4. Live Multi-Turn Demo Walkthrough (Gemini Enterprise)

> 🎬 **Watch the full high-definition video walkthrough of this multi-turn workflow:**  
> **[Open Interactive Demo Player (1080p Full HD)](https://rajanm.github.io/retail-enterprise-agents/demos/gemini-enterprise/marketing/email_sms_crm_orchestration.html)**  
> *(Video file: `demos/gemini-enterprise/marketing/email_sms_crm_orchestration.mp4`)*

---

## Data

All tables live in the shared `retail_ent_agents` BigQuery dataset, prefixed `mktg_esco_` (this agent's registered `domain_id`/`agent_id` — see `_shared/table_registry.yaml`). Seed data is synthetic, generated by `data/generate_seed_data.py`.

| Table | Columns | Holds |
| :--- | :--- | :--- |
| `mktg_esco_crm_campaign_sends` | `campaign_id, channel, campaign_name, send_timestamp, recipients_count, open_rate_pct, click_through_rate_pct, conversion_rate_pct` | Dispatched email and SMS marketing campaigns, recipient volumes, open rates, CTR, and conversion rates |
| `mktg_esco_lifecycle_journey_steps` | `journey_name, step_number, trigger_event, delay_hours, channel, step_conversion_pct, step_revenue_attributed_usd` | Automated customer lifecycle journeys (Cart Abandonment, Welcome Series), delay hours, step conversion %, and attributed revenue |
| `mktg_esco_revenue_per_recipient` | `campaign_id, channel, audience_segment, gross_revenue_usd, total_recipients, revenue_per_recipient_usd, aov_usd` | Audience segment campaign performance, total gross revenue, revenue per recipient ($), and customer AOV |
| `mktg_esco_unsubscribe_bounce_rates` | `channel, month, total_dispatched, delivered_count, deliverability_pct, unsubscribe_count, unsubscribe_rate_pct, spam_complaint_pct` | Monthly deliverability health, dispatch volume, delivery %, unsubscribe counts, and spam complaint % |

---

## Example Questions

Verified against this agent's `eval/agent.evalset.json`:

- "What is our average Revenue Per Recipient (RPR) across automated lifecycle flows vs one-off promotional email sends?"
- "Show conversion rates and attributed revenue across our Abandoned Cart 2-step email and SMS journey."
- "What are our monthly email deliverability, bounce, unsubscribe, and spam complaint rates?"
- "Which customer audience segments delivered the highest Average Order Value (AOV) from SMS push campaigns?"
- "How do open rates and click-through rates compare between personalized replenishment emails and weekly circulars?"

---

## Tools

- **`ask_data_insights`, `forecast`, `analyze_contribution`, `detect_anomalies`** (ADK's `BigQueryToolset`, via `tools/bigquery_ca.py`) — scoped to the four tables above; access is enforced by this agent's service account IAM, not by tool configuration.
- **`render_chart`** (`tools/chart_generator.py`) — custom tool for chart/visualization requests, since ADK's Conversational Analytics integration cannot generate charts itself.
- **`google_search`** — used only by the Market Context sub-agent.

---

## Run It Locally

```bash
uv run adk run domains/marketing/agents/email_sms_crm_orchestration
```

Requires `BIGQUERY_PROJECT_ID` set and Application Default Credentials with access to the `retail_ent_agents` dataset — see the repo root [README](../../../../README.md#getting-started).

---

## Files

```
email_sms_crm_orchestration/
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
