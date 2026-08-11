from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


def test_claude_and_agents_md_are_byte_identical():
    claude_md = (REPO_ROOT / "CLAUDE.md").read_bytes()
    agents_md = (REPO_ROOT / "AGENTS.md").read_bytes()
    assert claude_md == agents_md, "CLAUDE.md and AGENTS.md must be 100% byte-identical."


def test_claude_and_gemini_md_are_byte_identical():
    claude_md = (REPO_ROOT / "CLAUDE.md").read_bytes()
    gemini_md = (REPO_ROOT / "GEMINI.md").read_bytes()
    assert claude_md == gemini_md, "CLAUDE.md and GEMINI.md must be 100% byte-identical."


def test_canonical_file_mentions_byte_identity_rule():
    claude_text = (REPO_ROOT / "CLAUDE.md").read_text(encoding="utf-8")
    assert "CLAUDE.md" in claude_text
    assert "GEMINI.md" in claude_text
    assert "AGENTS.md" in claude_text
