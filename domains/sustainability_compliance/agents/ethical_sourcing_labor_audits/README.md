# ESG: Ethical Sourcing & Labor Audits Agent

An enterprise AI agent for **ESG: Ethical Sourcing & Labor Audits**, built with Google ADK for Gemini Enterprise.

---

## Why This Agent Matters

Retail executives and ESG leaders require real-time visibility into sustainability metrics, regulatory disclosures, and operational compliance to achieve net-zero targets, avoid statutory penalties, and enhance brand equity. This agent unifies internal operational telemetry (emissions, waste, renewable energy, supplier audits) with external market intelligence and global environmental standards.

---

## Key Metrics Tracked

| Metric | Business Description |
| :--- | :--- |
| **Audit Compliance Rate %** | Percentage of active suppliers with valid, passing social audits |
| **Zero-Tolerance Violations** | Count of severe human rights or safety violations (Target: 0) |
| **CAP On-Time Closure %** | Percentage of Corrective Action Plans closed by deadline |
| **Sedex SMETA Average Score** | Overall composite supplier ethical score |

---

## What It Answers & Sub-Agent Routing

The orchestrator routes user questions to specialized sub-agents:

- **Internal BigQuery Data (`data_insights`)**:
  - Supplier social audit scores, Sedex/SMETA 4-pillar ratings, zero-tolerance violation logs, or corrective action plan (CAP) remediation statuses
- **External Market Context (`market_context`)**:
  - Uyghur Forced Labor Prevention Act (UFLPA) compliance updates, ILO international labor standards, Fair Labor Association benchmark audits, or regional supply chain human rights laws
- **Synthesized Responses**:
  - Blends internal performance data with external market trends, standards, and benchmarks.

---

### 4. Live Multi-Turn Demo Walkthrough

An end-to-end multi-turn analytical reasoning session in Gemini Enterprise:

> 📺 **Watch Full HD 1080p Video Recording**:
> - [🎬 Interactive Demo Player](https://rajanm.github.io/retail-enterprise-agents/demos/gemini-enterprise/sustainability_compliance/ethical_sourcing_labor_audits.html)
> - [⬇️ Direct Video File (.mp4)](https://rajanm.github.io/retail-enterprise-agents/demos/gemini-enterprise/sustainability_compliance/ethical_sourcing_labor_audits.mp4)

```mermaid
sequenceDiagram
    autonumber
    actor User as Retail ESG Executive
    participant Agent as ESG: Ethical Sourcing & Labor Audits
    participant Canvas as Gemini Enterprise Canvas

    Note over User,Agent: Turn 1: Quantitative Data Insights (BigQuery)
    User->>Agent: Prompt 1: Supplier Sedex SMETA social audit compliance pass rates and zero-tolerance labor violation flags across tier-1 factories
    Agent-->>User: Synthesized metric breakdown grounded in authorized BigQuery tables

    Note over User,Agent: Turn 2: Real-time External Grounding (Google Search)
    User->>Agent: Prompt 2: Uyghur Forced Labor Prevention Act (UFLPA) supply chain traceability guidelines and ILO core labor convention standards
    Agent-->>User: Grounded market, regulatory & ESG framework analysis

    Note over User,Agent: Turn 3: Visual Chart Generation (Matplotlib)
    User->>Agent: Prompt 3: Render chart for key sustainability metrics
    Agent-->>User: Executable SQL query + Matplotlib PNG chart visualization

    Note over User,Canvas: Turn 4: Executive Presentation Deck (Canvas Mode)
    User->>Agent: Prompt 4: 4-slide executive presentation summarizing the Ethical Sourcing & Labor Audits analysis, key KPIs, and strategic recommendations
    Agent-->>User: Multi-slide markdown deck with KPIs, findings & actions
    User->>Canvas: Switch to Canvas Mode & paste deck content
    Canvas-->>User: Renders interactive 4-slide executive presentation
```

## Authorized BigQuery Tables

All tables reside in the `retail_ent_agents` BigQuery dataset:

- `esgc_esla_supplier_social_audits`
- `esgc_esla_sedex_smeta_scores`
- `esgc_esla_zero_tolerance_violations`
- `esgc_esla_corrective_action_plans`

---

## Example Questions

- "What is the breakdown of our active suppliers by social audit rating grade (A, B, C, D)?"
- "What are the latest CBP customs enforcement guidelines under the Uyghur Forced Labor Prevention Act?"
- "Are there any open zero-tolerance labor violations across our apparel and home goods suppliers?"
- "How does our supplier SMETA labor compliance score compare to global retail ethical sourcing standards?"
- "Show a chart of corrective action plan resolution status across supplier facilities."

---

## Sample Q&A Showcase

### 1. Internal BigQuery Data Insights
**User**: *What is the breakdown of our active suppliers by social audit rating grade (A, B, C, D)?*  
**Agent**: According to internal ethical sourcing records (`esgc_esla_supplier_social_audits`), **66.7% of active suppliers hold Grade A (Full Compliance)** (including GreenPackaging Innovations at 98.0 and CleanTech Electronics at 95.0), and **33.3% hold Grade B (Minor Corrective Action)**. Zero active suppliers are rated Grade C or D. All 4 open corrective action plans (CAPs) from Q2 audits have been successfully resolved and verified on-time with zero outstanding high-severity findings.

### 2. External Market Grounding
**User**: *What are the latest CBP customs enforcement guidelines under the Uyghur Forced Labor Prevention Act?*  
**Agent**: U.S. Customs and Border Protection (CBP) enforces a rebuttable presumption under the UFLPA prohibiting imports manufactured in whole or in part in the Xinjiang Uyghur Autonomous Region. Recent 2026 updates require importers of record to furnish full supply chain mapping down to the raw cotton gin and polysilicon mine, including DNA isotopic origin testing and third-party traceability audits.

### 3. Visual Analytics Artifact
**User**: *Show a chart of corrective action plan resolution status across supplier facilities.*  
**Agent**: Rendered chart artifact `sample_chart.png` illustrating performance metrics.

![Sample Performance Visualization](sample_chart.png)

---

## How to Run & Test

```bash
# 1. Run unit tests
uv run --frozen pytest domains/sustainability_compliance/agents/ethical_sourcing_labor_audits/tests/unit -v

# 2. Run local interactive adk chat
adk run domains/sustainability_compliance/agents/ethical_sourcing_labor_audits
```
