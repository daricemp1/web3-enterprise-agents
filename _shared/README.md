# Shared scaffolding infrastructure

Before scaffolding a **new** agent, create and check out a branch named exactly after it (see
"Starting a new agent: branch first" below):

    git checkout master && git pull
    git checkout -b <snake_case_name>

Then generate the logical agent:

    uv run python _shared/scripts/scaffold_logical_agent.py \
        --domain <domain> --name <snake_case_name> --display-name "<Human Readable Name>"

This copies `_shared/templates/logical_agent/` into
`domains/<domain>/agents/<snake_case_name>/` and substitutes tokens. After scaffolding, fill in
the `# TODO(scaffold):` markers left in `root_agent.yaml` and `sub_agents/data_insights.yaml`
with agent-specific routing guidance and authorized BigQuery table references, then add seed data
under `data/` (see that folder's README). Also fill in the scaffolded `README.md`'s own
placeholders — its routing/data/tools sections mirror the same information, but its **Example
Questions must be copied verbatim from `eval/agent.evalset.json` once that's written**, not
invented ahead of time; see any of the four existing agents' `README.md` for the pattern.

Shared persona/safety/formatting instructions live in `_shared/instructions/*.md` and are
concatenated into every scaffolded agent's instruction text at scaffold time — not at runtime.
Editing them only affects agents scaffolded *after* the edit; already-scaffolded agents must be
regenerated to pick up changes (see
docs/superpowers/specs/2026-07-25-retail-merchandising-adk-agents-design.md section 4 for why —
that file is local-only, gitignored, not on a fresh clone).

## Starting a new agent: branch first

(Added 2026-07-27; full rationale in `CLAUDE.md`'s "Branching for new agent builds".) A new
agent's initial build happens on its own branch, named exactly after the agent, not directly on
`master`. Before merging, the branch needs: the repo's existing test bar passing (`tests/tooling`,
the new agent's `tests/unit`, real eval cases, a filled-in `README.md`, registration in
`_shared/table_registry.yaml`), and a fingerprint/secret scan with no real GCP project ids,
service account emails, resource names, keys, or credentials anywhere in its commits or commit
messages — scanned before any feature branch commit, not after. Merge locally into `master` and
push (no GitHub PR) — but **only after the user has explicitly reviewed and approved the merge**,
even in a fully autonomous/auto run; this is a permanent manual checkpoint, never automated away.
When multiple new agents are built in parallel on separate branches, none of them get merged until
the user has reviewed all of them, then they're merged one at a time in the user's preferred
order — never batch-merged. Delete the branch after merging. This only applies to a new agent's
initial build; routine fixes to an already-merged agent go directly to `master` as before.

## Deploying: display name convention

When running `adk deploy agent_engine --display_name=...` or `agents-cli publish
gemini-enterprise --display-name=...`, prefix the agent's display name with its domain's
`display_name` from `_shared/table_registry.yaml` — e.g. `"Merchandising: Assortment Planning"`
— so agents are grouped/recognizable by domain in the Agent Engine console and Gemini Enterprise
UI. This isn't automated (deploys are manual, confirmed-before-execution); look up the domain's
`display_name` in the registry each time.
