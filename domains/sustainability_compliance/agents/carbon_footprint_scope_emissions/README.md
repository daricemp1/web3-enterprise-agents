# ESG: Carbon Footprint & Scope Emissions Agent

An enterprise AI agent for **ESG: Carbon Footprint & Scope Emissions**, built with Google ADK for Gemini Enterprise.

---

## Why This Agent Matters

Retail executives and ESG leaders require real-time visibility into sustainability metrics, regulatory disclosures, and operational compliance to achieve net-zero targets, avoid statutory penalties, and enhance brand equity. This agent unifies internal operational telemetry (emissions, waste, renewable energy, supplier audits) with external market intelligence and global environmental standards.

---

## Key Metrics Tracked

| Metric | Business Description |
| :--- | :--- |
| **Total GHG Emissions (CO2e)** | Total Scope 1 + 2 + 3 carbon emissions in metric tons |
| **Net-Zero Progress %** | YTD reduction vs baseline target |
| **Scope 2 Renewable Factor** | RECs and clean energy grid abatement |
| **Scope 3 Carbon Intensity** | MT CO2e per million dollars spend |

---

## What It Answers & Sub-Agent Routing

The orchestrator routes user questions to specialized sub-agents:

- **Internal BigQuery Data (`data_insights`)**:
  - Scope 1 direct fleet/facility emissions, Scope 2 grid electricity emissions, Scope 3 supply chain lifecycle emissions, net-zero reduction targets, or carbon intensity per dollar
- **External Market Context (`market_context`)**:
  - SBTi (Science Based Targets initiative) reporting guidelines, SEC climate disclosure rules, carbon credit market pricing, or CDP benchmarking standards
- **Synthesized Responses**:
  - Blends internal performance data with external market trends, standards, and benchmarks.

---

## Authorized BigQuery Tables

All tables reside in the `retail_ent_agents` BigQuery dataset:

- `esgc_cfse_scope1_fleet_facilities`
- `esgc_cfse_scope2_electricity_grid`
- `esgc_cfse_scope3_supply_chain_lifecycle`
- `esgc_cfse_net_zero_targets`

---

## Example Questions

- "What is our total Scope 1 GHG emissions in metric tons across all facilities in 2026 YTD?"
- "What are the latest SEC and European CSRD climate disclosure guidelines for retail Scope 3 reporting?"
- "Which product category has the highest Scope 3 supply chain carbon intensity per dollar of spend in 2026?"
- "How do our net-zero carbon reduction targets compare to leading retail peer commitments under SBTi?"
- "Show me a chart of monthly Scope 2 electricity emissions and renewable energy credits applied in 2026."

---

## Sample Q&A Showcase

### 1. Internal BigQuery Data Insights
**User**: *What is our total Scope 1 GHG emissions in metric tons across all facilities in 2026 YTD?*  
**Agent**: Based on internal BigQuery facility telemetry (`esgc_cfse_scope1_fleet_facilities`), our total Scope 1 direct greenhouse gas emissions across all retail stores and distribution centers for 2026 YTD (January through June) are **3,030.7 metric tons of CO2e**. Distribution centers account for 85.3% of direct emissions (primarily fleet logistics diesel and natural gas heating), with DC-101 generating 1,415.7 MT CO2e and DC-102 generating 1,120.5 MT CO2e.

### 2. External Market Grounding
**User**: *What are the latest SEC and European CSRD climate disclosure guidelines for retail Scope 3 reporting?*  
**Agent**: According to official SEC climate disclosure rulings and the European Corporate Sustainability Reporting Directive (CSRD / ESRS E1), retail enterprises operating in or exporting to the EU must disclose material Scope 3 value chain emissions. Key retail requirements include calculating Category 1 (Purchased Goods & Services) and Category 4 (Upstream Transportation) using primary supplier carbon accounting, verified under Science Based Targets initiative (SBTi) net-zero criteria.

### 3. Visual Analytics Artifact
**User**: *Show me a chart of monthly Scope 2 electricity emissions and renewable energy credits applied in 2026.*  
**Agent**: Rendered chart artifact `sample_chart.png` illustrating performance metrics.

![Sample Performance Visualization](sample_chart.png)

---

## How to Run & Test

```bash
# 1. Run unit tests
uv run --frozen pytest domains/sustainability_compliance/agents/carbon_footprint_scope_emissions/tests/unit -v

# 2. Run local interactive adk chat
adk run domains/sustainability_compliance/agents/carbon_footprint_scope_emissions
```
