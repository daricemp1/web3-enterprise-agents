"""Benchmark runner comparing Gemini 2.5 Flash (us-central1) vs Gemini 3.5 Flash (global)."""
import asyncio
import json
import os
from pathlib import Path
import sys
import time
from dataclasses import asdict, dataclass
import yaml

agent_parent_dir = Path(__file__).resolve().parents[1] / "domains" / "merchandising" / "agents"
sys.path.insert(0, str(agent_parent_dir))

from google.adk.agents.config_agent_utils import from_config
from google.adk.runners import InMemoryRunner
from google.genai import types

@dataclass
class BenchmarkResult:
    model: str
    location: str
    query_type: str
    query: str
    latency_seconds: float
    response_text: str
    subagent_authors: list[str]

TEST_QUERIES = [
    {
        "type": "BigQuery Analytics",
        "query": "What are the top 3 selling SKUs by revenue in July 2026?"
    },
    {
        "type": "Market Grounding",
        "query": "What are the current retail consumer trends in sustainable outdoor apparel for 2026?"
    },
    {
        "type": "Hybrid Synthesis",
        "query": "Compare our top-performing activewear category sales with current market demand trends."
    }
]

async def run_query(agent, query_text: str) -> tuple[float, str, list[str]]:
    runner = InMemoryRunner(agent=agent, app_name="assortment_planning")
    session = await runner.session_service.create_session(
        app_name="assortment_planning", user_id="benchmarker"
    )
    
    start_time = time.perf_counter()
    events = [
        event
        async for event in runner.run_async(
            user_id="benchmarker",
            session_id=session.id,
            new_message=types.Content(
                role="user", parts=[types.Part(text=query_text)]
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
    results = []
    
    configs = [
        ("gemini-2.5-flash", "us-central1"),
        ("gemini-3.5-flash", "global")
    ]
    
    os.environ["BIGQUERY_PROJECT_ID"] = "india-ce-demos-343207"
    os.environ["GOOGLE_CLOUD_PROJECT"] = "india-ce-demos-343207"
    os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "true"
    
    print("=== Starting Model & Region Migration Benchmark ===")
    
    # Read root_agent.yaml
    root_yaml_path = agent_dir / "root_agent.yaml"
    original_yaml_content = root_yaml_path.read_text()
    
    try:
        for model, loc in configs:
            print(f"\n==========================================")
            print(f"--- Running Config: {model} @ {loc} ---")
            print(f"==========================================")
            os.environ["GOOGLE_CLOUD_LOCATION"] = loc
            os.environ["VERTEXAI_LOCATION"] = loc
            
            # Temporarily configure model in root_agent.yaml for from_config loading
            raw_yaml = yaml.safe_load(original_yaml_content)
            raw_yaml["model"] = model
            root_yaml_path.write_text(yaml.dump(raw_yaml))
            
            agent = from_config(str(root_yaml_path))
            
            for q in TEST_QUERIES:
                print(f"\n[Query Type: {q['type']}]")
                print(f"Prompt: {q['query']}")
                latency, response, authors = await run_query(agent, q["query"])
                print(f"-> Latency: {latency:.2f}s")
                print(f"-> Authors / Sub-Agents: {authors}")
                print(f"-> Response Preview: {response[:150]}...")
                
                results.append(asdict(BenchmarkResult(
                    model=model,
                    location=loc,
                    query_type=q["type"],
                    query=q["query"],
                    latency_seconds=round(latency, 2),
                    response_text=response,
                    subagent_authors=authors
                )))
    finally:
        # Restore original yaml
        root_yaml_path.write_text(original_yaml_content)
        
    out_file = Path("benchmark_results.json")
    out_file.write_text(json.dumps(results, indent=2))
    print(f"\n✅ Benchmark complete! Results saved to {out_file}")

if __name__ == "__main__":
    asyncio.run(main())
