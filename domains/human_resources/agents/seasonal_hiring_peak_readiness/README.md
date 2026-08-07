# HR: Seasonal Hiring & Peak Readiness Agent

An enterprise AI agent for **HR: Seasonal Hiring & Peak Readiness**, built with Google ADK for Gemini Enterprise.

---

## Why This Agent Matters

Q4 holiday shopping, back-to-school, and spring surge seasons require onboarding hundreds of temporary store associates in tightly synchronized waves. Staffing deficits during peak shopping weeks cause lost sales and fulfillment bottlenecks, while hiring pipeline friction increases cost-per-hire. This agent tracks applicant funnel conversions, background check turnaround days, wave hiring targets vs. actuals, and seasonal-to-permanent conversion rates.

---

## Key Metrics Tracked

| Metric | Business Description | Target Benchmark |
| :--- | :--- | :--- |
| **Peak Hiring Target Fulfillment (%)** | Actual seasonal associates onboarded vs. budgeted headcount target | >= 98.0% |
| **Background Check Turnaround (Days)** | Average calendar days from offer acceptance to background clearance | <= 3.0 Days |
| **Applicant Funnel Conversion (%)** | Percentage of seasonal applicants progressing from application to offer accepted | >= 25.0% |
| **Seasonal-to-Permanent Conversion (%)** | High-performing seasonal associates retained into permanent part-time/full-time roles | >= 20.0% |

---

## What It Answers & Sub-Agent Routing

The orchestrator routes user questions to specialized sub-agents:

- **Internal BigQuery Data (`data_insights`)**:
  - Peak hiring plans, applicant tracking funnel stages, background screening cycle times, and seasonal onboarding wave rosters.
- **External Market Context (`market_context`)**:
  - Holiday retail seasonal hiring forecasts (NRF, Challenger Gray), hourly wage incentives, and seasonal labor pool trends.
- **Synthesized Responses**:
  - Compares recruiting pipeline velocity against target peak demand curves to prevent store staffing shortfalls.

---

## Authorized BigQuery Tables

All tables reside in the `retail_ent_agents` BigQuery dataset:

- `hrwm_shpr_peak_hiring_targets`
- `hrwm_shpr_applicant_funnel_stages`
- `hrwm_shpr_background_screening_days`
- `hrwm_shpr_seasonal_retention_conversions`

---

## Example Questions

- "What is our seasonal hiring progress against target across Wave 1 and Wave 2 for the upcoming holiday peak?"
- "What is the current average turnaround time in days for associate background check screenings?"
- "What percentage of seasonal associates from the previous holiday season were converted to permanent store positions?"
- "What are the national retail seasonal hiring projections and hourly wage trends for the 2026 holiday season?"
- "Show me a chart of seasonal hiring targets versus actual onboarded headcount by wave."

---

## Sample Q&A Showcase

### 1. Internal BigQuery Data Insights
**User**: *What is our seasonal hiring progress against target across Wave 1 and Wave 2 for the upcoming holiday peak?*  
**Agent**: Analyzing `retail_ent_agents.hrwm_shpr_peak_hiring_targets` and `hrwm_shpr_applicant_funnel_stages`:
- **Wave 1 (Oct 1–15)**: Target 450 associates | **472 onboarded (104.9% of target)**.
- **Wave 2 (Oct 16–31)**: Target 600 associates | **588 onboarded (98.0% of target)**.
- **Overall Funnel Conversion**: 28.4% application-to-hire rate with an average screening turnaround of **2.6 days**.

### 2. External Market Grounding
**User**: *What are the national retail seasonal hiring projections and hourly wage trends for the 2026 holiday season?*  
**Agent**: According to national retail labor market analysis (NRF and Challenger, Gray & Christmas):
- Retailers are projecting seasonal holiday hiring between **525,000 and 575,000 workers**, reflecting balanced consumer holiday demand.
- Top hiring incentives include immediate daily pay access, employee merchandise discounts (20%–30%), and flexible micro-shift scheduling.

### 3. Visual Analytics Artifact
**User**: *Show me a chart of seasonal hiring targets versus actual onboarded headcount by wave.*  
**Agent**: Visual comparison of hiring targets and actuals:

![Sample Performance Visualization](sample_chart.png)

---

## How to Run & Test

```bash
# 1. Run unit tests
uv run --frozen pytest domains/human_resources/agents/seasonal_hiring_peak_readiness/tests/unit -v

# 2. Run local interactive adk chat
adk run domains/human_resources/agents/seasonal_hiring_peak_readiness
```
