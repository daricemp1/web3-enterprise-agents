#!/usr/bin/env python3
import re
from pathlib import Path

REPO_ROOT = Path('/usr/local/google/home/daricemahtab/web3-enterprise-agents')

# 1. Update generate_portal_site.py
gps_file = REPO_ROOT / '_shared' / 'scripts' / 'generate_portal_site.py'
if gps_file.exists():
    c = gps_file.read_text(encoding='utf-8')
    c = c.replace('Gemini Enterprise Agents for Web3 — 10 Multi-Agent Catalog', 'Web3 Agent Catalog — 10 Multi-Agent Suite')
    c = c.replace('Gemini Enterprise Agents for Web3', 'Web3 Agent Catalog')
    c = c.replace('Google ADK & Gemini Enterprise Multi-Agent Platform', 'Autonomous Multi-Agent Intelligence Platform')
    c = c.replace('Gemini Enterprise Agents for <span>Web3</span>', 'Web3 Enterprise <span>Agents Catalog</span>')
    c = c.replace('Explore 10 specialized Gemini Enterprise Agents for Web3 on-chain analytics, CEX trading, infrastructure & DeFi operations, built on Google ADK, Gemini Enterprise, and BigQuery Conversational Analytics.',
                  'Explore 10 specialized Web3 Agents for on-chain analytics, CEX trading, infrastructure & DeFi operations, built on Google ADK, Vertex AI, and BigQuery Conversational Analytics.')
    c = c.replace('A declarative, multi-agent platform powered by Google Agent Development Kit (ADK), Gemini Enterprise, and BigQuery Conversational Analytics.',
                  'A declarative, multi-agent platform powered by Google Agent Development Kit (ADK), Vertex AI, and BigQuery Conversational Analytics.')
    c = c.replace('<div class="stat-label">Gemini Enterprise Agents</div>', '<div class="stat-label">Web3 Agents</div>')
    c = c.replace('Gemini Enterprise Canvas UI routes user prompts to root <code>LlmAgent</code>', 'Web3 Agent UI routes user prompts to root <code>LlmAgent</code>')
    c = c.replace('<span class="modal-meta-value">Gemini Enterprise</span>', '<span class="modal-meta-value">Web3 Agent Platform</span>')
    c = c.replace('Powered by Google ADK, Gemini Enterprise, and BigQuery.', 'Powered by Google ADK, Vertex AI, and BigQuery.')
    c = c.replace('Executive briefing generated in Gemini Enterprise Canvas.', 'Executive briefing generated in interactive Canvas mode.')
    gps_file.write_text(c, encoding='utf-8')
    print("Updated generate_portal_site.py")

# 2. Update generate_demo_html.py
gdh_file = REPO_ROOT / '_shared' / 'scripts' / 'generate_demo_html.py'
if gdh_file.exists():
    c = gdh_file.read_text(encoding='utf-8')
    c = c.replace('{display_name} — Gemini Enterprise Demo Walkthrough', '{display_name} — Web3 Agent Demo Walkthrough')
    c = c.replace('<span class="badge">Gemini Enterprise</span>', '<span class="badge">Vertex AI & BigQuery</span>')
    c = c.replace('Gemini Enterprise Agent Demo - {t1}', 'Web3 Agent Demo - {t1}')
    c = c.replace('Creates an executive briefing in Gemini Enterprise Canvas.', 'Creates an executive briefing in interactive Canvas mode.')
    gdh_file.write_text(c, encoding='utf-8')
    print("Updated generate_demo_html.py")

# 3. Update README.md
readme_file = REPO_ROOT / 'README.md'
if readme_file.exists():
    c = readme_file.read_text(encoding='utf-8')
    c = c.replace('Google Agent Development Kit (ADK) Agents for Gemini Enterprise', 'Google Agent Development Kit (ADK) Agents for Web3')
    c = c.replace('for **Gemini Enterprise**.', 'for **Web3 Enterprise Intelligence**.')
    c = c.replace('User Prompt (Gemini Enterprise)', 'User Prompt (Web3 Agent Platform)')
    readme_file.write_text(c, encoding='utf-8')
    print("Updated README.md")

# 4. Update ARCHITECTURE.md
arch_file = REPO_ROOT / 'ARCHITECTURE.md'
if arch_file.exists():
    c = arch_file.read_text(encoding='utf-8')
    c = c.replace('for **Gemini Enterprise**.', 'for **Web3 Enterprise Intelligence**.')
    c = c.replace('GE[\"Gemini Enterprise Assistant\"]', 'GE[\"Web3 Agent Platform\"]')
    c = c.replace('participant GE as Gemini Enterprise UI', 'participant GE as Web3 Agent UI')
    c = c.replace('participant Canvas as Gemini Enterprise Canvas', 'participant Canvas as Web3 Canvas')
    arch_file.write_text(c, encoding='utf-8')
    print("Updated ARCHITECTURE.md")

print("Branding update script complete!")
