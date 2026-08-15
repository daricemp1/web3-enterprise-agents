# HR: Store Associate Turnover & Retention

Part of the **Retail Enterprise Agents** platform for Gemini Enterprise.

---

## 1. Why This Agent Matters

### Business Problem
Retail store operations suffer from high associate turnover (especially in the first 90 days), resulting in recruiting surge costs, understaffed peak shifts, and customer checkout friction.

### Target Personas
Chief Human Resources Officer (CHRO), VP of Retail Operations, District HR Managers, Store General Managers

### Key Metrics Tracked
| Metric | Benchmark / Target | Business Impact |
| :--- | :--- | :--- |
| **Annualized Associate Turnover Rate %** | `Target: < 45.0%` | Total associate terminations annualized divided by average active store headcount. |
| **90-Day Associate Retention Cohort %** | `Target: >= 78.0%` | Percentage of newly hired store associates reaching 90 days of tenure without voluntary exit. |
| **Voluntary vs Involuntary Exit Ratio** | `Target: > 3.5x voluntary` | Ratio of voluntary employee resignations compared to operational/policy discharges. |
| **Associate Replacement Recruiting Cost** | `Target: < $4,200 / hire` | Total recruiting, onboarding, and training cost per replaced frontline associate. |
| **Exit Interview Pay & Scheduling Dissatisfaction %** | `Target: < 22.0%` | Percentage of exiting associates citing irregular hours or pay rates as primary departure reasons. |

---

## 2. What It Answers & Sub-Agent Routing

### Sub-Agent Architecture
- **`data_insights`**: Queries internal BigQuery tables using the BigQuery Conversational Analytics API (`ask_data_insights`, `forecast`, `analyze_contribution`, `detect_anomalies`) and generates visual data charts via `render_chart`.
- **`market_context`**: Leverages Google Search grounding for external retail labor market benchmarks, statutory wage/Fair Workweek regulations, BLS statistics, and HR industry standards.
- **`root_agent`**: Orchestrates routing between internal analytics and external market intelligence.

---

## 3. Sample Q&A Showcase

### Example 1: Internal Analytics (Data Insights)
*Question:* "What is the annualized store associate turnover rate across districts for 2026 YTD?"  
*Response:*  
> Based on BigQuery employee roster and separation telemetry (`hrwm_satr_associate_terminations`), our enterprise annualized store associate turnover rate for 2026 YTD is **41.2%**, beating our <45.0% enterprise threshold. District 4 (Midwest Metro) experienced the lowest turnover at **32.8%**, while District 9 (Southeast Coastal) had the highest at **51.4%**, driven by seasonal resort wage competition.

### Example 2: Market Grounding (Market Context)
*Question:* "What are current US Bureau of Labor Statistics (BLS) retail sector quit rate benchmarks and turnover trends?"  
*Response:*  
> According to the latest US Bureau of Labor Statistics (BLS) Job Openings and Labor Turnover Survey (JOLTS 2026), the retail trade sector maintains an average monthly quit rate of **2.9% to 3.2%**, translating to an annualized voluntary frontline turnover benchmark of **48% to 54%** across mass merchandisers and department stores. Retailers providing predictable scheduling and wage transparency average 12 percentage points lower turnover.

### Example 3: Chart Visualization (`sample_chart.png`)
*Question:* "Can you render a chart of 90-day associate retention rates across our top 5 operating districts in 2026?"  
*Generated Visual Artifact:*  
![Sample Chart](sample_chart.png)

---

### 4. Live Multi-Turn Demo Walkthrough (Gemini Enterprise)

Watch the deployed **HR: Store Associate Turnover & Retention** execute a live multi-turn analytical reasoning session in Gemini Enterprise:

> 📺 **Interactive Demo Player**: [Open Full HD Video Player (1080p)](https://rajanm.github.io/retail-enterprise-agents/demos/gemini-enterprise/human_resources/store_associate_turnover_retention.html)  
> 📹 **Direct MP4 Download**: [`store_associate_turnover_retention.mp4`](../../../../demos/gemini-enterprise/human_resources/store_associate_turnover_retention.mp4)

```
Turn 1: Quantitative analysis against BigQuery Conversational Analytics
Turn 2: Grounded real-time external retail search & regulatory synthesis
Turn 3: Visual matplotlib trend chart generation
Turn 4: Interactive executive slide presentation generated in Gemini Enterprise Canvas
```

---

## 4. Authorized BigQuery Tables

- `hrwm_satr_headcount_rosters` — Active store employee headcount by store, job role, department, employment status, and hire date.
- `hrwm_satr_associate_terminations` — Employee separation records, departure date, tenure months, exit reason category, and eligible for rehire status.
- `hrwm_satr_90_day_retention_cohorts` — Monthly hiring cohorts tracked at 30, 60, and 90-day retention milestones.
- `hrwm_satr_exit_interview_topics` — NLP-categorized associate exit survey responses, manager relationship sentiment, and wage satisfaction scores.

---

## 5. Example Questions

1. "What is the annualized store associate turnover rate across districts for 2026 YTD?"
2. "What are current US Bureau of Labor Statistics (BLS) retail sector quit rate benchmarks and turnover trends?"
3. "Which retail job roles (Cashier, Stocker, Department Lead) have the lowest 90-day retention cohort percentage?"
4. "What are the top three primary exit reasons reported in associate exit interviews over the past six months?"
5. "Can you render a chart of 90-day associate retention rates across our top 5 operating districts in 2026?"

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
uv run --frozen pytest domains/human_resources/agents/store_associate_turnover_retention/tests/unit -v

# Run interactively with ADK CLI
adk run domains/human_resources/agents/store_associate_turnover_retention
```
