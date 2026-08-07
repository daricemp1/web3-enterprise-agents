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


def test_readme_has_no_leftover_scaffold_todo():
  text = (AGENT_DIR / "README.md").read_text()
  assert "TODO(scaffold):" not in text
  assert "TODO(scaffold)" not in text


def test_data_insights_yaml_lists_the_four_authorized_tables():
  text = (AGENT_DIR / "sub_agents" / "data_insights.yaml").read_text()
  assert "retail_ent_agents.care_ossd_social_media_tickets" in text
  assert "retail_ent_agents.care_ossd_public_response_speed" in text
  assert "retail_ent_agents.care_ossd_escalation_sentiment_shift" in text
  assert "retail_ent_agents.care_ossd_dm_commerce_inquiries" in text


def test_data_insights_yaml_does_not_hardcode_a_real_project_id():
  text = (AGENT_DIR / "sub_agents" / "data_insights.yaml").read_text()
  table_refs = re.findall(
      r"^\s*-\s+(\S+\.retail_ent_agents\.care_ossd_\w+)\s*$", text, re.MULTILINE
  )
  assert len(table_refs) == 4
  assert all(ref.startswith("{temp:bq_project_id}.") for ref in table_refs)


def test_all_three_agent_instructions_reference_current_date():
  for path in [
      AGENT_DIR / "root_agent.yaml",
      AGENT_DIR / "sub_agents" / "data_insights.yaml",
      AGENT_DIR / "sub_agents" / "market_context.yaml",
  ]:
    assert "{temp:current_date}" in path.read_text(), (
        f"{path} missing current-date grounding"
    )


def test_every_agent_yaml_registers_the_current_date_callback():
  for path in [
      AGENT_DIR / "root_agent.yaml",
      AGENT_DIR / "sub_agents" / "data_insights.yaml",
      AGENT_DIR / "sub_agents" / "market_context.yaml",
  ]:
    assert (
        "omnichannel_social_support_desk.tools.callbacks.set_current_date"
        in path.read_text()
    ), f"{path} is missing the current-date callback"


def test_data_insights_yaml_registers_the_bigquery_project_callback():
  text = (AGENT_DIR / "sub_agents" / "data_insights.yaml").read_text()
  assert "omnichannel_social_support_desk.tools.callbacks.set_bigquery_project" in text
