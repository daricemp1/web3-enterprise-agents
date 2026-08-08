# Retail Enterprise Agents

Google ADK agents for Gemini Enterprise, organized by retail domain (merchandising first, supply
chain added 2026-07-26). Agents are defined declaratively via ADK's YAML Agent Config and answer
business questions by querying BigQuery through the Conversational Analytics API
(`ask_data_insights`), supplemented by Google Search grounding for external market context.

Full architecture rationale lives in
`docs/superpowers/specs/2026-07-25-retail-merchandising-adk-agents-design.md` — read it before
making structural changes; this file is a quick-reference, not a replacement.

**`CLAUDE.md`, `GEMINI.md`, and `AGENTS.md` must be kept 100% byte-identical** at all times via `cp CLAUDE.md GEMINI.md && cp CLAUDE.md AGENTS.md && cmp CLAUDE.md GEMINI.md && cmp CLAUDE.md AGENTS.md`. Always update all three in sync whenever project state, conventions, or instructions change.

**`docs/` is local-only, gitignored (`docs/**`), not shared via git** (decision made 2026-07-26,
final — reversed an earlier decision to track it). Its history contained GCP project/resource
identifiers throughout, and the call was to keep this content local rather than in shared git
history. This means `docs/superpowers/` exists on this machine but will **not** be present on a
fresh clone or for anyone else — don't assume it exists elsewhere, and don't rely on git to
distribute it.

## Current state

The scaffolding infrastructure (template, shared instruction fragments, generator script) is
built and is domain-agnostic — creating a new domain is just a new `--domain` value, no new
infra needed. Ninety-one agents are fully built, tested, deployed to Vertex AI Agent Engine (dev), and
registered with Gemini Enterprise:
- **Merchandising Domain (14 of 14 agents complete)** (`domains/merchandising/agents/`):
  - `assortment_planning` ("Merchandising: Assortment Planning")
  - `pricing_promotions` ("Merchandising: Pricing & Promotions")
  - `sell_through_inventory_health` ("Merchandising: Sell-Through & Inventory Health")
  - `vendor_negotiation_rebates` ("Merchandising: Vendor Negotiation & Rebates")
  - `markdown_clearance_optimization` ("Merchandising: Markdown & Clearance Optimization")
  - `price_matching_competitor_intel` ("Merchandising: Price Matching & Competitor Intel")
  - `space_planning_micro_merch` ("Merchandising: Space Planning & Micro-Merchandising", added 2026-08-07)
  - `private_brand_development` ("Merchandising: Private Brand Development", added 2026-08-07)
  - `seasonal_transition_planning` ("Merchandising: Seasonal Transition Planning", added 2026-08-07)
  - `category_growth_strategy` ("Merchandising: Category Growth Strategy", added 2026-08-07)
  - `size_pack_optimization` ("Merchandising: Size & Case Pack Optimization", added 2026-08-07)
  - `item_lifecycle_rationalization` ("Merchandising: Item Lifecycle & SKU Rationalization", added 2026-08-07)
  - `trade_spend_effectiveness` ("Merchandising: Trade Spend & Allowance Effectiveness", added 2026-08-07)
  - `localized_curation_clustering` ("Merchandising: Localized Assortment Clustering", added 2026-08-07)
- **Supply Chain & Logistics Domain (14 of 14 agents complete)** (`domains/supply_chain/agents/`):
  - `vendor_performance` ("Supply Chain: Vendor Performance", added 2026-07-26)
  - `inventory_planning` ("Supply Chain: Inventory Planning", added 2026-07-26)
  - `logistics_operations` ("Supply Chain: Logistics Operations", added 2026-07-27)
  - `warehouse_dc_operations` ("Supply Chain: Warehouse & DC Operations", added 2026-07-28)
  - `returns_reverse_logistics` ("Supply Chain: Returns & Reverse Logistics", added 2026-07-29)
  - `inbound_freight_optimization` ("Supply Chain: Inbound Freight Optimization", added 2026-08-07)
  - `last_mile_delivery_dispatch` ("Supply Chain: Last-Mile Delivery & Dispatch", added 2026-08-07)
  - `cold_chain_temperature_compliance` ("Supply Chain: Cold Chain Temperature Compliance", added 2026-08-07)
  - `multi_echelon_safety_stock` ("Supply Chain: Multi-Echelon Safety Stock", added 2026-08-07)
  - `supplier_risk_resilience` ("Supply Chain: Supplier Risk & Resilience", added 2026-08-07)
  - `cross_dock_flow_through` ("Supply Chain: Cross-Dock & Flow-Through Velocity", added 2026-08-07)
  - `customs_import_tariff_compliance` ("Supply Chain: Customs & Import Tariff Compliance", added 2026-08-07)
  - `dc_automation_robotics_kpis` ("Supply Chain: DC Automation & Robotics KPIs", added 2026-08-07)
  - `packaging_dunnage_optimization` ("Supply Chain: Packaging & Dunnage Optimization", added 2026-08-07)
- **Store Operations Domain (11 of 11 agents complete)** (`domains/store_operations/agents/`):
  - `labor_productivity` ("Store Operations: Labor Productivity", added 2026-07-27)
  - `store_fulfillment_execution` ("Store Operations: Store Fulfillment & Execution", added 2026-07-28)
  - `loss_prevention_shrinkage` ("Store Operations: Loss Prevention & Shrinkage", added 2026-07-28)
  - `visual_merchandising_compliance` ("Store Operations: Planogram & Visual Merchandising Compliance", added 2026-08-07)
  - `energy_facilities_maintenance` ("Store Operations: Store Energy & Facilities Maintenance", added 2026-08-07)
  - `pos_checkout_queue_analytics` ("Store Operations: POS & Checkout Queue Analytics", added 2026-08-07)
  - `store_cash_management_tills` ("Store Operations: Store Cash Management & Till Balancing", added 2026-08-07)
  - `omnichannel_returns_in_store` ("Store Operations: In-Store Omnichannel Returns & BORIS", added 2026-08-07)
  - `store_safety_incident_management` ("Store Operations: Store Safety & Incident Management", added 2026-08-07)
  - `curbside_pickup_speed_accuracy` ("Store Operations: Curbside Pickup Speed & Accuracy", added 2026-08-07)
  - `store_manager_operational_audit` ("Store Operations: Store Manager Operational Audits", added 2026-08-07)
- **Cart & Checkout Analytics** (`domains/e_commerce/agents/cart_checkout_analytics/`, display name
  "E-Commerce: Cart & Checkout Analytics") — first E-Commerce agent (added 2026-07-29). Tracks digital funnel
  conversion rates, checkout stage cart abandonment %, payment gateway decline rates, and promo validation errors.
- **Product Discovery & Analytics** (`domains/e_commerce/agents/search_merchandising_personalization/`, display name
  "E-Commerce: Product Discovery & Analytics") — second E-Commerce agent (added 2026-07-29). Tracks
  digital site search conversion rates, zero-result search query rates, recommendation carousel CTR %, and personalized revenue lift.
- **Finance, Real Estate & Accounting Domain (11 of 11 agents complete)** (`domains/finance/agents/`):
  - `gross_margin_profitability` ("Finance: Gross Margin & Profitability", added 2026-07-27)
  - `store_pnl_operating_costs` ("Finance: Store P&L & Operating Costs", added 2026-07-28)
  - `working_capital_cashflow` ("Finance: Working Capital & Cash Flow", added 2026-07-29)
  - `capex_store_remodel_roi` ("Finance: CapEx & Store Remodel ROI", added 2026-08-08)
  - `corporate_budget_variance_fpna` ("Finance: Corporate Budget Variance & FP&A", added 2026-08-08)
  - `foreign_exchange_landed_costs` ("Finance: FX Exposure & Landed Cost Hedging", added 2026-08-08)
  - `gift_card_breakage_liability` ("Finance: Gift Card Breakage & Liability", added 2026-08-08)
  - `inventory_valuation_provisions` ("Finance: Inventory Valuation & LCM Provisions", added 2026-08-08)
  - `sales_tax_nexus_compliance` ("Finance: Sales Tax Nexus & Jurisdictional Compliance", added 2026-08-08)
  - `store_real_estate_lease_mgmt` ("Finance: Store Real Estate & Lease Management", added 2026-08-08)
  - `vendor_recovery_audit_compliance` ("Finance: Vendor Recovery Audit & Compliance", added 2026-08-08)
- **Marketing & Retail Media Domain (10 of 10 agents complete)** (`domains/marketing/agents/`):
  - `campaign_performance_roi` ("Marketing: Campaign Performance & ROI", added 2026-07-28)
  - `customer_lifecycle_loyalty` ("Marketing: Customer Lifecycle & Loyalty", added 2026-07-28)
  - `retail_media_network_monetization` ("Marketing: Retail Media Network & Sponsored Ad Yield", added 2026-08-08)
  - `customer_churn_winback_analytics` ("Marketing: Churn Prediction & Win-Back Triggers", added 2026-08-08)
  - `email_sms_crm_orchestration` ("Marketing: CRM, Email & SMS Campaign Orchestration", added 2026-08-08)
  - `influencer_creator_campaign_roi` ("Marketing: Influencer & Creator Campaign ROI", added 2026-08-08)
  - `customer_acquisition_cost_cac` ("Marketing: CAC Payback Velocity & Unit Economics", added 2026-08-08)
  - `omnichannel_customer_cdp_insights` ("Marketing: Omnichannel CDP & Customer Identity", added 2026-08-08)
  - `geotargeted_local_marketing` ("Marketing: Geotargeted & Local Store Marketing", added 2026-08-08)
  - `brand_health_social_sentiment` ("Marketing: Brand Health & Social Sentiment", added 2026-08-08)
- **Customer Care & Experience Domain (10 agents)** (`domains/customer_care/agents/`, added 2026-08-07):
  - `contact_center_agent_performance` ("Customer Care: Contact Center Performance & FCR")
  - `wismo_order_tracking_resolution` ("Customer Care: WISMO & Order Inquiries")
  - `voice_of_customer_sentiment_nlp` ("Customer Care: Voice of Customer & NLP Sentiment")
  - `product_warranty_claims_repair` ("Customer Care: Product Warranty & Claims")
  - `ai_chatbot_deflection_handoff` ("Customer Care: AI Bot Containment & Escalations")
  - `vip_clientele_concierge_support` ("Customer Care: VIP & High-CLV Concierge")
  - `returns_appeals_exception_desk` ("Customer Care: Return Exceptions & Appeals")
  - `omnichannel_social_support_desk` ("Customer Care: Social Support & Public Sentiment")
  - `store_associate_support_hotline` ("Customer Care: Store Helpdesk & POS Support")
  - `damaged_goods_claims_resolution` ("Customer Care: Damaged Goods Claims & Recovery")
- **Sustainability, ESG & Compliance Domain (10 agents)** (`domains/sustainability_compliance/agents/`, added 2026-08-07):
  - `carbon_footprint_scope_emissions` ("ESG: Carbon Footprint & Scope Emissions")
  - `food_waste_spoilage_reduction` ("ESG: Food Waste Reduction & Diversion")
  - `sustainable_packaging_circularity` ("ESG: Sustainable Packaging & Circularity")
  - `ethical_sourcing_labor_audits` ("ESG: Ethical Sourcing & Labor Audits")
  - `product_safety_recall_readiness` ("ESG: Product Safety & Recall Execution")
  - `energy_renewable_grid_transition` ("ESG: Renewable Energy & Grid Transition")
  - `water_conservation_facility_audit` ("ESG: Water Conservation & Facility Audits")
  - `chemical_restricted_substances_rsl` ("ESG: Restricted Substances (RSL) & Chemical Safety")
  - `dei_supplier_diversity_spend` ("ESG: Supplier Diversity & Equity Spend")
  - `extended_producer_responsibility_epr` ("ESG: Extended Producer Responsibility (EPR) & Resale")
- **Human Resources & Workforce Management Domain (9 agents)** (`domains/human_resources/agents/`, added 2026-08-07):
  - `store_associate_turnover_retention` ("HR: Store Associate Turnover & Retention")
  - `workforce_scheduling_fairness` ("HR: Scheduling Fairness & Predictive Hours")
  - `training_onboarding_compliance` ("HR: Training & Onboarding Compliance")
  - `workplace_safety_workers_comp` ("HR: Workplace Safety & Workers' Comp")
  - `store_manager_bench_succession` ("HR: Store Leadership Bench & Succession")
  - `seasonal_hiring_peak_readiness` ("HR: Seasonal Hiring & Peak Readiness")
  - `associate_engagement_pulse_enps` ("HR: Associate Pulse & eNPS Analytics")
  - `labor_union_compliance_cba` ("HR: Labor Union & CBA Compliance")
  - `frontline_wage_market_benchmarks` ("HR: Frontline Wage & Market Benchmarks")

### 100-Agent Enterprise Retail Architecture (9 Strategic Domains)

The platform architecture defines a comprehensive footprint of **100 enterprise agents** registered in `_shared/table_registry.yaml` across **9 retail business domains**:
1. **Merchandising (`domain_id: merc`)**: 14 agents (Assortment, Pricing, Sell-Through, Rebates, Clearance, Price Matching, Space Planning, Private Brand, Seasonal, Category Strategy, Size/Pack, Item Lifecycle, Trade Spend, Localized Assortment).
2. **Supply Chain & Logistics (`domain_id: spch`)**: 14 agents (Vendor OTIF, Inventory Planning, Freight/Logistics, DC Operations, Reverse Logistics, Inbound Freight, Last Mile, Cold Chain, Safety Stock, Supplier Risk, Cross-Dock, Customs/Tariff, DC Robotics, Packaging).
3. **Store Operations (`domain_id: stop`)**: 11 agents (Labor Productivity, Store BOPIS, Loss Prevention, Visual Compliance, Facilities/Energy, POS Queues, Till Cash, In-Store Returns, Store Safety, Curbside Pickup, Store Audits).
4. **E-Commerce & Digital (`domain_id: ecom`)**: 11 agents (Cart Checkout, Site Search, Payment Fraud, Marketplace 3P, Mobile App, Web Vitals, PDP Optimization, Subscriptions, Promo Abuse, B2B Portal, SEO/Accessibility).
5. **Marketing & Retail Media (`domain_id: mktg`)**: 10 agents (Campaign ROAS, Customer CLV/Loyalty, Retail Media Network [RMN], Churn Win-Back, CRM/Email/SMS, Influencer ROI, CAC Payback, Omnichannel CDP, Geotargeting, Brand Health).
6. **Finance, Real Estate & Accounting (`domain_id: finc`)**: 11 agents (Gross Margin, Store P&L, Working Capital/Cash Flow, Lease/Real Estate, Remodel ROI, Inventory Valuation, Vendor Recovery Audit, Sales Tax Nexus, FP&A Budget, Gift Card Liability, FX Landed Cost).
7. **Customer Care & Experience (`domain_id: care`)**: 10 agents (Contact Center FCR, WISMO Order Inquiries, NLP VoC Sentiment, Warranty Claims, AI Bot Handoff, VIP Concierge, Return Appeals, Social Support, Store Helpdesk, Damaged Goods).
8. **Human Resources & Workforce (`domain_id: hrwm`)**: 9 agents (Associate Retention, Fair Scheduling, Training Compliance, Workplace Safety/OSHA, Store Leadership Bench, Seasonal Hiring, eNPS Pulse, Labor Union CBA, Frontline Wage Benchmarks).
9. **Sustainability, ESG & Compliance (`domain_id: esgc`)**: 10 agents (Scope 1-3 Carbon, Food Waste, Sustainable Packaging, Ethical Sourcing, Product Recall, Renewable Energy, Water Audits, Chemical RSL, Supplier Diversity, Extended Producer Responsibility).


## Repo layout

```
_shared/
  templates/logical_agent/   # scaffold skeleton, copied+token-substituted per new agent
                              # NOT runnable directly — do not `adk run` against it
  instructions/*.md           # shared persona/safety/formatting fragments, stitched into
                               # templates at SCAFFOLD time, not runtime (see below)
  scripts/
    scaffold_logical_agent.py # generates domains/<domain>/agents/<name>/ from the template
docs/superpowers/    # LOCAL ONLY — gitignored, purged from git history, not on a fresh clone
  specs/     # architecture + per-agent design docs (source of truth for "why")
  plans/     # step-by-step implementation plans for each spec
tests/tooling/  # tests for the _shared/scripts tooling itself
domains/        # one folder per retail domain, created by scaffolding
```

Once agents are scaffolded, each logical agent under `domains/<domain>/agents/<name>/` follows
this shape (see the architecture spec §3/§5 for full rationale):

```
README.md                   # agent-specific overview: what it answers, its data, example questions
root_agent.yaml            # orchestrator LlmAgent — the deployed/registered unit
sub_agents/
  data_insights.yaml        # BigQuery Conversational Analytics sub-agent
  market_context.yaml       # Google Search grounding sub-agent
tools/bigquery_ca.py        # Python factory: create_toolset(args) -> BigQueryToolset
eval/*.evalset.json          # ADK semantic/quality evals
tests/unit/                  # mocked, no network
tests/integration/           # hits real dev BigQuery + auth
data/*.csv                   # one seed CSV per BigQuery table this agent needs
deployment/{dev,prod}-example.yaml  # committed placeholders
deployment/{dev,prod}.yaml           # real values, gitignored like .env — copy from -example
```

## Commands & One-Time Prerequisites

### One-Time Prerequisites & Setup
1. **Python & `uv`**: Python >=3.10. Run `uv sync`. Always execute commands with `uv run --frozen` (e.g. `uv run --frozen pytest tests/tooling -v`) to avoid corporate package index proxy re-resolution errors.
2. **`google-agents-cli` >= 1.2.1**: Pinned tool version required for Gemini Enterprise registration (`--registration-type adk`). Upgrade via `uv tool upgrade google-agents-cli`.
3. **`gcloud` PATH Export**: `agents-cli` calls `gcloud` under the hood. Ensure `gcloud` is in `PATH`:
   `export PATH=$PATH:$HOME/Dev/google-cloud-sdk/bin`
4. **One-Time GCP API Enablement**:
   ```bash
   gcloud services enable \
       geminidataanalytics.googleapis.com \
       aiplatform.googleapis.com \
       discoveryengine.googleapis.com \
       bigquery.googleapis.com \
       --project <project_id>
   ```

### Basic Commands
```bash
uv sync                                    # install/sync dependencies
uv run --frozen pytest tests/tooling -v    # run the tooling test suite

# Starting a new agent's initial build: create its branch first (see "Branching for new
# agent builds" below), then scaffold:
git checkout master && git pull
git checkout -b <snake_case_name>
uv run --frozen python _shared/scripts/scaffold_logical_agent.py \
    --domain <domain> --name <snake_case_name> --display-name "<Human Readable Name>"
```

After scaffolding a new agent, fill in the `# TODO(scaffold):` markers in `root_agent.yaml` and
`sub_agents/data_insights.yaml` (routing guidance and authorized BigQuery tables), then add seed
data under the new agent's `data/` folder. Also fill in the scaffolded `README.md`'s
placeholders — routing summary, authorized-table list, and its tools/run-locally sections update
mechanically from the same information, but **Example Questions must be copied verbatim from the
agent's own `eval/agent.evalset.json` once that's written, never invented**.

## Workspace Isolation via Git Worktrees (`.worktrees/`)

Building a **new** agent from scratch or executing batch feature/migration work uses **Git Worktrees** located in project-local `.worktrees/<name>` (gitignored via `.gitignore`), rather than in-place branch checkouts in the root repository.

**Why Worktrees**:
- **Main repo remains on `master` continuously**: IDE/editor file watchers (VS Code, Jetski) never race against branch checkouts in the root directory, preventing `.git/index.lock` collisions.
- **Parallel & Isolated Development**: Feature batches and parallel subagents work in dedicated isolated directories without dirtying the root workspace.

### Standard Worktree Workflow

1. **Create Worktree**:
   From the clean root repository (on `master`):
   ```bash
   git worktree add .worktrees/<name> -b <name>
   ```
2. **Develop & Test in Worktree**:
   - Perform all edits, scaffolding, configuration updates, and tests inside `.worktrees/<name>/`.
   - Run tests: `cd .worktrees/<name> && uv run --frozen pytest ...`
   - Deploy to Vertex AI Agent Engine (`us-central1`) & publish to Gemini Enterprise.
   - Run live smoke tests and update `README.md` in the worktree.
3. **Pre-Merge Quality & Security Gate**:
   - Before merging, the worktree must satisfy:
     - The repo's test bar: `pytest tests/tooling -v` passes, agent `tests/unit` passes, and evalsets are populated.
     - Live post-deploy verification in Vertex AI Agent Engine (`us-central1`) and Gemini Enterprise.
     - A fingerprint/secret scan: zero real GCP project IDs, service account emails, keys, or credentials in git diff.
4. **Merge Checkpoint & User Review**:
   - **The merge into local `master` always requires explicit user review and approval first.**
   - Present diffs, scan results, and live smoke test outputs to the user.
5. **Merge & Cleanup (from root repository)**:
   ```bash
   # In root repo (which stayed on master the entire time):
   git merge <name>
   git push origin master
   git worktree remove .worktrees/<name>
   git branch -d <name>
   ```
6. **Parallel Agent Builds:** Multiple new agents or domain batches can be built concurrently in parallel across isolated worktrees (`.worktrees/<agent_1>`, `.worktrees/<agent_2>`):
   - Dispatch parallel background subagents (one subagent per worktree).
   - Once reviewed and approved by the user, merge branches sequentially into `master` one at a time, push to `origin/master`, and remove worktrees.

- **Git Execution, Concurrency & Lock Safety** (added 2026-08-06):
  - **Never chain state-changing git commands with `&&`**: Do not run `git checkout master && git merge <branch>` or `git add . && git commit` in a single line. Workspace file watchers and IDE Git extensions (VS Code, Jetski) immediately scan the index when files change on disk, holding `.git/index.lock` for ~50–150ms. Chained commands collide with this active lock and fail (`error: Unable to create '.git/index.lock': File exists`). Always execute state-changing git commands as separate sequential command calls.
  - **Commit Attribution Standard**: Always include the official co-authorship trailer at the bottom of commit messages:
    ```
    Co-authored-by: Google Gemini Code Assist <gemini-code-assist@google.com>
    ```
- **Every logical agent ships its own `README.md`, templated into the scaffold** (added
  2026-07-27, enhanced 2026-07-29) — covers **Why This Agent Matters** (business problem & target personas), **Key Metrics Tracked** (KPI table), what it answers & sub-agent routing, **Sample Q&A Showcase** (3 live post-deploy smoke test responses for BigQuery data, Google Search market grounding, and a generated `sample_chart.png` visual artifact), authorized BigQuery tables, real example questions, tools, and local execution flags. Every scaffolded agent includes these sections via `# TODO(scaffold):` placeholders.
- **ADK Deployment Region and Global Model Inference** (added 2026-08-03):
  - **ADK Deployment Region (`us-central1` only)**: All ADK Agent Engine deployments (`adk deploy agent_engine`) and Gemini Enterprise assistant registrations must target **only `us-central1`** (`--region us-central1`).
  - **Global Model Inference (`gemini-3.5-flash`)**: Agents specify `model: gemini-3.5-flash` in `root_agent.yaml`. Model inference routes to Vertex AI's `global` endpoint via `GOOGLE_CLOUD_LOCATION=global` (set in the agent's `.env` / runtime container), delivering ~30% faster turn latency across analytical and grounding queries while maintaining hosting consolidation in `us-central1`.
- **CLI Command Conventions & Flag Formats** (added 2026-07-29):
  - **PATH Export**: Ensure `gcloud` is in `PATH` via `export PATH=$PATH:$HOME/Dev/google-cloud-sdk/bin`.
  - **`adk deploy agent_engine`**: Deployment flags are passed directly via CLI flags (`--project <project_id> --region us-central1 --display_name "<Name>" --description "<Description>"`), not via `--config`.
  - **`agents-cli publish gemini-enterprise`**: Use `agents-cli publish gemini-enterprise` (not `agents-cli register`). Discover active Gemini Enterprise app IDs in the project via `agents-cli publish gemini-enterprise --list --project <project_id>`.
  - **`grant_table_access.py`**: The `--table` argument uses `action="append"`, requiring repeating `--table <table_1> --table <table_2>` per table.
  - **`load_agent_data.py`**: Requires `--domain <domain> --name <agent_name> --project <project_id> --dataset retail_ent_agents`.
- **Use `uv` for everything** — `uv sync`, `uv run ...`. Never bare `pip`/`python`.
- Python >=3.10 (required by `google-adk`).
- **Scaffold-time composition, not runtime includes.** `_shared/instructions/*.md` are
  concatenated into each agent's instructions when `scaffold_logical_agent.py` runs, not read at
  runtime. Editing a shared instruction fragment only affects agents scaffolded *after* the
  edit — already-scaffolded agents must be regenerated to pick up the change. See spec §4 for why
  a runtime shared-include approach was rejected.
- **Exactly four scaffold tokens, no others:** `__DOMAIN__`, `__LOGICAL_AGENT__`,
  `__DISPLAY_NAME__`, `__SHARED_INSTRUCTIONS__`. `__LOGICAL_AGENT__` is always the snake_case
  folder name.
- **Dotted Python paths in a logical agent's YAML are relative to that agent's own folder**, never
  the repo root (confirmed against ADK's `AgentLoader`, which imports the logical agent folder as
  a top-level module). Only the logical agent's own folder and its `tools/` subfolder get
  `__init__.py` — nothing above it does.
- **Current-date awareness uses a `before_agent_callbacks:` entry, not an instruction hack**
  (added 2026-07-26). YAML `instruction:` only accepts a static string — no dotted-path/callable
  option, unlike `tools:`. `tools/callbacks.py::set_current_date` writes
  `session.state['temp:current_date']`; the shared grounding-rules fragment references it via
  `{temp:current_date}`. **Registered on every agent (root and every sub-agent), not root only**
  (decision revised 2026-07-26) — root-only was assumed sufficient (a single write before any
  `transfer_to_agent`) and worked in direct SDK testing, but broke once queried live through
  Gemini Enterprise: `data_insights` hit `KeyError` even though root's own turns succeeded. The
  callback is cheap and idempotent, so every agent now sets its own copy rather than depending on
  invocation order. Known ADK quirk: this content-less callback's state delta does *not* show up
  via `get_session()` afterward, even though it's correctly visible live to every agent's
  instruction within the same turn — don't write a test asserting on `get_session()` state for
  this; a real response existing at all already proves it worked (a missing key raises `KeyError`
  during instruction rendering, failing the whole turn).
- **The dev BigQuery project id in `data_insights.yaml`'s authorized-table list is also injected
  via a `before_agent_callback`, not hardcoded** (decision revised 2026-07-26 — originally a
  literal `project.dataset.table` string). `tools/callbacks.py::set_bigquery_project` reads
  `BIGQUERY_PROJECT_ID` and writes `session.state['temp:bq_project_id']`; the instruction
  references it via `{temp:bq_project_id}.dataset.table`. Registered directly on
  `data_insights.yaml` only (the only agent whose instruction needs it) rather than depending on
  another agent's callback having run first, for the same reason as the current-date callback
  above. `BIGQUERY_PROJECT_ID` is already deployed as a real runtime env var on the Agent Engine
  resource — `adk deploy agent_engine` reads the agent folder's `.env` at deploy time and sets it
  on the deployed resource automatically; no new deployment plumbing was needed. Dataset name
  (`retail_ent_agents`) and table names (`merc_aspl_*`) stay as committed literal text — they're
  not environment fingerprints, just the shared-dataset naming convention; only the project id
  itself was being committed as one.
- **IAM is the real access boundary, not tool config.** `ask_data_insights` takes
  `table_references` from the LLM at call time; there's no static table allowlist in the tool.
  Each logical agent's actual data scoping comes from its dedicated service account's BigQuery
  IAM, not from anything in YAML. The authorized-table list in a `data_insights.yaml` instruction
  is a UX/accuracy aid only.
- **Service Account & Dataset IAM Requirements for Conversational Analytics (`ask_data_insights`):**
  Per-agent table access is granted via `_shared/scripts/grant_table_access.py`. However, BigQuery
  Conversational Analytics (`geminidataanalytics.googleapis.com`) requires additional permissions:
  1. **Dataset READER access**: Every agent service account AND the Reasoning Engine Execution Service
     Agent (`service-<project_number>@gcp-sa-aiplatform-re.iam.gserviceaccount.com`) must have dataset-level
     `READER` (`roles/bigquery.dataViewer`) permission on `retail_ent_agents` to inspect table metadata.
  2. **Project IAM Roles**: Every agent service account AND the Reasoning Engine Service Agent must have:
     - `roles/geminidataanalytics.dataAgentStatelessUser` (or `roles/geminidataanalytics.dataAgentUser`)
     - `roles/bigquery.jobUser`
     - `roles/aiplatform.user`
- **Use `uv run --frozen` uniformly**: Running bare `uv run` attempts dependency re-resolution against
  the corporate package index proxy, which fails. Always use `uv run --frozen` for all `pytest`, `adk`, and python script execution.
- **Credentials:** resolve via `google.auth.default()` uniformly in tool code (e.g.
  `tools/bigquery_ca.py`) — this is Application Default Credentials locally and the deployed Agent
  Engine service account in production. Don't branch this logic by environment name.
- **Charts/visualizations are possible via a custom tool, confirmed working in Gemini Enterprise
  (added 2026-07-26).** ADK's built-in `ask_data_insights` can never produce a chart — ADK itself
  sends a hardcoded system instruction to the Conversational Analytics API forbidding charts, with
  no config override (confirmed against ADK source). ADK's YAML Agent Config also has no
  `code_executor` field and no `built_in_code_execution` tool name, so the code-execution pattern
  Google's own `adk-samples` "data-science" agent uses isn't reachable from YAML either. The
  working approach: a plain custom Python tool function (`tools/chart_generator.py::render_chart`,
  same dotted-path-from-YAML `tools:` pattern as `bigquery_ca.py`/`callbacks.py` — no YAML
  structural change) that queries BigQuery directly, renders a chart with `matplotlib`, and saves
  it via ADK's documented `tool_context.save_artifact()`. Confirmed end-to-end on Assortment
  Planning: the artifact mechanism fires correctly (`actions.artifact_delta`) and — this was
  genuinely unconfirmed going in, given contradictory public reports — **the resulting image does
  render in the real Gemini Enterprise chat UI.** The tool must catch BigQuery query exceptions
  and return a structured error dict rather than letting them propagate — otherwise a bad
  LLM-generated SQL query (e.g. a guessed wrong column name) crashes the whole turn instead of
  letting the LLM see the error and retry with corrected SQL (confirmed via a real smoke test).
  Generalized into `_shared/templates/logical_agent/` as well, so every future agent gets this
  capability by default.
- **Demand forecasting uses ADK's built-in `forecast` tool live, not a precomputed table
  (established 2026-07-26 by Inventory Planning).** `forecast` (already in every agent's
  `tool_filter` inherited from the template, alongside `ask_data_insights`,
  `analyze_contribution`, `detect_anomalies`) wraps BigQuery's `AI.FORECAST` (TimesFM 2.0) —
  confirmed by reading the installed ADK source
  (`google/adk/integrations/bigquery/query_tool.py`). It takes a historical time-series table *or
  SQL query* as `history_data`, plus `timestamp_col`/`data_col` (and optional `id_cols` for
  multiple series) and a `horizon`, returning genuine AI-forecasted future values. This means an
  agent doing demand forecasting needs a real historical time-series table (e.g. daily units by
  SKU/store) in its data model, not a precomputed table of fabricated future numbers — the
  instruction must teach the LLM to pass a *filtered* SQL query as `history_data` (scoped to the
  specific SKU/store in question), not a bare table id, when the table holds multiple series
  mixed together. Since the tool's exact output isn't something seed-data generation controls
  (only the input historical trend is engineered), eval content for forecast-driven agents should
  be qualitative/directional ("demand is rising," "at risk of stocking out"), never asserting an
  exact forecasted number — same convention Assortment Planning's trend-based eval cases already
  use.
- **`deployment/dev.yaml`/`prod.yaml` are gitignored, like `.env`** (decision made 2026-07-26) —
  they hold live deployment identifiers (service account email, Agent Engine resource name,
  staging bucket, Agentspace app id). Copy the committed `dev-example.yaml`/`prod-example.yaml`
  and fill in real values, same pattern as `.env.example` → `.env`. This is *not* the same
  category as `sub_agents/data_insights.yaml`'s dataset/table name references — those are
  committed because they're required agent instruction content, not a deployment credential. The
  project id portion of those same references, however, *is* treated like a deployment
  identifier — it's injected dynamically (see the `set_bigquery_project` bullet above), not
  committed as a literal string, since a real GCP project id is an environment fingerprint the
  same way the service account email and Agent Engine resource name are.
- **Each logical agent owns synthetic seed data** under `data/*.csv` (one file per table), loaded
  into a **shared** dev dataset via `_shared/scripts/load_agent_data.py` (uses
  `google-cloud-bigquery`, not the `bq` CLI). Anything requiring live BigQuery access must skip
  gracefully when unconfigured, never fail CI. Assortment Planning's three tables are real, live
  tables in the dev project (not just planned) — see the table-naming decision below.
- **One shared BigQuery dataset for all domain agents: `retail_ent_agents`** (decision revised
  2026-07-26 — not a per-agent dataset; naming scheme revised again 2026-07-26 — see below).
  Collisions are prevented structurally, not just by convention: every **domain** gets a fixed
  4-lowercase-letter `domain_id` and every **agent** gets a fixed 4-lowercase-letter `agent_id`,
  recorded in `_shared/table_registry.yaml`'s `domains:` and `agents:` sections respectively (e.g.
  `merchandising` → `merc`, `assortment_planning` → `aspl`), and `load_agent_data.py` physically
  names every table `<domain_id>_<agent_id>_<csv_file_stem>` (e.g. `merc_aspl_product_catalog`) —
  two agents can use the same logical CSV name without colliding. Originally a single free-length
  (2-4 char) `agent_id` with no domain component (e.g. `assortment_planning` → `ap`); revised to
  this fixed domain_id+agent_id form for readability/organization as more domains and agents are
  added to the shared dataset. `agent_id` must still be unique across the *entire* registry, and
  `domain_id` unique across all domains (both enforced by `tests/tooling/test_table_registry.py`);
  register a new agent/table there before adding its `data/*.csv` file.
- **Dev-only scope for now (confirmed 2026-07-26).** Only the `dev` environment is being
  implemented. Don't build `prod` deployment, a prod BigQuery dataset, or prod-specific agent
  instructions until this is explicitly revisited — see architecture spec §10. Templates still
  scaffold a `deployment/prod.yaml` stub for structural consistency; that's not an implementation
  signal.
- **Agent Engine deployment + Gemini Enterprise registration are in scope for `dev`** (decision
  revised 2026-07-26 — originally deferred to a later "Plan 3"). Use ADK's own `adk deploy
  agent_engine` for deployment; use `agents-cli publish gemini-enterprise` narrowly for
  registration only (ADK has no native command for this, and it's the one tool actually built for
  it) — don't adopt the rest of the `agents-cli` toolchain, which would conflict with this repo's
  own scaffold/eval/deploy tooling. IAM/service-account creation and the deploy/publish commands
  themselves need explicit human confirmation before execution, never run autonomously.
- **Agent Engine and Gemini Enterprise display names & descriptions** (added 2026-07-26, expanded 2026-07-27):
  Prefix display names with domain: `"<domain display_name>: <agent display name>"`, e.g. `"Merchandising:
  Assortment Planning"`, `"Supply Chain: Logistics Operations"`. Always pass `--display_name` and `--description`
  to `adk deploy agent_engine`, and `--display-name`, `--description`, and `--tool-description` to
  `agents-cli publish gemini-enterprise`. Export `gcloud` to `PATH` prior to `agents-cli` calls
  (`export PATH=$PATH:/usr/local/google/home/rajanvasagam/Dev/google-cloud-sdk/bin`). Re-running deployment
  with `--agent_engine_id` / publishing with `--agent-runtime-id` updates existing resources in place.
- **Post-Deploy Live Smoke Testing Signature (google-adk 2.5.0):**
  When testing deployed Agent Engine instances via Python SDK `vertexai.agent_engines`:
  `create_session(user_id='...')` requires a mandatory `user_id` and returns a dict (`session['id']`),
  and `stream_query` requires `message='...'` (not `query='...'`) and `user_id='...'`.
- **v1 merchandising agents: originally 4, not 5 (confirmed 2026-07-26).** The proposed 5th
  "Merchandise Financial Performance" agent is not being built — see architecture spec §9/§10.
  **Decision revised 2026-07-26 (again): "Vendor & Supplier Performance" moved out of
  merchandising into its own new domain, Supply Chain, as a narrower MVP called "Vendor
  Performance"** (OTIF delivery + vendor scorecards only, cost/margin and chargebacks deferred).
  Merchandising's remaining unbuilt roadmap item is now just Sell-Through & Inventory Health.
- **Cross-agent seed-data guidelines: reuse identifiers, align date windows (added 2026-07-26).**
  When a new agent's data references an entity another agent already established (e.g. a SKU),
  reuse that agent's exact identifier values rather than inventing new ones; and anchor synthetic
  date-based data to the same real-world timeline other agents already use (same `WINDOW_END`
  -style constant, overlapping historical windows), not an arbitrary independent date range. This
  is on top of the existing self-containment rule (agents' tables stay physically independent
  even when content is duplicated) — see `_shared/table_registry.yaml`'s header comment and
  `_shared/templates/logical_agent/data/README.md` for the canonical wording. First exercised by
  Vendor Performance, which reuses Assortment Planning/Pricing & Promotions' SKU-001..006 ids and
  2026-07-24 date anchor. Also watch for accidental name collisions this can create — Vendor
  Performance's seed data originally named a vendor after a product brand it didn't fully supply,
  which caused the LLM to infer a wrong vendor-product relationship from name similarity instead
  of joining on the actual foreign keys; fixed by renaming the vendor and adding an explicit
  instruction to always join on IDs, never infer from name/brand similarity.
- **Testing split:** `tests/unit` is mocked/no-network and runs on every PR; `tests/integration`
  hits real dev BigQuery and is gated (pre-deploy/nightly, not every PR); `eval/` judges response
  *quality*, distinct from `tests/*` correctness checks; `tests/tooling` tests the shared scripts
  themselves.
- Design docs record decisions and rejected alternatives deliberately — when a spec explains why
  an approach was *not* taken, don't silently reintroduce it.

## Where to look for more

- `_shared/README.md` — scaffolding usage
- `docs/superpowers/specs/2026-07-25-retail-merchandising-adk-agents-design.md` — full
  architecture (topology, YAML composition strategy, BigQuery CA integration, deployment,
  telemetry). **Local only** (gitignored, not in git history) — exists on this machine but not on
  a fresh clone.
- `docs/superpowers/specs/2026-07-25-assortment-planning-agent-design.md` — first concrete agent's
  data/content design. **Local only**, same caveat.
- `docs/superpowers/specs/2026-07-26-pricing-promotions-agent-design.md` — second concrete agent's
  data/content design ("Plan 5"). **Local only**, same caveat.
- `docs/superpowers/plans/` — implementation plans matching the specs above. **Local only**, same
  caveat.
