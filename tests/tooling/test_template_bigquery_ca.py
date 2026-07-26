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


@patch("tools.bigquery_ca.google.auth.default")
@patch("tools.bigquery_ca.BigQueryToolset")
@patch("tools.bigquery_ca.BigQueryCredentialsConfig")
def test_create_toolset_requests_cloud_platform_scope_not_bare_bigquery(
    mock_credentials_config, mock_toolset, mock_auth_default
):
    # ask_data_insights calls the Conversational Analytics API
    # (geminidataanalytics.googleapis.com's :chat endpoint), which requires the
    # cloud-platform scope -- the narrower bigquery scope gets silently rejected with
    # no audit trail (confirmed against a real deployed agent, Task 12 of the
    # Assortment Planning plan). This only matters for service-account credentials
    # (google.auth.default(scopes=...) is a no-op for user ADC), so it's invisible
    # in `adk run`/tests/integration and only bites once a real service account is
    # attached at deploy time. Every future agent scaffolded from this template
    # inherits this fix automatically.
    mock_auth_default.return_value = (MagicMock(), "fake-project")
    mock_credentials_config.return_value = "fake-credentials-config"

    create_toolset(_make_args())

    _, kwargs = mock_auth_default.call_args
    assert kwargs["scopes"] == ["https://www.googleapis.com/auth/cloud-platform"]
