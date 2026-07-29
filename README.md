# Retail Enterprise Agents

Google Agent Development Kit (ADK) agents for Gemini Enterprise, organized by retail domain.
Each agent answers business questions by querying BigQuery through the Conversational Analytics
API, supplemented by Google Search grounding for external market context — defined declaratively
in YAML rather than as hand-written orchestration code.

This README covers what the repo is, why it's built the way it is, and how to work in it. The
full architecture rationale (including the decisions this document only summarizes) lives in a
local-only design spec — see [Architecture](#architecture).

---

## What's Built

| No. | Domain | Agent | Gemini Enterprise Display Name | Focus |
| :---: | :---: | :---: | :---: | :---: |
| 1 | Merchandising | [`assortment_planning`](domains/merchandising/agents/assortment_planning/README.md) | Merchandising: Assortment Planning | Product mix, category/SKU performance, assortment width vs. plan |
| 2 | Merchandising | [`pricing_promotions`](domains/merchandising/agents/pricing_promotions/README.md) | Merchandising: Pricing & Promotions | Price elasticity, promo effectiveness, markdown cadence |
| 3 | Merchandising | [`sell_through_inventory_health`](domains/merchandising/agents/sell_through_inventory_health/README.md) | Merchandising: Sell-Through & Inventory Health | Store-level sell-through rates, stock turn, aging inventory breakdown, weeks of supply, markdown triggers |
| 4 | Merchandising | [`vendor_negotiation_rebates`](domains/merchandising/agents/vendor_negotiation_rebates/README.md) | Merchandising: Vendor Negotiation & Rebates | Volume rebate agreement thresholds, YTD spend rebate tier progress, co-op marketing fund commitments/claims, vendor payment terms, net rebate realization % |
| 5 | Supply Chain | [`vendor_performance`](domains/supply_chain/agents/vendor_performance/README.md) | Supply Chain: Vendor Performance | OTIF delivery, vendor scorecards |
| 6 | Supply Chain | [`inventory_planning`](domains/supply_chain/agents/inventory_planning/README.md) | Supply Chain: Inventory Planning | Network-wide inventory position across stores and warehouses, live demand forecasting |
| 7 | Supply Chain | [`logistics_operations`](domains/supply_chain/agents/logistics_operations/README.md) | Supply Chain: Logistics Operations | Carrier performance, transit lane performance, shipment tracking, logistics exceptions |
| 8 | Supply Chain | [`warehouse_dc_operations`](domains/supply_chain/agents/warehouse_dc_operations/README.md) | Supply Chain: Warehouse & DC Operations | Daily DC inbound/outbound shipment throughput, dock turn times, dock-to-stock hours, pick/pack accuracy %, storage pallet capacity utilization |
| 9 | Store Operations | [`labor_productivity`](domains/store_operations/agents/labor_productivity/README.md) | Store Operations: Labor Productivity | Staffing alignment vs. foot traffic, overtime variance, labor cost budgets |
| 10 | Store Operations | [`store_fulfillment_execution`](domains/store_operations/agents/store_fulfillment_execution/README.md) | Store Operations: Store Fulfillment & Execution | BOPIS fulfillment SLAs, curbside pickup wait times, pick/pack accuracy %, fulfillment queue bottlenecks |
| 11 | Store Operations | [`loss_prevention_shrinkage`](domains/store_operations/agents/loss_prevention_shrinkage/README.md) | Store Operations: Loss Prevention & Shrinkage | Monthly store shrinkage rates (%), shrink dollars by cause (theft, damage, admin error, unknown loss), high-risk category losses, register audit exception alerts |
| 12 | Finance | [`gross_margin_profitability`](domains/finance/agents/gross_margin_profitability/README.md) | Finance: Gross Margin & Profitability | Gross margin rates (%), dollar margins, COGS variance, markdown discount erosion |
| 13 | Finance | [`store_pnl_operating_costs`](domains/finance/agents/store_pnl_operating_costs/README.md) | Finance: Store P&L & Operating Costs | Store-level P&L, net sales, gross profit, EBITDA, labor/rent/utilities OpEx variance, profitability targets |
| 14 | Marketing | [`campaign_performance_roi`](domains/marketing/agents/campaign_performance_roi/README.md) | Marketing: Campaign Performance & ROI | Campaign ROAS, channel attribution, CAC targets vs. actuals, conversion lift |
| 15 | Marketing | [`customer_lifecycle_loyalty`](domains/marketing/agents/customer_lifecycle_loyalty/README.md) | Marketing: Customer Lifecycle & Loyalty | Customer Lifetime Value (CLV), RFM segment migration, loyalty tier redemptions, churn risk |

All fifteen are deployed to Vertex AI Agent Engine (dev) and registered with Gemini Enterprise. The

scaffold infrastructure that generates a new logical agent (`_shared/`) is domain-agnostic —
adding a tenth agent, or a sixth domain, is a generator invocation, not new plumbing.

---

## Architecture

Three levels, each with one job:

- **Domain** (`merchandising`, `supply_chain`, ...) — a folder and an ownership boundary. Nothing
  runs at this level.
- **Logical agent** (`assortment_planning`, ...) — the unit of deployment. Each one is packaged,
  deployed to its own Agent Engine resource, and registered independently in Gemini Enterprise —
  a business user picks "Assortment Planning," not a domain-level router.
- **Inside a logical agent** — a thin orchestrator `LlmAgent` delegates to two sub-agents: **Data
  Insights**, which answers questions from BigQuery via the Conversational Analytics API, and
  **Market Context**, which answers external questions via Google Search grounding.

Every logical agent is generated from the same template (`_shared/templates/logical_agent/`) by
`_shared/scripts/scaffold_logical_agent.py`, so structure and conventions stay identical across
agents even as the business content differs.

### Models, Agents, Runtimes and Apps

This repo distinguishes between the models and infrastructure used to *build* the agents and the
models and infrastructure the agents actually *run* on — these are deliberately not the same:

| Layer | Technology | Role |
| :--- | :--- | :--- |
| Design and implementation | Claude Sonnet 5, Gemini 3.5 | AI coding assistants used to design this architecture and implement the agents, scaffolding, and supporting tooling — development-time only, not part of the running system |
| Agent inference | Gemini 2.5 Flash | The model each deployed agent calls at runtime to reason, route between sub-agents, and generate responses |
| Agent framework | Google Agent Development Kit (ADK) | Materializes each logical agent's YAML configuration into a running multi-agent program |
| Agent runtime | Vertex AI Agent Engine (GCP Agent Runtime) | Hosts each deployed agent as a managed, independently scalable service |
| Business-facing UI | Gemini Enterprise | Where end users discover and converse with a registered agent |

---

## Why YAML, and What ADK Provides

ADK's declarative **YAML Agent Config** is the core bet this repo makes: an agent — its model,
instructions, sub-agents, and tools — is data, not a Python program that constructs objects. A
few capabilities that fall out of that, used throughout this repo:

- **Built-in tools referenced by name, no wiring code.** `google_search` for market grounding,
  and BigQuery's `ask_data_insights` (Conversational Analytics — natural-language Q&A over named
  tables), `forecast` (`AI.FORECAST`/TimesFM 2.0), `analyze_contribution`, and `detect_anomalies`
  are all part of ADK's `BigQueryToolset` and drop into a `tools:` list with a name and, where
  needed, arguments — no client-library boilerplate in the common case.
- **Custom tools stay one factory function away.** Not everything fits a declarative arg list —
  `BigQueryToolset` needs a live credentials object, which YAML can't express. ADK's answer is a
  small Python factory function (`tools/bigquery_ca.py`) referenced from YAML by dotted path;
  everything else (instructions, sub-agent wiring, routing) stays pure YAML.
- **The `adk` CLI is the whole local dev loop.** `adk run <agent-folder>` and `adk web
  <agents-dir>` load a YAML-defined agent with zero extra scaffolding — the same `root_agent.yaml`
  that gets deployed is what you run locally.
- **`adk deploy agent_engine` and `agents-cli publish gemini-enterprise`** take that same
  artifact from a laptop to a hosted, registered agent — no separate build step translates YAML
  into something deployable.

None of this is unique to being "AI-generated" — it's what ADK is designed to do. The rest of
this repo is mostly about the parts ADK leaves to you: where instructions live, how data access
is scoped, and how many agents share one BigQuery dataset without colliding.

---

## Design Decisions

| Decision | Rationale |
| :--- | :--- |
| Shared instructions composed at **scaffold time**, not runtime | ADK's YAML has no cross-file include. A runtime loader would work but couples every agent's behavior to one shared file at request time. Baking shared persona/safety text into each agent when it's generated keeps agents self-contained; updating the shared text only affects agents scaffolded afterward — a deliberate trade-off over silent behavior drift in already-deployed agents. |
| **IAM is the real access boundary**, not tool configuration | `ask_data_insights` takes `table_references` from the model at call time — there's no static allowlist in the tool itself. Each agent's actual data scoping comes from its own service account's table-level BigQuery IAM (`_shared/scripts/grant_table_access.py`), not from anything in YAML. |
| **One shared BigQuery dataset** (`retail_ent_agents`), not one per agent | Collisions are prevented structurally: every domain and agent has a fixed 4-letter id (`_shared/table_registry.yaml`), and every table is physically named `<domain_id>_<agent_id>_<table>`. Two agents can use the same logical table name without colliding, and a shared dataset is simpler to operate than N datasets. |
| **Environment fingerprints never committed** — injected at runtime instead | Real GCP project ids, service account emails, and resource names are read from env vars via `before_agent_callback`s (`temp:bq_project_id`) or gitignored deployment files, not hardcoded in YAML. Established after an earlier commit accidentally included a real project id — see git history. |
| Charts via a **custom tool**, not `ask_data_insights` | ADK's Conversational Analytics integration sends a hardcoded instruction forbidding chart generation, with no override. A plain tool function that queries BigQuery, renders with `matplotlib`, and saves via `tool_context.save_artifact()` is the only path to a chart — confirmed to render in the real Gemini Enterprise chat UI. |
| Forecasting calls **`AI.FORECAST` live**, not a precomputed table | ADK's built-in `forecast` tool takes a historical time-series table or query and returns a genuine model-generated forecast. Agents needing this own a real historical table, not a table of pre-baked "future" numbers — and their evals judge forecasts qualitatively ("demand is rising"), never against an exact predicted value. |
| Deploys and registrations are **manual and confirmed**, never scripted end-to-end | IAM/service-account creation, `adk deploy agent_engine`, and `agents-cli publish gemini-enterprise` all require a human running the command, on purpose — this repo doesn't wire CI to deploy or register agents autonomously. |

---

## Trade-offs

**What this approach buys you:**

- A new agent is a generator invocation plus filling in a handful of `# TODO(scaffold):`
  markers, not a bespoke build — subsequent agents take a fraction of the first's effort.
- Business logic (instructions, routing, authorized tables) is readable YAML a non-engineer can
  review, separate from the Python that only exists where YAML genuinely can't reach (tool
  factories, callbacks).
- Table-level IAM plus a structural naming registry means adding an agent can't silently expose
  another agent's data, even though they share one dataset.

**What it costs:**

- YAML Agent Config is still an ADK feature under active development — several classes used here
  (`AgentConfig`, `LlmAgentConfig`) are already marked deprecated upstream in favor of a
  reflection-based loader that doesn't exist yet in the pinned `google-adk` version. This repo
  will need to track that migration.
- Scaffold-time composition means a shared-instruction fix doesn't retroactively reach agents
  already generated — re-scaffolding (or a manual patch) is a real, recurring maintenance action,
  not a one-line config change.
- `ask_data_insights` has no built-in table allowlist, so correct data scoping depends on IAM
  being set up correctly for every agent — a misconfigured service account is a silent data-leak
  risk that YAML review alone won't catch.
- One shared dataset is operationally simpler but means every agent's tables live under one
  BigQuery IAM/quota surface; a noisy-neighbor query-cost or quota problem in one agent is a
  shared-dataset problem, not an isolated one.

---

## Project Structure

```
retail-enterprise-agents/
  domains/
    <domain>/
      agents/
        <logical_agent>/
          root_agent.yaml            # orchestrator LlmAgent — the deployed/registered unit
          sub_agents/
            data_insights.yaml        # BigQuery Conversational Analytics sub-agent
            market_context.yaml       # Google Search grounding sub-agent
          tools/                      # Python: bigquery_ca.py, callbacks.py, chart_generator.py
          eval/*.evalset.json          # ADK semantic/quality evals
          tests/{unit,integration}/    # mocked vs. real-BigQuery tests
          data/*.csv                   # one seed CSV per BigQuery table this agent needs
          deployment/{dev,prod}-example.yaml   # committed placeholders
          deployment/{dev,prod}.yaml            # real values, gitignored like .env
  _shared/
    templates/logical_agent/    # scaffold skeleton, copied+token-substituted per new agent
    instructions/*.md            # shared persona/safety/formatting fragments (scaffold-time only)
    table_registry.yaml          # domain_id/agent_id registry for the shared BigQuery dataset
    scripts/                     # scaffold, load seed data, grant table-level IAM
  tests/tooling/                 # tests for the _shared/scripts tooling itself
```

---

## Getting Started

One-time machine setup, in the order it actually needs to happen:

1. **Install prerequisites**, if you don't already have them:
   - Git
   - Python 3.10+
   - [`uv`](https://docs.astral.sh/uv/getting-started/installation/) — the Python package/env
     manager this repo standardizes on
   - Node.js 18+ and `npm` (only needed for step 4, restoring this repo's agent skills)
   - [Google Cloud CLI](https://cloud.google.com/sdk/docs/install) (`gcloud`, which bundles `bq`)

2. **Clone the repo and `cd` into it.**

3. **Sync Python dependencies.** This also installs the `adk` CLI, since `google-adk` is a
   declared project dependency — no separate ADK install step exists or is needed.

   ```bash
   uv sync
   uv run adk --help   # verify: should print ADK's subcommands (run, web, eval, deploy, ...)
   ```

4. **Restore this repo's agent skills.** `.agents/skills/` is gitignored (machine-local), but
   the exact skill set is pinned in the committed `skills-lock.json` and reproducible from it:

   ```bash
   npx skills experimental_install
   ```

5. **Install the `agents-cli` tool** — used for `agents-cli publish gemini-enterprise`
   (registering a deployed agent with Gemini Enterprise) and the `.agents/skills/google-agents-cli-*`
   skill set:

   ```bash
   uv tool install google-agents-cli
   agents-cli --version   # verify
   ```

6. **Authenticate with Google Cloud** — two separate credentials for two separate purposes, both
   needed:

   ```bash
   gcloud auth login                            # your own identity, for gcloud/bq CLI commands
   gcloud auth application-default login        # Application Default Credentials -- what the
                                                 # agents' own code (google.auth.default()),
                                                 # `uv run adk run`, and tests/integration use
   gcloud config set project <YOUR_DEV_PROJECT_ID>   # ask a maintainer for the dev project id
   ```

After these six steps, `uv run pytest tests/tooling -v` and `uv run adk run
domains/<domain>/agents/<agent>` both work locally. See [Commands
Reference](#commands-reference) below for the day-to-day command reference once you're set up.

---

## Commands Reference

| Task | Command |
| :--- | :--- |
| Install/sync dependencies | `uv sync` |
| Run the tooling test suite | `uv run pytest tests/tooling -v` |
| Run a local agent | `uv run adk run domains/<domain>/agents/<agent>` |
| Browse all agents in a domain | `uv run adk web domains/<domain>/agents` |
| Scaffold a new logical agent | `uv run python _shared/scripts/scaffold_logical_agent.py --domain <domain> --name <snake_case_name> --display-name "<Human Readable Name>"` |
| Load an agent's seed data into BigQuery | `uv run python _shared/scripts/load_agent_data.py --domain <domain> --name <agent> --project <dev_project_id> --dataset retail_ent_agents` |
| Grant an agent's service account table-level access | `uv run python _shared/scripts/grant_table_access.py --project <dev_project_id> --dataset retail_ent_agents --service-account <sa_email> --table <table> [--table <table> ...]` |

After scaffolding, fill in the `# TODO(scaffold):` markers in `root_agent.yaml` and
`sub_agents/data_insights.yaml` (routing guidance and authorized BigQuery tables), register the
new agent in `_shared/table_registry.yaml`, and add its seed data under `data/`. See
`_shared/README.md` for the full walkthrough.

---

## Further Reading & Installed Agent Skills

This repository has **111 agent skills** pinned in [`skills-lock.json`](skills-lock.json) and reproducible via `npx skills experimental_install`:

### Source: `derailed-dash/dazbo-agent-skills` (6 skills)

| Skill Name | Path |
| :--- | :--- |
| `convert-to-devto` | `skills/convert-to-devto/SKILL.md` |
| `create-md-from-browsermcp-snapshot` | `skills/create-md-from-browsermcp-snapshot/SKILL.md` |
| `deploy-skills-in-antigravity` | `skills/deploy-skills-in-antigravity/SKILL.md` |
| `install-gemini-code-review-action` | `skills/install-gemini-code-review-action/SKILL.md` |
| `maintaining-core-documentation` | `skills/maintaining-core-documentation/SKILL.md` |
| `secrets-with-git-crypt` | `skills/secrets-with-git-crypt/SKILL.md` |

### Source: `google/skills` (90 skills)

| Skill Name | Path |
| :--- | :--- |
| `agent-platform-alert-configuration` | `skills/cloud/agent-platform-alert-configuration/SKILL.md` |
| `agent-platform-deploy` | `skills/cloud/agent-platform-deploy/SKILL.md` |
| `agent-platform-endpoint-management` | `skills/cloud/agent-platform-endpoint-management/SKILL.md` |
| `agent-platform-eval-flywheel` | `skills/cloud/agent-platform-eval-flywheel/SKILL.md` |
| `agent-platform-inference` | `skills/cloud/agent-platform-inference/SKILL.md` |
| `agent-platform-migrate-from-ai-studio` | `skills/cloud/agent-platform-migrate-from-ai-studio/SKILL.md` |
| `agent-platform-model-registry` | `skills/cloud/agent-platform-model-registry/SKILL.md` |
| `agent-platform-prompt-management` | `skills/cloud/agent-platform-prompt-management/SKILL.md` |
| `agent-platform-rag-engine-management` | `skills/cloud/agent-platform-rag-engine-management/SKILL.md` |
| `agent-platform-skill-registry` | `skills/cloud/agent-platform-skill-registry/SKILL.md` |
| `agent-platform-tuning` | `skills/cloud/agent-platform-tuning/SKILL.md` |
| `agent-platform-tuning-management` | `skills/cloud/agent-platform-tuning-management/SKILL.md` |
| `alloydb-basics` | `skills/cloud/alloydb-basics/SKILL.md` |
| `bigquery-ai-ml` | `skills/cloud/bigquery-ai-ml/SKILL.md` |
| `bigquery-basics` | `skills/cloud/bigquery-basics/SKILL.md` |
| `bigquery-bigframes` | `skills/cloud/bigquery-bigframes/SKILL.md` |
| `bigtable-basics` | `skills/cloud/bigtable-basics/SKILL.md` |
| `cloud-logging-query-generation` | `skills/cloud/cloud-logging-query-generation/SKILL.md` |
| `cloud-monitoring-metric-selection` | `skills/cloud/cloud-monitoring-metric-selection/SKILL.md` |
| `cloud-run-basics` | `skills/cloud/cloud-run-basics/SKILL.md` |
| `cloud-sql-basics` | `skills/cloud/cloud-sql-basics/SKILL.md` |
| `data-manager-api-audience-ingestion` | `skills/ads/data-manager-api-audience-ingestion/SKILL.md` |
| `data-manager-api-event-ingestion` | `skills/ads/data-manager-api-event-ingestion/SKILL.md` |
| `data-manager-api-setup` | `skills/ads/data-manager-api-setup/SKILL.md` |
| `datalineage-bigquery-asset-impact-analysis` | `skills/cloud/datalineage-bigquery-asset-impact-analysis/SKILL.md` |
| `datalineage-summary` | `skills/cloud/datalineage-summary/SKILL.md` |
| `detection-engineering-coverage-evaluation` | `skills/cloud/detection-engineering-coverage-evaluation/SKILL.md` |
| `firebase-basics` | `skills/cloud/firebase-basics/SKILL.md` |
| `gcloud` | `skills/cloud/gcloud/SKILL.md` |
| `gemini-agents-api` | `skills/cloud/gemini-agents-api/SKILL.md` |
| `gemini-api` | `skills/cloud/gemini-api/SKILL.md` |
| `gemini-interactions-api` | `skills/cloud/gemini-interactions-api/SKILL.md` |
| `gemini-live-api` | `skills/cloud/gemini-live-api/SKILL.md` |
| `gke-ai-troubleshooting-handle-disruption-gpu-tpu` | `skills/cloud/gke-ai-troubleshooting-handle-disruption-gpu-tpu/SKILL.md` |
| `gke-app-onboarding` | `skills/cloud/gke-app-onboarding/SKILL.md` |
| `gke-backup-dr` | `skills/cloud/gke-backup-dr/SKILL.md` |
| `gke-basics` | `skills/cloud/gke-basics/SKILL.md` |
| `gke-batch-hpc` | `skills/cloud/gke-batch-hpc/SKILL.md` |
| `gke-cluster-autoscaler` | `skills/cloud/gke-cluster-autoscaler/SKILL.md` |
| `gke-cluster-creation` | `skills/cloud/gke-cluster-creation/SKILL.md` |
| `gke-compute-classes` | `skills/cloud/gke-compute-classes/SKILL.md` |
| `gke-cost-analysis` | `skills/cloud/gke-cost-analysis/SKILL.md` |
| `gke-cost-optimization` | `skills/cloud/gke-cost-optimization/SKILL.md` |
| `gke-golden-path` | `skills/cloud/gke-golden-path/SKILL.md` |
| `gke-inference` | `skills/cloud/gke-inference/SKILL.md` |
| `gke-multitenancy` | `skills/cloud/gke-multitenancy/SKILL.md` |
| `gke-networking` | `skills/cloud/gke-networking/SKILL.md` |
| `gke-observability` | `skills/cloud/gke-observability/SKILL.md` |
| `gke-platform-security` | `skills/cloud/gke-platform-security/SKILL.md` |
| `gke-productionize` | `skills/cloud/gke-productionize/SKILL.md` |
| `gke-reliability` | `skills/cloud/gke-reliability/SKILL.md` |
| `gke-service-networking` | `skills/cloud/gke-service-networking/SKILL.md` |
| `gke-storage` | `skills/cloud/gke-storage/SKILL.md` |
| `gke-upgrades` | `skills/cloud/gke-upgrades/SKILL.md` |
| `gke-workload-scaling` | `skills/cloud/gke-workload-scaling/SKILL.md` |
| `gke-workload-security` | `skills/cloud/gke-workload-security/SKILL.md` |
| `google-ads-api-account-diagnostics` | `skills/ads/google-ads-api-account-diagnostics/SKILL.md` |
| `google-ads-api-mcp-setup` | `skills/ads/google-ads-api-mcp-setup/SKILL.md` |
| `google-ads-api-quickstart` | `skills/ads/google-ads-api-quickstart/SKILL.md` |
| `google-agents-cli-onboarding` | `skills/cloud/google-agents-cli-onboarding/SKILL.md` |
| `google-analytics-admin-api-basics` | `skills/analytics/google-analytics-admin-api-basics/SKILL.md` |
| `google-analytics-data-api-basics` | `skills/analytics/google-analytics-data-api-basics/SKILL.md` |
| `google-cloud-global-frontend-configuration` | `skills/cloud/google-cloud-global-frontend-configuration/SKILL.md` |
| `google-cloud-networking-observability` | `skills/cloud/google-cloud-networking-observability/SKILL.md` |
| `google-cloud-recipe-auth` | `skills/cloud/google-cloud-recipe-auth/SKILL.md` |
| `google-cloud-recipe-foundation-builder` | `skills/cloud/google-cloud-recipe-foundation-builder/SKILL.md` |
| `google-cloud-recipe-onboarding` | `skills/cloud/google-cloud-recipe-onboarding/SKILL.md` |
| `google-cloud-solution-agentic-ai-bidirectional-streaming` | `skills/cloud/google-cloud-solution-agentic-ai-bidirectional-streaming/SKILL.md` |
| `google-cloud-solution-agentic-ai-borderless-data-lakehouse` | `skills/cloud/google-cloud-solution-agentic-ai-borderless-data-lakehouse/SKILL.md` |
| `google-cloud-solution-agentic-ai-data-science-workflow` | `skills/cloud/google-cloud-solution-agentic-ai-data-science-workflow/SKILL.md` |
| `google-cloud-solution-agentic-analytics-spark-knowledge-catalog` | `skills/cloud/google-cloud-solution-agentic-analytics-spark-knowledge-catalog/SKILL.md` |
| `google-cloud-solution-architecture` | `skills/cloud/google-cloud-solution-architecture/SKILL.md` |
| `google-cloud-solution-build-deploy-agents` | `skills/cloud/google-cloud-solution-build-deploy-agents/SKILL.md` |
| `google-cloud-solution-guided-gke-ai-migration` | `skills/cloud/google-cloud-solution-guided-gke-ai-migration/SKILL.md` |
| `google-cloud-solution-n-tier-serverless-web-app` | `skills/cloud/google-cloud-solution-n-tier-serverless-web-app/SKILL.md` |
| `google-cloud-solution-rag-enterprise-search-gke-sqldb` | `skills/cloud/google-cloud-solution-rag-enterprise-search-gke-sqldb/SKILL.md` |
| `google-cloud-storage-basics` | `skills/cloud/google-cloud-storage-basics/SKILL.md` |
| `google-cloud-waf-cost-optimization` | `skills/cloud/google-cloud-waf-cost-optimization/SKILL.md` |
| `google-cloud-waf-operational-excellence` | `skills/cloud/google-cloud-waf-operational-excellence/SKILL.md` |
| `google-cloud-waf-performance-optimization` | `skills/cloud/google-cloud-waf-performance-optimization/SKILL.md` |
| `google-cloud-waf-reliability` | `skills/cloud/google-cloud-waf-reliability/SKILL.md` |
| `google-cloud-waf-security` | `skills/cloud/google-cloud-waf-security/SKILL.md` |
| `google-cloud-waf-sustainability` | `skills/cloud/google-cloud-waf-sustainability/SKILL.md` |
| `google-mobile-ads-android-migrate-to-next-gen` | `skills/ads/google-mobile-ads-android-migrate-to-next-gen/SKILL.md` |
| `google-mobile-ads-banner` | `skills/ads/google-mobile-ads-banner/SKILL.md` |
| `google-mobile-ads-get-started` | `skills/ads/google-mobile-ads-get-started/SKILL.md` |
| `google-mobile-ads-interstitial` | `skills/ads/google-mobile-ads-interstitial/SKILL.md` |
| `google-mobile-ads-rewarded` | `skills/ads/google-mobile-ads-rewarded/SKILL.md` |
| `ima-sdk-basics` | `skills/ads/ima-sdk-basics/SKILL.md` |
| `workload-manager-basics` | `skills/cloud/workload-manager-basics/SKILL.md` |

### Source: `obra/superpowers` (14 skills)

| Skill Name | Path |
| :--- | :--- |
| `brainstorming` | `skills/brainstorming/SKILL.md` |
| `dispatching-parallel-agents` | `skills/dispatching-parallel-agents/SKILL.md` |
| `executing-plans` | `skills/executing-plans/SKILL.md` |
| `finishing-a-development-branch` | `skills/finishing-a-development-branch/SKILL.md` |
| `receiving-code-review` | `skills/receiving-code-review/SKILL.md` |
| `requesting-code-review` | `skills/requesting-code-review/SKILL.md` |
| `subagent-driven-development` | `skills/subagent-driven-development/SKILL.md` |
| `systematic-debugging` | `skills/systematic-debugging/SKILL.md` |
| `test-driven-development` | `skills/test-driven-development/SKILL.md` |
| `using-git-worktrees` | `skills/using-git-worktrees/SKILL.md` |
| `using-superpowers` | `skills/using-superpowers/SKILL.md` |
| `verification-before-completion` | `skills/verification-before-completion/SKILL.md` |
| `writing-plans` | `skills/writing-plans/SKILL.md` |
| `writing-skills` | `skills/writing-skills/SKILL.md` |

### Source: `vercel-labs/skills` (1 skills)

| Skill Name | Path |
| :--- | :--- |
| `find-skills` | `skills/find-skills/SKILL.md` |

---
## License

Licensed under the [Apache License, Version 2.0](LICENSE).
