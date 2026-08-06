#!/usr/bin/env python3
"""Run live smoke tests for all 6 Merchandising agents and print full verbatim responses."""

import vertexai
from vertexai.agent_engines import get
import json
import time

PROJECT_ID = "india-ce-demos-343207"
REGION = "us-central1"

AGENTS = [
    {
        "folder": "assortment_planning",
        "name": "Merchandising: Assortment Planning",
        "re_id": "5308443788169969664",
        "queries": [
            ("Internal Data Analytics", "What are the top 3 performing SKUs by total revenue in Men's Outerwear in July 2026?"),
            ("Market Grounding", "What are the current retail consumer trends in sustainable outdoor apparel for Fall/Winter 2026?")
        ]
    },
    {
        "folder": "pricing_promotions",
        "name": "Merchandising: Pricing & Promotions",
        "re_id": "1448155220071677952",
        "queries": [
            ("Internal Data Analytics", "Which of our recent promotions delivered the strongest promotional sales lift percentage?"),
            ("Market Grounding", "What are major competitor promotional discount strategies in retail apparel for 2026?")
        ]
    },
    {
        "folder": "sell_through_inventory_health",
        "name": "Merchandising: Sell-Through & Inventory Health",
        "re_id": "4920483309332463616",
        "queries": [
            ("Internal Data Analytics", "What is the overall sell-through rate and aging inventory breakdown for SKU-001 in July 2026?"),
            ("Market Grounding", "What are industry standard inventory sell-through benchmarks for seasonal retail apparel?")
        ]
    },
    {
        "folder": "vendor_negotiation_rebates",
        "name": "Merchandising: Vendor Negotiation & Rebates",
        "re_id": "2093348643250634752",
        "queries": [
            ("Internal Data Analytics", "What is our current YTD spend, active tier, and earned rebate with Apex Outerwear?"),
            ("Market Grounding", "What are typical vendor volume rebate agreement structures in retail apparel?")
        ]
    },
    {
        "folder": "markdown_clearance_optimization",
        "name": "Merchandising: Markdown & Clearance Optimization",
        "re_id": "3424584545603682304",
        "queries": [
            ("Internal Data Analytics", "What is our current markdown budget spend and clearance sell-through velocity?"),
            ("Market Grounding", "What are best practices for retail end-of-season markdown discount ladders?")
        ]
    },
    {
        "folder": "price_matching_competitor_intel",
        "name": "Merchandising: Price Matching & Competitor Intel",
        "re_id": "2989987181562429440",
        "queries": [
            ("Internal Data Analytics", "What is our category price index parity and competitor price gap for Men's Outerwear?"),
            ("Market Grounding", "How do leading retail department stores manage automated competitor price matching in 2026?")
        ]
    }
]

def main():
    vertexai.init(project=PROJECT_ID, location=REGION)
    print("=================================================================")
    print("LIVE SMOKE TESTS & VERBATIM RESPONSE HARVESTING (GEMINI 3.5 FLASH)")
    print("=================================================================")
    
    harvested_results = {}

    for agent_info in AGENTS:
        folder = agent_info["folder"]
        name = agent_info["name"]
        re_id = agent_info["re_id"]
        re_uri = f"projects/27624031314/locations/{REGION}/reasoningEngines/{re_id}"
        
        print(f"\n=================================================================")
        print(f"🤖 AGENT: {name} ({re_id})")
        print(f"=================================================================")
        
        harvested_results[folder] = []
        agent = get(re_uri)
        session = agent.create_session(user_id="readme_updater")
        session_id = session.get("id") if isinstance(session, dict) else session.session_id
        
        for q_type, prompt in agent_info["queries"]:
            print(f"\n[{q_type}] Prompt: {prompt}")
            try:
                responses = list(agent.stream_query(session_id=session_id, message=prompt, user_id="readme_updater"))
                final_text = ""
                for r in responses:
                    if hasattr(r, "text") and r.text:
                        final_text += r.text
                    elif isinstance(r, dict) and "parts" in r:
                        for p in r["parts"]:
                            if "text" in p:
                                final_text += p["text"]
                
                print(f"Response:\n{final_text.strip()}\n")
                harvested_results[folder].append({
                    "type": q_type,
                    "prompt": prompt,
                    "response": final_text.strip()
                })
            except Exception as e:
                print(f"❌ Error: {e}")
                harvested_results[folder].append({
                    "type": q_type,
                    "prompt": prompt,
                    "error": str(e)
                })

    with open("scripts/harvested_merch_smoke_test_results.json", "w") as f:
        json.dump(harvested_results, f, indent=2)
    print("\nSaved all harvested responses to scripts/harvested_merch_smoke_test_results.json")

if __name__ == "__main__":
    main()
