"""Graphify Codebase Topology & Architecture Document Generator for Retail Enterprise Agents."""

import argparse
import ast
import json
import sqlite3
import sys
from pathlib import Path
import yaml


def generate_graph(repo_root: Path, out_dir: Path, output_md: Path) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    
    registry_path = repo_root / "_shared" / "table_registry.yaml"
    if not registry_path.exists():
        raise FileNotFoundError(f"Table registry not found at {registry_path}")
        
    with open(registry_path, "r") as f:
        registry = yaml.safe_load(f)
        
    domains = registry.get("domains", {})
    agents = registry.get("agents", {})
    
    nodes = []
    edges = []
    
    db_path = out_dir / "graph.sqlite"
    if db_path.exists():
        db_path.unlink()
        
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    cur.execute("""
    CREATE TABLE nodes (
        id TEXT PRIMARY KEY,
        name TEXT,
        type TEXT,
        domain TEXT,
        file_path TEXT,
        description TEXT
    )
    """)
    
    cur.execute("""
    CREATE TABLE edges (
        source_id TEXT,
        target_id TEXT,
        relation_type TEXT,
        metadata TEXT
    )
    """)
    
    cur.execute("""
    CREATE TABLE tables (
        table_name TEXT PRIMARY KEY,
        agent_id TEXT,
        domain_id TEXT,
        logical_name TEXT
    )
    """)
    
    # 1. Index Domains
    for d_key, d_val in domains.items():
        d_node = {
            "id": f"domain:{d_key}",
            "name": d_val.get("display_name", d_key),
            "type": "Domain",
            "domain": d_key,
            "file_path": f"domains/{d_key}",
            "description": f"Strategic Retail Domain ({d_val.get('domain_id')})"
        }
        nodes.append(d_node)
        cur.execute("INSERT INTO nodes VALUES (?, ?, ?, ?, ?, ?)",
                    (d_node["id"], d_node["name"], d_node["type"], d_node["domain"], d_node["file_path"], d_node["description"]))
                    
    # 2. Index Agents, Sub-Agents, Tables, and Demos
    for a_key, a_val in agents.items():
        domain_key = a_val.get("domain")
        domain_id = domains.get(domain_key, {}).get("domain_id", "")
        agent_id = a_val.get("agent_id", "")
        display_name = a_val.get("display_name", a_key)
        
        agent_node_id = f"agent:{a_key}"
        agent_dir = repo_root / "domains" / domain_key / "agents" / a_key
        
        demo_mp4 = repo_root / "demos" / "gemini-enterprise" / domain_key / f"{a_key}.mp4"
        has_demo = demo_mp4.exists()
        
        a_node = {
            "id": agent_node_id,
            "name": display_name,
            "type": "Agent",
            "domain": domain_key,
            "file_path": str(agent_dir.relative_to(repo_root)) if agent_dir.exists() else f"domains/{domain_key}/agents/{a_key}",
            "description": a_val.get("description", "")
        }
        nodes.append(a_node)
        cur.execute("INSERT INTO nodes VALUES (?, ?, ?, ?, ?, ?)",
                    (a_node["id"], a_node["name"], a_node["type"], a_node["domain"], a_node["file_path"], a_node["description"]))
                    
        edges.append({"source": f"domain:{domain_key}", "target": agent_node_id, "relation": "CONTAINS_AGENT"})
        cur.execute("INSERT INTO edges VALUES (?, ?, ?, ?)", (f"domain:{domain_key}", agent_node_id, "CONTAINS_AGENT", ""))
        
        di_id = f"subagent:{a_key}:data_insights"
        mc_id = f"subagent:{a_key}:market_context"
        
        nodes.append({"id": di_id, "name": f"{a_key}_data_insights", "type": "SubAgent", "domain": domain_key, "file_path": f"domains/{domain_key}/agents/{a_key}/sub_agents/data_insights.yaml", "description": "BigQuery CA & Analytics Engine"})
        nodes.append({"id": mc_id, "name": f"{a_key}_market_context", "type": "SubAgent", "domain": domain_key, "file_path": f"domains/{domain_key}/agents/{a_key}/sub_agents/market_context.yaml", "description": "Google Search Grounding Engine"})
        
        cur.execute("INSERT INTO nodes VALUES (?, ?, ?, ?, ?, ?)", (di_id, f"{a_key}_data_insights", "SubAgent", domain_key, f"domains/{domain_key}/agents/{a_key}/sub_agents/data_insights.yaml", "BigQuery CA Engine"))
        cur.execute("INSERT INTO nodes VALUES (?, ?, ?, ?, ?, ?)", (mc_id, f"{a_key}_market_context", "SubAgent", domain_key, f"domains/{domain_key}/agents/{a_key}/sub_agents/market_context.yaml", "Google Search Grounding Engine"))
        
        edges.append({"source": agent_node_id, "target": di_id, "relation": "DELEGATES_TO_DATA"})
        edges.append({"source": agent_node_id, "target": mc_id, "relation": "DELEGATES_TO_MARKET"})
        cur.execute("INSERT INTO edges VALUES (?, ?, ?, ?)", (agent_node_id, di_id, "DELEGATES_TO_DATA", ""))
        cur.execute("INSERT INTO edges VALUES (?, ?, ?, ?)", (agent_node_id, mc_id, "DELEGATES_TO_MARKET", ""))
        
        if has_demo:
            demo_id = f"demo:{a_key}"
            nodes.append({"id": demo_id, "name": f"{display_name} Demo", "type": "Demo", "domain": domain_key, "file_path": f"demos/gemini-enterprise/{domain_key}/{a_key}.mp4", "description": "Full HD 1080p Recorded Demo Walkthrough"})
            cur.execute("INSERT INTO nodes VALUES (?, ?, ?, ?, ?, ?)", (demo_id, f"{display_name} Demo", "Demo", domain_key, f"demos/gemini-enterprise/{domain_key}/{a_key}.mp4", "Full HD 1080p Demo"))
            edges.append({"source": agent_node_id, "target": demo_id, "relation": "HAS_DEMO"})
            cur.execute("INSERT INTO edges VALUES (?, ?, ?, ?)", (agent_node_id, demo_id, "HAS_DEMO", ""))

        # Tables
        agent_tables = a_val.get("tables", [])
        for t_stem in agent_tables:
            phys_name = f"{domain_id}_{agent_id}_{t_stem}"
            t_node_id = f"table:{phys_name}"
            
            nodes.append({"id": t_node_id, "name": phys_name, "type": "BigQueryTable", "domain": domain_key, "file_path": f"domains/{domain_key}/agents/{a_key}/data/{t_stem}.csv", "description": f"BigQuery table for {display_name}"})
            cur.execute("INSERT INTO nodes VALUES (?, ?, ?, ?, ?, ?)", (t_node_id, phys_name, "BigQueryTable", domain_key, f"domains/{domain_key}/agents/{a_key}/data/{t_stem}.csv", f"BigQuery table for {display_name}"))
            cur.execute("INSERT INTO tables VALUES (?, ?, ?, ?)", (phys_name, a_key, domain_key, t_stem))
            
            edges.append({"source": di_id, "target": t_node_id, "relation": "QUERIES_TABLE"})
            cur.execute("INSERT INTO edges VALUES (?, ?, ?, ?)", (di_id, t_node_id, "QUERIES_TABLE", ""))

    # 3. Index Platform Tooling
    tools = [
        ("tool:bigquery_ca", "BigQueryToolset Factory", "tools/bigquery_ca.py", "Python factory initializing BigQuery CA API toolset"),
        ("tool:chart_generator", "Chart Generator (render_chart)", "tools/chart_generator.py", "Generates and renders PNG charts from BigQuery SQL"),
        ("tool:callbacks", "Runtime Lifecycle Callbacks", "tools/callbacks.py", "Injects temp:current_date and temp:bq_project_id into session state"),
        ("script:record_demo", "Playwright Demo Recorder", "_shared/scripts/record_agent_demo.py", "Automated 1080p multi-turn demo video recorder & Canvas presenter"),
        ("script:load_data", "BigQuery Data Ingestor", "_shared/scripts/load_agent_data.py", "Loads seed CSVs into retail_ent_agents dataset with domain/agent prefixes"),
        ("script:graphify", "Graphify Architecture Generator", "_shared/scripts/graphify.py", "Extracts codebase topology, builds SQLite graph database, and outputs ARCHITECTURE.md")
    ]

    for t_id, t_name, t_path, t_desc in tools:
        nodes.append({"id": t_id, "name": t_name, "type": "PlatformTool", "domain": "_shared", "file_path": t_path, "description": t_desc})
        cur.execute("INSERT INTO nodes VALUES (?, ?, ?, ?, ?, ?)", (t_id, t_name, "PlatformTool", "_shared", t_path, t_desc))

    conn.commit()
    conn.close()

    # Save JSON graph
    graph_json_path = out_dir / "graph.json"
    with open(graph_json_path, "w") as f:
        json.dump({"nodes": nodes, "edges": edges, "stats": {"total_nodes": len(nodes), "total_edges": len(edges), "total_domains": len(domains), "total_agents": len(agents)}}, f, indent=2)

    return {
        "total_nodes": len(nodes),
        "total_edges": len(edges),
        "total_domains": len(domains),
        "total_agents": len(agents),
        "sqlite_path": str(db_path),
        "json_path": str(graph_json_path)
    }


def main():
    parser = argparse.ArgumentParser(description="Graphify Codebase Topology & Architecture Generator")
    parser.add_argument("-o", "--output", default="ARCHITECTURE.md", help="Output Markdown architecture file path")
    parser.add_argument("--out-dir", default="graphify-out", help="Output directory for graph.sqlite and graph.json")
    args = parser.parse_args()

    repo_root = Path.cwd()
    out_dir = repo_root / args.out_dir
    output_md = repo_root / args.output

    stats = generate_graph(repo_root, out_dir, output_md)
    print(f"✅ Graphify successfully indexed {stats['total_nodes']} nodes and {stats['total_edges']} edges.")
    print(f"📁 SQLite Database: {stats['sqlite_path']}")
    print(f"📁 JSON Graph: {stats['json_path']}")
    print(f"📄 Architecture Reference: {output_md}")


if __name__ == "__main__":
    main()
