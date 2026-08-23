#!/usr/bin/env python3
"""
generate_portal_site.py — Web3 Enterprise Agents Portal Generator
Generates index.html matching 100% pixel-perfect design from retail-enterprise-agents.
"""

import json
from pathlib import Path
import yaml

REPO_ROOT = Path('/usr/local/google/home/daricemahtab/web3-enterprise-agents')

DOMAIN_ICONS = {
    "cex": "🏦",
    "infra": "⚡",
    "defi": "🦄",
}

DOMAIN_TITLES = {
    "cex": "Centralized Exchanges & Trading Domain",
    "infra": "Blockchain Infrastructure & L2 Domain",
    "defi": "Decentralized Finance & Protocols Domain",
}

DOMAIN_DISPLAY_NAMES = {
    "cex": "Centralized Exchanges & Trading",
    "infra": "Blockchain Infrastructure & L2",
    "defi": "Decentralized Finance & Protocols",
}

DOMAIN_ORDER = ["cex", "infra", "defi"]

AGENT_KPIS = {
    "order_book_depth": ["Bid-Ask Spread: < 0.5 bps", "2% Depth: > $10M", "Imbalance: 1.03"],
    "proof_of_reserves": ["Solvency: Over-Collateralized", "BTC Ratio: 104.98%", "Cold Vault: > 90%"],
    "whale_custody_flows": ["Deposit Alert: > $10M", "Hot Wallet: < 10%", "Cold Sweeps: Active"],
    "l2_sequencer_throughput": ["Rollup TPS: > 50 TPS", "Batch Latency: < 2.0s", "Blob Savings: > 90%"],
    "validator_rpc_health": ["RPC Latency: < 35ms", "Attestation: > 99%", "Slash Risk: 0"],
    "mev_arbitrage_radar": ["Sandwich Loss: Tracked", "Builder Bribes: Real-time", "Mempool Bundles"],
    "dex_amm_liquidity": ["Volume/TVL: > 1.0", "Fee APY: > 20%", "IL Loss: < 0.5%"],
    "lending_liquidation_risk": ["Bad Debt: $0.00", "Health Factor: > 1.10", "Liquidation Radar"],
    "yield_staking_optimizer": ["Net APY: > 8%", "LST Staking: > 3.4%", "Peg Discount: < 3 bps"],
    "bridge_outflow_monitor": ["Transfer Velocity: Tracked", "Pool Utilization: < 80%", "Flight Alerts"],
}

def extract_agent_metadata(agent_name: str, domain: str, reg_agent: dict, repo_root: Path) -> dict:
    agent_dir = repo_root / "domains" / domain / "agents" / agent_name
    readme_path = agent_dir / "README.md"
    eval_path = agent_dir / "eval" / "agent.evalset.json"
    
    display_name = reg_agent.get("display_name", agent_name.replace("_", " ").title())
    location = reg_agent.get("location", "us-central1")
    tables = reg_agent.get("tables", [])
    agent_id = reg_agent.get("agent_id", agent_name[:4])
    
    description = f"Autonomous Web3 on-chain reasoning agent for {display_name}."
    prompts = []
    
    if eval_path.exists():
        try:
            eval_json = json.loads(eval_path.read_text(encoding="utf-8"))
            for case in eval_json.get("eval_cases", []):
                conv = case.get("conversation", [])
                if len(conv) >= 1:
                    u = conv[0].get("content", "")
                    if u not in prompts:
                        prompts.append(u)
        except Exception:
            pass
            
    if readme_path.exists():
        content = readme_path.read_text(encoding="utf-8")
        lines = [l.strip() for l in content.splitlines() if l.strip() and not l.strip().startswith("#") and not l.strip().startswith("**Domain:")]
        if lines:
            description = lines[0]
            
    if len(prompts) < 3:
        prompts = [
            f"What are the top quantitative metrics for {display_name} across on-chain activity?",
            f"What are current crypto market benchmarks and protocol best practices for {display_name}?",
            f"Show me a comparison chart visualizing {display_name} performance vs historical benchmark."
        ]
        
    kpis = AGENT_KPIS.get(agent_name, ["On-Chain Grounding: 100%", "Dual Sub-Agents: Active"])
    
    return {
        "id": agent_id,
        "name": agent_name,
        "display_name": display_name,
        "domain": domain,
        "domain_display": DOMAIN_DISPLAY_NAMES.get(domain, domain.upper()),
        "icon": DOMAIN_ICONS.get(domain, "💎"),
        "location": location,
        "description": description,
        "kpis": kpis,
        "prompts": prompts[:3],
        "tables": tables,
        "demo_html": f"demos/gemini-enterprise/{domain}/{agent_name}.html",
        "demo_mp4": f"demos/gemini-enterprise/{domain}/{agent_name}.mp4",
        "readme": f"domains/{domain}/agents/{agent_name}/README.md",
    }


def build_portal_html(agents_data: list[dict]) -> str:
    total_agents = len(agents_data)
    total_domains = len(DOMAIN_ORDER)
    total_tables = sum(len(a.get("tables", [])) for a in agents_data)
    
    domain_counts = {}
    for a in agents_data:
        d = a["domain"]
        domain_counts[d] = domain_counts.get(d, 0) + 1
        
    agents_json = json.dumps(agents_data, indent=2)
    
    return f"""<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Web3 Agent Catalog — 10 Multi-Agent Suite</title>
  <meta name="description" content="Explore 10 specialized Web3 Agent Catalog on-chain analytics, CEX trading, infrastructure & DeFi operations, built on Google ADK, Gemini Enterprise, and BigQuery Conversational Analytics.">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500;600;700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  
  <script>
    (function() {{
      const savedTheme = localStorage.getItem('web3_agents_theme') || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
      document.documentElement.setAttribute('data-theme', savedTheme);
    }})();
  </script>

  <style>
    :root, [data-theme="dark"] {{
      --bg-primary: #0f172a;
      --bg-secondary: #1e293b;
      --bg-card: #1e293b;
      --bg-card-hover: #243248;
      --bg-surface: #0f172a;
      --bg-input: #0f172a;
      --border-color: #334155;
      --border-faint: rgba(255, 255, 255, 0.14);
      --border-focus: #38bdf8;
      --text-primary: #f8fafc;
      --text-secondary: #94a3b8;
      --text-muted: #64748b;
      --accent-blue: #38bdf8;
      --accent-blue-hover: #0284c7;
      --accent-indigo: #818cf8;
      --accent-emerald: #34d399;
      --badge-bg: rgba(56, 189, 248, 0.12);
      --badge-border: rgba(56, 189, 248, 0.28);
      --badge-text: #38bdf8;
      --kpi-bg: rgba(52, 211, 153, 0.1);
      --kpi-border: rgba(52, 211, 153, 0.25);
      --kpi-text: #34d399;
      --region-bg: rgba(129, 140, 248, 0.12);
      --region-border: rgba(129, 140, 248, 0.28);
      --region-text: #a5b4fc;
      --shadow-card: 0 10px 25px -5px rgba(0, 0, 0, 0.4);
      --shadow-modal: 0 25px 50px -12px rgba(0, 0, 0, 0.7);
      --modal-overlay: rgba(15, 23, 42, 0.85);
    }}

    [data-theme="light"] {{
      --bg-primary: #f8fafc;
      --bg-secondary: #ffffff;
      --bg-card: #ffffff;
      --bg-card-hover: #f8fafc;
      --bg-surface: #f1f5f9;
      --bg-input: #ffffff;
      --border-color: #cbd5e1;
      --border-faint: #cbd5e1;
      --border-focus: #0284c7;
      --text-primary: #0f172a;
      --text-secondary: #475569;
      --text-muted: #64748b;
      --accent-blue: #0284c7;
      --accent-blue-hover: #0369a1;
      --accent-indigo: #6366f1;
      --accent-emerald: #059669;
      --badge-bg: #e0f2fe;
      --badge-border: #bae6fd;
      --badge-text: #0284c7;
      --kpi-bg: #d1fae5;
      --kpi-border: #a7f3d0;
      --kpi-text: #065f46;
      --region-bg: #e0e7ff;
      --region-border: #c7d2fe;
      --region-text: #4338ca;
      --shadow-card: 0 4px 6px -1px rgba(0, 0, 0, 0.07);
      --shadow-modal: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
      --modal-overlay: rgba(15, 23, 42, 0.6);
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: 'Inter', sans-serif;
      background-color: var(--bg-primary);
      color: var(--text-primary);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      line-height: 1.5;
    }}
    .site-header {{
      background: var(--bg-secondary);
      border-bottom: 1px solid var(--border-color);
      position: sticky;
      top: 0;
      z-index: 40;
      backdrop-filter: blur(8px);
    }}
    .header-inner {{
      max-width: 1360px;
      margin: 0 auto;
      padding: 14px 24px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 16px;
    }}
    .brand-logo {{ display: flex; align-items: center; gap: 12px; text-decoration: none; color: var(--text-primary); }}
    .brand-icon {{ font-size: 1.6rem; }}
    .brand-title {{ font-family: 'Google Sans', sans-serif; font-size: 1.15rem; font-weight: 700; color: var(--text-primary); }}
    .brand-subtitle {{ font-size: 0.75rem; color: var(--text-secondary); font-weight: 500; }}
    .header-actions {{ display: flex; align-items: center; gap: 10px; }}
    .btn-header {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 8px 14px;
      border-radius: 8px;
      font-size: 0.85rem;
      font-weight: 600;
      cursor: pointer;
      text-decoration: none;
      border: 1px solid var(--border-color);
      background: var(--bg-card);
      color: var(--text-primary);
      transition: all 0.15s ease;
    }}
    .btn-header:hover {{ background: var(--bg-surface); border-color: var(--border-focus); color: var(--accent-blue); }}
    .btn-primary-header {{ background: var(--accent-blue); color: #0f172a !important; border-color: var(--accent-blue); font-weight: 700; }}
    .hero {{ padding: 48px 24px 32px; max-width: 1360px; margin: 0 auto; width: 100%; text-align: center; }}
    .hero-pill {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 6px 14px;
      border-radius: 9999px;
      background: var(--badge-bg);
      border: 1px solid var(--badge-border);
      color: var(--badge-text);
      font-size: 0.85rem;
      font-weight: 600;
      margin-bottom: 20px;
    }}
    .hero-title {{ font-family: 'Google Sans', sans-serif; font-size: 2.75rem; font-weight: 700; margin-bottom: 16px; }}
    .hero-title span {{ background: linear-gradient(135deg, var(--accent-blue) 0%, var(--accent-indigo) 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
    .hero-desc {{ max-width: 780px; margin: 0 auto 36px; font-size: 1.05rem; color: var(--text-secondary); line-height: 1.6; }}
    .stat-row {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 16px; max-width: 1000px; margin: 0 auto 40px; }}
    .stat-card {{ background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 12px; padding: 16px 20px; text-align: center; }}
    .stat-number {{ font-family: 'Google Sans', sans-serif; font-size: 1.75rem; font-weight: 700; color: var(--accent-blue); }}
    .stat-label {{ font-size: 0.8rem; color: var(--text-secondary); margin-top: 4px; font-weight: 500; }}
    .main-container {{ max-width: 1360px; margin: 0 auto; padding: 24px; width: 100%; flex: 1; }}
    .toolbar {{ background: var(--bg-secondary); border: 1px solid var(--border-faint); border-radius: 14px; padding: 18px; margin-bottom: 28px; box-shadow: var(--shadow-card); }}
    .search-row {{ display: flex; gap: 12px; margin-bottom: 16px; position: relative; }}
    .search-input-wrapper {{ position: relative; flex: 1; }}
    .search-icon {{ position: absolute; left: 14px; top: 50%; transform: translateY(-50%); color: var(--text-muted); font-size: 1rem; pointer-events: none; }}
    .search-input {{ width: 100%; background: var(--bg-input); border: 1px solid var(--border-faint); border-radius: 10px; padding: 12px 14px 12px 42px; font-size: 0.95rem; color: var(--text-primary); font-family: inherit; outline: none; }}
    .search-input:focus {{ border-color: var(--border-focus); box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.2); }}
    .search-clear {{ position: absolute; right: 12px; top: 50%; transform: translateY(-50%); background: none; border: none; color: var(--text-muted); cursor: pointer; font-size: 1rem; padding: 4px; display: none; }}
    .domain-pills {{ display: flex; gap: 8px; flex-wrap: wrap; }}
    .domain-btn {{ background: var(--bg-surface); border: 1px solid var(--border-faint); color: var(--text-secondary); padding: 8px 14px; border-radius: 9999px; font-size: 0.85rem; font-weight: 600; cursor: pointer; display: inline-flex; align-items: center; gap: 6px; }}
    .domain-btn.active {{ background: var(--accent-blue); color: #0f172a; border-color: var(--accent-blue); font-weight: 700; }}
    .domain-count {{ font-size: 0.72rem; padding: 2px 6px; border-radius: 9999px; background: rgba(0, 0, 0, 0.15); font-family: 'JetBrains Mono', monospace; }}
    .results-bar {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; padding: 0 4px; }}
    .results-count {{ font-size: 0.9rem; font-weight: 600; color: var(--text-secondary); }}
    .agent-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(390px, 1fr)); gap: 20px; }}
    .agent-card {{
      background: var(--bg-card);
      border: 1px solid var(--border-faint);
      border-radius: 14px;
      padding: 22px;
      display: flex;
      flex-direction: column;
      box-shadow: var(--shadow-card);
      transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
      position: relative;
    }}
    .agent-card:hover {{ transform: translateY(-3px); border-color: var(--border-focus); box-shadow: 0 14px 30px -8px rgba(0, 0, 0, 0.35); }}
    .card-top {{ display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px; gap: 8px; }}
    .card-badges {{ display: flex; gap: 6px; flex-wrap: wrap; }}
    .badge-domain {{ display: inline-flex; align-items: center; gap: 4px; font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.04em; padding: 3px 8px; border-radius: 6px; background: var(--badge-bg); border: 1px solid var(--badge-border); color: var(--badge-text); }}
    .badge-region {{ display: inline-flex; align-items: center; gap: 4px; font-size: 0.7rem; font-weight: 700; padding: 3px 8px; border-radius: 6px; background: var(--region-bg); border: 1px solid var(--region-border); color: var(--region-text); font-family: 'JetBrains Mono', monospace; }}
    .card-title {{ font-family: 'Google Sans', sans-serif; font-size: 1.2rem; font-weight: 700; color: var(--text-primary); margin-bottom: 8px; line-height: 1.35; }}
    .card-desc {{ font-size: 0.88rem; color: var(--text-secondary); line-height: 1.5; margin-bottom: 16px; flex: 1; display: -webkit-box; -webkit-line-clamp: 4; -webkit-box-orient: vertical; overflow: hidden; }}
    .kpi-row {{ display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 16px; }}
    .kpi-pill {{ font-size: 0.72rem; font-weight: 600; padding: 3px 8px; border-radius: 6px; background: var(--kpi-bg); border: 1px solid var(--kpi-border); color: var(--kpi-text); display: inline-flex; align-items: center; gap: 4px; }}
    .prompts-container {{ border-top: 1px solid var(--border-color); padding-top: 12px; margin-bottom: 16px; }}
    .prompts-toggle {{ background: none; border: none; color: var(--text-secondary); font-size: 0.78rem; font-weight: 600; display: flex; align-items: center; justify-content: space-between; width: 100%; cursor: pointer; padding: 2px 0; }}
    .prompts-toggle:hover {{ color: var(--accent-blue); }}
    .prompts-list {{ margin-top: 8px; display: none; flex-direction: column; gap: 6px; }}
    .prompts-list.open {{ display: flex; }}
    .prompt-item {{ font-size: 0.78rem; color: var(--text-secondary); background: var(--bg-surface); padding: 6px 10px; border-radius: 6px; border-left: 3px solid var(--accent-indigo); line-height: 1.4; font-style: italic; }}
    .card-actions {{ display: flex; gap: 8px; align-items: center; margin-top: auto; padding-top: 14px; border-top: 1px solid var(--border-color); }}
    .btn-watch {{ flex: 1; display: inline-flex; align-items: center; justify-content: center; gap: 6px; background: var(--accent-blue); color: #0f172a; padding: 9px 14px; border-radius: 8px; font-size: 0.85rem; font-weight: 700; border: none; cursor: pointer; transition: all 0.15s ease; }}
    .btn-watch:hover {{ background: var(--accent-blue-hover); color: #ffffff; transform: translateY(-1px); }}
    .btn-showcase {{ display: inline-flex; align-items: center; justify-content: center; gap: 4px; background: var(--bg-surface); color: var(--text-primary); padding: 9px 12px; border-radius: 8px; font-size: 0.82rem; font-weight: 600; text-decoration: none; border: 1px solid var(--border-color); transition: all 0.15s ease; }}
    .btn-showcase:hover {{ border-color: var(--border-focus); color: var(--accent-blue); }}
    .btn-doc {{ display: inline-flex; align-items: center; justify-content: center; background: none; color: var(--text-muted); padding: 8px; border-radius: 8px; font-size: 1rem; text-decoration: none; border: 1px solid transparent; transition: all 0.15s ease; }}
    .btn-doc:hover {{ color: var(--text-primary); border-color: var(--border-color); background: var(--bg-surface); }}
    .no-results {{ grid-column: 1 / -1; text-align: center; padding: 60px 20px; background: var(--bg-card); border: 1px dashed var(--border-color); border-radius: 14px; display: none; }}
    .no-results-icon {{ font-size: 3rem; margin-bottom: 12px; }}
    
    /* Video Modal Styles matching Screenshots 1 & 2 */
    .modal-backdrop {{ position: fixed; inset: 0; background: var(--modal-overlay); z-index: 100; display: none; align-items: center; justify-content: center; padding: 20px; backdrop-filter: blur(6px); }}
    .modal-dialog {{ background: var(--bg-card); border: 1px solid var(--border-faint); border-radius: 16px; width: 100%; max-width: 900px; max-height: 90vh; display: flex; flex-direction: column; box-shadow: var(--shadow-modal); overflow: hidden; }}
    .modal-header {{ padding: 18px 24px; border-bottom: 1px solid var(--border-color); display: flex; justify-content: space-between; align-items: center; }}
    .modal-body {{ padding: 24px; overflow-y: auto; display: flex; flex-direction: column; gap: 18px; }}
    .modal-video-wrapper {{ width: 100%; background: #000; border-radius: 10px; overflow: hidden; border: 1px solid var(--border-faint); }}
    .modal-video {{ width: 100%; display: block; max-height: 480px; }}
    .modal-meta-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px; background: var(--bg-surface); border: 1px solid var(--border-faint); border-radius: 10px; padding: 14px; }}
    .modal-meta-item {{ display: flex; flex-direction: column; gap: 4px; }}
    .modal-meta-label {{ font-size: 0.72rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600; }}
    .modal-meta-value {{ font-size: 0.85rem; font-weight: 600; color: var(--text-primary); }}
    .modal-sequence-box {{ background: var(--bg-surface); border: 1px solid var(--border-faint); border-radius: 10px; padding: 16px; }}
    .modal-sequence-title {{ font-family: 'Google Sans', sans-serif; font-size: 0.95rem; font-weight: 700; color: var(--accent-indigo); margin-bottom: 10px; display: flex; align-items: center; gap: 6px; }}
    .modal-turns-list {{ list-style: none; display: flex; flex-direction: column; gap: 8px; font-size: 0.85rem; color: var(--text-secondary); }}
    .modal-turns-list strong {{ color: var(--text-primary); }}
    .modal-footer {{ padding: 16px 24px; border-top: 1px solid var(--border-color); display: flex; justify-content: flex-end; align-items: center; gap: 10px; }}
    .modal-close {{ background: none; border: none; font-size: 1.4rem; color: var(--text-muted); cursor: pointer; }}
    .btn-download {{ display: inline-flex; align-items: center; gap: 6px; background: var(--bg-surface); border: 1px solid var(--border-color); color: var(--text-primary); padding: 9px 14px; border-radius: 8px; font-size: 0.85rem; font-weight: 600; text-decoration: none; cursor: pointer; }}
    .btn-download:hover {{ border-color: var(--border-focus); color: var(--accent-blue); }}
    .btn-open-showcase {{ display: inline-flex; align-items: center; gap: 6px; background: var(--accent-blue); color: #0f172a !important; border: 1px solid var(--accent-blue); padding: 9px 16px; border-radius: 8px; font-size: 0.85rem; font-weight: 700; text-decoration: none; }}
    .btn-open-showcase:hover {{ background: var(--accent-blue-hover); color: #ffffff !important; }}
    .site-footer {{ background: var(--bg-secondary); border-top: 1px solid var(--border-color); padding: 36px 24px; text-align: center; margin-top: auto; }}
    .footer-text {{ font-size: 0.85rem; color: var(--text-secondary); }}
  </style>
</head>
<body>

  <!-- Global Header -->
  <header class="site-header">
    <div class="header-inner">
      <a href="index.html" class="brand-logo">
        <span class="brand-icon">🌐</span>
        <div class="brand-text">
          <span class="brand-title">Web3 Agent Catalog</span>
          <span class="brand-subtitle">Autonomous Multi-Agent Intelligence Platform</span>
        </div>
      </a>
      <div class="header-actions">
        <button id="archBtn" class="btn-header"><span>📐</span> Architecture Blueprint</button>
        <button id="themeToggleBtn" class="btn-header"><span id="themeIcon">☀️</span> <span id="themeText">Light</span></button>
      </div>
    </div>
  </header>

  <!-- Hero Section -->
  <section class="hero">
    <div class="hero-pill">
      <span>🚀</span> 10 Enterprise Web3 Agents Fully Deployed across 3 Domains
    </div>
    <h1 class="hero-title">
      Web3 Enterprise <span>Agents Catalog</span>
    </h1>
    <p class="hero-desc">
      A declarative, multi-agent platform powered by Google Agent Development Kit (ADK), Vertex AI, and BigQuery Conversational Analytics. Real-time quantitative querying against on-chain datasets, grounded with external Google Search market intelligence.
    </p>

    <!-- Platform Stats -->
    <div class="stat-row">
      <div class="stat-card">
        <div class="stat-number">{total_agents}</div>
        <div class="stat-label">Web3 Agents</div>
      </div>
      <div class="stat-card">
        <div class="stat-number">{total_domains}</div>
        <div class="stat-label">Strategic Web3 Domains</div>
      </div>
      <div class="stat-card">
        <div class="stat-number">{total_tables}</div>
        <div class="stat-label">BigQuery Tables</div>
      </div>
      <div class="stat-card">
        <div class="stat-number">gemini-3.5-flash</div>
        <div class="stat-label">Core Reasoning LLM</div>
      </div>
    </div>
  </section>

  <!-- Main Content Area -->
  <main class="main-container">
    
    <!-- Toolbar: Search & Domain Filters -->
    <section class="toolbar">
      <div class="search-row">
        <div class="search-input-wrapper">
          <span class="search-icon">🔍</span>
          <input type="text" id="searchInput" class="search-input" placeholder="Search 10 agents by name, KPI (e.g. TPS, APY, TVL), question, or BigQuery table..." autocomplete="off">
          <button id="searchClear" class="search-clear">✕</button>
        </div>
      </div>

      <!-- Domain Pills -->
      <div class="domain-pills" id="domainPills">
        <button class="domain-btn active" data-domain="all">
          <span>🌐</span> All Domains <span class="domain-count">{total_agents}</span>
        </button>
        {"".join([f'''<button class="domain-btn" data-domain="{d}">
          <span>{DOMAIN_ICONS[d]}</span> {DOMAIN_DISPLAY_NAMES[d]} <span class="domain-count">{domain_counts.get(d, 0)}</span>
        </button>''' for d in DOMAIN_ORDER])}
      </div>
    </section>

    <!-- Results Header -->
    <div class="results-bar">
      <div class="results-count" id="resultsCount">
        Showing <strong>{total_agents}</strong> of {total_agents} enterprise agents
      </div>
    </div>

    <!-- Agent Grid -->
    <div class="agent-grid" id="agentGrid">
      <!-- Injected via JavaScript -->
    </div>

    <!-- No Results Fallback -->
    <div class="no-results" id="noResults">
      <div class="no-results-icon">🔎</div>
      <div style="font-size: 1.25rem; font-weight: 700; margin-bottom: 8px;">No Matching Web3 Agents Found</div>
      <p style="color: var(--text-secondary);">Try refining your search keyword or switching domain filter tabs.</p>
    </div>

  </main>

  <!-- Architecture Modal -->
  <div class="modal-backdrop" id="archModal">
    <div class="modal-dialog" style="max-width: 800px;">
      <div class="modal-header">
        <h2 style="font-family: 'Google Sans'; font-size: 1.25rem;">📐 Web3 Enterprise Multi-Agent Architecture</h2>
        <button class="modal-close" id="archClose">✕</button>
      </div>
      <div class="modal-body">
        <div style="background: var(--bg-surface); padding: 16px; border-radius: 8px; border: 1px solid var(--border-color);">
          <h3 style="color: var(--accent-blue); margin-bottom: 8px;">Tier 1: Presentation & Orchestration</h3>
          <p style="font-size: 0.9rem; color: var(--text-secondary);">Web3 Agent UI routes user prompts to root <code>LlmAgent</code> (powered by <code>gemini-3.5-flash</code>).</p>
        </div>
        <div style="background: var(--bg-surface); padding: 16px; border-radius: 8px; border: 1px solid var(--border-color);">
          <h3 style="color: var(--accent-indigo); margin-bottom: 8px;">Tier 2: Dual Sub-Agent Reasoning</h3>
          <p style="font-size: 0.9rem; color: var(--text-secondary);">• <strong>Data Insights Sub-Agent:</strong> BigQuery Conversational Analytics API (NL-to-SQL, forecasting, anomalies).<br>• <strong>Market Context Sub-Agent:</strong> Google Search grounding for live token prices & protocol news.</p>
        </div>
        <div style="background: var(--bg-surface); padding: 16px; border-radius: 8px; border: 1px solid var(--border-color);">
          <h3 style="color: var(--accent-emerald); margin-bottom: 8px;">Tier 3: Enterprise Web3 Data Lakehouse</h3>
          <p style="font-size: 0.9rem; color: var(--text-secondary);">GCP BigQuery project <code>gcda-apac-sc.web3_enterprise_agents</code> hosting 20 partitioned tables across CEX, INFRA, and DEFI.</p>
        </div>
      </div>
      <div class="modal-footer">
        <button class="btn-header btn-primary-header" id="archOk">Close Blueprint</button>
      </div>
    </div>
  </div>

  <!-- Video Modal (Screenshots 1 & 2) -->
  <div class="modal-backdrop" id="videoModal">
    <div class="modal-dialog">
      <div class="modal-header">
        <div style="display: flex; align-items: center; gap: 10px;">
          <h2 id="modalAgentTitle" style="font-family: 'Google Sans'; font-size: 1.25rem;">Agent Demo</h2>
          <span id="modalDomainBadge" class="badge-domain"></span>
          <span id="modalRegionBadge" class="badge-region"></span>
        </div>
        <button class="modal-close" id="modalCloseBtn">✕</button>
      </div>
      <div class="modal-body">
        
        <!-- Video Player -->
        <div class="modal-video-wrapper">
          <video id="modalVideo" class="modal-video" controls autoplay muted playsinline preload="auto">
            <source src="" type="video/mp4">
            Your browser does not support HTML5 video.
          </video>
        </div>

        <!-- Meta Grid -->
        <div class="modal-meta-grid">
          <div class="modal-meta-item">
            <span class="modal-meta-label">Resolution</span>
            <span class="modal-meta-value">1080p Full HD (1920×1080)</span>
          </div>
          <div class="modal-meta-item">
            <span class="modal-meta-label">Model Reasoning</span>
            <span class="modal-meta-value">Gemini 3.5 Flash (Global)</span>
          </div>
          <div class="modal-meta-item">
            <span class="modal-meta-label">Platform UI</span>
            <span class="modal-meta-value">Web3 Agent Platform</span>
          </div>
          <div class="modal-meta-item">
            <span class="modal-meta-label">Data Execution</span>
            <span class="modal-meta-value">BigQuery Conversational Analytics</span>
          </div>
        </div>

        <!-- Demonstration Workflow Sequence -->
        <div class="modal-sequence-box">
          <div class="modal-sequence-title">🎬 Demonstration Workflow Sequence</div>
          <ul class="modal-turns-list" id="modalTurnsList">
            <!-- Injected via JavaScript -->
          </ul>
        </div>

      </div>
      <div class="modal-footer">
        <a id="modalDownloadBtn" href="#" download class="btn-download">⬇ Download MP4</a>
        <a id="modalShowcaseBtn" href="#" target="_blank" class="btn-open-showcase">🚀 Open Full Showcase Player</a>
      </div>
    </div>
  </div>

  <!-- Site Footer -->
  <footer class="site-footer">
    <p class="footer-text">
      10 Enterprise Agents across 3 Strategic Web3 Domains (CEX, INFRA, DEFI). Powered by Google ADK, Vertex AI, and BigQuery.
    </p>
  </footer>

  <!-- Client Script -->
  <script>
    const AGENTS_DATA = {agents_json};

    let activeDomain = 'all';
    let searchQuery = '';

    const searchInput = document.getElementById('searchInput');
    const searchClear = document.getElementById('searchClear');
    const domainPills = document.getElementById('domainPills');
    const agentGrid = document.getElementById('agentGrid');
    const noResults = document.getElementById('noResults');
    const resultsCount = document.getElementById('resultsCount');
    const themeToggleBtn = document.getElementById('themeToggleBtn');
    const themeIcon = document.getElementById('themeIcon');
    const themeText = document.getElementById('themeText');

    // Modals
    const archModal = document.getElementById('archModal');
    const archBtn = document.getElementById('archBtn');
    const archClose = document.getElementById('archClose');
    const archOk = document.getElementById('archOk');

    const videoModal = document.getElementById('videoModal');
    const modalVideo = document.getElementById('modalVideo');
    const modalAgentTitle = document.getElementById('modalAgentTitle');
    const modalDomainBadge = document.getElementById('modalDomainBadge');
    const modalRegionBadge = document.getElementById('modalRegionBadge');
    const modalTurnsList = document.getElementById('modalTurnsList');
    const modalDownloadBtn = document.getElementById('modalDownloadBtn');
    const modalShowcaseBtn = document.getElementById('modalShowcaseBtn');
    const modalCloseBtn = document.getElementById('modalCloseBtn');

    archBtn.onclick = () => archModal.style.display = 'flex';
    archClose.onclick = () => archModal.style.display = 'none';
    archOk.onclick = () => archModal.style.display = 'none';

    modalCloseBtn.onclick = () => {{
      videoModal.style.display = 'none';
      modalVideo.pause();
    }};

    window.onclick = (e) => {{
      if (e.target === archModal) archModal.style.display = 'none';
      if (e.target === videoModal) {{
        videoModal.style.display = 'none';
        modalVideo.pause();
      }}
    }};

    function openVideoModal(agentName) {{
      const agent = AGENTS_DATA.find(a => a.name === agentName);
      if (!agent) return;

      modalAgentTitle.textContent = `${{agent.icon}} ${{agent.display_name}}`;
      modalDomainBadge.textContent = agent.domain_display;
      modalRegionBadge.textContent = agent.location;
      
      modalVideo.src = agent.demo_mp4;
      modalVideo.play().catch(() => {{}});
      
      modalDownloadBtn.href = agent.demo_mp4;
      modalShowcaseBtn.href = agent.demo_html;

      modalTurnsList.innerHTML = `
        <li><strong>Turn 1 (Data Insights):</strong> "${{agent.prompts[0] || 'Analyze on-chain transaction metrics.'}}"</li>
        <li><strong>Turn 2 (Market Grounding):</strong> "${{agent.prompts[1] || 'Compare against crypto industry benchmarks.'}}"</li>
        <li><strong>Turn 3 (Visual Analytics):</strong> "${{agent.prompts[2] || 'Render comparison chart artifact.'}}"</li>
        <li><strong>Turn 4 (Canvas Presentation):</strong> Executive briefing generated in interactive Canvas mode.</li>
      `;

      videoModal.style.display = 'flex';
    }}

    function togglePrompts(btn) {{
      const list = btn.nextElementSibling;
      const icon = btn.querySelector('.toggle-icon');
      if (list.classList.contains('open')) {{
        list.classList.remove('open');
        icon.textContent = '▼';
      }} else {{
        list.classList.add('open');
        icon.textContent = '▲';
      }}
    }}

    function htmlEscape(str) {{
      if (!str) return '';
      return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;');
    }}

    function renderAgents() {{
      const query = searchQuery.toLowerCase().trim();
      const filtered = AGENTS_DATA.filter(agent => {{
        const matchesDomain = activeDomain === 'all' || agent.domain === activeDomain;
        if (!matchesDomain) return false;
        if (!query) return true;

        const textPool = [
          agent.display_name,
          agent.name,
          agent.domain_display,
          agent.description,
          agent.location,
          ...(agent.kpis || []),
          ...(agent.prompts || []),
          ...(agent.tables || [])
        ].join(' ').toLowerCase();

        return textPool.includes(query);
      }});

      resultsCount.innerHTML = `Showing <strong>${{filtered.length}}</strong> of ${{AGENTS_DATA.length}} enterprise agents`;

      if (filtered.length === 0) {{
        agentGrid.innerHTML = '';
        noResults.style.display = 'block';
        return;
      }}

      noResults.style.display = 'none';

      agentGrid.innerHTML = filtered.map(agent => {{
        const kpiPills = (agent.kpis || []).map(kpi => 
          `<span class="kpi-pill">🎯 ${{htmlEscape(kpi)}}</span>`
        ).join('');

        const promptItems = (agent.prompts || []).map((prompt) => 
          `<div class="prompt-item">"${{htmlEscape(prompt)}}"</div>`
        ).join('');

        return `
          <div class="agent-card" data-agent-id="${{agent.id}}">
            <div class="card-top">
              <div class="card-badges">
                <span class="badge-domain">${{agent.icon}} ${{htmlEscape(agent.domain_display)}}</span>
                <span class="badge-region">${{agent.location}}</span>
              </div>
            </div>
            <h3 class="card-title">${{htmlEscape(agent.display_name)}}</h3>
            <p class="card-desc">${{htmlEscape(agent.description)}}</p>

            ${{kpiPills ? `<div class="kpi-row">${{kpiPills}}</div>` : ''}}

            ${{promptItems ? `
              <div class="prompts-container">
                <button class="prompts-toggle" onclick="togglePrompts(this)">
                  <span>💬 Sample Business Questions (${{agent.prompts.length}})</span>
                  <span class="toggle-icon">▼</span>
                </button>
                <div class="prompts-list">
                  ${{promptItems}}
                </div>
              </div>
            ` : ''}}

            <div class="card-actions">
              <button class="btn-watch" onclick="openVideoModal('${{agent.name}}')">
                <span>🎬</span> Watch Demo
              </button>
              <a href="${{agent.demo_html}}" target="_blank" rel="noopener noreferrer" class="btn-showcase" title="Open Dedicated Showcase Player">
                <span>📄</span> Showcase
              </a>
              <a href="${{agent.readme}}" target="_blank" rel="noopener noreferrer" class="btn-doc" title="View Technical README">
                <span>📖</span>
              </a>
            </div>
          </div>
        `;
      }}).join('');
    }}

    searchInput.addEventListener('input', (e) => {{
      searchQuery = e.target.value;
      searchClear.style.display = searchQuery ? 'block' : 'none';
      renderAgents();
    }});

    searchClear.addEventListener('click', () => {{
      searchInput.value = '';
      searchQuery = '';
      searchClear.style.display = 'none';
      renderAgents();
      searchInput.focus();
    }});

    domainPills.addEventListener('click', (e) => {{
      const btn = e.target.closest('.domain-btn');
      if (!btn) return;
      document.querySelectorAll('.domain-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      activeDomain = btn.dataset.domain;
      renderAgents();
    }});

    function updateThemeUI(theme) {{
      if (theme === 'dark') {{
        themeIcon.textContent = '☀️';
        themeText.textContent = 'Light';
      }} else {{
        themeIcon.textContent = '🌙';
        themeText.textContent = 'Dark';
      }}
    }}

    themeToggleBtn.addEventListener('click', () => {{
      const current = document.documentElement.getAttribute('data-theme') || 'dark';
      const next = current === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', next);
      localStorage.setItem('web3_agents_theme', next);
      updateThemeUI(next);
    }});

    updateThemeUI(document.documentElement.getAttribute('data-theme') || 'dark');
    renderAgents();
  </script>
</body>
</html>
"""

def main():
    repo_root = REPO_ROOT
    registry_file = repo_root / "_shared" / "table_registry.yaml"
    with open(registry_file, "r", encoding="utf-8") as f:
        reg_data = yaml.safe_load(f)
        
    agents_map = reg_data.get("agents", {})
    agents_data = []
    
    for agent_name, reg_agent in agents_map.items():
        domain = reg_agent.get("domain", "defi")
        meta = extract_agent_metadata(agent_name, domain, reg_agent, repo_root)
        agents_data.append(meta)
        
    html_output = build_portal_html(agents_data)
    (repo_root / "index.html").write_text(html_output, encoding="utf-8")
    print(f"✓ Generated complete index.html with {len(agents_data)} agents across {len(DOMAIN_ORDER)} domains!")

if __name__ == "__main__":
    main()
