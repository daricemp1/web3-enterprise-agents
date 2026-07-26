"""Unit tests for the BigQuery seed-data loader, using a mocked bigquery.Client
so no network calls are made.
"""
import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest
from google.cloud import bigquery

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "_shared" / "scripts"))

from load_agent_data import load_csvs_to_bigquery  # noqa: E402


@pytest.fixture
def fake_agent_data_dir(tmp_path):
    data_dir = tmp_path / "domains" / "test_domain" / "agents" / "widget_analytics" / "data"
    data_dir.mkdir(parents=True)
    (data_dir / "product_catalog.csv").write_text("product_id,product_name\nSKU-001,Widget\n")
    (data_dir / "sales_by_sku.csv").write_text("date,product_id,units_sold\n2026-01-01,SKU-001,5\n")
    return tmp_path / "domains"


@pytest.fixture
def fake_registry_path(tmp_path):
    registry_file = tmp_path / "table_registry.yaml"
    registry_file.write_text(
        "dataset: fake_dataset\n"
        "project: fake-project\n"
        "agents:\n"
        "  widget_analytics:\n"
        "    domain: test_domain\n"
        "    agent_id: wa\n"
        "    tables:\n"
        "      - product_catalog\n"
        "      - sales_by_sku\n"
    )
    return registry_file


def test_load_csvs_to_bigquery_raises_if_no_csv_files(tmp_path, fake_registry_path):
    empty_domains_root = tmp_path / "domains"
    (empty_domains_root / "test_domain" / "agents" / "widget_analytics" / "data").mkdir(
        parents=True
    )

    with pytest.raises(FileNotFoundError):
        load_csvs_to_bigquery(
            domain="test_domain",
            name="widget_analytics",
            project="fake-project",
            dataset="fake_dataset",
            domains_root=empty_domains_root,
            client=MagicMock(),
            registry_path=fake_registry_path,
        )


def test_load_csvs_to_bigquery_raises_if_agent_not_in_registry(fake_agent_data_dir, tmp_path):
    empty_registry = tmp_path / "empty_registry.yaml"
    empty_registry.write_text("dataset: fake_dataset\nproject: fake-project\nagents: {}\n")

    with pytest.raises(KeyError):
        load_csvs_to_bigquery(
            domain="test_domain",
            name="widget_analytics",
            project="fake-project",
            dataset="fake_dataset",
            domains_root=fake_agent_data_dir,
            client=MagicMock(),
            registry_path=empty_registry,
        )


def test_load_csvs_to_bigquery_raises_if_table_not_registered(fake_agent_data_dir, tmp_path):
    partial_registry = tmp_path / "partial_registry.yaml"
    partial_registry.write_text(
        "dataset: fake_dataset\n"
        "project: fake-project\n"
        "agents:\n"
        "  widget_analytics:\n"
        "    domain: test_domain\n"
        "    agent_id: wa\n"
        "    tables:\n"
        "      - product_catalog\n"  # missing sales_by_sku on purpose
    )

    with pytest.raises(KeyError):
        load_csvs_to_bigquery(
            domain="test_domain",
            name="widget_analytics",
            project="fake-project",
            dataset="fake_dataset",
            domains_root=fake_agent_data_dir,
            client=MagicMock(),
            registry_path=partial_registry,
        )


def test_load_csvs_to_bigquery_creates_dataset_if_missing(fake_agent_data_dir, fake_registry_path):
    mock_client = MagicMock()
    mock_client.load_table_from_file.return_value.result.return_value = None

    load_csvs_to_bigquery(
        domain="test_domain",
        name="widget_analytics",
        project="fake-project",
        dataset="fake_dataset",
        domains_root=fake_agent_data_dir,
        client=mock_client,
        registry_path=fake_registry_path,
    )

    mock_client.create_dataset.assert_called_once()
    args, kwargs = mock_client.create_dataset.call_args
    assert isinstance(args[0], bigquery.Dataset)
    assert args[0].reference == bigquery.DatasetReference("fake-project", "fake_dataset")
    assert kwargs["exists_ok"] is True


def test_load_csvs_to_bigquery_prefixes_table_names_with_agent_id(
    fake_agent_data_dir, fake_registry_path
):
    mock_client = MagicMock()
    mock_client.load_table_from_file.return_value.result.return_value = None

    loaded_tables = load_csvs_to_bigquery(
        domain="test_domain",
        name="widget_analytics",
        project="fake-project",
        dataset="fake_dataset",
        domains_root=fake_agent_data_dir,
        client=mock_client,
        registry_path=fake_registry_path,
    )

    assert loaded_tables == ["wa_product_catalog", "wa_sales_by_sku"]
    assert mock_client.load_table_from_file.call_count == 2

    expected_table_ids = {"wa_product_catalog", "wa_sales_by_sku"}
    seen_table_ids = set()
    for call_args in mock_client.load_table_from_file.call_args_list:
        args, kwargs = call_args
        table_ref = args[1]
        assert isinstance(table_ref, bigquery.TableReference)
        seen_table_ids.add(table_ref.table_id)

        job_config = kwargs["job_config"]
        assert job_config.autodetect is True
        assert job_config.write_disposition == bigquery.WriteDisposition.WRITE_TRUNCATE
        assert job_config.skip_leading_rows == 1

    assert seen_table_ids == expected_table_ids
