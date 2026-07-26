# Retail Enterprise Agents

ADK agents for Gemini Enterprise, organized by retail domain. See
`docs/superpowers/specs/2026-07-25-retail-merchandising-adk-agents-design.md` for the full
architecture. That file is local-only (gitignored, not in git history) — it won't exist on a
fresh clone; ask whoever owns this repo's design docs for a copy if you need it.

## Setup

    uv sync

## Run the tooling test suite

    uv run pytest tests/tooling -v

## Add a new logical agent

See `_shared/README.md`.
