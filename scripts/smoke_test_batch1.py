#!/usr/bin/env python3
"""Smoke test all Batch 1 deployed agents."""

import vertexai
from vertexai.agent_engines import get

PROJECT_ID = "india-ce-demos-343207"
REGION = "us-central1"

TESTS = [
    {
        "name": "Pricing & Promotions",
        "re_id": "1448155220071677952",
        "prompt": "What was the promotional lift percentage for Down Parka during the Winter Clearance campaign?"
    },
    {
        "name": "Sell-Through & Inventory Health",
        "re_id": "4920483309332463616",
        "prompt": "What is the store-level sell-through rate for SKU-001 across all stores in July 2026?"
    },
    {
        "name": "Vendor Negotiation & Rebates",
        "re_id": "2093348643250634752",
        "prompt": "What is our current YTD spend and rebate tier progress with Apex Outerwear?"
    },
    {
        "name": "Markdown & Clearance Optimization",
        "re_id": "3424584545603682304",
        "prompt": "What is the recommended clearance discount depth for aging outerwear styles?"
    },
    {
        "name": "Price Matching & Competitor Intel",
        "re_id": "2989987181562429440",
        "prompt": "What is our price index parity and competitor price gap for Men's Outerwear compared to Market Leader?"
    }
]

def run_smoke_tests():
    vertexai.init(project=PROJECT_ID, location=REGION)
    print("========================================================")
    print("RUNNING LIVE SMOKE TESTS FOR BATCH 1 (MERCHANDISING)")
    print("========================================================")
    
    results = {}
    for t in TESTS:
        name = t["name"]
        re_id = t["re_id"]
        prompt = t["prompt"]
        re_uri = f"projects/27624031314/locations/{REGION}/reasoningEngines/{re_id}"
        
        print(f"\n🔍 Testing {name} ({re_id})...")
        print(f"   Prompt: {prompt}")
        try:
            agent = get(re_uri)
            session = agent.create_session(user_id="smoke_tester_batch1")
            session_id = session.get("id") if isinstance(session, dict) else session.session_id
            
            responses = list(agent.stream_query(session_id=session_id, message=prompt, user_id="smoke_tester_batch1"))
            
            final_text = ""
            for r in responses:
                if hasattr(r, "text") and r.text:
                    final_text += r.text
                elif isinstance(r, dict) and "parts" in r:
                    for p in r["parts"]:
                        if "text" in p:
                            final_text += p["text"]
            
            if final_text:
                print(f"   ✅ Response snippet: {final_text[:180]}...")
                results[name] = True
            else:
                print(f"   ⚠️ No text response received.")
                results[name] = False
        except Exception as e:
            print(f"   ❌ Error: {e}")
            results[name] = False

    print("\n========================================================")
    print("BATCH 1 SMOKE TEST SUMMARY:")
    for name, success in results.items():
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"  - {name}: {status}")
    print("========================================================")

if __name__ == "__main__":
    run_smoke_tests()
