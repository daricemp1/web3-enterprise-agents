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
placeholders — including its **Why This Agent Matters** business problem and personas, **Key Metrics Tracked** table,
and **Sample Q&A Showcase** capturing 3 live post-deploy smoke test responses (BigQuery data, Google Search market grounding, and a generated `sample_chart.png` visual artifact). Its **Example Questions must be copied verbatim from `eval/agent.evalset.json` once that's written**, not
invented ahead of time; see any of the existing agents' `README.md` for the pattern.

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
1. **Table Access**: Run `_shared/scripts/grant_table_access.py` (repeating `--table` per table) to grant table-level `roles/bigquery.dataViewer` permissions:
   ```bash
   uv run --frozen python _shared/scripts/grant_table_access.py \
       --project <project_id> --dataset retail_ent_agents \
       --service-account <service_account_email> \
       --table <table_1> --table <table_2>
   ```
2. **Dataset Reader Access**: Grant dataset-level `READER` (`roles/bigquery.dataViewer`) permission on `retail_ent_agents` to both the agent service account AND the Reasoning Engine Execution Service Agent (`service-<project_number>@gcp-sa-aiplatform-re.iam.gserviceaccount.com`).
3. **Project IAM Roles**: Grant the following project-level IAM roles to both service accounts:
   - `roles/geminidataanalytics.dataAgentStatelessUser` (or `roles/geminidataanalytics.dataAgentUser`)
   - `roles/bigquery.jobUser`
   - `roles/aiplatform.user`

### Deployment & Registration Commands
All ADK Agent Engine deployments must target **only `us-central1`** (`--region us-central1`), while model inference uses `gemini-3.5-flash` via the `global` Vertex AI endpoint (`GOOGLE_CLOUD_LOCATION=global` in the agent's `.env`). Prefix display names with the domain's `display_name` from `_shared/table_registry.yaml` (e.g., `"Supply Chain: Logistics Operations"`):

```bash
# 1. Deploy to Agent Engine (us-central1 only)
export PATH=$PATH:$HOME/Dev/google-cloud-sdk/bin
uv run --frozen adk deploy agent_engine \
    --project <project_id> \
    --region us-central1 \
    --display_name "<Domain Display Name>: <Agent Display Name>" \
    --description "<Full Agent Description>" \
    domains/<domain>/agents/<agent_name>

# 2. Discover active Gemini Enterprise Apps in Project
uv run --frozen agents-cli publish gemini-enterprise --list --project <project_id>

# 3. Register to Gemini Enterprise (us-central1 runtime)
uv run --frozen agents-cli publish gemini-enterprise \
    --registration-type adk \
    --agent-runtime-id projects/<project_number>/locations/us-central1/reasoningEngines/<agent_engine_id> \
    --gemini-enterprise-app-id projects/<project_number>/locations/global/collections/default_collection/engines/<app_id> \
    --display-name "<Domain Display Name>: <Agent Display Name>" \
    --description "<Full Agent Description>" \
    --project <project_id>
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

---

## Recording Agent Demos: Playwright + FFmpeg Pipeline

`_shared/scripts/record_agent_demo.py` automates end-to-end multi-turn video recording of registered Gemini Enterprise assistants:

* **Browser Automation & Screen Capture**: Powered by **Playwright** (`playwright.chromium`), driving Google Chrome with persistent authenticated profiles, 1.25x high-DPI viewport scaling, and real-time screen capture.
* **Prompt Discovery**: Automatically extracts the 3 curated business prompts from the target agent's `README.md` via `_shared/scripts/prompt_parser.py`.
* **Agent @Mention Selection**: Automatically focuses the prompt input bar, types `@<agent_keyword>`, and selects the agent card above the prompt box.
* **Stop-to-Action Response Synchronization**: Uses a 4-phase async state machine monitoring the prompt submission button lifecycle (**Stop $\to$ Action transition**), ensuring BigQuery SQL generation, data retrieval, and LLM streaming are 100% finished before initiating subsequent turns.
* **Dynamic Canvas Executive Presentation Creation**: Activates Canvas mode from the Tools menu and submits a tailored, agent-specific executive presentation prompt passed dynamically by default across all runs (`"Create a 4-slide executive presentation summarizing the <Agent Title> analysis and recommendations above."`), with support for custom `--canvas-prompt` CLI overrides.
* **Bottom Slide Thumbnail Rail Navigation**: Automatically expands the Canvas split stage and navigates sequentially across all 4 generated slides via calibrated bottom thumbnail coordinates at $Y=995$ with smooth cursor gliding (`steps=15`), hover states, and 2.5s pacing per slide.
* **Full Conversation History Scroll Walkthrough**: After all responses and Canvas slides render, smoothly scrolls the left conversation pane up to Turn 1 (pausing 3.0s at top to showcase the pinned agent pill and initial BigQuery response) and smoothly down through all turns and chart artifacts.
* **1080p MP4 Video Transcoding**: Transcoded via **FFmpeg** (`ffmpeg -c:v libx264 -crf 22 -preset medium -movflags +faststart`) to produce web-optimized Full HD video files under `demos/gemini-enterprise/<domain>/<agent_name>.mp4`.
* **Automated HTML Showcase Player Generation**: Auto-generates a standalone responsive dark-mode HTML5 video player at `demos/gemini-enterprise/<domain>/<agent_name>.html` complete with metadata grid, multi-turn flow summary, and GitHub links.

---

### Commands & Options

```bash
# 1. Initialize environment configuration from template
cp .env.example .env
# Set GEMINI_ENTERPRISE_URL and Chrome Profile settings in .env

# 2. Record a single agent demo (1080p MP4 + HTML player)
uv run --frozen python _shared/scripts/record_agent_demo.py \
    --domain e_commerce \
    --name cart_checkout_analytics \
    --speed normal \
    --format mp4

# 3. Custom Canvas presentation prompt override (optional)
uv run --frozen python _shared/scripts/record_agent_demo.py \
    --name assortment_planning \
    --canvas-prompt "Create a 4-slide executive presentation summarizing our top revenue drivers."

# 4. Record all agents in a domain
uv run --frozen python _shared/scripts/record_agent_demo.py --domain merchandising --all

# 5. Dry-run prompt parsing validation (no browser launched)
uv run --frozen python _shared/scripts/record_agent_demo.py --name cart_checkout_analytics --dry-run
```

---

## Parallel Recording & Chrome Profile Isolation

Chromium places an exclusive filesystem lock (`SingletonLock`) on its user data directory. To record 2 or more agent demos concurrently in parallel, provide dedicated user data directories via `--user-data-dir` or the `CHROME_USER_DATA_DIR` environment variable:

```bash
# Worker 1 (in background task / terminal 1):
uv run --frozen python _shared/scripts/record_agent_demo.py \
    --name assortment_planning \
    --user-data-dir ~/.config/google-chrome-demo-recorder-worker-1 &

# Worker 2 (in background task / terminal 2):
uv run --frozen python _shared/scripts/record_agent_demo.py \
    --name pricing_promotions \
    --user-data-dir ~/.config/google-chrome-demo-recorder-worker-2 &
```

The script automatically synchronizes authentication cookies from the base master profile (`~/.config/google-chrome-demo-recorder`) into the target worker directory while excluding active runtime locks (`Singleton*`, `*lock*`, `Crashpad`).

---

## Standalone HTML Demo Video Showcase Player

Every recorded demo includes a self-contained HTML5 web player generated via `_shared/scripts/generate_demo_html.py`:

```bash
# Generate HTML player for a specific agent
uv run --frozen python _shared/scripts/generate_demo_html.py --name cart_checkout_analytics

# Generate HTML players for an entire domain
uv run --frozen python _shared/scripts/generate_demo_html.py --domain merchandising --all
```

### Standard Cross-Linking Convention

When a demo video and HTML player are published, link them across documentation as follows:

1. **Root `README.md` (in domain agent tables)**:
   ```markdown
   | 1 | [`cart_checkout_analytics`](domains/e_commerce/agents/cart_checkout_analytics/README.md) (<a href="https://rajanm.github.io/retail-enterprise-agents/demos/gemini-enterprise/e_commerce/cart_checkout_analytics.html" target="_blank" rel="noopener noreferrer">🎬 Demo ↗</a>) | E-Commerce: Cart & Checkout Analytics | ... |
   ```

2. **Individual Agent `README.md` (under `## Sample Q&A Showcase`)**:
   ```markdown
   > 🎬 **Interactive Video Walkthrough:** <a href="https://rajanm.github.io/retail-enterprise-agents/demos/gemini-enterprise/e_commerce/cart_checkout_analytics.html" target="_blank" rel="noopener noreferrer">Watch 1080p Web Player Demo ↗</a>
   ```


