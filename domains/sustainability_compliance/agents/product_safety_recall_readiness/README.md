# ESG: Product Safety & Recall Execution

Part of the **Retail Enterprise Agents** platform for Gemini Enterprise.

---

## 1. Why This Agent Matters

### Business Problem
When safety defects, choking hazards, or chemical contaminations emerge, retailers must rapidly execute product recalls, lock point-of-sale registers, quarantine store stock, and notify consumers to prevent injuries and regulatory sanctions.

### Target Personas
VP of Quality Assurance & Safety, Retail Operations Director, General Counsel / Product Liability Lead

### Key Metrics Tracked
| Metric | Benchmark / Target | Business Impact |
| :--- | :--- | :--- |
| **Store Shelf Quarantine Speed (Hours)** | `Target: < 4.0 hours` | Average time from recall publication to 100% store shelf removal and backroom lock. |
| **POS Register Block Execution (Minutes)** | `Target: < 15 minutes` | Time elapsed to propagate barcode scan blocks across all retail checkout registers. |
| **Direct Customer Notification Delivery %** | `Target: >= 98%` | Percentage of identified loyalty/e-commerce purchasers successfully contacted via email/SMS/app. |
| **Total Recalled Units Recovered %** | `Target: >= 85%` | Percentage of sold defective units returned, refunded, or safely disposed of by consumers. |
| **Regulatory Agency Filing SLA (Hours)** | `Target: < 24 hours` | Time to file mandatory Section 15(b) reports with CPSC or FDA safety portals. |

---

## 2. What It Answers & Sub-Agent Routing

### Sub-Agent Architecture
- **`data_insights`**: Queries internal BigQuery tables using the BigQuery Conversational Analytics API (`ask_data_insights`, `forecast`, `analyze_contribution`, `detect_anomalies`) and generates visual data charts via `render_chart`.
- **`market_context`**: Leverages Google Search grounding for external retail ESG benchmarks, statutory regulations, environmental frameworks, and industry standards.
- **`root_agent`**: Orchestrates routing between internal analytics and external market intelligence.

---

## 3. Sample Q&A Showcase

### Example 1: Internal Analytics (Data Insights)
*Question:* "What was the average execution time in hours for stores to complete shelf quarantine for active 2026 recalls?"  
*Response:*  
> According to BigQuery operational quarantine telemetry (`esgc_psrr_store_quarantine_logs`), the enterprise average store shelf quarantine execution time across three active 2026 safety recalls was **2.8 hours**, well within our 4.0-hour SLA. All 340 stores completed physical shelf removal, backroom quarantine tagging, and manager portal sign-off within 5 hours of central notification.

### Example 2: Market Grounding (Market Context)
*Question:* "What are current CPSC and FDA regulations regarding mandatory customer notification timelines for Class 1 product recalls?"  
*Response:*  
> Under CPSC Fast Track protocols and FDA 21 CFR Part 7 guidelines, Class 1 recalls (situations with reasonable probability of serious adverse health consequences or death) mandate immediate public press releases and direct customer notification within **24 hours**. Retailers with loyalty or online transaction records must execute direct digital notifications and provide a dedicated customer toll-free hotline and web claim portal.

### Example 3: Chart Visualization (`sample_chart.png`)
*Question:* "Show me a chart tracking store quarantine completion percentage by hour following the latest safety recall notice."  
*Generated Visual Artifact:*  
![Sample Chart](sample_chart.png)

---

### 4. Live Multi-Turn Demo Walkthrough (Gemini Enterprise)

Watch the deployed **ESG: Product Safety & Recall Execution** execute a live multi-turn analytical reasoning session in Gemini Enterprise:

> 📺 **Interactive Demo Player**: [Open Full HD Video Player (1080p)](https://rajanm.github.io/retail-enterprise-agents/demos/gemini-enterprise/sustainability_compliance/product_safety_recall_readiness.html)  
> 📹 **Direct MP4 Download**: [`product_safety_recall_readiness.mp4`](../../../../demos/gemini-enterprise/sustainability_compliance/product_safety_recall_readiness.mp4)

```
Turn 1: Quantitative analysis against BigQuery Conversational Analytics
Turn 2: Grounded real-time external retail search & regulatory synthesis
Turn 3: Visual matplotlib trend chart generation
Turn 4: Interactive executive slide presentation generated in Gemini Enterprise Canvas
```

---

## 4. Authorized BigQuery Tables

- `esgc_psrr_active_recalls` — Recall notice id, affected SKU, hazard category, issuing agency (CPSC, FDA, NHTSA), and date.
- `esgc_psrr_store_quarantine_logs` — Store-by-store shelf lock confirmation timestamp, quarantined unit counts, and manager sign-off.
- `esgc_psrr_pos_register_blocks` — System-wide barcode POS lock propagation status and blocked transaction logs.
- `esgc_psrr_customer_notification_metrics` — Targeted customer outreach counts, email open rates, SMS delivery %, and refund claims.

---

## 5. Example Questions

1. "What was the average execution time in hours for stores to complete shelf quarantine for active 2026 recalls?"
2. "What are current CPSC and FDA regulations regarding mandatory customer notification timelines for Class 1 product recalls?"
3. "How many customer notifications were sent and what was the open rate for the recent baby gear recall?"
4. "Are there any stores that have not yet submitted manager sign-off for the active recall quarantine?"
5. "Show me a chart tracking store quarantine completion percentage by hour following the latest safety recall notice."

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
uv run --frozen pytest domains/sustainability_compliance/agents/product_safety_recall_readiness/tests/unit -v

# Run interactively with ADK CLI
adk run domains/sustainability_compliance/agents/product_safety_recall_readiness
```
