# ESG: Restricted Substances (RSL) & Chemical Safety Agent

An enterprise AI agent for **ESG: Restricted Substances (RSL) & Chemical Safety**, built with Google ADK for Gemini Enterprise.

---

## Why This Agent Matters

Retail executives and ESG leaders require real-time visibility into sustainability metrics, regulatory disclosures, and operational compliance to achieve net-zero targets, avoid statutory penalties, and enhance brand equity. This agent unifies internal operational telemetry (emissions, waste, renewable energy, supplier audits) with external market intelligence and global environmental standards.

---

## Key Metrics Tracked

| Metric | Business Description |
| :--- | :--- |
| **RSL Lab Test Pass Rate %** | Percentage of tested merchandise lots passing chemical safety limits |
| **Active Certificate Coverage %** | Suppliers with valid, unexpired chemical compliance certifications |
| **PFAS Phaseout Progress %** | Completion percentage of eliminating forever chemicals from products |
| **Prop 65 Warning Compliance %** | Merchandise screened and compliant with warning label laws |

---

## What It Answers & Sub-Agent Routing

The orchestrator routes user questions to specialized sub-agents:

- **Internal BigQuery Data (`data_insights`)**:
  - RSL laboratory testing results and ppm levels, vendor chemical compliance certificates, Prop 65 / REACH SVHC screenings, or hazardous chemical phaseout roadmaps
- **External Market Context (`market_context`)**:
  - EU REACH SVHC candidate list additions, California Proposition 65 settlement trends, PFAS phaseout bans in apparel/cookware, or OEKO-TEX standard updates
- **Synthesized Responses**:
  - Blends internal performance data with external market trends, standards, and benchmarks.

---

## Authorized BigQuery Tables

All tables reside in the `retail_ent_agents` BigQuery dataset:

- `esgc_crsr_rsl_testing_results`
- `esgc_crsr_chemical_compliance_certificates`
- `esgc_crsr_prop65_reach_screenings`
- `esgc_crsr_hazardous_phaseout_plans`

---

## Example Questions

- "What is our overall RSL chemical lab testing pass rate and how many test failures occurred in Q2 2026?"
- "What new substances were added to the EU REACH SVHC authorization list and California Prop 65 in 2026?"
- "Which product lines are currently tracked under the PFAS chemical phaseout plan and what is their migration progress %?"
- "How does our restricted substances testing protocol compare to AFIRM Group industry apparel safety standards?"
- "Provide a chart of chemical compliance certificate statuses across our active vendor base."

---

## Sample Q&A Showcase

### 1. Internal BigQuery Data Insights
**User**: *What is our overall RSL chemical lab testing pass rate and how many test failures occurred in Q2 2026?*  
**Agent**: According to third-party laboratory testing results (`esgc_crsr_rsl_testing_results`), our overall RSL chemical pass rate is **100% across all tested lots** in 2026 YTD, with zero regulatory test failures. One apparel SKU (SKU-002 Recycled Jacket) detected 12.0 ppm total fluorine against the 50.0 ppm safety threshold, remaining within statutory compliance while our fluorine-free bio-based DWR phaseout reaches 85% completion.

### 2. External Market Grounding
**User**: *What new substances were added to the EU REACH SVHC authorization list and California Prop 65 in 2026?*  
**Agent**: In 2026, the European Chemicals Agency (ECHA) added additional per- and polyfluoroalkyl substances (PFAS) and specialized oligomeric flame retardants to the REACH Candidate List of Substances of Very High Concern (SVHC), triggering supply chain notification duties above 0.1% w/w. California OEHHA updated Proposition 65 with refined Safe Harbor No Significant Risk Levels (NSRLs) for specific plasticizers and bisphenol analogues.

### 3. Visual Analytics Artifact
**User**: *Provide a chart of chemical compliance certificate statuses across our active vendor base.*  
**Agent**: Rendered chart artifact `sample_chart.png` illustrating performance metrics.

![Sample Performance Visualization](sample_chart.png)

---

## How to Run & Test

```bash
# 1. Run unit tests
uv run --frozen pytest domains/sustainability_compliance/agents/chemical_restricted_substances_rsl/tests/unit -v

# 2. Run local interactive adk chat
adk run domains/sustainability_compliance/agents/chemical_restricted_substances_rsl
```
