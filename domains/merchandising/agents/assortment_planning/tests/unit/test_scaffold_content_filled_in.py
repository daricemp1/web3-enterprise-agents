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


def test_all_three_agent_instructions_reference_current_date():
    # Guards against the three-file manual edit (root_agent.yaml + both sub_agents/*.yaml) that
    # this agent needed on top of the shared instruction fragment: the agent was already
    # scaffolded before the fragment gained the {temp:current_date} placeholder, so a future
    # edit to any one of these three files could silently drop it without a re-scaffold to catch
    # the drift.
    for path in [
        AGENT_DIR / "root_agent.yaml",
        AGENT_DIR / "sub_agents" / "data_insights.yaml",
        AGENT_DIR / "sub_agents" / "market_context.yaml",
    ]:
        assert "{temp:current_date}" in path.read_text(), f"{path} missing current-date grounding"


def test_every_agent_yaml_registers_the_current_date_callback():
    # Originally registered on the root agent only (a single before_agent_callback there,
    # firing before any transfer_to_agent, was assumed sufficient for every sub-agent within the
    # same turn) -- that assumption broke once deployed and queried live through Gemini
    # Enterprise: data_insights hit "context variable temp:current_date not found" even though
    # root's own turns succeeded. Every agent now sets its own copy; see architecture spec §5b.
    for path in [
        AGENT_DIR / "root_agent.yaml",
        AGENT_DIR / "sub_agents" / "data_insights.yaml",
        AGENT_DIR / "sub_agents" / "market_context.yaml",
    ]:
        assert "assortment_planning.tools.callbacks.set_current_date" in path.read_text(), (
            f"{path} is missing the current-date callback"
        )
