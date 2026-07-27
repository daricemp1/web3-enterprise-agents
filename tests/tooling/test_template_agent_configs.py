"""Static checks on the real agent-config template files. These are independent
of the scaffold engine (tested in test_scaffold_logical_agent.py against a
synthetic fixture) and of full end-to-end scaffolding
(test_scaffold_template_integration.py, Task 6) — this task only verifies the
template's own YAML/JSON content is well-formed and shaped correctly.
"""
import json
from pathlib import Path

import yaml

TEMPLATE_DIR = Path(__file__).resolve().parents[2] / "_shared" / "templates" / "logical_agent"


def test_root_agent_yaml_is_valid_yaml_with_expected_shape():
    raw = yaml.safe_load((TEMPLATE_DIR / "root_agent.yaml").read_text())
    assert raw["agent_class"] == "LlmAgent"
    assert "__SHARED_INSTRUCTIONS__" in raw["instruction"]
    sub_agent_paths = {sa["config_path"] for sa in raw["sub_agents"]}
    assert sub_agent_paths == {
        "sub_agents/data_insights.yaml",
        "sub_agents/market_context.yaml",
    }


def test_root_agent_yaml_sets_an_explicit_model():
    # Without this, ADK's LlmAgent falls back to its own built-in DEFAULT_MODEL, which is not
    # guaranteed to be an available publisher model in every project/region (confirmed: Assortment
    # Planning's integration test 404'd against that default in the dev project/region until this
    # was added). Sub-agents inherit this from the nearest ancestor that sets one, so
    # only the root needs it.
    raw = yaml.safe_load((TEMPLATE_DIR / "root_agent.yaml").read_text())
    assert raw.get("model"), "root_agent.yaml must set an explicit model"


def test_every_agent_yaml_registers_the_current_date_callback():
    # Without this, an agent's "{temp:current_date}" instruction placeholder (from
    # safety_and_grounding_rules.md) raises KeyError on its first LLM call -- inject_session_state()
    # only substitutes keys already present in session.state, and nothing else in ADK populates a
    # date on its own. Originally registered on the root agent only (reasoning that a single
    # before_agent_callback there, firing before any transfer_to_agent, would cover every
    # sub-agent within the same turn) -- that assumption broke once deployed and queried live
    # through Gemini Enterprise: a sub-agent (data_insights) hit exactly this KeyError even though
    # the root agent's own turns succeeded. Every agent now sets its own copy; see
    # docs/superpowers/specs/2026-07-25-retail-merchandising-adk-agents-design.md section 5b
    # (local-only doc, gitignored, not on a fresh clone).
    for rel_path in [
        "root_agent.yaml",
        "sub_agents/data_insights.yaml",
        "sub_agents/market_context.yaml",
    ]:
        raw = yaml.safe_load((TEMPLATE_DIR / rel_path).read_text())
        callback_names = [c["name"] for c in raw.get("before_agent_callbacks", [])]
        assert "__LOGICAL_AGENT__.tools.callbacks.set_current_date" in callback_names, (
            f"{rel_path} is missing the current-date callback"
        )


def test_data_insights_yaml_registers_the_bigquery_project_callback():
    # Only data_insights.yaml's instruction references BigQuery table names, so only it needs
    # this callback -- it reads BIGQUERY_PROJECT_ID at runtime rather than a scaffolded agent
    # hardcoding a real GCP project id into its instruction text (an environment fingerprint, same
    # category this repo already keeps out of git elsewhere).
    raw = yaml.safe_load((TEMPLATE_DIR / "sub_agents" / "data_insights.yaml").read_text())
    callback_names = [c["name"] for c in raw.get("before_agent_callbacks", [])]
    assert "__LOGICAL_AGENT__.tools.callbacks.set_bigquery_project" in callback_names


def test_data_insights_yaml_references_bigquery_ca_tool():
    raw = yaml.safe_load(
        (TEMPLATE_DIR / "sub_agents" / "data_insights.yaml").read_text()
    )
    tool_names = [t["name"] for t in raw["tools"]]
    assert "__LOGICAL_AGENT__.tools.bigquery_ca.create_toolset" in tool_names
    bigquery_tool = next(
        t for t in raw["tools"] if t["name"] == "__LOGICAL_AGENT__.tools.bigquery_ca.create_toolset"
    )
    tool_filter = bigquery_tool["args"]["tool_filter"]
    assert tool_filter == [
        "ask_data_insights",
        "forecast",
        "analyze_contribution",
        "detect_anomalies",
    ]
    assert bigquery_tool["args"]["write_mode"] == "blocked"


def test_data_insights_yaml_references_chart_generator_tool():
    # ADK's built-in ask_data_insights can never produce a chart (hardcoded off in ADK itself,
    # see docs/superpowers/specs/2026-07-25-retail-merchandising-adk-agents-design.md section 5d,
    # local-only doc, gitignored) -- render_chart is a custom tool that works around this by
    # querying BigQuery directly and rendering with matplotlib, confirmed rendering correctly in
    # Gemini Enterprise via a real deployed-agent smoke test (Assortment Planning).
    raw = yaml.safe_load((TEMPLATE_DIR / "sub_agents" / "data_insights.yaml").read_text())
    tool_names = [t["name"] for t in raw["tools"]]
    assert "__LOGICAL_AGENT__.tools.chart_generator.render_chart" in tool_names


def test_market_context_yaml_uses_google_search_builtin():
    raw = yaml.safe_load(
        (TEMPLATE_DIR / "sub_agents" / "market_context.yaml").read_text()
    )
    assert raw["tools"] == [{"name": "google_search"}]


def test_market_context_yaml_disallows_agent_transfer():
    # Without this, ADK auto-injects a transfer_to_agent function-declaration tool into this
    # sub-agent's own LLM call (it has a parent and a sibling sub-agent). Gemini rejects any
    # request combining a built-in tool like google_search with a function-declaration tool
    # ("Multiple tools are supported only when they are all search tools") — confirmed: Assortment
    # Planning's market_context sub-agent hard-errored with a 400 on every real question until
    # this was added. Every future agent's market_context sub-agent has the same shape (built-in
    # search tool + parent + sibling), so this must be set here, not per-agent.
    raw = yaml.safe_load(
        (TEMPLATE_DIR / "sub_agents" / "market_context.yaml").read_text()
    )
    assert raw.get("disallow_transfer_to_parent") is True
    assert raw.get("disallow_transfer_to_peers") is True


def test_deployment_manifests_are_valid_yaml():
    # Templates ship as dev-example.yaml/prod-example.yaml (copied to dev.yaml/prod.yaml by the
    # developer, like .env.example -> .env) — those real files are gitignored since they hold
    # live, deployment-specific identifiers, so only the -example versions exist in the template.
    for env_name, env_file in [("dev", "dev-example.yaml"), ("prod", "prod-example.yaml")]:
        raw = yaml.safe_load((TEMPLATE_DIR / "deployment" / env_file).read_text())
        assert raw["environment"] == env_name


def test_requirements_txt_pins_bigquery_and_dataplex():
    # tools/bigquery_ca.py imports google.adk.integrations.bigquery.BigQueryToolset, whose module
    # chain hard-imports google.cloud.bigquery and google.cloud.dataplex_v1 -- neither ships with
    # the base google-adk install. `adk deploy agent_engine` only reads a requirements.txt in the
    # agent's own folder (it does not see this repo's pyproject.toml); without one, it
    # auto-generates a minimal requirements.txt containing only google-adk[a2a], and the deployed
    # container fails every request with `ImportError: cannot import name 'dataplex_v1'`
    # (confirmed: Assortment Planning's Task 12 post-deployment smoke check hit exactly this).
    text = (TEMPLATE_DIR / "requirements.txt").read_text()
    assert "google-cloud-bigquery" in text
    assert "google-cloud-dataplex" in text


def test_requirements_txt_pins_matplotlib():
    # tools/chart_generator.py renders charts with matplotlib -- not part of the base
    # google-adk install, so it must be listed here for `adk deploy agent_engine` to package it
    # (see test_requirements_txt_pins_bigquery_and_dataplex above for why this file exists at
    # all).
    text = (TEMPLATE_DIR / "requirements.txt").read_text()
    assert "matplotlib" in text


def test_eval_set_matches_adk_schema():
    from google.adk.evaluation.eval_set import EvalSet

    raw = json.loads((TEMPLATE_DIR / "eval" / "agent.evalset.json").read_text())
    EvalSet.model_validate(raw)


def test_readme_is_a_real_per_agent_readme_not_template_meta_doc():
    # A README.md now belongs inside the copied tree (added 2026-07-27) -- every scaffolded agent
    # gets its own, unlike the earlier mistake of putting template-meta documentation ("this
    # directory is a scaffold template, do not run adk run directly against it") in this exact
    # location, which would have shipped into every real agent. That meta-doc still correctly
    # lives one level up at _shared/templates/README.md, outside the copied tree. Guard against
    # the old mistake reappearing here by checking this file is genuinely the per-agent kind (has
    # scaffold tokens and TODO(scaffold) placeholders) rather than static "this is a template"
    # text.
    text = (TEMPLATE_DIR / "README.md").read_text()
    assert "__DISPLAY_NAME__" in text
    assert "TODO(scaffold)" in text
    assert "do not run" not in text.lower()
    assert "not a runnable agent" not in text.lower()
