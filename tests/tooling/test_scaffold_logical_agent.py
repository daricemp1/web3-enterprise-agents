"""Unit tests for the scaffold engine itself, using a minimal synthetic template
fixture — not the real `_shared/templates/logical_agent` content (that's authored
in Task 4/5 and exercised end-to-end in test_scaffold_template_integration.py).
This keeps engine logic testable independent of template content.
"""
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "_shared" / "scripts"))

import scaffold_logical_agent  # noqa: E402
from scaffold_logical_agent import render_logical_agent  # noqa: E402


@pytest.fixture
def fake_template_dir(tmp_path, monkeypatch):
    template_dir = tmp_path / "fake_template"
    (template_dir / "sub_agents").mkdir(parents=True)
    (template_dir / "root_agent.yaml").write_text(
        "name: __LOGICAL_AGENT___root\n"
        "description: Orchestrator for __DISPLAY_NAME__ in __DOMAIN__.\n"
        "instruction: |\n"
        "  __SHARED_INSTRUCTIONS__\n"
        "\n"
        "  Specific instructions for __DISPLAY_NAME__.\n"
    )
    (template_dir / "sub_agents" / "data_insights.yaml").write_text(
        "name: __LOGICAL_AGENT___data_insights\n"
    )

    monkeypatch.setattr(scaffold_logical_agent, "TEMPLATE_DIR", template_dir)
    monkeypatch.setattr(
        scaffold_logical_agent,
        "load_shared_instructions",
        lambda: "Line one of shared instructions.\nLine two of shared instructions.",
    )
    return template_dir


def test_render_logical_agent_copies_all_template_files(fake_template_dir, tmp_path):
    domains_root = tmp_path / "domains"
    target = render_logical_agent(
        domain="test_domain",
        name="widget_analytics",
        display_name="Widget Analytics",
        domains_root=domains_root,
    )

    assert target == domains_root / "test_domain" / "agents" / "widget_analytics"
    assert (target / "root_agent.yaml").is_file()
    assert (target / "sub_agents" / "data_insights.yaml").is_file()


def test_render_logical_agent_substitutes_simple_tokens(fake_template_dir, tmp_path):
    target = render_logical_agent(
        domain="test_domain",
        name="widget_analytics",
        display_name="Widget Analytics",
        domains_root=tmp_path / "domains",
    )

    text = (target / "root_agent.yaml").read_text()
    assert "widget_analytics_root" in text
    assert "Widget Analytics" in text
    assert "test_domain" in text
    assert "__LOGICAL_AGENT__" not in text
    assert "__DISPLAY_NAME__" not in text
    assert "__DOMAIN__" not in text


def test_render_logical_agent_indents_shared_instructions_block(fake_template_dir, tmp_path):
    target = render_logical_agent(
        domain="test_domain",
        name="widget_analytics",
        display_name="Widget Analytics",
        domains_root=tmp_path / "domains",
    )

    text = (target / "root_agent.yaml").read_text()
    assert "  Line one of shared instructions." in text
    assert "  Line two of shared instructions." in text
    assert "__SHARED_INSTRUCTIONS__" not in text


def test_render_logical_agent_raises_if_target_already_exists(fake_template_dir, tmp_path):
    domains_root = tmp_path / "domains"
    render_logical_agent(
        domain="test_domain",
        name="widget_analytics",
        display_name="Widget Analytics",
        domains_root=domains_root,
    )
    with pytest.raises(FileExistsError):
        render_logical_agent(
            domain="test_domain",
            name="widget_analytics",
            display_name="Widget Analytics",
            domains_root=domains_root,
        )
