#!/usr/bin/env python3
"""Grants a service account read access to specific tables in the shared BigQuery dataset.

All domain agents share one BigQuery dataset (see
docs/superpowers/specs/2026-07-25-retail-merchandising-adk-agents-design.md section 6a, updated
2026-07-26 — that file is local-only, gitignored, not on a fresh clone), so per-agent data
scoping is enforced with table-level IAM bindings, not
dataset-level ones — each agent's service account only gets `roles/bigquery.dataViewer` on the
specific tables listed for it in `_shared/table_registry.yaml`.

Usage:
    uv run python _shared/scripts/grant_table_access.py \
        --project REDACTED_GCP_PROJECT_ID --dataset retail_ent_agents \
        --service-account REPLACE_WITH_DEV_SERVICE_ACCOUNT_EMAIL \
        --table ap_product_catalog --table ap_sales_by_sku --table ap_planogram_space_allocation
"""
from __future__ import annotations

import argparse

from google.cloud import bigquery


def grant_table_viewer_access(
    project: str,
    dataset: str,
    service_account: str,
    tables: list[str],
    client: bigquery.Client | None = None,
) -> None:
  """Grants `roles/bigquery.dataViewer` on each named table to one service account."""
  client = client or bigquery.Client(project=project)
  member = f"serviceAccount:{service_account}"

  for table_name in tables:
    table_ref = bigquery.DatasetReference(project, dataset).table(table_name)
    policy = client.get_iam_policy(table_ref)
    policy["roles/bigquery.dataViewer"].add(member)
    client.set_iam_policy(table_ref, policy)


def main() -> None:
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument("--project", required=True)
  parser.add_argument("--dataset", required=True)
  parser.add_argument("--service-account", required=True)
  parser.add_argument("--table", action="append", required=True, dest="tables")
  args = parser.parse_args()

  grant_table_viewer_access(
      project=args.project,
      dataset=args.dataset,
      service_account=args.service_account,
      tables=args.tables,
  )
  print(f"Granted {args.service_account} dataViewer on {len(args.tables)} table(s)")


if __name__ == "__main__":
  main()
