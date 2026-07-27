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

## Deploying: IAM setup & display name convention

### IAM Requirements
When creating a dedicated service account for a new agent (e.g., `<agent_name>-dev@<project_id>.iam.gserviceaccount.com`):
1. **Table Access**: Run `_shared/scripts/grant_table_access.py` to grant table-level `roles/bigquery.dataViewer` permissions.
2. **Dataset Reader Access**: Grant dataset-level `READER` (`roles/bigquery.dataViewer`) permission on `retail_ent_agents` to both the agent service account AND the Reasoning Engine Execution Service Agent (`service-<project_number>@gcp-sa-aiplatform-re.iam.gserviceaccount.com`).
3. **Project IAM Roles**: Grant the following project-level IAM roles to both service accounts:
   - `roles/geminidataanalytics.dataAgentStatelessUser` (or `roles/geminidataanalytics.dataAgentUser`)
   - `roles/bigquery.jobUser`
   - `roles/aiplatform.user`

### Deployment & Registration Commands
Prefix display names with the domain's `display_name` from `_shared/table_registry.yaml` (e.g., `"Supply Chain: Logistics Operations"`):

```bash
# 1. Deploy to Agent Engine
uv run --frozen adk deploy agent_engine \
    domains/<domain>/agents/<agent_name> \
    --project <project_id> \
    --region <region> \
    --agent_engine_id <optional_existing_id> \
    --display_name "<Domain Display Name>: <Agent Display Name>" \
    --description "<Full Agent Description>"

# 2. Register to Gemini Enterprise
export PATH=$PATH:/usr/local/google/home/rajanvasagam/Dev/google-cloud-sdk/bin
uv run --frozen agents-cli publish gemini-enterprise \
    --registration-type adk \
    --agent-runtime-id projects/<project_number>/locations/<region>/reasoningEngines/<agent_engine_id> \
    --gemini-enterprise-app-id projects/<project_number>/locations/global/collections/default_collection/engines/<app_id> \
    --display-name "<Domain Display Name>: <Agent Display Name>" \
    --description "<Full Agent Description>" \
    --tool-description "<Full Agent Description>"
```

### Post-Deploy Testing
Test deployed Agent Engine instances using the Python SDK (`vertexai.agent_engines`):

```python
import vertexai
from vertexai.agent_engines import get

vertexai.init(project='<project_id>', location='<region>')
agent = get('projects/<project_number>/locations/<region>/reasoningEngines/<agent_engine_id>')
session = agent.create_session(user_id='test_user')
session_id = session.get('id') if isinstance(session, dict) else session.session_id

for response in agent.stream_query(
    session_id=session_id,
    message='<your_test_question>',
    user_id='test_user'
):
    print(response)
```

