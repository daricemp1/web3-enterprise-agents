# HR: Scheduling Fairness & Predictive Hours

Part of the **Retail Enterprise Agents** platform for Gemini Enterprise.

---

## 1. Why This Agent Matters

### Business Problem
Retail store managers struggle to balance customer foot-traffic demand curves with municipal Fair Workweek statutory regulations, schedule advance notice deadlines, clopening rest periods, and shift-swap flexibility.

### Target Personas
VP of Workforce Management, Retail Labor Compliance Director, Store Operations Directors, Store Schedulers

### Key Metrics Tracked
| Metric | Benchmark / Target | Business Impact |
| :--- | :--- | :--- |
| **Fair Workweek 14-Day Advance Notice %** | `Target: >= 96.0%` | Percentage of employee weekly shift schedules published at least 14 days prior to shift start. |
| **Clopening Shift Violations (<11h rest)** | `Target: 0 incidents` | Number of back-to-back closing and opening shifts scheduled without required 11-hour rest window. |
| **Predictability Pay Penalty Liability ($)** | `Target: < $15,000 / quarter` | Statutory employer penalty fees incurred due to employer-initiated last-minute schedule alterations. |
| **Peer Shift-Swap Fulfillment Rate %** | `Target: >= 88.0%` | Percentage of associate shift-trade requests successfully picked up and approved prior to shift start. |
| **Core Part-Time Scheduled Hours Variance** | `Target: < 10% variance` | Consistency of weekly scheduled hours awarded to core part-time associates week-over-week. |

---

## 2. What It Answers & Sub-Agent Routing

### Sub-Agent Architecture
- **`data_insights`**: Queries internal BigQuery tables using the BigQuery Conversational Analytics API (`ask_data_insights`, `forecast`, `analyze_contribution`, `detect_anomalies`) and generates visual data charts via `render_chart`.
- **`market_context`**: Leverages Google Search grounding for external retail labor market benchmarks, statutory wage/Fair Workweek regulations, BLS statistics, and HR industry standards.
- **`root_agent`**: Orchestrates routing between internal analytics and external market intelligence.

---

## 3. Sample Q&A Showcase

### Example 1: Internal Analytics (Data Insights)
*Question:* "What percentage of store employee schedules were published with 14+ days advance notice in Q2 2026?"  
*Response:*  
> Based on scheduling audit records in BigQuery (`hrwm_wsfa_published_schedules`), **96.8%** of store shift schedules across all retail regions were published with 14 or more days advance notice in Q2 2026. Stores in Fair Workweek regulated jurisdictions (NYC, Chicago, Los Angeles) achieved **99.2% compliance**, reducing predictability pay penalty liability to just $8,450 for the quarter.

### Example 2: Market Grounding (Market Context)
*Question:* "What are the specific statutory penalty rules and rest period mandates under the New York City Fair Workweek Law?"  
*Response:*  
> Under the NYC Fair Workweek Law (Admin Code § 20-1201), retail employers must provide written schedules at least 14 days in advance. Last-minute schedule changes incur mandatory predictability pay ranging from $15 (shift change with <14 days notice) to $75 (shift cancellation with <24 hours notice). Clopening shifts (closing and opening shifts separated by less than 11 hours) are prohibited without written employee consent and require a mandatory $100 premium payment.

### Example 3: Chart Visualization (`sample_chart.png`)
*Question:* "Show me a chart of 14-day schedule advance notice compliance percentages across all retail regions."  
*Generated Visual Artifact:*  
![Sample Chart](sample_chart.png)

---

### 4. Live Multi-Turn Demo Walkthrough (Gemini Enterprise)

Watch the deployed **HR: Scheduling Fairness & Predictive Hours** execute a live multi-turn analytical reasoning session in Gemini Enterprise:

> 📺 **Interactive Demo Player**: [Open Full HD Video Player (1080p)](https://rajanm.github.io/retail-enterprise-agents/demos/gemini-enterprise/human_resources/workforce_scheduling_fairness.html)  
> 📹 **Direct MP4 Download**: [`workforce_scheduling_fairness.mp4`](../../../../demos/gemini-enterprise/human_resources/workforce_scheduling_fairness.mp4)

```
Turn 1: Quantitative analysis against BigQuery Conversational Analytics
Turn 2: Grounded real-time external retail search & regulatory synthesis
Turn 3: Visual matplotlib trend chart generation
Turn 4: Interactive executive slide presentation generated in Gemini Enterprise Canvas
```

---

## 4. Authorized BigQuery Tables

- `hrwm_wsfa_published_schedules` — Weekly published employee work schedules, shift start/end timestamps, published date, and assigned department.
- `hrwm_wsfa_fair_workweek_compliance` — Fair Workweek ordinance tracking (NYC, Chicago, Seattle, LA), advance notice days, and audit status.
- `hrwm_wsfa_shift_swap_fulfillment` — Mobile associate shift swap requests, marketplace claim timestamps, manager approvals, and fulfillment rates.
- `hrwm_wsfa_clopening_violations` — Identified clopening shift pairs, inter-shift rest hours (<11 hours), and premium pay disbursement logs.

---

## 5. Example Questions

1. "What percentage of store employee schedules were published with 14+ days advance notice in Q2 2026?"
2. "What are the specific statutory penalty rules and rest period mandates under the New York City Fair Workweek Law?"
3. "How many clopening shift violations occurred across metropolitan stores in the last 60 days?"
4. "What is our peer-to-peer shift swap fulfillment rate in the mobile associate app?"
5. "Show me a chart of 14-day schedule advance notice compliance percentages across all retail regions."

---

## 6. Tools & Architecture

- **`ask_data_insights`**: BigQuery Conversational Analytics natural language to SQL.
- **`render_chart`**: BigQuery SQL to Matplotlib PNG visual rendering.
- **`google_search`**: Google Search market context grounding.
- **LLM Inference**: `gemini-3.5-flash` with `GOOGLE_CLOUD_LOCATION=global`.
- **Runtime Engine**: Vertex AI Agent Engine (`us-central1`).

---

## 7. Run Locally

```bash
# Run unit tests
uv run --frozen pytest domains/human_resources/agents/workforce_scheduling_fairness/tests/unit -v

# Run interactively with ADK CLI
adk run domains/human_resources/agents/workforce_scheduling_fairness
```
