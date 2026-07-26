"""Guards against leftover scaffold TODO markers in this agent's core config,
so a scaffolded-but-unfilled agent can't accidentally ship.
"""
from pathlib import Path

AGENT_DIR = Path(__file__).resolve().parents[2]


def test_root_agent_yaml_has_no_leftover_scaffold_todo():
    text = (AGENT_DIR / "root_agent.yaml").read_text()
    assert "# TODO(scaffold):" not in text


def test_data_insights_yaml_has_no_leftover_scaffold_todo():
    text = (AGENT_DIR / "sub_agents" / "data_insights.yaml").read_text()
    assert "# TODO(scaffold):" not in text


def test_data_insights_yaml_lists_the_three_authorized_tables():
    text = (AGENT_DIR / "sub_agents" / "data_insights.yaml").read_text()
    assert "retail_ent_agents.ap_product_catalog" in text
    assert "retail_ent_agents.ap_sales_by_sku" in text
    assert "retail_ent_agents.ap_planogram_space_allocation" in text
