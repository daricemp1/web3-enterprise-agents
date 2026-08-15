# HR: Associate Pulse & eNPS Analytics

Part of the **Retail Enterprise Agents** platform for Gemini Enterprise.

---

## 1. Why This Agent Matters

### Business Problem
Frontline retail associate burnout, communication silos between corporate and store teams, and low employee Net Promoter Scores (eNPS) drive quiet quitting, customer dissatisfaction, and store turnover.

### Target Personas
VP of Employee Experience, Internal Communications Director, People Analytics Lead, District Operations Managers

### Key Metrics Tracked
| Metric | Benchmark / Target | Business Impact |
| :--- | :--- | :--- |
| **Employee Net Promoter Score (eNPS)** | `Target: >= +32` | Calculated as percentage of Promoter associates (ratings 9-10) minus Detractor associates (ratings 0-6). |
| **Quarterly Pulse Survey Participation Rate %** | `Target: >= 78.0%` | Percentage of eligible active frontline associates completing confidential quarterly mobile pulse surveys. |
| **Manager Leadership & Recognition Sentiment** | `Target: >= 4.2 / 5.0` | Associate satisfaction rating evaluating direct store manager support, fairness, and daily recognition. |
| **High Flight-Risk Store Clusters Identified** | `Target: 0 unaddressed clusters` | Number of retail store locations with declining eNPS (>15 pt drop) and elevated turnover risk. |
| **Pulse Action Plan Implementation Rate %** | `Target: >= 90.0%` | Percentage of store general managers completing quarterly associate feedback action plans within 30 days. |

---

## 2. What It Answers & Sub-Agent Routing

### Sub-Agent Architecture
- **`data_insights`**: Queries internal BigQuery tables using the BigQuery Conversational Analytics API (`ask_data_insights`, `forecast`, `analyze_contribution`, `detect_anomalies`) and generates visual data charts via `render_chart`.
- **`market_context`**: Leverages Google Search grounding for external retail labor market benchmarks, statutory wage/Fair Workweek regulations, BLS statistics, and HR industry standards.
- **`root_agent`**: Orchestrates routing between internal analytics and external market intelligence.

---

## 3. Sample Q&A Showcase

### Example 1: Internal Analytics (Data Insights)
*Question:* "What was our overall Employee Net Promoter Score (eNPS) across retail stores in the latest Q2 pulse survey?"  
*Response:*  
> Based on pulse survey analytics in BigQuery (`hrwm_aepe_enps_survey_responses`), our enterprise retail associate eNPS for Q2 2026 is **+36.4** across 15,200 participating associates (79.2% participation rate). Promoters comprised 54.2%, Passives 28.0%, and Detractors 17.8%, representing a +5.2 point improvement over Q1.

### Example 2: Market Grounding (Market Context)
*Question:* "What are current retail industry employee engagement and frontline eNPS benchmarks according to Gallup and Culture Amp?"  
*Response:*  
> According to Culture Amp and Gallup State of the Global Workplace reports (2026), the retail industry averages an eNPS of **+14 to +22**, with frontline retail employees frequently scoring lower than corporate peers due to shift irregularity and customer-facing friction. Top-decile retail organizations achieve **+35 to +45** by implementing mobile recognition programs and transparent store bonus pools.

### Example 3: Chart Visualization (`sample_chart.png`)
*Question:* "Can you render a chart of quarterly eNPS sentiment trends across our 4 operating regions over the past 2 years?"  
*Generated Visual Artifact:*  
![Sample Chart](sample_chart.png)

---

### 4. Live Multi-Turn Demo Walkthrough (Gemini Enterprise)

Watch the deployed **HR: Associate Pulse & eNPS Analytics** execute a live multi-turn analytical reasoning session in Gemini Enterprise:

> 📺 **Interactive Demo Player**: [Open Full HD Video Player (1080p)](https://rajanm.github.io/retail-enterprise-agents/demos/gemini-enterprise/human_resources/associate_engagement_pulse_enps.html)  
> 📹 **Direct MP4 Download**: [`associate_engagement_pulse_enps.mp4`](../../../../demos/gemini-enterprise/human_resources/associate_engagement_pulse_enps.mp4)

```
Turn 1: Quantitative analysis against BigQuery Conversational Analytics
Turn 2: Grounded real-time external retail search & regulatory synthesis
Turn 3: Visual matplotlib trend chart generation
Turn 4: Interactive executive slide presentation generated in Gemini Enterprise Canvas
```

---

## 4. Authorized BigQuery Tables

- `hrwm_aepe_enps_survey_responses` — Individual confidential associate pulse responses, Likert scores, promoter/passive/detractor tags, and survey date.
- `hrwm_aepe_department_sentiment_index` — Department-level sentiment breakdown (Pay, Scheduling, Culture, Tools, Safety, Recognition).
- `hrwm_aepe_manager_feedback_scores` — Manager support indices, store leadership trust ratings, and two-way communication scores.
- `hrwm_aepe_flight_risk_indicators` — Predictive store flight-risk indices combining low eNPS, overtime hours, and historical attrition velocity.

---

## 5. Example Questions

1. "What was our overall Employee Net Promoter Score (eNPS) across retail stores in the latest Q2 pulse survey?"
2. "What are current retail industry employee engagement and frontline eNPS benchmarks according to Gallup and Culture Amp?"
3. "Which store departments (e.g., Customer Service, Stocking, Bakery) have the highest and lowest eNPS scores?"
4. "What are the top recurring themes identified in detractor feedback regarding workplace tools and equipment?"
5. "Can you render a chart of quarterly eNPS sentiment trends across our 4 operating regions over the past 2 years?"

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
uv run --frozen pytest domains/human_resources/agents/associate_engagement_pulse_enps/tests/unit -v

# Run interactively with ADK CLI
adk run domains/human_resources/agents/associate_engagement_pulse_enps
```
