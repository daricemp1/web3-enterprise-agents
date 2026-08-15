# HR: Frontline Wage & Market Benchmarks

Part of the **Retail Enterprise Agents** platform for Gemini Enterprise.

---

## 1. Why This Agent Matters

### Business Problem
Retailers must navigate rapidly changing municipal and state minimum wage ordinances, market wage compression between new hires and tenured associates, and local competitor hourly pay premiums.

### Target Personas
VP of Total Rewards & Compensation, Retail HR Strategy Lead, Market Compensation Analysts, Regional VPs

### Key Metrics Tracked
| Metric | Benchmark / Target | Business Impact |
| :--- | :--- | :--- |
| **Market Wage Competitiveness Index (P50)** | `Target: >= 102.0% of market P50` | Store entry wage divided by median retail wage benchmark in the local metropolitan statistical area (MSA). |
| **Wage Compression Risk Ratio** | `Target: < 1.15x ratio` | Starting wage of new hire divided by wage of a 2-year tenured associate in the same job classification. |
| **Statutory Minimum Wage Impact Liability ($)** | `Target: Model 100% of upcoming hikes` | Projected annualized payroll cost increase resulting from enacted statutory state/city minimum wage hikes. |
| **Premium Pay Shift Differential Adoption %** | `Target: 100% compliant` | Application of overnight freight and weekend peak shift wage differentials ($1.50 - $2.50/hr). |
| **Annual Compensation Market Adjustment Cadence** | `Target: Semi-annual reviews` | Frequency of geographic pay tier reviews against Bureau of Labor Statistics (BLS) and Mercer retail surveys. |

---

## 2. What It Answers & Sub-Agent Routing

### Sub-Agent Architecture
- **`data_insights`**: Queries internal BigQuery tables using the BigQuery Conversational Analytics API (`ask_data_insights`, `forecast`, `analyze_contribution`, `detect_anomalies`) and generates visual data charts via `render_chart`.
- **`market_context`**: Leverages Google Search grounding for external retail labor market benchmarks, statutory wage/Fair Workweek regulations, BLS statistics, and HR industry standards.
- **`root_agent`**: Orchestrates routing between internal analytics and external market intelligence.

---

## 3. Sample Q&A Showcase

### Example 1: Internal Analytics (Data Insights)
*Question:* "How does our entry-level cashier base wage compare against the local market median (P50) across our top 10 metropolitan areas?"  
*Response:*  
> According to compensation telemetry in BigQuery (`hrwm_fwmb_wage_tiers_by_role`), our entry-level cashier base wages average **103.4% of the local market median (P50)** across our top 10 metropolitan markets. In Seattle ($20.75/hr) and Chicago ($18.50/hr), our starting rates lead local mass retail averages by $0.75/hr, maintaining applicant volume while reducing 90-day turnover.

### Example 2: Market Grounding (Market Context)
*Question:* "What state and municipal minimum wage rate increases are taking effect across the US in 2026 and 2027?"  
*Response:*  
> In 2026, over 22 states and 40 municipalities implemented statutory minimum wage increases, with California reaching $16.50/hr (with $20.00/hr fast-food/hospitality sectors), Washington at $16.66/hr, and New York City at $16.50/hr. Looking ahead to 2027, multiple states have indexed statutory increases tied to CPI-W inflation, requiring proactive payroll modeling to prevent wage compression among tenured department specialists.

### Example 3: Chart Visualization (`sample_chart.png`)
*Question:* "Can you render a chart comparing our store starting wages against regional retail market P50 benchmarks across 6 metropolitan areas?"  
*Generated Visual Artifact:*  
![Sample Chart](sample_chart.png)

---

### 4. Live Multi-Turn Demo Walkthrough (Gemini Enterprise)

Watch the deployed **HR: Frontline Wage & Market Benchmarks** execute a live multi-turn analytical reasoning session in Gemini Enterprise:

> 📺 **Interactive Demo Player**: [Open Full HD Video Player (1080p)](https://rajanm.github.io/retail-enterprise-agents/demos/gemini-enterprise/human_resources/frontline_wage_market_benchmarks.html)  
> 📹 **Direct MP4 Download**: [`frontline_wage_market_benchmarks.mp4`](../../../../demos/gemini-enterprise/human_resources/frontline_wage_market_benchmarks.mp4)

```
Turn 1: Quantitative analysis against BigQuery Conversational Analytics
Turn 2: Grounded real-time external retail search & regulatory synthesis
Turn 3: Visual matplotlib trend chart generation
Turn 4: Interactive executive slide presentation generated in Gemini Enterprise Canvas
```

---

## 4. Authorized BigQuery Tables

- `hrwm_fwmb_wage_tiers_by_role` — Store-level base wage rates, job grade, pay tier (Tier 1 Metro, Tier 2 Suburban, Tier 3 Rural), and tenure differentials.
- `hrwm_fwmb_metro_wage_benchmarks` — External market wage benchmarks by Metropolitan Statistical Area (MSA), 25th, 50th, and 75th percentiles from BLS/Mercer.
- `hrwm_fwmb_minimum_wage_impact_models` — Enacted state and municipal minimum wage rate increases, effective dates, and financial impact models.
- `hrwm_fwmb_wage_compression_index` — Departmental wage compression metrics comparing entry rate vs 1-year, 2-year, and 3-year associate earnings.

---

## 5. Example Questions

1. "How does our entry-level cashier base wage compare against the local market median (P50) across our top 10 metropolitan areas?"
2. "What state and municipal minimum wage rate increases are taking effect across the US in 2026 and 2027?"
3. "What is our projected annual payroll liability resulting from scheduled minimum wage increases in California and Washington?"
4. "Which retail job roles are experiencing high wage compression between new hires and 2-year associates?"
5. "Can you render a chart comparing our store starting wages against regional retail market P50 benchmarks across 6 metropolitan areas?"

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
uv run --frozen pytest domains/human_resources/agents/frontline_wage_market_benchmarks/tests/unit -v

# Run interactively with ADK CLI
adk run domains/human_resources/agents/frontline_wage_market_benchmarks
```
