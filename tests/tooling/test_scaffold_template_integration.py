"""End-to-end test: scaffolds a real logical agent from the actual shared template
and validates the output the way a human author would — does it parse as valid
ADK config, does its Python compile, do its own generated tests pass.
"""
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "_shared" / "scripts"))

from scaffold_logical_agent import render_logical_agent  # noqa: E402


@pytest.fixture
def scaffolded_agent(tmp_path):
    return render_logical_agent(
        domain="test_domain",
        name="widget_analytics",
        display_name="Widget Analytics",
        domains_root=tmp_path / "domains",
    )


def test_scaffolded_agent_has_all_expected_files(scaffolded_agent):
    expected = [
        "__init__.py",
        "conftest.py",
        "root_agent.yaml",
        "sub_agents/data_insights.yaml",
        "sub_agents/market_context.yaml",
        "tools/__init__.py",
        "tools/bigquery_ca.py",
        "tools/callbacks.py",
        "tests/unit/test_bigquery_ca.py",
        "tests/unit/test_callbacks.py",
        "tests/integration/test_agent_end_to_end.py",
        "eval/agent.evalset.json",
        "deployment/dev-example.yaml",
        "deployment/prod-example.yaml",
        ".env.example",
        "data/README.md",
        "requirements.txt",
    ]
    for rel_path in expected:
        assert (scaffolded_agent / rel_path).is_file(), f"missing {rel_path}"


def test_scaffolded_agent_configs_pass_adk_validation(scaffolded_agent):
    from google.adk.agents.agent_config import AgentConfig

    for rel_path in [
        "root_agent.yaml",
        "sub_agents/data_insights.yaml",
        "sub_agents/market_context.yaml",
    ]:
        raw = yaml.safe_load((scaffolded_agent / rel_path).read_text())
        AgentConfig.model_validate(raw)


def test_scaffolded_bigquery_ca_module_compiles(scaffolded_agent):
    import py_compile

    py_compile.compile(str(scaffolded_agent / "tools" / "bigquery_ca.py"), doraise=True)


def test_scaffolded_callbacks_module_compiles(scaffolded_agent):
    import py_compile

    py_compile.compile(str(scaffolded_agent / "tools" / "callbacks.py"), doraise=True)


def test_scaffolded_agent_no_leftover_tokens(scaffolded_agent):
    tokens = ["__DOMAIN__", "__LOGICAL_AGENT__", "__DISPLAY_NAME__", "__SHARED_INSTRUCTIONS__"]
    for path in scaffolded_agent.rglob("*"):
        if not path.is_file():
            continue
        text = path.read_text()
        for token in tokens:
            assert token not in text, f"leftover token {token} in {path}"


def test_scaffolded_agent_generated_unit_tests_pass(scaffolded_agent):
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/unit", "-q"],
        cwd=scaffolded_agent,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
