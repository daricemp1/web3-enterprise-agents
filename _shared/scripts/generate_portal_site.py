#!/usr/bin/env python3
"""Generates the single-page responsive Web3 Agent Catalog with full parity to retail-enterprise-agents."""

import json
import yaml
from pathlib import Path

REPO_ROOT = Path('/usr/local/google/home/daricemahtab/web3-enterprise-agents')

DOMAIN_ORDER = ["cex", "infra", "defi"]

DOMAIN_NAMES = {
    "cex": "Centralized Exchanges & Trading",
    "infra": "Blockchain Infrastructure & L2",
    "defi": "Decentralized Finance & Protocols",
}

DOMAIN_ICONS = {
    "cex": "🏦",
    "infra": "⚡",
    "defi": "🦄",
}

DOMAIN_BADGE_SHORT = {
    "cex": "🏦 CEX",
    "infra": "⚡ INFRA",
    "defi": "🦄 DEFI",
}

DOMAIN_COLORS = {
    "cex": "#38bdf8",
    "infra": "#818cf8",
    "defi": "#34d399",
}


def load_all_agents():
    registry_file = REPO_ROOT / "_shared" / "table_registry.yaml"
    with open(registry_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    raw_agents = data.get("agents", {})
    agents_list = []

    for name, agent in raw_agents.items():
        domain = agent.get("domain", "defi")
        display_name = agent.get("display_name", name.replace("_", " ").title())
        description = agent.get("description", "")
        
        # Load sample prompts
        agent_dir = REPO_ROOT / "domains" / domain / "agents" / name
        eval_file = agent_dir / "eval" / "agent.evalset.json"
        prompts = []
        if eval_file.exists():
            try:
                eval_data = json.loads(eval_file.read_text(encoding="utf-8"))
                for case in eval_data.get("eval_cases", []):
                    conv = case.get("conversation", [])
                    if conv and len(conv) >= 1:
                        prompts.append(conv[0].get("content", ""))
            except Exception:
                pass

        if len(prompts) < 3:
            prompts = [
                f"What are the top quantitative metrics for {display_name} across on-chain activity?",
                f"What are current crypto market benchmarks and protocol best practices for {display_name}?",
                f"Show me a comparison chart visualizing {display_name} performance vs historical benchmark.",
            ]

        agents_list.append(
            format_agent_entry(name, agent, domain, display_name, description, prompts)
        )

    agents_list.sort(key=lambda a: (DOMAIN_ORDER.index(a["domain"]) if a["domain"] in DOMAIN_ORDER else 99, a["name"]))
    return agents_list


def format_agent_entry(agent_name, agent, domain, display_name, description, prompts):
    clean_title = display_name.split(":")[-1].strip() if ":" in display_name else display_name
    return {
        "id": agent_name[:8],
        "name": agent_name,
        "display_name": display_name,
        "clean_title": clean_title,
        "domain": domain,
        "domain_display": DOMAIN_NAMES.get(domain, domain.upper()),
        "domain_badge_short": DOMAIN_BADGE_SHORT.get(domain, domain.upper()),
        "icon": DOMAIN_ICONS.get(domain, "💎"),
        "color": DOMAIN_COLORS.get(domain, "#38bdf8"),
        "location": "us-central1",
        "description": description,
        "prompts": prompts[:3],
        "tables": agent.get("tables", []),
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
  <meta name="description" content="Explore 10 specialized Web3 Agents for on-chain analytics, CEX trading, infrastructure & DeFi operations, built on Google ADK, Vertex AI, and BigQuery Conversational Analytics.">
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
      --bg-primary: #0b1120;
      --bg-secondary: #111c30;
      --bg-card: #152238;
      --bg-card-hover: #1c2c47;
      --bg-surface: #0b1120;
      --bg-input: #0b1120;
      --border-color: #23334d;
      --border-faint: rgba(255, 255, 255, 0.08);
      --border-focus: #38bdf8;
      --text-primary: #f8fafc;
      --text-secondary: #94a3b8;
      --text-muted: #64748b;
      --accent-blue: #38bdf8;
      --accent-blue-hover: #0ea5e9;
      --accent-indigo: #818cf8;
      --accent-emerald: #34d399;
      --badge-bg: rgba(45, 212, 191, 0.12);
      --badge-border: rgba(45, 212, 191, 0.28);
      --badge-text: #2dd4bf;
      --region-bg: rgba(167, 139, 250, 0.12);
      --region-border: rgba(167, 139, 250, 0.28);
      --region-text: #a78bfa;
      --shadow-card: 0 10px 25px -5px rgba(0, 0, 0, 0.4);
      --shadow-modal: 0 25px 50px -12px rgba(0, 0, 0, 0.7);
      --modal-overlay: rgba(11, 17, 32, 0.82);
    }}

    [data-theme="light"] {{
      --bg-primary: #f8fafc;
      --bg-secondary: #f1f5f9;
      --bg-card: #ffffff;
      --bg-card-hover: #f8fafc;
      --bg-surface: #f1f5f9;
      --bg-input: #ffffff;
      --border-color: #e2e8f0;
      --border-faint: #e2e8f0;
      --border-focus: #0284c7;
      --text-primary: #0f172a;
      --text-secondary: #475569;
      --text-muted: #64748b;
      --accent-blue: #0284c7;
      --accent-blue-hover: #0369a1;
      --accent-indigo: #6366f1;
      --accent-emerald: #059669;
      --badge-bg: #ccfbf1;
      --badge-border: #99f6e4;
      --badge-text: #0f766e;
      --region-bg: #ede9fe;
      --region-border: #ddd6fe;
      --region-text: #6d28d9;
      --shadow-card: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
      --shadow-modal: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
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

    /* Global Header */
    .site-header {{
      background: var(--bg-secondary);
      border-bottom: 1px solid var(--border-faint);
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
    
    /* Hero Section */
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
    
    /* Main Layout */
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
    .results-count {{ font-size: 0.95rem; font-weight: 500; color: var(--text-secondary); }}
    .results-count strong {{ color: var(--text-primary); font-weight: 700; }}

    /* Agent Card Grid matching Retail parity */
    .agent-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(420px, 1fr)); gap: 24px; }}
    .agent-card {{
      background: var(--bg-card);
      border: 1px solid var(--border-faint);
      border-radius: 16px;
      padding: 24px;
      display: flex;
      flex-direction: column;
      box-shadow: var(--shadow-card);
      transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
      position: relative;
    }}
    .agent-card:hover {{ transform: translateY(-3px); border-color: var(--border-focus); box-shadow: 0 16px 32px -8px rgba(0, 0, 0, 0.45); }}
    
    .card-top {{ display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 14px; gap: 8px; }}
    .card-badges {{ display: flex; gap: 8px; align-items: center; flex-wrap: wrap; }}
    .badge-domain {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 0.72rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.04em;
      padding: 4px 10px;
      border-radius: 6px;
      background: var(--badge-bg);
      border: 1px solid var(--badge-border);
      color: var(--badge-text);
    }}
    .badge-region {{
      display: inline-flex;
      align-items: center;
      gap: 4px;
      font-size: 0.72rem;
      font-weight: 700;
      padding: 4px 10px;
      border-radius: 6px;
      background: var(--region-bg);
      border: 1px solid var(--region-border);
      color: var(--region-text);
      font-family: 'JetBrains Mono', monospace;
    }}
    
    .card-title {{ font-family: 'Google Sans', sans-serif; font-size: 1.25rem; font-weight: 700; color: var(--text-primary); margin-bottom: 10px; line-height: 1.35; }}
    .card-desc {{ font-size: 0.9rem; color: var(--text-secondary); line-height: 1.55; margin-bottom: 20px; flex: 1; }}
    
    .prompts-container {{ border-top: 1px solid var(--border-color); padding-top: 14px; margin-bottom: 20px; }}
    .prompts-toggle {{ background: none; border: none; color: var(--text-secondary); font-size: 0.82rem; font-weight: 600; display: flex; align-items: center; justify-content: space-between; width: 100%; cursor: pointer; padding: 2px 0; }}
    .prompts-toggle:hover {{ color: var(--accent-blue); }}
    .prompts-list {{ margin-top: 10px; display: none; flex-direction: column; gap: 8px; }}
    .prompts-list.open {{ display: flex; }}
    .prompt-item {{ font-size: 0.82rem; color: var(--text-secondary); background: var(--bg-surface); padding: 8px 12px; border-radius: 6px; border-left: 3px solid var(--accent-indigo); line-height: 1.45; font-style: italic; }}
    
    .card-actions {{ display: flex; gap: 10px; align-items: center; margin-top: auto; padding-top: 16px; border-top: 1px solid var(--border-color); }}
    .btn-watch {{
      flex: 1;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      background: var(--accent-blue);
      color: #0f172a;
      padding: 10px 16px;
      border-radius: 8px;
      font-size: 0.9rem;
      font-weight: 700;
      border: none;
      cursor: pointer;
      transition: all 0.15s ease;
    }}
    .btn-watch:hover {{ background: var(--accent-blue-hover); color: #ffffff; transform: translateY(-1px); }}
    .btn-showcase {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      background: var(--bg-surface);
      color: var(--text-primary);
      padding: 10px 14px;
      border-radius: 8px;
      font-size: 0.85rem;
      font-weight: 600;
      text-decoration: none;
      border: 1px solid var(--border-color);
      transition: all 0.15s ease;
    }}
    .btn-showcase:hover {{ border-color: var(--border-focus); color: var(--accent-blue); }}
    .btn-doc {{ display: inline-flex; align-items: center; justify-content: center; background: none; color: var(--text-muted); padding: 10px; border-radius: 8px; font-size: 1.1rem; text-decoration: none; border: 1px solid transparent; transition: all 0.15s ease; }}
    .btn-doc:hover {{ color: var(--text-primary); border-color: var(--border-color); background: var(--bg-surface); }}
    .no-results {{ grid-column: 1 / -1; text-align: center; padding: 60px 20px; background: var(--bg-card); border: 1px dashed var(--border-color); border-radius: 14px; display: none; }}
    .no-results-icon {{ font-size: 3rem; margin-bottom: 12px; }}
    
    /* Video Modal matching Retail layout exactly */
    .modal-backdrop {{ position: fixed; inset: 0; background: var(--modal-overlay); z-index: 100; display: none; align-items: center; justify-content: center; padding: 24px; backdrop-filter: blur(8px); }}
    .modal-dialog {{ background: var(--bg-card); border: 1px solid var(--border-faint); border-radius: 18px; width: 100%; max-width: 1200px; max-height: 94vh; display: flex; flex-direction: column; box-shadow: var(--shadow-modal); overflow: hidden; }}
    .modal-header {{ display: flex; justify-content: space-between; align-items: flex-start; padding: 24px 28px 18px; border-bottom: 1px solid var(--border-color); }}
    .modal-header-left {{ display: flex; flex-direction: column; gap: 8px; }}
    .modal-badges-row {{ display: flex; gap: 8px; align-items: center; }}
    .modal-title {{ font-family: 'Google Sans', sans-serif; font-size: 1.55rem; font-weight: 700; color: var(--text-primary); line-height: 1.25; }}
    .modal-close {{ width: 36px; height: 36px; border-radius: 8px; background: rgba(255, 255, 255, 0.06); border: 1px solid var(--border-color); color: var(--text-secondary); display: flex; align-items: center; justify-content: center; font-size: 1.15rem; cursor: pointer; transition: all 0.15s ease; }}
    .modal-close:hover {{ background: var(--bg-surface); color: var(--text-primary); border-color: var(--border-focus); }}
    .modal-body {{ padding: 24px 28px; overflow-y: auto; display: flex; flex-direction: column; gap: 20px; }}
    .modal-video-wrapper {{ position: relative; width: 100%; background: #000; border-radius: 14px; overflow: hidden; border: 1px solid var(--border-color); box-shadow: 0 12px 30px rgba(0, 0, 0, 0.5); aspect-ratio: 16 / 9; }}
    .modal-video {{ width: 100%; height: 100%; object-fit: contain; background: #000; display: block; }}
    .modal-meta-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; background: var(--bg-surface); border: 1px solid var(--border-color); border-radius: 10px; padding: 18px 22px; }}
    .modal-meta-item {{ display: flex; flex-direction: column; gap: 4px; }}
    .modal-meta-label {{ font-size: 0.72rem; font-weight: 700; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.05em; }}
    .modal-meta-value {{ font-size: 0.95rem; font-weight: 600; color: var(--text-primary); }}
    .modal-sequence-box {{ background: var(--bg-surface); border: 1px solid var(--border-color); border-radius: 10px; padding: 22px 24px; }}
    .modal-sequence-title {{ font-size: 0.95rem; font-weight: 700; color: var(--accent-indigo); margin-bottom: 12px; }}
    .modal-turns-list {{ list-style: none; display: flex; flex-direction: column; gap: 10px; font-size: 0.9rem; color: var(--text-secondary); line-height: 1.55; }}
    .modal-turns-list strong {{ color: var(--text-primary); }}
    .modal-footer {{ padding: 18px 28px; border-top: 1px solid var(--border-color); display: flex; justify-content: flex-end; gap: 12px; background: var(--bg-card); }}
    .btn-download {{ display: inline-flex; align-items: center; gap: 6px; padding: 10px 18px; border-radius: 8px; font-size: 0.9rem; font-weight: 600; color: var(--text-primary); text-decoration: none; border: 1px solid var(--border-color); background: var(--bg-surface); transition: all 0.15s ease; }}
    .btn-download:hover {{ border-color: var(--border-focus); color: var(--accent-blue); }}
    .btn-open-showcase {{ display: inline-flex; align-items: center; gap: 6px; padding: 10px 22px; border-radius: 8px; font-size: 0.9rem; font-weight: 700; color: #0f172a; background: var(--accent-blue); text-decoration: none; transition: all 0.15s ease; }}
    .btn-open-showcase:hover {{ background: var(--accent-blue-hover); color: #ffffff; }}
    
    /* Footer */
    .site-footer {{ margin-top: auto; padding: 32px 24px; background: var(--bg-secondary); border-top: 1px solid var(--border-faint); text-align: center; }}
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
        <button class="domain-btn" data-domain="cex">
          <span>🏦</span> Centralized Exchanges <span class="domain-count">{domain_counts.get('cex', 0)}</span>
        </button>
        <button class="domain-btn" data-domain="infra">
          <span>⚡</span> L2 Infrastructure <span class="domain-count">{domain_counts.get('infra', 0)}</span>
        </button>
        <button class="domain-btn" data-domain="defi">
          <span>🦄</span> DeFi Protocols <span class="domain-count">{domain_counts.get('defi', 0)}</span>
        </button>
      </div>
    </section>

    <!-- Results Status Bar -->
    <div class="results-bar">
      <div class="results-count" id="resultsCount">Showing <strong>{total_agents}</strong> of {total_agents} enterprise agents</div>
    </div>

    <!-- Agent Card Grid -->
    <div class="agent-grid" id="agentGrid">
      <!-- Injected via JavaScript -->
    </div>

    <!-- No Results State -->
    <div class="no-results" id="noResults">
      <div class="no-results-icon">🔎</div>
      <h3>No matching Web3 agents found</h3>
      <p>Try searching for different keywords, token metrics, or clearing domain filters.</p>
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
          <p style="font-size: 0.9rem; color: var(--text-secondary);">Web3 Multi-Agent Interface routes user prompts to root <code>LlmAgent</code> (powered by <code>gemini-3.5-flash</code>).</p>
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

  <!-- Video Modal matching Retail Layout Exactly -->
  <div class="modal-backdrop" id="videoModal">
    <div class="modal-dialog">
      <div class="modal-header">
        <div class="modal-header-left">
          <div class="modal-badges-row">
            <span id="modalDomainBadge" class="badge-domain"></span>
            <span id="modalRegionBadge" class="badge-region"></span>
          </div>
          <h2 id="modalAgentTitle" class="modal-title">Agent Demo</h2>
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
      modalDomainBadge.textContent = agent.domain_badge_short;
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
      const isOpen = list.classList.contains('open');
      
      if (isOpen) {{
        list.classList.remove('open');
        icon.textContent = '▼';
      }} else {{
        list.classList.add('open');
        icon.textContent = '▲';
      }}
    }}

    function htmlEscape(str) {{
      return String(str || '')
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;');
    }}

    function renderAgents() {{
      const query = searchQuery.trim().toLowerCase();

      const filtered = AGENTS_DATA.filter(agent => {{
        const matchesDomain = (activeDomain === 'all' || agent.domain === activeDomain);
        if (!matchesDomain) return false;
        if (!query) return true;

        const textPool = [
          agent.display_name,
          agent.name,
          agent.domain_display,
          agent.domain_badge_short,
          agent.description,
          agent.location,
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
        const promptItems = (agent.prompts || []).map((prompt) => 
          `<div class="prompt-item">"${{htmlEscape(prompt)}}"</div>`
        ).join('');

        return `
          <div class="agent-card" data-agent-id="${{agent.id}}">
            <div class="card-top">
              <div class="card-badges">
                <span class="badge-domain">${{agent.domain_badge_short}}</span>
                <span class="badge-region">${{agent.location}}</span>
              </div>
            </div>
            <h3 class="card-title">${{htmlEscape(agent.display_name)}}</h3>
            <p class="card-desc">${{htmlEscape(agent.description)}}</p>

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
    agents = load_all_agents()
    html = build_portal_html(agents)
    out_file = REPO_ROOT / "index.html"
    out_file.write_text(html, encoding="utf-8")
    print(f"✓ Generated complete index.html with {len(agents)} agents across {len(DOMAIN_ORDER)} domains matching Retail parity!")

if __name__ == "__main__":
    main()
