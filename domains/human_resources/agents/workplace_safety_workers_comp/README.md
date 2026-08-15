# HR: Workplace Safety & Workers' Comp

Part of the **Retail Enterprise Agents** platform for Gemini Enterprise.

---

## 1. Why This Agent Matters

### Business Problem
Workplace injuries (slips, trips, repetitive motion, backroom pallet lifting) drive up workers' compensation insurance reserves, increase OSHA recordable incident rates (TRIR), and lead to lost operational workdays.

### Target Personas
VP of Environmental Health & Safety (EHS), Workers' Comp Risk Manager, Store Safety Committee Chairs, Operations VPs

### Key Metrics Tracked
| Metric | Benchmark / Target | Business Impact |
| :--- | :--- | :--- |
| **Total Recordable Incident Rate (TRIR)** | `Target: < 2.2 per 100 FTE` | Annualized OSHA recordable injuries and illnesses per 200,000 associate work hours. |
| **Days Away, Restricted, or Transferred (DART)** | `Target: < 1.4 per 100 FTE` | Work-related injury cases resulting in lost workdays, job transfer, or medical work restrictions. |
| **Workers' Comp Total Incurred Incurred Losses ($)** | `Target: < $3.2M / year` | Total medical expenses, indemnity payments, and open case insurance loss reserves. |
| **Average Days to Return-to-Work (RTW)** | `Target: < 18.0 days` | Average days required to transition injured associates into modified light-duty or full duty. |
| **Store Safety Audit Hazard Remediation SLA** | `Target: < 48 hours` | Time elapsed to remediate physical store and DC safety hazard inspection findings. |

---

## 2. What It Answers & Sub-Agent Routing

### Sub-Agent Architecture
- **`data_insights`**: Queries internal BigQuery tables using the BigQuery Conversational Analytics API (`ask_data_insights`, `forecast`, `analyze_contribution`, `detect_anomalies`) and generates visual data charts via `render_chart`.
- **`market_context`**: Leverages Google Search grounding for external retail labor market benchmarks, statutory wage/Fair Workweek regulations, BLS statistics, and HR industry standards.
- **`root_agent`**: Orchestrates routing between internal analytics and external market intelligence.

---

## 3. Sample Q&A Showcase

### Example 1: Internal Analytics (Data Insights)
*Question:* "What is our Total Recordable Incident Rate (TRIR) and DART rate across retail stores in 2026 YTD?"  
*Response:*  
> Based on BigQuery OSHA 300 logs (`hrwm_wswc_osha_recordable_logs`), our enterprise Total Recordable Incident Rate (TRIR) for 2026 YTD is **1.92 per 100 FTEs**, outperforming our 2.20 safety target and the retail industry average (3.10). Our DART rate is **1.18 per 100 FTEs**, down 14% year-over-year following the rollout of mechanized pallet lifts in distribution centers.

### Example 2: Market Grounding (Market Context)
*Question:* "What are current OSHA retail industry injury rate benchmarks for general merchandise and grocery stores?"  
*Response:*  
> According to US BLS and OSHA Workplace Injury and Illness reporting (2026), the retail trade sector averages a TRIR of **3.1 to 3.4 recordable injuries per 100 FTEs**, with supermarket and grocery store formats averaging higher at **3.8 to 4.2** due to heavy material handling in stockrooms and commercial food prep. Top-quartile safety leaders maintain TRIR rates below **2.0** through automated lift-assists and ergonomic footwear mandates.

### Example 3: Chart Visualization (`sample_chart.png`)
*Question:* "Show me a chart of monthly OSHA recordable incident counts compared against our annual safety reduction target."  
*Generated Visual Artifact:*  
![Sample Chart](sample_chart.png)

---

### 4. Live Multi-Turn Demo Walkthrough (Gemini Enterprise)

Watch the deployed **HR: Workplace Safety & Workers' Comp** execute a live multi-turn analytical reasoning session in Gemini Enterprise:

> 📺 **Interactive Demo Player**: [Open Full HD Video Player (1080p)](https://rajanm.github.io/retail-enterprise-agents/demos/gemini-enterprise/human_resources/workplace_safety_workers_comp.html)  
> 📹 **Direct MP4 Download**: [`workplace_safety_workers_comp.mp4`](../../../../demos/gemini-enterprise/human_resources/workplace_safety_workers_comp.mp4)

```
Turn 1: Quantitative analysis against BigQuery Conversational Analytics
Turn 2: Grounded real-time external retail search & regulatory synthesis
Turn 3: Visual matplotlib trend chart generation
Turn 4: Interactive executive slide presentation generated in Gemini Enterprise Canvas
```

---

## 4. Authorized BigQuery Tables

- `hrwm_wswc_osha_recordable_logs` — OSHA 300 log incident entries, incident date, body part, injury nature, store location, and root cause.
- `hrwm_wswc_lost_workday_cases` — DART case tracking, lost workdays count, restricted duty days, and modified-duty assignment logs.
- `hrwm_wswc_workers_comp_claims` — Workers' compensation claim numbers, paid medical costs, paid indemnity, outstanding reserves, and TPA status.
- `hrwm_wswc_safety_audit_compliance` — Quarterly store physical safety inspection scores, identified slip/fall hazards, and remediation closure dates.

---

## 5. Example Questions

1. "What is our Total Recordable Incident Rate (TRIR) and DART rate across retail stores in 2026 YTD?"
2. "What are current OSHA retail industry injury rate benchmarks for general merchandise and grocery stores?"
3. "What are the top three injury categories (e.g., material handling, slip/trip/fall) by total incurred workers' comp cost?"
4. "How many open workers' comp claims currently have an active return-to-work modified duty plan?"
5. "Show me a chart of monthly OSHA recordable incident counts compared against our annual safety reduction target."

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
uv run --frozen pytest domains/human_resources/agents/workplace_safety_workers_comp/tests/unit -v

# Run interactively with ADK CLI
adk run domains/human_resources/agents/workplace_safety_workers_comp
```
