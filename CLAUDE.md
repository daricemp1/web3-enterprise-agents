# Retail Enterprise Agents

Google ADK agents for Gemini Enterprise, organized by retail domain (merchandising first, supply
chain added 2026-07-26). Agents are defined declaratively via ADK's YAML Agent Config and answer
business questions by querying BigQuery through the Conversational Analytics API
(`ask_data_insights`), supplemented by Google Search grounding for external market context.

Full architecture rationale lives in
`docs/superpowers/specs/2026-07-25-retail-merchandising-adk-agents-design.md` — read it before
making structural changes; this file is a quick-reference, not a replacement.

**`docs/` is local-only, gitignored (`docs/**`), not shared via git** (decision made 2026-07-26,
final — reversed an earlier decision to track it). Its history contained GCP project/resource
identifiers throughout, and the call was to keep this content local rather than in shared git
history — same treatment as `CLAUDE.md`/`GEMINI.md` themselves. This means `docs/superpowers/`
exists on this machine but will **not** be present on a fresh clone or for anyone else — don't
assume it exists elsewhere, and don't rely on git to distribute it.

## Current state

The scaffolding infrastructure (template, shared instruction fragments, generator script) is
built and is domain-agnostic — creating a new domain is just a new `--domain` value, no new
infra needed. Seven agents are fully built, tested, deployed to Vertex AI Agent Engine (dev), and
registered with Gemini Enterprise:
- **Assortment Planning** (`domains/merchandising/agents/assortment_planning/`, display name
  "Merchandising: Assortment Planning")
- **Pricing & Promotions** (`domains/merchandising/agents/pricing_promotions/`, display name
  "Merchandising: Pricing & Promotions")
- **Vendor Performance** (`domains/supply_chain/agents/vendor_performance/`, display name
  "Supply Chain: Vendor Performance") — the first agent in a new **Supply Chain** domain (added
  2026-07-26). This absorbs what was originally scoped as merchandising's unbuilt "Vendor &
  Supplier Performance" agent, moved into its own domain as a narrower MVP (OTIF delivery +
  vendor scorecards only; cost/margin and chargebacks deferred). Merchandising's remaining
  roadmap item is now just **Sell-Through & Inventory Health**, not yet scaffolded.
- **Inventory Planning** (`domains/supply_chain/agents/inventory_planning/`, display name
  "Supply Chain: Inventory Planning") — second Supply Chain agent (added 2026-07-26). Tracks
  network-wide inventory position across stores AND warehouses (the first agent to introduce a
  warehouse location dimension), and uses ADK's built-in `forecast` tool (BigQuery `AI.FORECAST`)
  live against a real historical demand time series to assess stockout/overstock risk — no
  precomputed forecast table. Deliberately kept distinct from Sell-Through & Inventory Health
  (that remains a separate, still-unbuilt merchandising agent focused on store-level sell-through
  diagnostics, not network inventory position/forecasting).
- **Logistics Operations** (`domains/supply_chain/agents/logistics_operations/`, display name
  "Supply Chain: Logistics Operations") — third Supply Chain agent (added 2026-07-27). Tracks
  carrier performance (on-time delivery rates, delay frequency), transit lane performance,
  shipment tracking, and active logistics exceptions across the supply chain network.
- **Labor Productivity** (`domains/store_operations/agents/labor_productivity/`, display name
  "Store Operations: Labor Productivity") — the first agent in a new **Store Operations** domain
  (added 2026-07-27). Tracks store staffing presence vs. hourly customer foot traffic alignment,
  department overtime variance, and store labor budget metrics.
- **Gross Margin & Profitability** (`domains/finance/agents/gross_margin_profitability/`, display name
  "Finance: Gross Margin & Profitability") — the first agent in a new **Finance** domain
  (added 2026-07-27). Tracks gross margin rates (%), dollar margins by SKU, category, and store,
  COGS variance, markdown discount erosion, and category margin targets.

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
3. **`gcloud` PATH Export**: `agents-cli` calls `gcloud` under the hood. Export `gcloud` to `PATH` before publishing:
   `export PATH=$PATH:/usr/local/google/home/rajanvasagam/Dev/google-cloud-sdk/bin`
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
agent's own `eval/agent.evalset.json` once that's written, never invented** — see the four
existing agents' `README.md` files for the pattern.

## Branching for new agent builds

(Added 2026-07-27.) Building a **new** agent from scratch starts on its own branch, not directly
on `master`:

1. Branch from an up-to-date `master`, named exactly after the agent's snake_case name (matches
   its folder name and the scaffold's `--name` argument) — e.g. `git checkout -b
   sell_through_inventory_health`.
2. Do all build work (scaffold, fill in TODOs, seed data, tests, eval, README) as commits on that
   branch — same granular commit style already used throughout this repo's history.
3. Before merging, the branch must satisfy:
   - The repo's existing test bar: `uv run pytest tests/tooling -v` passes, the new agent's
     `tests/unit` passes, `eval/agent.evalset.json` has real cases (not the scaffold
     placeholder), `README.md`'s TODOs are filled in with Example Questions copied verbatim from
     the eval set, and the agent is registered in `_shared/table_registry.yaml`.
   - A fingerprint/secret scan: no real GCP project ids, service account emails, resource names,
     keys, or credentials anywhere in the branch's commit content *or* commit messages — same
     scan discipline used before this repo's first GitHub push. Scan before any feature branch
     commit, not after.
4. Merge locally into `master`, then push: `git checkout master && git merge <branch>` followed
   by `git push origin master`. No GitHub PR for this.
5. **The merge into local `master` always requires explicit user review and approval first —
   stated explicitly here so it is never skipped, even if the rest of the agent-build process is
   run in a fully autonomous/auto mode.** This is a permanent manual checkpoint, the same way
   IAM/service-account creation and deploy/publish commands are already permanent manual
   checkpoints in this repo's conventions — automation may do everything up to this point, but
   never the merge itself.
6. Multiple new agents built in parallel (e.g. via a subagent/workflow pattern, one feature
   branch per agent): do not merge *any* of the branches until the user has reviewed *all* of
   them. Once reviewed, merge one at a time, in whichever order the user prefers — never merge
   one branch while another is still pending review, and never batch-merge without a per-branch
   review.
7. Delete the branch (local, and remote if it was pushed) after merge.
8. **Scope:** initial build of a *new* agent only. Routine fixes/doc edits to an already-merged
   agent don't need a branch — direct commits to `master` remain fine, as done throughout this
   repo's history so far.

## Key conventions and constraints

- **Every logical agent ships its own `README.md`, templated into the scaffold** (added
  2026-07-27) — covers what the agent answers and how it routes between its two sub-agents, its
  authorized BigQuery tables, real example questions, its tools, and how to run it locally.
  Retrofitted onto the four already-built agents before being added to
  `_shared/templates/logical_agent/`, so every agent scaffolded from now on gets one
  automatically (with `# TODO(scaffold):`-style placeholders, same pattern as `root_agent.yaml`)
  instead of it being a manual step someone could forget.
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
