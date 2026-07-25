"""Direct unit tests against the template's tools/bigquery_ca.py, imported without
going through the scaffold engine. This file contains no scaffold tokens, so it
can be tested in place; scaffold-level validation is in
test_scaffold_template_integration.py (Task 6).
"""
import sys
from pathlib import Path
from unittest.mock import MagicMock
from unittest.mock import patch

from google.adk.tools.tool_configs import ToolArgsConfig

TEMPLATE_DIR = Path(__file__).resolve().parents[2] / "_shared" / "templates" / "logical_agent"
sys.path.insert(0, str(TEMPLATE_DIR))

from tools.bigquery_ca import create_toolset  # noqa: E402


def _make_args(**overrides):
    defaults = {
        "tool_filter": ["ask_data_insights", "forecast", "analyze_contribution", "detect_anomalies"],
        "write_mode": "blocked",
        "application_name": "widget_analytics",
        "job_labels": {"domain": "test_domain", "logical_agent": "widget_analytics"},
    }
    defaults.update(overrides)
    return ToolArgsConfig.model_validate(defaults)


@patch("tools.bigquery_ca.google.auth.default")
@patch("tools.bigquery_ca.BigQueryToolset")
@patch("tools.bigquery_ca.BigQueryCredentialsConfig")
def test_create_toolset_wires_tool_filter_and_credentials(
    mock_credentials_config, mock_toolset, mock_auth_default
):
    mock_auth_default.return_value = (MagicMock(), "fake-project")
    mock_credentials_config.return_value = "fake-credentials-config"

    create_toolset(_make_args())

    _, kwargs = mock_toolset.call_args
    assert kwargs["tool_filter"] == [
        "ask_data_insights",
        "forecast",
        "analyze_contribution",
        "detect_anomalies",
    ]
    assert kwargs["credentials_config"] == "fake-credentials-config"
    assert kwargs["bigquery_tool_config"].write_mode.value == "blocked"


@patch("tools.bigquery_ca.google.auth.default")
@patch("tools.bigquery_ca.BigQueryToolset")
@patch("tools.bigquery_ca.BigQueryCredentialsConfig")
def test_create_toolset_passes_through_job_labels_and_application_name(
    mock_credentials_config, mock_toolset, mock_auth_default
):
    mock_auth_default.return_value = (MagicMock(), "fake-project")
    mock_credentials_config.return_value = "fake-credentials-config"

    create_toolset(_make_args())

    _, kwargs = mock_toolset.call_args
    tool_config = kwargs["bigquery_tool_config"]
    assert tool_config.application_name == "widget_analytics"
    assert tool_config.job_labels == {
        "domain": "test_domain",
        "logical_agent": "widget_analytics",
    }
