"""Unit tests for the Retail Enterprise Agents Portal Site Generator."""

import json
from pathlib import Path
import re
import sys
import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from _shared.scripts.generate_portal_site import (
    DOMAIN_ORDER,
    DOMAIN_DISPLAY_NAMES,
    DOMAIN_ICONS,
    build_portal_html,
    extract_agent_metadata,
)


@pytest.fixture
def table_registry_data():
    registry_file = REPO_ROOT / "_shared" / "table_registry.yaml"
    assert registry_file.exists(), f"Registry file not found at {registry_file}"
    return yaml.safe_load(registry_file.read_text(encoding="utf-8"))


def test_table_registry_contains_100_agents(table_registry_data):
    agents = table_registry_data.get("agents", {})
    assert len(agents) == 100, f"Expected 100 agents in table_registry.yaml, found {len(agents)}"


def test_extract_agent_metadata_for_sample_agents(table_registry_data):
    agents = table_registry_data.get("agents", {})
    
    # Test merchandising agent
    aspl = agents.get("assortment_planning")
    assert aspl is not None
    meta = extract_agent_metadata("assortment_planning", "merchandising", aspl, REPO_ROOT)
    assert meta["name"] == "assortment_planning"
    assert meta["domain"] == "merchandising"
    assert meta["location"] == "us-central1"
    assert len(meta["prompts"]) >= 3
    assert meta["demo_html"] == "demos/gemini-enterprise/merchandising/assortment_planning.html"
    assert meta["demo_mp4"] == "demos/gemini-enterprise/merchandising/assortment_planning.mp4"
    assert (REPO_ROOT / meta["demo_html"]).exists()
    assert (REPO_ROOT / meta["demo_mp4"]).exists()

    # Test HR agent in us-east4
    wmp = agents.get("workplace_safety_workers_comp")
    assert wmp is not None
    meta_hr = extract_agent_metadata("workplace_safety_workers_comp", "human_resources", wmp, REPO_ROOT)
    assert meta_hr["name"] == "workplace_safety_workers_comp"
    assert meta_hr["domain"] == "human_resources"
    assert meta_hr["location"] == "us-east4"
    assert len(meta_hr["prompts"]) >= 3


def test_generated_index_html_file_exists_and_is_valid():
    index_file = REPO_ROOT / "index.html"
    assert index_file.exists(), "index.html does not exist at repo root"
    
    content = index_file.read_text(encoding="utf-8")
    assert len(content) > 50_000, f"index.html is unexpectedly small ({len(content)} bytes)"
    
    # Verify core HTML structure
    assert "<!DOCTYPE html>" in content
    assert '<html lang="en" data-theme="dark">' in content
    assert "Gemini Enterprise Agents for Retail" in content
    assert "100 Enterprise Agents Fully Deployed (9 Retail Domains)" in content
    assert "Gemini Enterprise Agents" in content
    assert "Agents on Gemini Enterprise" in content
    
    # Verify dual-theme CSS variables
    assert '[data-theme="dark"]' in content
    assert '[data-theme="light"]' in content
    assert "retail_agents_theme" in content
    
    # Verify search and modal components
    assert 'id="searchInput"' in content
    assert 'id="domainPills"' in content
    assert 'id="videoModal"' in content
    assert 'id="archModal"' in content
    assert "Gemini Enterprise Agent Platform" in content
    assert "Gemini Enterprise" in content
    assert "Google ADK & Gemini Enterprise Multi-Agent Swarm" in content
    assert "https://github.com/rajanm/retail-enterprise-agents/blob/master/README.md" in content
    assert "https://github.com/rajanm/retail-enterprise-agents/blob/master/ARCHITECTURE.md" in content


def test_all_100_agents_present_in_embedded_json():
    index_file = REPO_ROOT / "index.html"
    content = index_file.read_text(encoding="utf-8")
    
    match = re.search(r"const AGENTS_DATA = (\[.*?\]);\s*\n\s*let activeDomain", content, re.DOTALL)
    assert match is not None, "Could not extract AGENTS_DATA JSON from index.html"
    
    agents = json.loads(match.group(1))
    assert len(agents) == 100, f"Expected 100 agents in AGENTS_DATA, found {len(agents)}"
    
    agent_names = {a["name"] for a in agents}
    assert len(agent_names) == 100, "Duplicate agent names found in AGENTS_DATA"
    
    # Check domain distribution
    domains = {a["domain"] for a in agents}
    assert len(domains) == 9
    assert set(DOMAIN_ORDER) == domains


def test_all_demo_mp4_and_html_files_exist_on_disk():
    index_file = REPO_ROOT / "index.html"
    content = index_file.read_text(encoding="utf-8")
    
    match = re.search(r"const AGENTS_DATA = (\[.*?\]);\s*\n\s*let activeDomain", content, re.DOTALL)
    agents = json.loads(match.group(1))
    
    missing_html = []
    missing_mp4 = []
    
    for agent in agents:
        html_path = REPO_ROOT / agent["demo_html"]
        mp4_path = REPO_ROOT / agent["demo_mp4"]
        readme_path = REPO_ROOT / agent["readme"]
        
        if not html_path.exists():
            missing_html.append(str(html_path))
        if not mp4_path.exists():
            missing_mp4.append(str(mp4_path))
        assert readme_path.exists(), f"README missing: {readme_path}"
        
    assert not missing_html, f"Missing HTML demo files: {missing_html[:5]}"
    assert not missing_mp4, f"Missing MP4 demo files: {missing_mp4[:5]}"


def test_all_100_agent_descriptions_are_clean_and_complete():
    index_file = REPO_ROOT / "index.html"
    content = index_file.read_text(encoding="utf-8")
    
    match = re.search(r"const AGENTS_DATA = (\[.*?\]);\s*\n\s*let activeDomain", content, re.DOTALL)
    agents = json.loads(match.group(1))
    
    bad_descriptions = []
    for a in agents:
        desc = a.get("description", "").strip()
        if desc.startswith("#") or "###" in desc or desc == "### Business Problem" or len(desc) < 40:
            bad_descriptions.append((a["name"], a["domain"], desc))
            
    assert not bad_descriptions, f"Found truncated or markdown-polluted agent descriptions: {bad_descriptions}"

