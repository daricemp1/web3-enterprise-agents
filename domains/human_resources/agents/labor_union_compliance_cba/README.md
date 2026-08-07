# HR: Labor Union & CBA Compliance Agent

An enterprise AI agent for **HR: Labor Union & CBA Compliance**, built with Google ADK for Gemini Enterprise.

---

## Why This Agent Matters

Operating union-represented retail stores requires strict compliance with Collective Bargaining Agreements (CBAs). Missed grievance filing deadlines, improper seniority shift allocation, or unresolved labor disputes result in costly arbitration penalties and strained labor relations. This agent monitors grievance logs, contractual SLA timelines, seniority bidding compliance, and shop steward interaction audits.

---

## Key Metrics Tracked

| Metric | Business Description | Target Benchmark |
| :--- | :--- | :--- |
| **Grievance Resolution SLA Compliance (%)** | CBA grievances resolved within contractual timeline stages (Step 1-3) | >= 95.0% |
| **Open Grievance Volume (#)** | Total active open labor grievances across union store locations | < 10 per local |
| **Seniority Shift Bidding Compliance (%)** | Scheduled shifts allocated strictly according to contractual seniority rosters | 100.0% |
| **Arbitration Escalation Rate (%)** | Percent of grievances escalating to binding external arbitration | < 2.0% |

---

## What It Answers & Sub-Agent Routing

The orchestrator routes user questions to specialized sub-agents:

- **Internal BigQuery Data (`data_insights`)**:
  - Active grievance logs, contractual timeline milestone tracking, seniority shift bid records, and arbitration logs.
- **External Market Context (`market_context`)**:
  - National Labor Relations Board (NLRB) retail rulings, UFCW / Teamsters CBA precedent patterns, and statutory labor laws.
- **Synthesized Responses**:
  - Flags potential grievance SLA breaches and ensures consistent CBA interpretation across union retail facilities.

---

## Authorized BigQuery Tables

All tables reside in the `retail_ent_agents` BigQuery dataset:

- `hrwm_lucc_cba_grievance_logs`
- `hrwm_lucc_grievance_sla_tracking`
- `hrwm_lucc_seniority_shift_bidding`
- `hrwm_lucc_arbitration_records`

---

## Example Questions

- "What is our current open grievance count and resolution SLA compliance percentage by union local?"
- "Are there any Step 2 or Step 3 grievances currently within 5 days of contractual SLA expiration?"
- "What is our seniority shift bidding audit compliance rate across union-represented store locations?"
- "What are standard CBA timelines and best practices for Step 1 through Step 3 grievance resolution in retail agreements?"
- "Show me a chart of grievance volume and resolution SLA compliance by union local."

---

## Sample Q&A Showcase

### 1. Internal BigQuery Data Insights
**User**: *What is our current open grievance count and resolution SLA compliance percentage by union local?*  
**Agent**: Querying `retail_ent_agents.hrwm_lucc_cba_grievance_logs` and `hrwm_lucc_grievance_sla_tracking`:
- **Overall Union Portfolio**: **59 total grievances** logged YTD across 5 union locals with **92.4% overall SLA resolution compliance**.
- **Teamsters Local 55**: 7 grievances, **98.0% SLA compliance** (average resolution in 11.2 days).
- **UFCW Local 204**: 19 grievances, **82.0% SLA compliance** (2 Step 2 scheduling grievances currently under joint review).

### 2. External Market Grounding
**User**: *What are standard CBA timelines and best practices for Step 1 through Step 3 grievance resolution in retail agreements?*  
**Agent**: Standard retail collective bargaining agreements (e.g., UFCW Master Agreements) typically structure:
- **Step 1 (Immediate Supervisor)**: Filing within 14 calendar days of incident; supervisor response within 7–10 days.
- **Step 2 (HR / Store Leadership)**: Formal meeting within 10 days of Step 1 appeal; written answer within 10 days.
- **Step 3 (Corporate Labor Relations & Union Leadership)**: Meeting within 30 days prior to arbitration submission.

### 3. Visual Analytics Artifact
**User**: *Show me a chart of grievance volume and resolution SLA compliance by union local.*  
**Agent**: Union local grievance and SLA compliance distribution:

![Sample Performance Visualization](sample_chart.png)

---

## How to Run & Test

```bash
# 1. Run unit tests
uv run --frozen pytest domains/human_resources/agents/labor_union_compliance_cba/tests/unit -v

# 2. Run local interactive adk chat
adk run domains/human_resources/agents/labor_union_compliance_cba
```
