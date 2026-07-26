# Seed data for this logical agent

Add one CSV file per BigQuery table this agent's `data_insights` sub-agent needs to reference.
Each file must have a header row; sample rows should be representative enough to answer
realistic questions, not production-scale.

**Before adding a table, register this agent (and this table) in `_shared/table_registry.yaml`.**
All domain agents share one BigQuery dataset (`retail_ent_agents`). Collisions are prevented
structurally: every domain gets a fixed 4-letter `domain_id` (under `domains:`, e.g. `merc`) and
every agent gets a fixed 4-letter `agent_id` (under `agents:`, e.g. `aspl`), and the loader
physically names each table `<domain_id>_<agent_id>_<this_csv's_file_stem>` (e.g.
`merc_aspl_sales_by_sku`) — so it's fine for two agents to each use the same logical CSV name
(e.g. both calling something `sales_by_sku`). List your agent's logical (unprefixed) table names
under its entry in the registry; the loader refuses to load a table that isn't listed there.

Load these into the shared dev BigQuery dataset with:

    uv run python _shared/scripts/load_agent_data.py --domain <domain> --name <logical_agent> --project <dev_project_id> --dataset retail_ent_agents

See docs/superpowers/specs/2026-07-25-retail-merchandising-adk-agents-design.md section 6a for
the full rationale (shared dataset, table-level IAM scoping via
`_shared/scripts/grant_table_access.py`). That file is local-only, gitignored, not on a fresh
clone.
