"""Eval suite comparing Gemini 2.5 Flash vs Gemini 3.5 Flash on golden eval scenarios."""
import asyncio
import json
import os
from pathlib import Path
import sys
import time
import yaml

agent_parent_dir = Path(__file__).resolve().parents[1] / "domains" / "merchandising" / "agents"
sys.path.insert(0, str(agent_parent_dir))

from google.adk.agents.config_agent_utils import from_config
from google.adk.runners import InMemoryRunner
from google.genai import types

async def run_eval_case(agent, prompt: str) -> tuple[float, str, list[str]]:
    runner = InMemoryRunner(agent=agent, app_name="assortment_planning")
    session = await runner.session_service.create_session(
        app_name="assortment_planning", user_id="evaluator"
    )
    
    start_time = time.perf_counter()
    events = [
        event
        async for event in runner.run_async(
            user_id="evaluator",
            session_id=session.id,
            new_message=types.Content(
                role="user", parts=[types.Part(text=prompt)]
            ),
        )
    ]
    latency = time.perf_counter() - start_time
    
    final_texts = [
        part.text
        for event in events
        if event.content
        for part in event.content.parts
        if part.text
    ]
    
    authors = [
        event.author
        for event in events
        if hasattr(event, "author") and event.author
    ]
    
    return latency, "\n".join(final_texts), list(dict.fromkeys(authors))

async def main():
    agent_dir = Path(__file__).resolve().parents[1] / "domains" / "merchandising" / "agents" / "assortment_planning"
    eval_file = agent_dir / "eval" / "agent.evalset.json"
    eval_data = json.loads(eval_file.read_text())
    
    configs = [
        ("gemini-2.5-flash", "us-central1"),
        ("gemini-3.5-flash", "global")
    ]
    
    os.environ["BIGQUERY_PROJECT_ID"] = "india-ce-demos-343207"
    os.environ["GOOGLE_CLOUD_PROJECT"] = "india-ce-demos-343207"
    os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "true"
    
    root_yaml_path = agent_dir / "root_agent.yaml"
    original_yaml_content = root_yaml_path.read_text()
    
    results = {}
    
    print("=== Running Golden Eval Scenarios ===")
    try:
        for model, loc in configs:
            print(f"\n==========================================")
            print(f"--- Eval Config: {model} @ {loc} ---")
            print(f"==========================================")
            os.environ["GOOGLE_CLOUD_LOCATION"] = loc
            os.environ["VERTEXAI_LOCATION"] = loc
            
            raw_yaml = yaml.safe_load(original_yaml_content)
            raw_yaml["model"] = model
            root_yaml_path.write_text(yaml.dump(raw_yaml))
            
            agent = from_config(str(root_yaml_path))
            
            model_results = []
            for case in eval_data["eval_cases"]:
                eval_id = case["eval_id"]
                prompt = case["conversation"][0]["user_content"]["parts"][0]["text"]
                expected = case["conversation"][0]["final_response"]["parts"][0]["text"]
                
                print(f"\nRunning Eval [{eval_id}]: {prompt}")
                latency, response, authors = await run_eval_case(agent, prompt)
                print(f"-> Latency: {latency:.2f}s")
                print(f"-> Sub-Agents: {authors}")
                print(f"-> Response: {response[:150]}...")
                
                model_results.append({
                    "eval_id": eval_id,
                    "prompt": prompt,
                    "expected": expected,
                    "actual": response,
                    "latency_seconds": round(latency, 2),
                    "subagent_authors": authors
                })
            results[f"{model}@{loc}"] = model_results
    finally:
        root_yaml_path.write_text(original_yaml_content)
        
    out_file = Path("eval_comparison_results.json")
    out_file.write_text(json.dumps(results, indent=2))
    print(f"\n✅ Eval run complete! Results saved to {out_file}")

if __name__ == "__main__":
    asyncio.run(main())
