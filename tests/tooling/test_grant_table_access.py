"""Unit tests for the table-level BigQuery IAM grant script, using a mocked
bigquery.Client so no network calls or real IAM changes are made.
"""
import sys
from pathlib import Path
from unittest.mock import MagicMock

from google.api_core.iam import Policy

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "_shared" / "scripts"))

from grant_table_access import grant_table_viewer_access  # noqa: E402


def test_grant_table_viewer_access_adds_member_to_each_table_policy():
    mock_client = MagicMock()
    mock_client.get_iam_policy.side_effect = lambda table_ref: Policy()

    grant_table_viewer_access(
        project="fake-project",
        dataset="fake_dataset",
        service_account="agent-sa@fake-project.iam.gserviceaccount.com",
        tables=["product_catalog", "sales_by_sku"],
        client=mock_client,
    )

    assert mock_client.set_iam_policy.call_count == 2
    granted_table_ids = set()
    for call_args in mock_client.set_iam_policy.call_args_list:
        table_ref, policy = call_args[0]
        granted_table_ids.add(table_ref.table_id)
        members = policy["roles/bigquery.dataViewer"]
        assert "serviceAccount:agent-sa@fake-project.iam.gserviceaccount.com" in members

    assert granted_table_ids == {"product_catalog", "sales_by_sku"}
