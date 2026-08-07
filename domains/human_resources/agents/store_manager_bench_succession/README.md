# HR: Store Leadership Bench & Succession Agent

An enterprise AI agent for **HR: Store Leadership Bench & Succession**, built with Google ADK for Gemini Enterprise.

---

## Why This Agent Matters

Store Manager vacancies directly degrade retail store profitability, associate retention, and operational execution. Having a qualified pipeline of Assistant Store Managers (ASMs) ready for promotion minimizes store manager vacancy downtime and costly external recruitment. This agent evaluates leadership readiness scores, 9-box talent matrix distributions, succession coverage ratios, and store manager vacancy durations.

---

## Key Metrics Tracked

| Metric | Business Description | Target Benchmark |
| :--- | :--- | :--- |
| **Store Manager Bench Readiness (%)** | Percentage of ASMs evaluated as 'Ready Now' (Readiness Score >= 80) | >= 75.0% |
| **Store Manager Vacancy Duration (Days)** | Average calendar days required to fill an open Store Manager position | <= 21.0 Days |
| **Internal Leadership Promotion Rate (%)** | Percent of Store Manager vacancies filled through internal promotion | >= 70.0% |
| **Succession Bench Coverage Ratio** | Average number of qualified internal candidates identified per store | >= 2.0 candidates |

---

## What It Answers & Sub-Agent Routing

The orchestrator routes user questions to specialized sub-agents:

- **Internal BigQuery Data (`data_insights`)**:
  - Leadership bench evaluations, 9-box performance/potential ratings, open manager vacancy logs, and internal promotion history.
- **External Market Context (`market_context`)**:
  - Retail leadership turnover trends, executive succession benchmarks, and leadership development frameworks.
- **Synthesized Responses**:
  - Identifies leadership succession vulnerabilities across retail districts before critical store manager vacancies occur.

---

## Authorized BigQuery Tables

All tables reside in the `retail_ent_agents` BigQuery dataset:

- `hrwm_smbs_leadership_bench_rosters`
- `hrwm_smbs_9_box_talent_evaluations`
- `hrwm_smbs_store_manager_vacancies`
- `hrwm_smbs_internal_promotions`

---

## Example Questions

- "What is the current percentage of Assistant Store Managers evaluated as 'Ready Now' for promotion across Region West?"
- "What is our average Store Manager vacancy duration in days, and how does internal promotion speed compare to external hires?"
- "Which store districts currently have zero qualified succession candidates on their Store Manager bench?"
- "What are retail industry best practices and benchmarks for Store Manager internal promotion rates and vacancy fill times?"
- "Show me a chart comparing leadership bench readiness with store manager vacancy duration by region."

---

## Sample Q&A Showcase

### 1. Internal BigQuery Data Insights
**User**: *What is the current percentage of Assistant Store Managers evaluated as 'Ready Now' for promotion across Region West?*  
**Agent**: Based on `retail_ent_agents.hrwm_smbs_leadership_bench_rosters` and `hrwm_smbs_9_box_talent_evaluations`:
- **Region West**: **88.5% of ASMs** (23 of 26 evaluated) hold a readiness score >= 80, maintaining the highest bench strength across the company.
- **Average Store Manager Vacancy Fill Time**: **14.5 days** in Region West (vs. enterprise average of 23.2 days), with 85% of positions filled via internal promotion.

### 2. External Market Grounding
**User**: *What are retail industry best practices and benchmarks for Store Manager internal promotion rates and vacancy fill times?*  
**Agent**: Research from retail leadership advisory firms and industry benchmarks indicates:
- Top-performing retail organizations maintain **70%–80% internal promotion rates** for Store Manager positions.
- External Store Manager onboarding carries a **40% higher 12-month failure rate** and takes an average of **45–60 days** to fill versus **15–25 days** for internal bench promotions.

### 3. Visual Analytics Artifact
**User**: *Show me a chart comparing leadership bench readiness with store manager vacancy duration by region.*  
**Agent**: Visual correlation of bench readiness and vacancy duration:

![Sample Performance Visualization](sample_chart.png)

---

## How to Run & Test

```bash
# 1. Run unit tests
uv run --frozen pytest domains/human_resources/agents/store_manager_bench_succession/tests/unit -v

# 2. Run local interactive adk chat
adk run domains/human_resources/agents/store_manager_bench_succession
```
