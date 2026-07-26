"""Direct unit tests against the template's tools/chart_generator.py, imported without
going through the scaffold engine. This file contains no scaffold tokens, so it
can be tested in place; scaffold-level validation is in
test_scaffold_template_integration.py (Task 6).
"""
import sys
from pathlib import Path
from unittest.mock import AsyncMock
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest

TEMPLATE_DIR = Path(__file__).resolve().parents[2] / "_shared" / "templates" / "logical_agent"
sys.path.insert(0, str(TEMPLATE_DIR))

from tools.chart_generator import CHART_ARTIFACT_FILENAME  # noqa: E402
from tools.chart_generator import render_chart  # noqa: E402


def _mock_client_with_rows(rows):
    mock_client = MagicMock()
    mock_client.query.return_value.result.return_value = rows
    return mock_client


@pytest.mark.asyncio
async def test_render_chart_rejects_non_select_queries():
    mock_tool_context = MagicMock()
    mock_tool_context.save_artifact = AsyncMock()

    result = await render_chart("DELETE FROM table", "Some Chart", mock_tool_context)

    assert result["status"] == "error"
    mock_tool_context.save_artifact.assert_not_called()


@pytest.mark.asyncio
@patch("tools.chart_generator._resolve_bigquery_client")
async def test_render_chart_returns_a_clear_error_instead_of_raising_on_bad_sql(
    mock_resolve_client,
):
    # Every future agent scaffolded from this template inherits this fix automatically -- see
    # the equivalent test in the real Assortment Planning agent for the production bug this
    # guards against.
    mock_client = MagicMock()
    mock_client.query.return_value.result.side_effect = Exception("Name x not found inside t2")
    mock_resolve_client.return_value = mock_client
    mock_tool_context = MagicMock()
    mock_tool_context.save_artifact = AsyncMock()

    result = await render_chart("SELECT bad_col FROM t", "Title", mock_tool_context)

    assert result["status"] == "error"
    assert "Name x not found inside t2" in result["message"]
    mock_tool_context.save_artifact.assert_not_called()


@pytest.mark.asyncio
@patch("tools.chart_generator._resolve_bigquery_client")
async def test_render_chart_saves_a_png_artifact_on_success(mock_resolve_client):
    mock_resolve_client.return_value = _mock_client_with_rows([("Widget", 5)])
    mock_tool_context = MagicMock()
    mock_tool_context.save_artifact = AsyncMock(return_value=1)

    result = await render_chart("SELECT name, units FROM t", "Units", mock_tool_context)

    assert result["status"] == "success"
    assert result["artifact_filename"] == CHART_ARTIFACT_FILENAME
    mock_tool_context.save_artifact.assert_awaited_once()
    _, kwargs = mock_tool_context.save_artifact.call_args
    assert kwargs["artifact"].inline_data.mime_type == "image/png"
