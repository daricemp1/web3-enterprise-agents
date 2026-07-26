"""Guards against leftover scaffold TODO markers in this agent's core config,
so a scaffolded-but-unfilled agent can't accidentally ship.
"""
import re
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
    assert "retail_ent_agents.spch_inpl_product_catalog" in text
    assert "retail_ent_agents.spch_inpl_inventory_position" in text
    assert "retail_ent_agents.spch_inpl_demand_history" in text


def test_data_insights_yaml_does_not_hardcode_a_real_project_id():
    # The project id portion of each authorized-table reference is injected at runtime by the
    # set_bigquery_project callback from BIGQUERY_PROJECT_ID (see tools/callbacks.py), not
    # committed as a literal string -- a real GCP project id is an environment fingerprint, same
    # category as the service account email / Agent Engine resource name this repo already keeps
    # out of git via gitignored deployment/dev.yaml. Deliberately checked structurally (every
    # authorized-table line must start with the placeholder) rather than by asserting a specific
    # real project id string is absent, which would just re-embed that exact fingerprint here.
    text = (AGENT_DIR / "sub_agents" / "data_insights.yaml").read_text()
    table_refs = re.findall(r"^\s*-\s+(\S+\.retail_ent_agents\.spch_inpl_\w+)\s*$", text, re.MULTILINE)
    assert len(table_refs) == 3
    assert all(ref.startswith("{temp:bq_project_id}.") for ref in table_refs)


def test_all_three_agent_instructions_reference_current_date():
    for path in [
        AGENT_DIR / "root_agent.yaml",
        AGENT_DIR / "sub_agents" / "data_insights.yaml",
        AGENT_DIR / "sub_agents" / "market_context.yaml",
    ]:
        assert "{temp:current_date}" in path.read_text(), f"{path} missing current-date grounding"


def test_every_agent_yaml_registers_the_current_date_callback():
    # Registered on every agent (root and every sub-agent), not root only -- see architecture
    # spec §5b for why (a production bug on Assortment Planning where Gemini Enterprise reached a
    # sub-agent without root's before_agent_callback having run first). Inherited from the
    # template, so this is a drift guard rather than a fix being applied here.
    for path in [
        AGENT_DIR / "root_agent.yaml",
        AGENT_DIR / "sub_agents" / "data_insights.yaml",
        AGENT_DIR / "sub_agents" / "market_context.yaml",
    ]:
        assert "inventory_planning.tools.callbacks.set_current_date" in path.read_text(), (
            f"{path} is missing the current-date callback"
        )


def test_data_insights_yaml_registers_the_bigquery_project_callback():
    # Only data_insights.yaml's instruction references BigQuery table names, so only it needs
    # this callback -- registered directly here (not depending on root having run first) for the
    # same reason as the current-date callback above.
    text = (AGENT_DIR / "sub_agents" / "data_insights.yaml").read_text()
    assert "inventory_planning.tools.callbacks.set_bigquery_project" in text
