#!/usr/bin/env python3
"""Loads all 10 Web3 agents' seed CSVs into BigQuery."""

import argparse
from pathlib import Path
import yaml
import sys

REPO_ROOT = Path('/usr/local/google/home/daricemahtab/web3-enterprise-agents')
sys.path.insert(0, str(REPO_ROOT))

from _shared.scripts.load_agent_data import load_csvs_to_bigquery

def main():
    parser = argparse.ArgumentParser(description="Load all Web3 seed data to BigQuery")
    parser.add_argument("--project", default="gcda-apac-sc", help="GCP Project ID (default: gcda-apac-sc)")
    parser.add_argument("--dataset", default="web3_enterprise_agents", help="BigQuery dataset name")
    args = parser.parse_args()

    registry_path = REPO_ROOT / "_shared" / "table_registry.yaml"
    registry = yaml.safe_load(registry_path.read_text())
    
    domains_root = REPO_ROOT / "domains"
    
    print(f"🚀 Loading Web3 datasets into GCP Project '{args.project}' dataset '{args.dataset}'...\n")
    
    for agent_name, agent_entry in registry.get("agents", {}).items():
        domain = agent_entry.get("domain")
        print(f"🔹 Loading {domain}/{agent_name}...")
        try:
            loaded_tables = load_csvs_to_bigquery(
                domain=domain,
                name=agent_name,
                project=args.project,
                dataset=args.dataset,
                domains_root=domains_root,
                registry_path=registry_path
            )
            print(f"   ✓ Loaded tables: {', '.join(loaded_tables)}")
        except Exception as e:
            print(f"   ❌ Error loading {agent_name}: {e}")

    print("\n✅ Finished BigQuery ingestion pass!")

if __name__ == "__main__":
    main()
