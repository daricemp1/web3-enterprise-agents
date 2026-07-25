# Seed data for this logical agent

Add one CSV file per BigQuery table this agent's `data_insights` sub-agent needs to reference.
Each file must have a header row; sample rows should be representative enough to answer
realistic questions, not production-scale.

Load these into a dev BigQuery dataset with:

    uv run python _shared/scripts/load_agent_data.py --domain <domain> --name <logical_agent> --dataset <dev_dataset>

(`load_agent_data.py` is built in a later plan — this file documents the convention scaffolded
agents should follow in the meantime. See
docs/superpowers/specs/2026-07-25-retail-merchandising-adk-agents-design.md section 6a.)
