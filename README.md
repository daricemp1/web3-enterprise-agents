# Retail Enterprise Agents

Google Agent Development Kit (ADK) agents for Gemini Enterprise, organized by retail domain.
Each agent answers business questions by querying BigQuery through the Conversational Analytics
API, supplemented by Google Search grounding for external market context — defined declaratively
in YAML rather than as hand-written orchestration code.

This README covers what the repo is, why it's built the way it is, and how to work in it. The
full architecture rationale (including the decisions this document only summarizes) lives in a
local-only design spec — see [Further Reading](#further-reading).

---

## What's Built

| No. | Domain | Agent | Gemini Enterprise Display Name | Focus |
| :--- | :--- | :--- | :--- | :--- |
| 1 | Merchandising | `assortment_planning` | Merchandising: Assortment Planning | Product mix, category/SKU performance, assortment width vs. plan |
| 2 | Merchandising | `pricing_promotions` | Merchandising: Pricing & Promotions | Price elasticity, promo effectiveness, markdown cadence |
| 3 | Supply Chain | `vendor_performance` | Supply Chain: Vendor Performance | OTIF delivery, vendor scorecards |
| 4 | Supply Chain | `inventory_planning` | Supply Chain: Inventory Planning | Network-wide inventory position across stores and warehouses, live demand forecasting |

All four are deployed to Vertex AI Agent Engine (dev) and registered with Gemini Enterprise. The
scaffolding infrastructure that generates a new logical agent (`_shared/`) is domain-agnostic —
adding a fifth agent, or a third domain, is a generator invocation, not new plumbing.

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
  markers, not a bespoke build — the fourth agent (Inventory Planning) took a fraction of the
  first's effort.
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

## Further Reading

The full architecture spec — YAML composition strategy, BigQuery Conversational Analytics
integration details, deployment/telemetry design, and every decision's complete rationale — lives
in `docs/superpowers/specs/`. That directory is intentionally **local-only** (gitignored, not in
git history): an earlier version of it contained real GCP project/resource identifiers throughout
its history, and the call was to keep this class of content local rather than carry it in shared
git history, the same treatment given to `CLAUDE.md`/`GEMINI.md`'s *content* even though those
files are themselves tracked. It won't exist on a fresh clone — ask whoever owns this repo's
design docs for a copy if you need the full detail behind a decision summarized above.

---

## License

Licensed under the [Apache License, Version 2.0](LICENSE).
