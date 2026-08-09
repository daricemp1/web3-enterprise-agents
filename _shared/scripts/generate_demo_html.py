#!/usr/bin/env python3
"""
generate_demo_html.py — Standalone HTML Demo Video Showcase Generator

Generates high-fidelity, responsive HTML5 video showcase pages for recorded agent demo MP4s
matching the standard Gemini Enterprise demo player design (dark mode, badge row, metadata grid,
multi-turn conversation flow breakdown, and GitHub links).

Usage:
    uv run python _shared/scripts/generate_demo_html.py --name cart_checkout_analytics
    uv run python _shared/scripts/generate_demo_html.py --domain merchandising --all
    uv run python _shared/scripts/generate_demo_html.py --all
"""

import argparse
from pathlib import Path
import re
import sys
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from _shared.scripts.prompt_parser import parse_agent_prompts, resolve_agent_domain

DOMAIN_ICONS = {
    "merchandising": "🛍️",
    "supply_chain": "🚚",
    "store_operations": "🏬",
    "e_commerce": "🛒",
    "finance": "💰",
    "marketing": "📊",
    "customer_care": "🎧",
    "human_resources": "👥",
    "sustainability_compliance": "🌱",
}

DOMAIN_TITLES = {
    "merchandising": "Merchandising Domain",
    "supply_chain": "Supply Chain & Logistics Domain",
    "store_operations": "Store Operations Domain",
    "e_commerce": "E-Commerce Domain",
    "finance": "Finance, Real Estate & Accounting Domain",
    "marketing": "Marketing & Retail Media Domain",
    "customer_care": "Customer Care & Experience Domain",
    "human_resources": "Human Resources & Workforce Domain",
    "sustainability_compliance": "Sustainability, ESG & Compliance Domain",
}

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{page_title}</title>
  <style>
    :root {{
      --bg-primary: #0f172a;
      --bg-card: #1e293b;
      --border-color: #334155;
      --text-primary: #f8fafc;
      --text-secondary: #94a3b8;
      --accent-blue: #38bdf8;
      --accent-indigo: #818cf8;
      --badge-bg: #0f2744;
      --badge-border: #1e4976;
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      background-color: var(--bg-primary);
      color: var(--text-primary);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: 32px 16px;
    }}

    .container {{
      max-width: 1080px;
      width: 100%;
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 16px;
      padding: 28px;
      box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.6);
    }}

    header {{
      margin-bottom: 20px;
    }}

    .badge-row {{
      display: flex;
      gap: 8px;
      margin-bottom: 12px;
      flex-wrap: wrap;
    }}

    .badge {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 0.75rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      padding: 4px 10px;
      border-radius: 9999px;
      background: var(--badge-bg);
      border: 1px solid var(--badge-border);
      color: var(--accent-blue);
    }}

    h1 {{
      font-size: 1.65rem;
      font-weight: 700;
      color: var(--text-primary);
      margin-bottom: 6px;
      display: flex;
      align-items: center;
      gap: 10px;
    }}

    p.subtitle {{
      color: var(--text-secondary);
      font-size: 0.95rem;
      line-height: 1.5;
    }}

    .video-wrapper {{
      position: relative;
      width: 100%;
      background: #000;
      border-radius: 12px;
      overflow: hidden;
      margin: 20px 0;
      box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.4);
    }}

    video {{
      width: 100%;
      display: block;
      max-height: 620px;
    }}

    .meta-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 12px;
      background: #0f172a;
      border: 1px solid var(--border-color);
      border-radius: 10px;
      padding: 16px;
      margin-bottom: 24px;
    }}

    .meta-item {{
      display: flex;
      flex-direction: column;
      gap: 4px;
    }}

    .meta-label {{
      font-size: 0.75rem;
      color: var(--text-secondary);
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }}

    .meta-value {{
      font-size: 0.9rem;
      font-weight: 600;
      color: var(--text-primary);
    }}

    .turns-section {{
      background: #0f172a;
      border: 1px solid var(--border-color);
      border-radius: 10px;
      padding: 20px;
      margin-bottom: 24px;
    }}

    .turns-section h2 {{
      font-size: 1.1rem;
      margin-bottom: 12px;
      color: var(--accent-indigo);
    }}

    .turn-list {{
      list-style: none;
      display: flex;
      flex-direction: column;
      gap: 10px;
    }}

    .turn-list li {{
      font-size: 0.9rem;
      line-height: 1.5;
      color: var(--text-secondary);
    }}

    .turn-list strong {{
      color: var(--text-primary);
    }}

    footer {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 12px;
      padding-top: 16px;
      border-top: 1px solid var(--border-color);
    }}

    .btn-link {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      color: var(--accent-blue);
      text-decoration: none;
      font-size: 0.9rem;
      font-weight: 500;
      transition: color 0.15s ease;
    }}

    .btn-link:hover {{
      color: #7dd3fc;
      text-decoration: underline;
    }}
  </style>
</head>
<body>
  <div class="container">
    <header>
      <div class="badge-row">
        <span class="badge">Retail Enterprise Agents</span>
        <span class="badge">{domain_badge}</span>
        <span class="badge">Gemini Enterprise</span>
      </div>
      <h1>{icon} {display_name}</h1>
      <p class="subtitle">
        {subtitle}
      </p>
    </header>

    <div class="video-wrapper">
      <video controls autoplay muted playsinline preload="auto">
        <source src="{video_filename}" type="video/mp4">
        Your browser does not support HTML5 video.
      </video>
    </div>

    <div class="meta-grid">
      <div class="meta-item">
        <span class="meta-label">Duration</span>
        <span class="meta-value">{duration_text}</span>
      </div>
      <div class="meta-item">
        <span class="meta-label">Resolution</span>
        <span class="meta-value">1080p Full HD (1920×1080)</span>
      </div>
      <div class="meta-item">
        <span class="meta-label">UI Scaling</span>
        <span class="meta-value">1.25x High-DPI Scaled Text</span>
      </div>
      <div class="meta-item">
        <span class="meta-label">Model Runtime</span>
        <span class="meta-value">gemini-3.5-flash (Vertex AI)</span>
      </div>
    </div>

    <div class="turns-section">
      <h2>📋 Multi-Turn Conversation Flow</h2>
      <ul class="turn-list">
{turn_items_html}
      </ul>
    </div>

    <footer>
      <a class="btn-link" href="https://github.com/rajanm/retail-enterprise-agents/tree/master/domains/{domain}/agents/{agent_name}" target="_blank" rel="noopener noreferrer">
        ← View Agent Code & Documentation on GitHub
      </a>
      <a class="btn-link" href="https://github.com/rajanm/retail-enterprise-agents" target="_blank" rel="noopener noreferrer">
        🏠 Retail Enterprise Agents Repository
      </a>
    </footer>
  </div>
</body>
</html>
"""


def get_agent_info(agent_name: str, domain: str) -> dict:
    """Extracts agent metadata, display name, and subtitle description."""
    agent_dir = REPO_ROOT / "domains" / domain / "agents" / agent_name
    readme_path = agent_dir / "README.md"
    root_agent_path = agent_dir / "root_agent.yaml"
    
    display_name = agent_name.replace("_", " ").title()
    subtitle = "Authentic multi-turn interactive video recording showcasing agent @mention invocation, BigQuery conversational analytics SQL synthesis, Google Search market grounding, and visual chart artifact generation."
    
    if readme_path.exists():
        try:
            content = readme_path.read_text(encoding="utf-8")
            for line in content.splitlines():
                if "**Gemini Enterprise display name:**" in line:
                    display_name = line.split("**Gemini Enterprise display name:**")[-1].strip()
                    break
                elif line.startswith("# ") and "Agent" in line:
                    display_name = line.replace("# ", "").replace(" Agent", "").strip()
            for line in content.splitlines():
                if line.startswith("Answers questions about"):
                    subtitle = line.strip()
                    break
        except Exception:
            pass
            
    if root_agent_path.exists() and display_name == agent_name.replace("_", " ").title():
        try:
            data = yaml.safe_load(root_agent_path.read_text(encoding="utf-8"))
            display_name = data.get("display_name", display_name)
        except Exception:
            pass
            
    return {
        "display_name": display_name,
        "subtitle": subtitle,
    }


def generate_html_showcase(
    agent_name: str,
    domain: str,
    output_dir: Path,
    duration_text: str = "5:45 (Normal Pacing)",
) -> Path:
    """Renders and writes the standalone HTML demo player file for an agent."""
    domain_output_dir = output_dir / domain
    domain_output_dir.mkdir(parents=True, exist_ok=True)
    html_target = domain_output_dir / f"{agent_name}.html"
    
    info = get_agent_info(agent_name, domain)
    display_name = info["display_name"]
    subtitle = info["subtitle"]
    
    domain_badge = DOMAIN_TITLES.get(domain, domain.replace("_", " ").title())
    icon = DOMAIN_ICONS.get(domain, "🤖")
    
    readme_path = REPO_ROOT / "domains" / domain / "agents" / agent_name / "README.md"
    prompts = parse_agent_prompts(readme_path) if readme_path.exists() else []
    
    # Format turns
    turn_1_prompt = prompts[0] if len(prompts) > 0 else "What are the key performance metrics for this category?"
    turn_2_prompt = prompts[1] if len(prompts) > 1 else "What are the latest industry benchmarks and market trends?"
    turn_3_prompt = prompts[2] if len(prompts) > 2 else "Can you render a chart visualizing these metrics?"
    
    agent_clean_title = display_name.split(":")[-1].strip() if ":" in display_name else display_name
    turn_4_prompt = f"Create a 4-slide executive presentation summarizing the {agent_clean_title} analysis and recommendations above."
    
    turn_items = [
        f'        <li><strong>Turn 1 (Data Insights / BigQuery):</strong> <em>"{turn_1_prompt}"</em> — Synthesizes internal BigQuery conversational analytics query and computes KPI summary.</li>',
        f'        <li><strong>Turn 2 (Market Context / Google Search):</strong> <em>"{turn_2_prompt}"</em> — Grounds analysis against external retail benchmarks and industry context.</li>',
        f'        <li><strong>Turn 3 (Visual Artifact / Matplotlib):</strong> <em>"{turn_3_prompt}"</em> — Generates and renders a custom chart visualization artifact inline.</li>',
        f'        <li><strong>Turn 4 (Executive Canvas Presentation):</strong> <em>"{turn_4_prompt}"</em> — Automatically creates a 4-slide deck and showcases each slide via the bottom thumbnail rail.</li>',
    ]
    
    html_content = HTML_TEMPLATE.format(
        page_title=f"{display_name} — Gemini Enterprise Demo Walkthrough",
        domain_badge=domain_badge,
        icon=icon,
        display_name=display_name,
        subtitle=subtitle,
        video_filename=f"{agent_name}.mp4",
        duration_text=duration_text,
        turn_items_html="\n".join(turn_items),
        domain=domain,
        agent_name=agent_name,
    )
    
    html_target.write_text(html_content, encoding="utf-8")
    print(f"✅ Generated HTML demo player: {html_target}", flush=True)
    return html_target


def main():
    parser = argparse.ArgumentParser(description="Generate HTML Demo Video Showcase Player for Gemini Enterprise Agents.")
    parser.add_argument("--name", type=str, help="Target agent directory name (e.g. cart_checkout_analytics)")
    parser.add_argument("--domain", type=str, help="Target retail domain (e.g. e_commerce)")
    parser.add_argument("--all", action="store_true", help="Generate HTML for all recorded videos or all agents in domain")
    parser.add_argument("--output-dir", type=Path, default=REPO_ROOT / "demos" / "gemini-enterprise", help="Base output directory for HTML demo players")
    
    args = parser.parse_args()
    
    if not args.name and not args.all:
        parser.error("Must provide either --name <agent_name> or --all")
        
    agents_to_generate = []
    
    if args.name:
        domain = args.domain or resolve_agent_domain(args.name, REPO_ROOT)
        agents_to_generate.append((args.name, domain))
    elif args.all:
        if args.domain:
            agent_dirs = sorted((REPO_ROOT / "domains" / args.domain / "agents").glob("*"))
            for ad in agent_dirs:
                if ad.is_dir() and (ad / "README.md").exists():
                    agents_to_generate.append((ad.name, args.domain))
        else:
            agent_dirs = sorted(REPO_ROOT.glob("domains/*/agents/*"))
            for ad in agent_dirs:
                if ad.is_dir() and (ad / "README.md").exists():
                    domain = ad.parent.parent.name
                    agents_to_generate.append((ad.name, domain))
                    
    print(f"📋 Generating HTML demo players for {len(agents_to_generate)} agent(s)...", flush=True)
    for agent_name, domain in agents_to_generate:
        generate_html_showcase(agent_name, domain, args.output_dir)


if __name__ == "__main__":
    main()
