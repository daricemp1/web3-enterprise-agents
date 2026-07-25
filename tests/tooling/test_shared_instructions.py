"""Regression tests guarding the shared instruction fragments' required content.

These fragments get concatenated at scaffold time (Task 3) into every logical
agent's instruction text. If a required line disappears here, every future
scaffolded agent silently loses that behavior — these tests exist to catch that.
"""
from pathlib import Path

INSTRUCTIONS_DIR = Path(__file__).resolve().parents[2] / "_shared" / "instructions"


def test_persona_fragment_exists_and_has_required_content():
    content = (INSTRUCTIONS_DIR / "persona_retail_analyst.md").read_text()
    assert "senior retail merchandising data analyst" in content


def test_safety_fragment_exists_and_has_required_content():
    content = (INSTRUCTIONS_DIR / "safety_and_grounding_rules.md").read_text()
    assert "Never fabricate a number" in content


def test_output_formatting_fragment_exists_and_has_required_content():
    content = (INSTRUCTIONS_DIR / "output_formatting.md").read_text()
    assert "Respond in plain text" in content
