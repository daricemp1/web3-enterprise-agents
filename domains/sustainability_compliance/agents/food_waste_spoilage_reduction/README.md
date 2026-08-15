# ESG: Food Waste Reduction & Diversion

Part of the **Retail Enterprise Agents** platform for Gemini Enterprise.

---

## 1. Why This Agent Matters

### Business Problem
Grocery and multi-category retailers face significant financial shrink and high landfill methane emissions from perishable food waste, markdown delays, and inefficient food bank donation pipelines.

### Target Personas
VP of Fresh Merchandising, Sustainability Director, Store Operations VP, Community Relations Lead

### Key Metrics Tracked
| Metric | Benchmark / Target | Business Impact |
| :--- | :--- | :--- |
| **Perishable Food Waste Shrink Cost** | `Target: < $1.2M / quarter` | Total retail inventory write-off from spoiled perishables and expired goods. |
| **Food Waste Diversion Rate %** | `Target: >= 85%` | Percentage of unsold food diverted to charity donations, animal feed, or composting. |
| **Dynamic Markdown Rescue Revenue** | `Target: > $450k / quarter` | Incremental gross revenue captured through timely AI dynamic markdown markdowns. |
| **Meals Donated to Food Banks** | `Target: > 500,000 meals YTD` | Equivalent meals generated through Feeding America partner charity donations. |
| **Landfill Methane Avoidance (MT CO2e)** | `Target: > 1,200 MT` | Greenhouse gas emissions prevented by diverting organic waste from municipal landfills. |

---

## 2. What It Answers & Sub-Agent Routing

### Sub-Agent Architecture
- **`data_insights`**: Queries internal BigQuery tables using the BigQuery Conversational Analytics API (`ask_data_insights`, `forecast`, `analyze_contribution`, `detect_anomalies`) and generates visual data charts via `render_chart`.
- **`market_context`**: Leverages Google Search grounding for external retail ESG benchmarks, statutory regulations, environmental frameworks, and industry standards.
- **`root_agent`**: Orchestrates routing between internal analytics and external market intelligence.

---

## 3. Sample Q&A Showcase

### Example 1: Internal Analytics (Data Insights)
*Question:* "What was our total perishable food waste shrink cost and spoiled units across stores in Q2 2026?"  
*Response:*  
> Based on BigQuery inventory records (`esgc_fwsr_spoilage_by_department`), total perishable food waste shrink across all stores in Q2 2026 was **$1,084,250** across **412,890 spoiled units**. Fresh Produce accounted for $462,100 (42.6%), followed by Dairy & Prepared Foods ($318,400) and Fresh Meat/Seafood ($303,750). Dynamic markdown interventions recovered an estimated $382,000 in revenue that would have otherwise resulted in total loss.

### Example 2: Market Grounding (Market Context)
*Question:* "What are current best practices and retail case studies for AI-driven dynamic markdown pricing in fresh grocery?"  
*Response:*  
> Recent retail case studies (FMI / ReFED 2026) show that computer-vision and shelf-life aware dynamic markdown pricing models reduce perishable food waste by **28% to 35%** while increasing recovered margin by **18%**. Best practices involve automated 2-tier discounting (30% off at 48 hours to expiry, 50% off at 24 hours) combined with digital electronic shelf label (ESL) updates and customer app notifications for local flash-sales.

### Example 3: Chart Visualization (`sample_chart.png`)
*Question:* "Can you render a chart of monthly food waste diversion tonnage broken down by donations, composting, and landfill?"  
*Generated Visual Artifact:*  
![Sample Chart](sample_chart.png)

---

### 4. Live Multi-Turn Demo Walkthrough (Gemini Enterprise)

Watch the deployed **ESG: Food Waste Reduction & Diversion** execute a live multi-turn analytical reasoning session in Gemini Enterprise:

> 📺 **Interactive Demo Player**: [Open Full HD Video Player (1080p)](https://rajanm.github.io/retail-enterprise-agents/demos/gemini-enterprise/sustainability_compliance/food_waste_spoilage_reduction.html)  
> 📹 **Direct MP4 Download**: [`food_waste_spoilage_reduction.mp4`](../../../../demos/gemini-enterprise/sustainability_compliance/food_waste_spoilage_reduction.mp4)

```
Turn 1: Quantitative analysis against BigQuery Conversational Analytics
Turn 2: Grounded real-time external retail search & regulatory synthesis
Turn 3: Visual matplotlib trend chart generation
Turn 4: Interactive executive slide presentation generated in Gemini Enterprise Canvas
```

---

## 4. Authorized BigQuery Tables

- `esgc_fwsr_spoilage_by_department` — Daily perishable waste, shrink cost, and spoiled weight by store department.
- `esgc_fwsr_dynamic_markdown_performance` — Dynamic discount execution, sell-through velocity, and recovered gross margin.
- `esgc_fwsr_donation_compost_diversion` — Pounds of food donated to food banks vs sent to commercial composting facilities.
- `esgc_fwsr_epa_diversion_benchmarks` — EPA 2030 food loss reduction goals and store-level diversion compliance.

---

## 5. Example Questions

1. "What was our total perishable food waste shrink cost and spoiled units across stores in Q2 2026?"
2. "What are current best practices and retail case studies for AI-driven dynamic markdown pricing in fresh grocery?"
3. "How many total pounds of food and estimated meals were donated to charity partners in 2026 YTD?"
4. "Which store district has the lowest composting diversion rate % in fresh bakery and produce?"
5. "Can you render a chart of monthly food waste diversion tonnage broken down by donations, composting, and landfill?"

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
uv run --frozen pytest domains/sustainability_compliance/agents/food_waste_spoilage_reduction/tests/unit -v

# Run interactively with ADK CLI
adk run domains/sustainability_compliance/agents/food_waste_spoilage_reduction
```
