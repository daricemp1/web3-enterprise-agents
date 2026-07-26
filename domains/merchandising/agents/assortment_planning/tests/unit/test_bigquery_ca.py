"""Unit tests for this logical agent's BigQuery Conversational Analytics tool factory.

These tests mock all Google Cloud calls — no network access, no real credentials.
"""
from unittest.mock import MagicMock
from unittest.mock import patch

from google.adk.tools.tool_configs import ToolArgsConfig

from tools.bigquery_ca import create_toolset


def _make_args(**overrides):
    defaults = {
        "tool_filter": ["ask_data_insights", "forecast", "analyze_contribution", "detect_anomalies"],
        "write_mode": "blocked",
        "application_name": "assortment_planning",
        "job_labels": {"domain": "merchandising", "logical_agent": "assortment_planning"},
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
    assert tool_config.application_name == "assortment_planning"
    assert tool_config.job_labels == {
        "domain": "merchandising",
        "logical_agent": "assortment_planning",
    }
