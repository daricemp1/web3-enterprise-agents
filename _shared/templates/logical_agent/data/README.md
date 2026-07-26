# Seed data for this logical agent

Add one CSV file per BigQuery table this agent's `data_insights` sub-agent needs to reference.
Each file must have a header row; sample rows should be representative enough to answer
realistic questions, not production-scale.

**Before adding a table, check `_shared/table_registry.yaml`** — all domain agents share one
BigQuery dataset (`retail_ent_agents`), so table names must be unique across every agent. Add an
entry to that file in the same change that adds a table here.

Load these into the shared dev BigQuery dataset with:

    uv run python _shared/scripts/load_agent_data.py --domain <domain> --name <logical_agent> --project <dev_project_id> --dataset retail_ent_agents

See docs/superpowers/specs/2026-07-25-retail-merchandising-adk-agents-design.md section 6a for
the full rationale (shared dataset, table-level IAM scoping via
`_shared/scripts/grant_table_access.py`).
