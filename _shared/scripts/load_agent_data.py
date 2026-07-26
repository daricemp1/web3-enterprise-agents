#!/usr/bin/env python3
"""Loads a logical agent's data/*.csv seed files into a dev BigQuery dataset.

Creates the target dataset if it doesn't already exist. Each CSV is loaded into a table named
`<agent_id>_<csv_file_stem>` (agent_id comes from this agent's entry in
_shared/table_registry.yaml) with autodetected schema, replacing any existing table content —
safe to rerun. The agent_id prefix prevents table-name collisions across agents sharing the
dataset; the registry lookup also fails loudly if a CSV isn't listed under that agent's `tables:`,
so the registry can't silently drift from what's actually loaded. See
docs/superpowers/specs/2026-07-25-retail-merchandising-adk-agents-design.md section 6a (local-only
doc, gitignored, not on a fresh clone).

Usage:
    uv run python _shared/scripts/load_agent_data.py \
        --domain merchandising --name assortment_planning \
        --project <dev_gcp_project_id> --dataset retail_ent_agents
"""
from __future__ import annotations

import argparse
from pathlib import Path

import yaml
from google.cloud import bigquery

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_REGISTRY_PATH = REPO_ROOT / "_shared" / "table_registry.yaml"


def load_csvs_to_bigquery(
    domain: str,
    name: str,
    project: str,
    dataset: str,
    domains_root: Path,
    client: bigquery.Client | None = None,
    registry_path: Path | None = None,
) -> list[str]:
  """Loads every data/*.csv file for one logical agent into `project.dataset`.

  Table names are `<agent_id>_<csv_file_stem>`, where `agent_id` comes from this agent's entry
  in the table registry. Returns the sorted list of prefixed table names loaded.
  """
  data_dir = domains_root / domain / "agents" / name / "data"
  csv_files = sorted(data_dir.glob("*.csv"))
  if not csv_files:
    raise FileNotFoundError(f"No CSV files found under {data_dir}")

  registry_path = registry_path or DEFAULT_REGISTRY_PATH
  registry = yaml.safe_load(registry_path.read_text())
  agent_entry = (registry.get("agents") or {}).get(name)
  if agent_entry is None:
    raise KeyError(
        f"Agent '{name}' has no entry under 'agents:' in {registry_path} — add one with an "
        "agent_id before loading its data."
    )
  agent_id = agent_entry.get("agent_id")
  if not agent_id:
    raise KeyError(
        f"Agent '{name}' has no agent_id under 'agents:' in {registry_path} — add a short, "
        "unique agent_id before loading its data."
    )
  registered_tables = set(agent_entry.get("tables", []))

  client = client or bigquery.Client(project=project)

  dataset_ref = bigquery.DatasetReference(project, dataset)
  client.create_dataset(bigquery.Dataset(dataset_ref), exists_ok=True)

  job_config = bigquery.LoadJobConfig(
      source_format=bigquery.SourceFormat.CSV,
      skip_leading_rows=1,
      autodetect=True,
      write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
  )

  loaded_tables = []
  for csv_path in csv_files:
    logical_name = csv_path.stem
    if logical_name not in registered_tables:
      raise KeyError(
          f"'{logical_name}' is not listed under agents.{name}.tables in {registry_path} — "
          "add it there before loading."
      )
    table_name = f"{agent_id}_{logical_name}"
    table_ref = dataset_ref.table(table_name)
    with open(csv_path, "rb") as source_file:
      load_job = client.load_table_from_file(source_file, table_ref, job_config=job_config)
    load_job.result()
    loaded_tables.append(table_name)

  return loaded_tables


def main() -> None:
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument("--domain", required=True)
  parser.add_argument("--name", required=True, help="snake_case logical agent folder name")
  parser.add_argument("--project", required=True, help="target GCP project id")
  parser.add_argument("--dataset", required=True, help="target BigQuery dataset id")
  parser.add_argument(
      "--domains-root",
      type=Path,
      default=REPO_ROOT / "domains",
      help="Root directory containing domain folders (default: repo domains/)",
  )
  args = parser.parse_args()

  loaded_tables = load_csvs_to_bigquery(
      domain=args.domain,
      name=args.name,
      project=args.project,
      dataset=args.dataset,
      domains_root=args.domains_root,
  )
  print(
      f"Loaded {len(loaded_tables)} table(s) into {args.project}.{args.dataset}: "
      f"{', '.join(loaded_tables)}"
  )


if __name__ == "__main__":
  main()
