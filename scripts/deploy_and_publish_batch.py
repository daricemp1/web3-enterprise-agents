#!/usr/bin/env python3
"""Batch deployment and Gemini Enterprise publication script."""

import argparse
import subprocess
import sys
import time
from pathlib import Path

BATCH_1 = [
    {
        "name": "pricing_promotions",
        "domain": "merchandising",
        "re_id": "1448155220071677952",
        "display_name": "Merchandising: Pricing & Promotions",
        "description": "Answers pricing and promotions questions for merchandising buyers and planners -- price history and elasticity, markdown cadence and depth, and promotion lift/effectiveness -- using internal BigQuery pricing data and external market/competitive search."
    },
    {
        "name": "sell_through_inventory_health",
        "domain": "merchandising",
        "re_id": "4920483309332463616",
        "display_name": "Merchandising: Sell-Through & Inventory Health",
        "description": "Answers merchandising questions on store-level sell-through rates, stock turn, aging inventory breakdown, weeks of supply, and sell-through markdown triggers."
    },
    {
        "name": "vendor_negotiation_rebates",
        "domain": "merchandising",
        "re_id": "2093348643250634752",
        "display_name": "Merchandising: Vendor Negotiation & Rebates",
        "description": "Answers volume rebate agreement thresholds, YTD spend rebate tier progress, co-op marketing fund commitments/claims, vendor payment terms, and net rebate realization % questions using BigQuery Conversational Analytics and market benchmarks."
    },
    {
        "name": "markdown_clearance_optimization",
        "domain": "merchandising",
        "re_id": "3424584545603682304",
        "display_name": "Merchandising: Markdown & Clearance Optimization",
        "description": "Answers questions about end-of-season clearance discount depth, sell-through velocity, markdown budgets, and salvage recovery."
    },
    {
        "name": "price_matching_competitor_intel",
        "domain": "merchandising",
        "re_id": "2989987181562429440",
        "display_name": "Merchandising: Price Matching & Competitor Intel",
        "description": "Answers questions about competitor price gap %, market price index parity, POS price match claims, and holding margin opportunity."
    }
]

PROJECT_ID = "india-ce-demos-343207"
PROJECT_NUM = "27624031314"
GE_APP_ID = "projects/27624031314/locations/global/collections/default_collection/engines/agsp-test_1740183477744"
REGION = "us-central1"


def deploy_and_publish_agent(agent: dict):
    name = agent["name"]
    domain = agent["domain"]
    re_id = agent["re_id"]
    display_name = agent["display_name"]
    description = agent["description"]
    agent_path = f"domains/{domain}/agents/{name}"

    print(f"\n========================================================")
    print(f"🚀 Deploying {display_name} ({re_id})...")
    print(f"========================================================")

    # 1. ADK deploy
    deploy_cmd = [
        "uv", "run", "--frozen", "adk", "deploy", "agent_engine",
        "--project", PROJECT_ID,
        "--region", REGION,
        "--agent_engine_id", re_id,
        "--display_name", display_name,
        "--description", description,
        agent_path
    ]
    
    env_vars = dict(subprocess.os.environ)
    env_vars["PATH"] = env_vars.get("PATH", "") + ":" + str(Path.home() / "Dev/google-cloud-sdk/bin")
    env_vars["BIGQUERY_PROJECT_ID"] = PROJECT_ID

    res = subprocess.run(deploy_cmd, env=env_vars, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"❌ Deploy failed for {name}: {res.stderr}")
        return False
    print(f"✅ Deployed {name} to Agent Engine ({re_id})")

    # Cleanup temp dirs
    subprocess.run(f"rm -rf domains/{domain}/agents/*_tmp*", shell=True)

    # 2. Publish to Gemini Enterprise
    publish_cmd = [
        "uv", "run", "--frozen", "agents-cli", "publish", "gemini-enterprise",
        "--registration-type", "adk",
        "--agent-runtime-id", f"projects/{PROJECT_NUM}/locations/{REGION}/reasoningEngines/{re_id}",
        "--gemini-enterprise-app-id", GE_APP_ID,
        "--display-name", display_name,
        "--description", description,
        "--project", PROJECT_ID
    ]
    pub_res = subprocess.run(publish_cmd, env=env_vars, capture_output=True, text=True)
    if pub_res.returncode != 0:
        print(f"❌ Publish failed for {name}: {pub_res.stderr}")
        return False
    print(f"✅ Published {name} to Gemini Enterprise")
    return True


def main():
    print("Starting Batch 1 Deployment (5 Merchandising Agents)...")
    results = {}
    for agent in BATCH_1:
        success = deploy_and_publish_agent(agent)
        results[agent["name"]] = success

    print("\n========================================================")
    print("BATCH 1 DEPLOYMENT RESULTS:")
    for name, success in results.items():
        status = "✅ SUCCESS" if success else "❌ FAILED"
        print(f"  - {name}: {status}")
    print("========================================================")


if __name__ == "__main__":
    main()
