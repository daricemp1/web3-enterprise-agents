# ESG: Supplier Diversity & Equity Spend

Part of the **Retail Enterprise Agents** platform for Gemini Enterprise.

---

## 1. Why This Agent Matters

### Business Problem
Retailers seek to build resilient, equitable supply chains and meet corporate diversity procurement commitments by expanding spend with certified Minority, Women, Veteran, LGBTQ+, and Disability-Owned enterprises.

### Target Personas
Chief Procurement Officer, Supplier Diversity Director, Category Sourcing Managers, ESG Reporting Lead

### Key Metrics Tracked
| Metric | Benchmark / Target | Business Impact |
| :--- | :--- | :--- |
| **Diverse Supplier Procurement Spend ($)** | `Target: > $450M / year` | Total enterprise spend awarded to certified diverse business enterprises (DBE/MBE/WBE/VBE). |
| **Diverse Spend % of Total Procurement** | `Target: >= 12.0% of spend` | Percentage of total commercial merchandise and corporate non-merchandise spend awarded to diverse vendors. |
| **Diverse Vendor Network Growth (Count)** | `Target: > 75 new vendors / year` | Net new certified diverse suppliers onboarded across retail merchandise departments. |
| **Diverse Brand Incubator Graduation Rate %** | `Target: >= 70%` | Percentage of small diverse brands in accelerator programs reaching national multi-store distribution. |
| **Tier-2 Diversity Reporting Compliance %** | `Target: >= 85%` | Compliance rate of Tier-1 prime suppliers reporting diverse subcontractor spend. |

---

## 2. What It Answers & Sub-Agent Routing

### Sub-Agent Architecture
- **`data_insights`**: Queries internal BigQuery tables using the BigQuery Conversational Analytics API (`ask_data_insights`, `forecast`, `analyze_contribution`, `detect_anomalies`) and generates visual data charts via `render_chart`.
- **`market_context`**: Leverages Google Search grounding for external retail ESG benchmarks, statutory regulations, environmental frameworks, and industry standards.
- **`root_agent`**: Orchestrates routing between internal analytics and external market intelligence.

---

## 3. Sample Q&A Showcase

### Example 1: Internal Analytics (Data Insights)
*Question:* "What is our total procurement spend with certified diverse suppliers in 2026 YTD and what percentage of total spend does it represent?"  
*Response:*  
> Based on procurement ledger records in BigQuery (`esgc_dsds_supplier_spend_ledger`), our total certified diverse supplier spend in 2026 YTD (January - June) is **$248,650,000**, representing **13.1% of total enterprise procurement** (exceeding our 12.0% annual milestone). Spend spans 318 certified vendors, led by Women-Owned Business Enterprises (WBE: $112.4M) and Minority-Owned Business Enterprises (MBE: $98.2M).

### Example 2: Market Grounding (Market Context)
*Question:* "What are average supplier diversity spend benchmarks for Fortune 500 retail and consumer goods companies according to NMSDC and WBENC?"  
*Response:*  
> According to the National Minority Supplier Development Council (NMSDC) and WBENC 2026 Retail Benchmark Report, leading Fortune 500 consumer retailers average **8% to 11%** of total procurement spend with certified diverse businesses, with top-decile 'Billion Dollar Roundtable' leaders exceeding **14%**. Growth is fastest in Private Brand grocery, beauty/personal care, and logistics/fulfillment contract services.

### Example 3: Chart Visualization (`sample_chart.png`)
*Question:* "Show me a chart of diverse supplier procurement spend broken down by diversity ownership classification in 2026."  
*Generated Visual Artifact:*  
![Sample Chart](sample_chart.png)

---

### 4. Live Multi-Turn Demo Walkthrough (Gemini Enterprise)

Watch the deployed **ESG: Supplier Diversity & Equity Spend** execute a live multi-turn analytical reasoning session in Gemini Enterprise:

> 📺 **Interactive Demo Player**: [Open Full HD Video Player (1080p)](https://rajanm.github.io/retail-enterprise-agents/demos/gemini-enterprise/sustainability_compliance/dei_supplier_diversity_spend.html)  
> 📹 **Direct MP4 Download**: [`dei_supplier_diversity_spend.mp4`](../../../../demos/gemini-enterprise/sustainability_compliance/dei_supplier_diversity_spend.mp4)

```
Turn 1: Quantitative analysis against BigQuery Conversational Analytics
Turn 2: Grounded real-time external retail search & regulatory synthesis
Turn 3: Visual matplotlib trend chart generation
Turn 4: Interactive executive slide presentation generated in Gemini Enterprise Canvas
```

---

## 4. Authorized BigQuery Tables

- `esgc_dsds_supplier_spend_ledger` — Purchase order spend by supplier, product category, certifying agency, and diversity classification.
- `esgc_dsds_diverse_vendor_profiles` — Supplier certification details (NMSDC, WBENC, NGLCC, Disability:IN), ownership %, and tier.
- `esgc_dsds_tier2_prime_reports` — Tier-1 prime supplier reported indirect and direct diverse subcontractor spend.
- `esgc_dsds_diversity_spend_targets` — Annual category-level diverse spend goals, baseline spend, and variance vs target.

---

## 5. Example Questions

1. "What is our total procurement spend with certified diverse suppliers in 2026 YTD and what percentage of total spend does it represent?"
2. "What are average supplier diversity spend benchmarks for Fortune 500 retail and consumer goods companies according to NMSDC and WBENC?"
3. "Which diversity category (Women-Owned, Minority-Owned, Veteran-Owned) has achieved the highest spend target achievement %?"
4. "How much Tier-2 diverse spend was reported by our top 10 prime logistics and packaging suppliers?"
5. "Show me a chart of diverse supplier procurement spend broken down by diversity ownership classification in 2026."

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
uv run --frozen pytest domains/sustainability_compliance/agents/dei_supplier_diversity_spend/tests/unit -v

# Run interactively with ADK CLI
adk run domains/sustainability_compliance/agents/dei_supplier_diversity_spend
```
