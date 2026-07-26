# Shared scaffolding infrastructure

Generate a new logical agent:

    uv run python _shared/scripts/scaffold_logical_agent.py \
        --domain <domain> --name <snake_case_name> --display-name "<Human Readable Name>"

This copies `_shared/templates/logical_agent/` into
`domains/<domain>/agents/<snake_case_name>/` and substitutes tokens. After scaffolding, fill in
the two `# TODO(scaffold):` markers left in `root_agent.yaml` and
`sub_agents/data_insights.yaml` with agent-specific routing guidance and authorized BigQuery
table references, then add seed data under `data/` (see that folder's README).

Shared persona/safety/formatting instructions live in `_shared/instructions/*.md` and are
concatenated into every scaffolded agent's instruction text at scaffold time — not at runtime.
Editing them only affects agents scaffolded *after* the edit; already-scaffolded agents must be
regenerated to pick up changes (see
docs/superpowers/specs/2026-07-25-retail-merchandising-adk-agents-design.md section 4 for why —
that file is local-only, gitignored, not on a fresh clone).

## Deploying: display name convention

When running `adk deploy agent_engine --display_name=...` or `agents-cli publish
gemini-enterprise --display-name=...`, prefix the agent's display name with its domain's
`display_name` from `_shared/table_registry.yaml` — e.g. `"Merchandising: Assortment Planning"`
— so agents are grouped/recognizable by domain in the Agent Engine console and Gemini Enterprise
UI. This isn't automated (deploys are manual, confirmed-before-execution); look up the domain's
`display_name` in the registry each time.
