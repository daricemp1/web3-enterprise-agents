# ESG: Sustainable Packaging & Circularity

Part of the **Retail Enterprise Agents** platform for Gemini Enterprise.

---

## 1. Why This Agent Matters

### Business Problem
Retailers must navigate complex state-level Extended Producer Responsibility (EPR) laws, virgin plastic reduction targets, and consumer demand for curbside recyclable and post-consumer recycled (PCR) packaging.

### Target Personas
Head of Packaging Engineering, Private Brand Director, ESG Compliance Officer, Sourcing Director

### Key Metrics Tracked
| Metric | Benchmark / Target | Business Impact |
| :--- | :--- | :--- |
| **Post-Consumer Recycled (PCR) Content %** | `Target: >= 30% average` | Average recycled material content across primary and secondary product packaging. |
| **Virgin Plastic Reduction (Tons)** | `Target: > 450 tons eliminated` | Cumulative reduction in virgin single-use plastics compared to baseline year. |
| **Curbside Recyclability Index %** | `Target: >= 90% compliant` | Percentage of private brand packaging certified for curbside recycling under How2Recycle. |
| **Polybag Elimination in DCs** | `Target: >= 80% reduction` | Reduction in single-use plastic shipping polybags replaced with 100% recycled paper mailers. |
| **State EPR Packaging Compliance Score** | `Target: 100% compliant` | Full adherence to state packaging fee filings and EPR statutory mandates (CA, OR, CO, ME). |

---

## 2. What It Answers & Sub-Agent Routing

### Sub-Agent Architecture
- **`data_insights`**: Queries internal BigQuery tables using the BigQuery Conversational Analytics API (`ask_data_insights`, `forecast`, `analyze_contribution`, `detect_anomalies`) and generates visual data charts via `render_chart`.
- **`market_context`**: Leverages Google Search grounding for external retail ESG benchmarks, statutory regulations, environmental frameworks, and industry standards.
- **`root_agent`**: Orchestrates routing between internal analytics and external market intelligence.

---

## 3. Sample Q&A Showcase

### Example 1: Internal Analytics (Data Insights)
*Question:* "What is our average post-consumer recycled (PCR) packaging content percentage across product categories?"  
*Response:*  
> According to BigQuery packaging registry telemetry (`esgc_spac_packaging_materials_sku`), our enterprise average PCR packaging content is **32.8%**, surpassing our 30.0% enterprise milestone. Household Essentials leads with **48.2% PCR** (driven by 100% rPET detergent and cleaning bottles), while Personal Care currently averages **21.5% PCR** due to multi-layer cosmetic pump constraints.

### Example 2: Market Grounding (Market Context)
*Question:* "What are the latest state plastic bag and packaging bans enacted across the US in 2026?"  
*Response:*  
> As of 2026, 12 states (including California, New York, New Jersey, Washington, and Colorado) have implemented statewide single-use plastic bag prohibitions and minimum recycled content mandates. Furthermore, California SB 54 and Colorado HB 22-1355 have enacted producer responsibility regulations requiring a 25% reduction in single-use plastic packaging by 2032 and 65% curbside recyclability by 2028.

### Example 3: Chart Visualization (`sample_chart.png`)
*Question:* "Show me a chart of virgin plastic tons eliminated by product category in 2026 YTD."  
*Generated Visual Artifact:*  
![Sample Chart](sample_chart.png)

---

### 4. Live Multi-Turn Demo Walkthrough (Gemini Enterprise)

Watch the deployed **ESG: Sustainable Packaging & Circularity** execute a live multi-turn analytical reasoning session in Gemini Enterprise:

> 📺 **Interactive Demo Player**: [Open Full HD Video Player (1080p)](https://rajanm.github.io/retail-enterprise-agents/demos/gemini-enterprise/sustainability_compliance/sustainable_packaging_circularity.html)  
> 📹 **Direct MP4 Download**: [`sustainable_packaging_circularity.mp4`](../../../../demos/gemini-enterprise/sustainability_compliance/sustainable_packaging_circularity.mp4)

```
Turn 1: Quantitative analysis against BigQuery Conversational Analytics
Turn 2: Grounded real-time external retail search & regulatory synthesis
Turn 3: Visual matplotlib trend chart generation
Turn 4: Interactive executive slide presentation generated in Gemini Enterprise Canvas
```

---

## 4. Authorized BigQuery Tables

- `esgc_spac_packaging_materials_sku` — SKU-level packaging weight, plastic polymer type, PCR %, and recyclability status.
- `esgc_spac_virgin_plastic_reduction` — Annual and quarterly tons of virgin plastic eliminated by product department.
- `esgc_spac_state_epr_fees_filings` — Packaging material weight reported to state producer responsibility organizations (PROs).
- `esgc_spac_supplier_packaging_audits` — Supplier factory certifications for recycled content and plastic reduction claims.

---

## 5. Example Questions

1. "What is our average post-consumer recycled (PCR) packaging content percentage across product categories?"
2. "What are the latest state plastic bag and packaging bans enacted across the US in 2026?"
3. "How many tons of virgin plastic and single-use polybags have been eliminated across distribution centers in 2026?"
4. "Which private brand suppliers are lagging behind our 30% PCR packaging threshold in Household Cleaning?"
5. "Show me a chart of virgin plastic tons eliminated by product category in 2026 YTD."

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
uv run --frozen pytest domains/sustainability_compliance/agents/sustainable_packaging_circularity/tests/unit -v

# Run interactively with ADK CLI
adk run domains/sustainability_compliance/agents/sustainable_packaging_circularity
```
