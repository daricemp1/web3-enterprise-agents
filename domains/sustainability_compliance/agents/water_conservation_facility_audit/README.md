# ESG: Water Conservation & Facility Audits Agent

An enterprise AI agent for **ESG: Water Conservation & Facility Audits**, built with Google ADK for Gemini Enterprise.

---

## Why This Agent Matters

Retail executives and ESG leaders require real-time visibility into sustainability metrics, regulatory disclosures, and operational compliance to achieve net-zero targets, avoid statutory penalties, and enhance brand equity. This agent unifies internal operational telemetry (emissions, waste, renewable energy, supplier audits) with external market intelligence and global environmental standards.

---

## Key Metrics Tracked

| Metric | Business Description |
| :--- | :--- |
| **Water Usage Intensity (Gal/Sq.Ft)** | Water consumption normalized by facility square footage |
| **Cooling Tower Efficiency %** | Recycled water recycling and cycles of concentration |
| **Rainwater Harvested (Gallons)** | Total rainwater collected and reused for irrigation |
| **High-Stress Watershed Exposure %** | Facilities located in extremely high water-stressed regions |

---

## What It Answers & Sub-Agent Routing

The orchestrator routes user questions to specialized sub-agents:

- **Internal BigQuery Data (`data_insights`)**:
  - Facility water meter logs, cooling tower cycles of concentration and efficiency, rainwater harvesting volume, or watershed water stress risk ratings
- **External Market Context (`market_context`)**:
  - WRI Aqueduct Water Risk Atlas data, municipal commercial water tariff hikes, retail water stewardship standards (AWS), or drought emergency water restrictions
- **Synthesized Responses**:
  - Blends internal performance data with external market trends, standards, and benchmarks.

---

## Authorized BigQuery Tables

All tables reside in the `retail_ent_agents` BigQuery dataset:

- `esgc_wcfa_facility_water_meters`
- `esgc_wcfa_cooling_tower_efficiency`
- `esgc_wcfa_rainwater_harvesting_logs`
- `esgc_wcfa_watershed_stress_index`

---

## Example Questions

- "Which retail store facilities have the highest water usage intensity in gallons per square foot in 2026?"
- "What are the latest municipal water conservation restrictions and tier rate hikes affecting commercial facilities in the Southwest US?"
- "How many gallons of rainwater were collected and reused for facility irrigation in 2026?"
- "How do our water efficiency metrics for cooling towers compare to Alliance for Water Stewardship benchmarks?"
- "Generate a chart showing water utility costs across facility types."

---

## Sample Q&A Showcase

### 1. Internal BigQuery Data Insights
**User**: *Which retail store facilities have the highest water usage intensity in gallons per square foot in 2026?*  
**Agent**: Based on facility utility metering data (`esgc_wcfa_facility_water_meters`), **Store 102 (Dallas Flagship)** exhibits the highest water usage intensity at **0.71 gallons/sq.ft** (peaking at 1.03 gal/sq.ft in June due to HVAC cooling loads in Trinity River Basin), followed by **Store 101 (Chicago)** at **0.61 gal/sq.ft**. DC-101 maintains the lowest intensity at **0.33 gal/sq.ft**, benefiting from an on-site 80% efficient closed-loop cooling tower recycling system.

### 2. External Market Grounding
**User**: *What are the latest municipal water conservation restrictions and tier rate hikes affecting commercial facilities in the Southwest US?*  
**Agent**: Municipal water authorities across the Southwestern US (including Texas, Arizona, and Southern California) have implemented Stage 2/Stage 3 drought surcharges, increasing commercial tier-2 volumetric water rates by 18–25% for facilities exceeding seasonal conservation allocations. Authorities mandate automated blowdown controls on commercial cooling towers and ban non-recycled decorative irrigation.

### 3. Visual Analytics Artifact
**User**: *Generate a chart showing water utility costs across facility types.*  
**Agent**: Rendered chart artifact `sample_chart.png` illustrating performance metrics.

![Sample Performance Visualization](sample_chart.png)

---

## How to Run & Test

```bash
# 1. Run unit tests
uv run --frozen pytest domains/sustainability_compliance/agents/water_conservation_facility_audit/tests/unit -v

# 2. Run local interactive adk chat
adk run domains/sustainability_compliance/agents/water_conservation_facility_audit
```
