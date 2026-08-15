# ESG: Extended Producer Responsibility (EPR) & Resale Agent

An enterprise AI agent for **ESG: Extended Producer Responsibility (EPR) & Resale**, built with Google ADK for Gemini Enterprise.

---

## Why This Agent Matters

Retail executives and ESG leaders require real-time visibility into sustainability metrics, regulatory disclosures, and operational compliance to achieve net-zero targets, avoid statutory penalties, and enhance brand equity. This agent unifies internal operational telemetry (emissions, waste, renewable energy, supplier audits) with external market intelligence and global environmental standards.

---

## Key Metrics Tracked

| Metric | Business Description |
| :--- | :--- |
| **Total EPR Compliance Fees $** | Total statutory fees paid across state EPR packaging jurisdictions |
| **Take-Back Volume (Tons)** | Total customer trade-in volume diverted from landfills |
| **Recommerce Recovery Revenue $** | Gross revenue generated from resale of refurbished goods |
| **Circular Net Profit Margin %** | Profitability of circular trade-in and resale operations |

---

## What It Answers & Sub-Agent Routing

The orchestrator routes user questions to specialized sub-agents:

- **Internal BigQuery Data (`data_insights`)**:
  - EPR state packaging fees paid, take-back program collected tonnage and rewards, refurbished textile and electronics resale inventory, or net circular recovery profit
- **External Market Context (`market_context`)**:
  - State EPR packaging laws (California SB 54, Colorado, Oregon, Maine), textile recycling regulations, recommerce market growth trends (ThredUp / Trove), or electronics e-waste mandates
- **Synthesized Responses**:
  - Blends internal performance data with external market trends, standards, and benchmarks.

---

### 4. Live Multi-Turn Demo Walkthrough

An end-to-end multi-turn analytical reasoning session in Gemini Enterprise:

> 📺 **Watch Full HD 1080p Video Recording**:
> - [🎬 Interactive Demo Player](https://rajanm.github.io/retail-enterprise-agents/demos/gemini-enterprise/sustainability_compliance/extended_producer_responsibility_epr.html)
> - [⬇️ Direct Video File (.mp4)](https://rajanm.github.io/retail-enterprise-agents/demos/gemini-enterprise/sustainability_compliance/extended_producer_responsibility_epr.mp4)

```mermaid
sequenceDiagram
    autonumber
    actor User as Retail ESG Executive
    participant Agent as ESG: Extended Producer Responsibility (EPR) & Resale
    participant Canvas as Gemini Enterprise Canvas

    Note over User,Agent: Turn 1: Quantitative Data Insights (BigQuery)
    User->>Agent: Prompt 1: Statutory packaging EPR compliance fee liabilities, customer garment/electronics take-back tonnage, and circular recommerce resale revenue
    Agent-->>User: Synthesized metric breakdown grounded in authorized BigQuery tables

    Note over User,Agent: Turn 2: Real-time External Grounding (Google Search)
    User->>Agent: Prompt 2: California SB 54, Oregon Plastic Pollution and Recycling Modernization Act, and circular economy garment recommerce valuation models
    Agent-->>User: Grounded market, regulatory & ESG framework analysis

    Note over User,Agent: Turn 3: Visual Chart Generation (Matplotlib)
    User->>Agent: Prompt 3: Render chart for key sustainability metrics
    Agent-->>User: Executable SQL query + Matplotlib PNG chart visualization

    Note over User,Canvas: Turn 4: Executive Presentation Deck (Canvas Mode)
    User->>Agent: Prompt 4: 4-slide executive presentation summarizing the Extended Producer Responsibility (EPR) & Resale analysis, key KPIs, and strategic recommendations
    Agent-->>User: Multi-slide markdown deck with KPIs, findings & actions
    User->>Canvas: Switch to Canvas Mode & paste deck content
    Canvas-->>User: Renders interactive 4-slide executive presentation
```

## Authorized BigQuery Tables

All tables reside in the `retail_ent_agents` BigQuery dataset:

- `esgc_epre_epr_packaging_fees_paid`
- `esgc_epre_take_back_program_tonnage`
- `esgc_epre_textile_electronic_resale`
- `esgc_epre_circular_recovery_revenue`

---

## Example Questions

- "What are our total EPR packaging compliance fees assessed and paid by state jurisdiction in 2026?"
- "What are the latest compliance deadlines and producer responsibility organization (PRO) fee structures under California SB 54 and Oregon EPR laws?"
- "How many tons of used apparel and electronics have been collected through our customer take-back program in 2026?"
- "How does our recommerce resale recovery margin compare to industry benchmarks from ThredUp and Trove circular retail reports?"
- "Generate a chart of monthly circular recovery revenue and net profit."

---

## Sample Q&A Showcase

### 1. Internal BigQuery Data Insights
**User**: *What are our total EPR packaging compliance fees assessed and paid by state jurisdiction in 2026?*  
**Agent**: According to state regulatory filing logs (`esgc_epre_epr_packaging_fees_paid`), total Extended Producer Responsibility (EPR) packaging fees assessed and paid across all jurisdictions in 2026 Q1 totaled **$331,040.00**. California (SB 54) represents the largest assessment at $206,700 across rigid plastics, flexible films, and corrugate, followed by Colorado ($62,560), Oregon ($62,100), and Maine ($39,680). All compliance filings have been certified and submitted.

### 2. External Market Grounding
**User**: *What are the latest compliance deadlines and producer responsibility organization (PRO) fee structures under California SB 54 and Oregon EPR laws?*  
**Agent**: Under California SB 54, producers must join an approved Producer Responsibility Organization (PRO like Circular Action Alliance) with statutory eco-modulated fees based on package recyclability, PCR percentage, and material toxicity. In Oregon (SB 582 Recycling Modernization Act), PRO program plans require producers to finance statewide collection infrastructure upgrades, with fee discounts of up to 40% for packaging utilizing high post-consumer recycled content.

### 3. Visual Analytics Artifact
**User**: *Generate a chart of monthly circular recovery revenue and net profit.*  
**Agent**: Rendered chart artifact `sample_chart.png` illustrating performance metrics.

![Sample Performance Visualization](sample_chart.png)

---

## How to Run & Test

```bash
# 1. Run unit tests
uv run --frozen pytest domains/sustainability_compliance/agents/extended_producer_responsibility_epr/tests/unit -v

# 2. Run local interactive adk chat
adk run domains/sustainability_compliance/agents/extended_producer_responsibility_epr
```
