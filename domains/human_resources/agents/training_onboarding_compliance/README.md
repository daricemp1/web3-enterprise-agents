# HR: Training & Onboarding Compliance

Part of the **Retail Enterprise Agents** platform for Gemini Enterprise.

---

## 1. Why This Agent Matters

### Business Problem
Delays in mandatory compliance training, safety onboarding, and product knowledge certifications lead to extended time-to-productivity for new hires and exposure to regulatory non-compliance fines.

### Target Personas
Chief Learning Officer, Retail Training & Development Director, District Human Resources Managers, Store Trainers

### Key Metrics Tracked
| Metric | Benchmark / Target | Business Impact |
| :--- | :--- | :--- |
| **Mandatory Safety & Compliance Completion %** | `Target: >= 98.0%` | Percentage of store associates completing annual required safety, anti-harassment, and OSHA modules within SLA. |
| **New Hire Time-to-Productivity (Days)** | `Target: < 14.0 days` | Average days elapsed from associate hire date to completion of core job pathway and first unassisted solo shift. |
| **Forklift & Equipment Certification Pass %** | `Target: >= 95.0%` | Percentage of warehouse and backroom logistics associates holding active, verified power equipment certifications. |
| **Digital Micro-Learning Course Engagement %** | `Target: >= 82.0%` | Associate participation rate in mobile micro-learning modules on new product launches and POS features. |
| **Overdue Training Course Incident Count** | `Target: < 25 enterprise-wide` | Total number of active associate training courses past mandatory completion deadline. |

---

## 2. What It Answers & Sub-Agent Routing

### Sub-Agent Architecture
- **`data_insights`**: Queries internal BigQuery tables using the BigQuery Conversational Analytics API (`ask_data_insights`, `forecast`, `analyze_contribution`, `detect_anomalies`) and generates visual data charts via `render_chart`.
- **`market_context`**: Leverages Google Search grounding for external retail labor market benchmarks, statutory wage/Fair Workweek regulations, BLS statistics, and HR industry standards.
- **`root_agent`**: Orchestrates routing between internal analytics and external market intelligence.

---

## 3. Sample Q&A Showcase

### Example 1: Internal Analytics (Data Insights)
*Question:* "What is our enterprise completion rate for mandatory annual safety and compliance training in 2026?"  
*Response:*  
> According to BigQuery LMS learning telemetry (`hrwm_tocl_lms_course_completions`), our enterprise completion rate for mandatory annual safety and compliance training stands at **98.6%** across 18,400 active store associates. Food Handler and Active Threat certifications achieved 100% completion across all culinary and front-of-store teams.

### Example 2: Market Grounding (Market Context)
*Question:* "What are current OSHA and state compliance guidelines regarding mandatory workplace safety certification renewal intervals?"  
*Response:*  
> Under OSHA general industry standards (29 CFR 1910) and California Title 8, employers must conduct annual refresher training for hazard communication (HazCom), bloodborne pathogens, and emergency evacuation. Powered industrial truck (forklift) operators must undergo triennial recertification and formal performance evaluation every 3 years or immediately following a safety incident or observed unsafe operation.

### Example 3: Chart Visualization (`sample_chart.png`)
*Question:* "Can you render a chart showing training module completion percentages across our top 5 store departments?"  
*Generated Visual Artifact:*  
![Sample Chart](sample_chart.png)

---

### 4. Live Multi-Turn Demo Walkthrough (Gemini Enterprise)

Watch the deployed **HR: Training & Onboarding Compliance** execute a live multi-turn analytical reasoning session in Gemini Enterprise:

> 📺 **Interactive Demo Player**: [Open Full HD Video Player (1080p)](https://rajanm.github.io/retail-enterprise-agents/demos/gemini-enterprise/human_resources/training_onboarding_compliance.html)  
> 📹 **Direct MP4 Download**: [`training_onboarding_compliance.mp4`](../../../../demos/gemini-enterprise/human_resources/training_onboarding_compliance.mp4)

```
Turn 1: Quantitative analysis against BigQuery Conversational Analytics
Turn 2: Grounded real-time external retail search & regulatory synthesis
Turn 3: Visual matplotlib trend chart generation
Turn 4: Interactive executive slide presentation generated in Gemini Enterprise Canvas
```

---

## 4. Authorized BigQuery Tables

- `hrwm_tocl_lms_course_completions` — LMS course enrollment records, module name, completion status, test scores, and completion timestamp.
- `hrwm_tocl_mandatory_certifications` — Required statutory compliance certifications (OSHA, Food Handler, TIPS, Anti-Harassment) and renewal dates.
- `hrwm_tocl_time_to_productivity_days` — New hire onboarding milestones, mentor sign-off dates, and days elapsed to first standalone shift.
- `hrwm_tocl_safety_training_records` — Material safety, fire drill, active threat, and equipment operation training compliance logs.

---

## 5. Example Questions

1. "What is our enterprise completion rate for mandatory annual safety and compliance training in 2026?"
2. "What are current OSHA and state compliance guidelines regarding mandatory workplace safety certification renewal intervals?"
3. "What is the average time-to-productivity in days for newly onboarded frontline department specialists?"
4. "Which retail store locations have more than five overdue mandatory training certifications?"
5. "Can you render a chart showing training module completion percentages across our top 5 store departments?"

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
uv run --frozen pytest domains/human_resources/agents/training_onboarding_compliance/tests/unit -v

# Run interactively with ADK CLI
adk run domains/human_resources/agents/training_onboarding_compliance
```
