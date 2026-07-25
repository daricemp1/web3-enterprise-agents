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


def test_data_insights_yaml_references_bigquery_ca_tool():
    raw = yaml.safe_load(
        (TEMPLATE_DIR / "sub_agents" / "data_insights.yaml").read_text()
    )
    tool_names = [t["name"] for t in raw["tools"]]
    assert tool_names == ["__LOGICAL_AGENT__.tools.bigquery_ca.create_toolset"]
    tool_filter = raw["tools"][0]["args"]["tool_filter"]
    assert tool_filter == [
        "ask_data_insights",
        "forecast",
        "analyze_contribution",
        "detect_anomalies",
    ]
    assert raw["tools"][0]["args"]["write_mode"] == "blocked"


def test_market_context_yaml_uses_google_search_builtin():
    raw = yaml.safe_load(
        (TEMPLATE_DIR / "sub_agents" / "market_context.yaml").read_text()
    )
    assert raw["tools"] == [{"name": "google_search"}]


def test_deployment_manifests_are_valid_yaml():
    for env_name, env_file in [("dev", "dev.yaml"), ("prod", "prod.yaml")]:
        raw = yaml.safe_load((TEMPLATE_DIR / "deployment" / env_file).read_text())
        assert raw["environment"] == env_name


def test_eval_set_matches_adk_schema():
    from google.adk.evaluation.eval_set import EvalSet

    raw = json.loads((TEMPLATE_DIR / "eval" / "agent.evalset.json").read_text())
    EvalSet.model_validate(raw)
