#!/usr/bin/env python3
import re
from pathlib import Path

REPO_ROOT = Path('/usr/local/google/home/daricemahtab/web3-enterprise-agents')
gps_file = REPO_ROOT / '_shared' / 'scripts' / 'generate_portal_site.py'

content = gps_file.read_text(encoding='utf-8')

# 1. Update Stat Row CSS
old_stat_css = """    .stat-row { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 16px; max-width: 1000px; margin: 0 auto 40px; }
    .stat-card { background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 12px; padding: 16px 20px; text-align: center; }
    .stat-number { font-family: 'Google Sans', sans-serif; font-size: 1.75rem; font-weight: 700; color: var(--accent-blue); }
    .stat-label { font-size: 0.8rem; color: var(--text-secondary); margin-top: 4px; font-weight: 500; }"""

new_stat_css = """    .brand-logo { display: flex; align-items: center; gap: 12px; text-decoration: none; color: var(--text-primary); }
    .brand-icon { font-size: 1.8rem; }
    .brand-text { display: flex; flex-direction: column; gap: 2px; }
    .brand-title { font-family: 'Google Sans', sans-serif; font-size: 1.15rem; font-weight: 700; color: var(--text-primary); line-height: 1.2; }
    .brand-subtitle { font-size: 0.76rem; color: var(--text-muted); font-weight: 500; }
    
    .stat-row { display: grid; grid-template-columns: repeat(5, 1fr); gap: 16px; max-width: 1200px; margin: 0 auto 40px; }
    .stat-card { background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 12px; padding: 18px 14px; text-align: center; }
    .stat-number { font-family: 'Google Sans', sans-serif; font-size: 1.95rem; font-weight: 700; color: var(--text-primary); }
    .stat-label { font-size: 0.72rem; color: var(--text-muted); margin-top: 6px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; }"""

content = content.replace(old_stat_css, new_stat_css)

# 2. Update Header, Hero, and Stat HTML
old_header_hero_html = """  <!-- Global Header -->
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
  </section>"""

new_header_hero_html = """  <!-- Global Header matching Retail Top Navbar -->
  <header class="site-header">
    <div class="header-inner">
      <a href="index.html" class="brand-logo">
        <span class="brand-icon">🏛️</span>
        <div class="brand-text">
          <span class="brand-title">Web3 Enterprise Agents Catalog</span>
          <span class="brand-subtitle">Google ADK & Vertex AI Multi-Agent Swarm</span>
        </div>
      </a>
      <div class="header-actions">
        <button id="archBtn" class="btn-header"><span>📐</span> Architecture Blueprint</button>
        <button id="themeToggleBtn" class="btn-header"><span id="themeIcon">☀️</span> <span id="themeText">Light</span></button>
        <a href="https://github.com/daricemp1/web3-enterprise-agents" target="_blank" rel="noopener noreferrer" class="btn-header btn-primary-header"><span>⭐</span> GitHub Repository</a>
      </div>
    </div>
  </header>

  <!-- Hero Section matching Retail Hero Exactly -->
  <section class="hero">
    <div class="hero-pill">
      <span>🚀</span> 10 Enterprise Agents Fully Deployed (3 Web3 Domains)
    </div>
    <h1 class="hero-title">
      Web3 Enterprise Agents for <span>Decentralized Web</span>
    </h1>
    <p class="hero-desc">
      A declarative, multi-agent platform powered by Google Agent Development Kit (ADK), Vertex AI, and BigQuery Conversational Analytics. Real-time quantitative querying against 20+ enterprise Web3 datasets, grounded with external Google Search market intelligence.
    </p>

    <!-- Platform Stats: 5-card row matching Retail 100% -->
    <div class="stat-row">
      <div class="stat-card">
        <div class="stat-number">10</div>
        <div class="stat-label">ENTERPRISE AGENTS</div>
      </div>
      <div class="stat-card">
        <div class="stat-number">3</div>
        <div class="stat-label">WEB3 DOMAINS</div>
      </div>
      <div class="stat-card">
        <div class="stat-number">20</div>
        <div class="stat-label">BIGQUERY TABLES</div>
      </div>
      <div class="stat-card">
        <div class="stat-number">1</div>
        <div class="stat-label">GCP HOSTING REGION</div>
      </div>
      <div class="stat-card">
        <div class="stat-number">100%</div>
        <div class="stat-label">AGENTS DEMOS READY</div>
      </div>
    </div>
  </section>"""

content = content.replace(old_header_hero_html, new_header_hero_html)
content = content.replace(
    'placeholder="Search 10 agents by name, KPI (e.g. TPS, APY, TVL), question, or BigQuery table..."',
    'placeholder="Search 10 agents by name, KPI (e.g. TPS, APY, TVL), business question, or BigQuery table..."'
)

gps_file.write_text(content, encoding='utf-8')
print("Successfully refined Header, Hero, and 5-Card Stats Row!")
