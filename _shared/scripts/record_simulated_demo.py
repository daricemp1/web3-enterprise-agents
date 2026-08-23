#!/usr/bin/env python3
"""High-Fidelity Web3 Agent UI Demo Video Recorder for Web3 Enterprise Agents.

Generates pixel-perfect 1080p MP4 screen recordings of the Web3 Agent Catalog interface:
- Left sidebar with navigation, agents, and recent chats.
- Agents search & card selection from "From your organization".
- Multi-turn conversation flow:
    Turn 1: BigQuery Conversational Analytics NL-to-SQL synthesis and tabular metrics.
    Turn 2: Google Search grounding with market benchmarks and citations.
    Turn 3: High-resolution visual chart artifact.
    Turn 4: Split-screen Web3 Agent Catalog Canvas 4-slide presentation deck.
- Smooth mouse movements, scrolling, and slide transitions.
"""

import asyncio
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path
import yaml

REPO_ROOT = Path('/usr/local/google/home/daricemahtab/web3-enterprise-agents')

def generate_gemini_enterprise_html(agent_name: str, reg_agent: dict) -> str:
    domain = reg_agent.get('domain', 'defi')
    display_name = reg_agent.get('display_name', agent_name.replace('_', ' ').title())
    description = reg_agent.get('description', '')
    kpis = reg_agent.get('kpis', ["Throughput: 1,420 TPS", "Latency: 280ms", "Efficiency: 99.8%"])
    tables = reg_agent.get('tables', ['order_events', 'market_depth'])
    
    domain_icons = {'cex': '🏦', 'infra': '⚡', 'defi': '🦄'}
    domain_titles = {'cex': 'Centralized Exchanges & Trading', 'infra': 'Blockchain Infrastructure & L2', 'defi': 'Decentralized Finance & Protocols'}
    
    icon = domain_icons.get(domain, '💎')
    domain_title = domain_titles.get(domain, domain.upper())
    
    clean_title = display_name.split(':')[-1].strip() if ':' in display_name else display_name
    
    prompts = [
        f"What are the top quantitative metrics for {display_name} across on-chain activity?",
        f"What are current crypto market benchmarks and protocol best practices for {display_name}?",
        f"Show me a comparison chart visualizing {display_name} performance vs historical benchmark.",
        f"Create a 4-slide executive presentation summarizing this {clean_title} analysis."
    ]
    
    t1_table_rows = ""
    for kpi in kpis:
        parts = kpi.split(':')
        m_name = parts[0].strip()
        m_val = parts[1].strip() if len(parts) > 1 else "Optimal"
        t1_table_rows += f"""
        <tr>
            <td style="font-weight:600; color:#1e293b;">{m_name}</td>
            <td style="color:#0284c7; font-family:'JetBrains Mono',monospace; font-weight:600;">{m_val}</td>
            <td style="color:#64748b;">Industry Baseline</td>
            <td><span style="background:#ecfdf5; color:#059669; font-weight:600; font-size:11px; padding:3px 8px; border-radius:12px; border:1px solid #a7f3d0;">HEALTHY (Top 5%)</span></td>
        </tr>
        """
        
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Web3 Agent Catalog - {display_name}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500;600;700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: 'Google Sans', 'Inter', sans-serif;
    background: #ffffff;
    color: #1e293b;
    width: 1920px;
    height: 1080px;
    overflow: hidden;
    display: flex;
    user-select: none;
  }}

  /* Virtual Cursor */
  #virtualCursor {{
    position: fixed;
    top: 540px;
    left: 960px;
    width: 24px;
    height: 24px;
    z-index: 99999;
    pointer-events: none;
    transition: transform 0.05s ease-out;
  }}

  /* Sidebar */
  .sidebar {{
    width: 320px;
    height: 1080px;
    background: #f8fafc;
    border-right: 1px solid #e2e8f0;
    display: flex;
    flex-direction: column;
    padding: 16px 12px;
    flex-shrink: 0;
  }}
  .logo-row {{
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 8px 12px 16px;
    border-bottom: 1px solid #edf2f7;
    margin-bottom: 12px;
  }}
  .logo-text {{
    font-size: 17px;
    font-weight: 700;
    color: #1e293b;
    letter-spacing: -0.02em;
  }}
  .nav-group {{
    display: flex;
    flex-direction: column;
    gap: 4px;
    margin-bottom: 18px;
  }}
  .nav-item {{
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px 14px;
    border-radius: 8px;
    font-size: 17px;
    font-weight: 500;
    color: #475569;
    cursor: pointer;
  }}
  .nav-item.active {{
    background: #e0f2fe;
    color: #0284c7;
    font-weight: 600;
  }}
  .nav-section-title {{
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #94a3b8;
    padding: 10px 14px 4px;
    font-weight: 600;
  }}
  .recent-item {{
    padding: 8px 14px;
    font-size: 13px;
    color: #64748b;
    border-radius: 6px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }}

  /* Main Container */
  .main-wrapper {{
    flex: 1;
    height: 1080px;
    display: flex;
    position: relative;
    overflow: hidden;
  }}

  /* Screen 1: Agent Directory */
  #directoryScreen {{
    width: 100%;
    height: 100%;
    padding: 48px 64px;
    display: flex;
    flex-direction: column;
    background: #ffffff;
  }}
  .dir-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 28px;
  }}
  .dir-title {{
    font-size: 38px;
    font-weight: 600;
    color: #0f172a;
  }}
  .btn-new-agent {{
    background: #1a73e8;
    color: #ffffff;
    border: none;
    border-radius: 20px;
    padding: 10px 22px;
    font-size: 17px;
    font-weight: 600;
    cursor: pointer;
  }}
  .search-bar-box {{
    width: 100%;
    max-width: 960px;
    height: 62px;
    border: 1px solid #cbd5e1;
    border-radius: 28px;
    display: flex;
    align-items: center;
    padding: 0 20px;
    gap: 14px;
    margin-bottom: 40px;
    background: #ffffff;
    box-shadow: 0 2px 6px rgba(0,0,0,0.03);
  }}
  .search-text {{
    font-size: 20px;
    color: #1e293b;
    flex: 1;
  }}
  .dir-section-title {{
    font-size: 17px;
    font-weight: 600;
    color: #64748b;
    margin-bottom: 16px;
  }}
  .agent-card {{
    width: 440px;
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 18px;
    padding: 20px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.04);
    cursor: pointer;
    transition: all 0.2s;
  }}
  .agent-card:hover, .agent-card.hovered {{
    border-color: #38bdf8;
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(56,189,248,0.15);
  }}
  .agent-card-icon {{
    width: 44px;
    height: 44px;
    border-radius: 10px;
    background: #f1f5f9;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
    margin-bottom: 14px;
  }}
  .agent-card-title {{
    font-size: 20px;
    font-weight: 600;
    color: #0f172a;
    margin-bottom: 6px;
    line-height: 1.3;
  }}
  .agent-card-desc {{
    font-size: 13px;
    color: #64748b;
    line-height: 1.4;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }}

  /* Screen 2: Chat View & Split Canvas */
  #chatScreen {{
    width: 100%;
    height: 100%;
    display: none;
    flex-direction: row;
    position: relative;
  }}
  .chat-pane {{
    flex: 1;
    height: 1080px;
    display: flex;
    flex-direction: column;
    background: #ffffff;
    overflow-y: auto;
    scroll-behavior: smooth;
  }}
  .chat-header {{
    height: 64px;
    border-bottom: 1px solid #e2e8f0;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 32px;
    background: #ffffff;
    flex-shrink: 0;
  }}
  .agent-badge-pill {{
    display: flex;
    align-items: center;
    gap: 8px;
    background: #f1f5f9;
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 600;
    color: #0f172a;
    border: 1px solid #e2e8f0;
  }}
  .messages-container {{
    flex: 1;
    padding: 32px 48px 160px;
    display: flex;
    flex-direction: column;
    gap: 28px;
  }}
  .user-msg {{
    align-self: flex-end;
    background: #f1f5f9;
    color: #0f172a;
    padding: 14px 20px;
    border-radius: 20px 20px 4px 20px;
    font-size: 18px;
    max-width: 750px;
    line-height: 1.5;
    box-shadow: 0 2px 4px rgba(0,0,0,0.02);
  }}
  .agent-msg {{
    align-self: flex-start;
    display: flex;
    gap: 16px;
    max-width: 900px;
  }}
  .agent-avatar {{
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background: #e0f2fe;
    color: #0284c7;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    flex-shrink: 0;
  }}
  .agent-content {{
    flex: 1;
    font-size: 18px;
    line-height: 1.6;
    color: #334155;
  }}
  .status-pill {{
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: #f8fafc;
    border: 1px solid #cbd5e1;
    color: #475569;
    font-size: 12px;
    font-weight: 600;
    padding: 4px 12px;
    border-radius: 16px;
    margin-bottom: 12px;
  }}
  .status-pill .spinner {{
    width: 10px;
    height: 10px;
    border: 2px solid #0284c7;
    border-top-color: transparent;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
  }}
  @keyframes spin {{ to {{ transform: rotate(360deg); }} }}

  /* Tables */
  .data-table {{
    width: 100%;
    border-collapse: collapse;
    margin: 14px 0;
    font-size: 20px;
    border-radius: 8px;
    overflow: hidden;
    border: 1px solid #e2e8f0;
  }}
  .data-table th {{
    background: #f8fafc;
    padding: 10px 14px;
    font-weight: 600;
    color: #475569;
    text-align: left;
    border-bottom: 1px solid #e2e8f0;
  }}
  .data-table td {{
    padding: 10px 14px;
    border-bottom: 1px solid #f1f5f9;
  }}

  /* Charts */
  .chart-box {{
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 20px;
    margin: 14px 0;
  }}

  /* Prompt Input Bar */
  .prompt-bar-wrapper {{
    position: absolute;
    bottom: 24px;
    left: 48px;
    right: 48px;
    max-width: 900px;
    margin: 0 auto;
    background: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 28px;
    padding: 12px 20px;
    display: flex;
    align-items: center;
    gap: 12px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.06);
  }}
  .prompt-input-text {{
    flex: 1;
    font-size: 18px;
    color: #1e293b;
  }}
  .prompt-btn {{
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background: #1a73e8;
    color: white;
    border: none;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    cursor: pointer;
  }}

  /* Split Canvas Mode */
  .canvas-pane {{
    width: 740px;
    height: 1080px;
    background: #f8fafc;
    border-left: 1px solid #e2e8f0;
    display: none;
    flex-direction: column;
    padding: 24px;
    box-shadow: -8px 0 24px rgba(0,0,0,0.03);
    position: relative;
  }}
  .canvas-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
  }}
  .canvas-slide-stage {{
    flex: 1;
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 32px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.04);
    display: flex;
    flex-direction: column;
    justify-content: center;
  }}
  .canvas-rail {{
    height: 90px;
    display: flex;
    gap: 12px;
    margin-top: 18px;
  }}
  .slide-thumb {{
    flex: 1;
    background: #ffffff;
    border: 2px solid #cbd5e1;
    border-radius: 8px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    font-size: 11px;
    font-weight: 600;
    color: #64748b;
    cursor: pointer;
    transition: all 0.2s;
  }}
  .slide-thumb.active {{
    border-color: #0284c7;
    background: #e0f2fe;
    color: #0284c7;
  }}
</style>
</head>
<body>

<!-- Virtual Cursor -->
<svg id="virtualCursor" viewBox="0 0 24 24" fill="none">
  <path d="M5.5 3.2L18.8 12.3C19.7 12.9 19.3 14.3 18.2 14.3H12.6L16.2 20.9C16.6 21.6 15.9 22.3 15.2 21.9L12.4 20.3L9.6 15.2H5.5C4.4 15.2 3.8 13.9 4.6 13.2L5.5 3.2Z" fill="#0f172a" stroke="#ffffff" stroke-width="1.5"/>
</svg>

<!-- Sidebar -->
<aside class="sidebar">
  <div class="logo-row">
    <svg width="24" height="24" viewBox="0 0 24 24">
      <path d="M12 2L14.5 9.5L22 12L14.5 14.5L12 22L9.5 14.5L2 12L9.5 9.5L12 2Z" fill="#1a73e8"/>
    </svg>
    <span class="logo-text">Web3 Agent Catalog</span>
  </div>

  <div class="nav-group">
    <div class="nav-item">💬 New chat</div>
    <div class="nav-item">🔍 Search</div>
    <div class="nav-item">📚 Library</div>
  </div>

  <div class="nav-section-title">Workspace</div>
  <div class="nav-group">
    <div class="nav-item active" id="sidebarAgents">🤖 Agents</div>
    <div class="nav-item">📓 Gemini Notebook</div>
    <div class="nav-item">🔬 Deep Research</div>
    <div class="nav-item">➕ New agent</div>
  </div>

  <div class="nav-section-title">Recent</div>
  <div class="nav-group">
    <div class="recent-item">4-slide presentation</div>
    <div class="recent-item">Working capital presentation</div>
    <div class="recent-item">DEX Liquidity analysis</div>
    <div class="recent-item">Validator RPC uptime report</div>
    <div class="recent-item">Whale custody transfer flow</div>
  </div>
</aside>

<!-- Main Area -->
<div class="main-wrapper">

  <!-- Screen 1: Directory -->
  <div id="directoryScreen">
    <div class="dir-header">
      <h1 class="dir-title">Agents</h1>
      <button class="btn-new-agent">+ New agent</button>
    </div>

    <div class="search-bar-box">
      <span style="color:#94a3b8; font-size:18px;">🔍</span>
      <span class="search-text" id="dirSearchText"></span>
      <span style="color:#94a3b8; cursor:pointer;">✕</span>
    </div>

    <div class="dir-section-title">From your organization</div>
    
    <div class="agent-card" id="targetAgentCard">
      <div class="agent-card-icon">{icon}</div>
      <div class="agent-card-title">{display_name}</div>
      <div class="agent-card-desc">{description}</div>
    </div>
  </div>

  <!-- Screen 2: Chat & Split Canvas -->
  <div id="chatScreen">
    <div class="chat-pane" id="chatPane">
      <div class="chat-header">
        <div class="agent-badge-pill">
          <span>{icon}</span>
          <span>{display_name}</span>
          <span style="color:#94a3b8;">•</span>
          <span style="color:#0284c7; font-weight:600;">gemini-3.5-flash</span>
        </div>
        <div style="font-size:12px; color:#64748b; font-weight:500;">
          BigQuery Conversational Analytics Engine
        </div>
      </div>

      <div class="messages-container" id="messagesContainer">
        <!-- Turns injected via JavaScript animation -->
      </div>

      <div class="prompt-bar-wrapper">
        <span style="color:#94a3b8; font-size:18px;">+</span>
        <div class="prompt-input-text" id="promptInputText">Ask a question or enter a prompt...</div>
        <button class="prompt-btn" id="promptSendBtn">▲</button>
      </div>
    </div>

    <!-- Canvas Mode Split Pane -->
    <div class="canvas-pane" id="canvasPane">
      <div class="canvas-header">
        <div style="display:flex; align-items:center; gap:8px;">
          <span style="font-size:16px;">📊</span>
          <span style="font-weight:700; font-size:15px; color:#0f172a;">Executive Briefing Deck</span>
        </div>
        <span style="font-size:12px; color:#0284c7; font-weight:600; background:#e0f2fe; padding:4px 8px; border-radius:6px;">Web3 Canvas</span>
      </div>

      <div class="canvas-slide-stage" id="canvasSlideStage">
        <!-- Slide content dynamically updated -->
      </div>

      <div class="canvas-rail">
        <div class="slide-thumb active" id="thumb1" onclick="selectSlide(1)">Slide 1<br><span style="font-size:9px; font-weight:400;">Overview</span></div>
        <div class="slide-thumb" id="thumb2" onclick="selectSlide(2)">Slide 2<br><span style="font-size:9px; font-weight:400;">Metrics</span></div>
        <div class="slide-thumb" id="thumb3" onclick="selectSlide(3)">Slide 3<br><span style="font-size:9px; font-weight:400;">Grounding</span></div>
        <div class="slide-thumb" id="thumb4" onclick="selectSlide(4)">Slide 4<br><span style="font-size:9px; font-weight:400;">Action Plan</span></div>
      </div>
    </div>
  </div>

</div>

<script>
  const cursor = document.getElementById('virtualCursor');
  function moveCursor(x, y) {{
    cursor.style.transform = `translate(${{x}}px, ${{y}}px)`;
  }}

  const slidesData = [
    {{
      title: "Executive Summary: {clean_title}",
      subtitle: "Web3 Enterprise Intelligence & On-Chain Governance",
      bullets: [
        "Real-time NL-to-SQL synthesis across BigQuery datasets in `gcda-apac-sc.web3_enterprise_agents`.",
        "Grounding via Google Search and live market protocol telemetry.",
        "Zero-latency anomaly detection and automated spread/liquidity risk management."
      ]
    }},
    {{
      title: "Core Performance & Execution Metrics",
      subtitle: "Benchmark Health: TOP 5% TIER",
      bullets: [
        "Spread & Slippage: Within sub-0.5 bps tolerance.",
        "Execution Throughput: Peak stability across volatile volume bursts.",
        "Automated Liquidation & Solvency Buffer: Exceeds standard Basel/DeFi covenants."
      ]
    }},
    {{
      title: "Competitive Market Context",
      subtitle: "Grounded Comparison vs Tier-1 Protocols",
      bullets: [
        "Protocol efficiency outpaces Binance, Uniswap v3, and Curve pools by 14.2%.",
        "MEV resilience: Sandwich protection active with zero toxic routing.",
        "Regulatory compliance: Complete verifiable audit trail via BigQuery lineage."
      ]
    }},
    {{
      title: "Strategic Recommendations & Next Steps",
      subtitle: "Q3-Q4 Execution Roadmap",
      bullets: [
        "Automate dynamic fee adjustments based on real-time AMM volatility.",
        "Expand cross-chain bridge monitoring for Layer-2 blob throughput.",
        "Publish continuous telemetry reports directly to executive dashboard."
      ]
    }}
  ];

  function renderSlide(idx) {{
    const s = slidesData[idx - 1];
    document.querySelectorAll('.slide-thumb').forEach((t, i) => {{
      t.classList.toggle('active', i === idx - 1);
    }});
    document.getElementById('canvasSlideStage').innerHTML = `
      <div style="font-size:12px; color:#0284c7; font-weight:700; text-transform:uppercase; margin-bottom:8px;">SLIDE ${{idx}} OF 4</div>
      <h2 style="font-size:20px; font-weight:700; color:#0f172a; margin-bottom:6px;">${{s.title}}</h2>
      <div style="font-size:13px; color:#64748b; font-weight:500; margin-bottom:20px;">${{s.subtitle}}</div>
      <ul style="padding-left:18px; color:#334155; font-size:13.5px; line-height:1.7;">
        ${{s.bullets.map(b => `<li>${{b}}</li>`).join('')}}
      </ul>
    `;
  }}
  renderSlide(1);

  // Animation timeline trigger
  window.runDemoSequence = async function() {{
    const sleep = ms => new Promise(r => setTimeout(r, ms));

    // Phase 1: Search agent in directory
    await sleep(800);
    moveCursor(500, 160);
    await sleep(500);
    const searchTarget = "{clean_title}";
    const searchEl = document.getElementById('dirSearchText');
    for (let i = 1; i <= searchTarget.length; i++) {{
      searchEl.textContent = searchTarget.slice(0, i);
      await sleep(35);
    }}
    await sleep(600);

    // Phase 2: Click card
    moveCursor(220, 290);
    document.getElementById('targetAgentCard').classList.add('hovered');
    await sleep(600);
    document.getElementById('directoryScreen').style.display = 'none';
    document.getElementById('chatScreen').style.display = 'flex';
    moveCursor(700, 980);
    await sleep(800);

    // Turn 1
    const p1 = "{prompts[0]}";
    const promptInput = document.getElementById('promptInputText');
    promptInput.style.color = '#1e293b';
    for (let i = 1; i <= p1.length; i++) {{
      promptInput.textContent = p1.slice(0, i);
      await sleep(15);
    }}
    await sleep(400);
    moveCursor(910, 980);
    await sleep(300);
    promptInput.textContent = 'Ask a question or enter a prompt...';
    promptInput.style.color = '#94a3b8';

    const msgCont = document.getElementById('messagesContainer');
    msgCont.innerHTML += `
      <div class="user-msg">${{p1}}</div>
      <div class="agent-msg">
        <div class="agent-avatar">{icon}</div>
        <div class="agent-content">
          <div class="status-pill"><div class="spinner"></div> Synthesizing SQL on BigQuery dataset gcda-apac-sc.web3_enterprise_agents...</div>
          <div style="font-weight:600; margin-bottom:8px; color:#0f172a;">📊 Executive Key Performance Metrics for {display_name}</div>
          <p>Based on continuous analysis of the latest on-chain transaction records from <code>{tables[0]}</code>, here is the structured health assessment:</p>
          <table class="data-table">
            <thead>
              <tr><th>Metric</th><th>Current Value</th><th>Benchmark Reference</th><th>Status</th></tr>
            </thead>
            <tbody>
              {t1_table_rows}
            </tbody>
          </table>
          <p><strong>Recommendation:</strong> Protocol risk metrics are well within safe thresholds. Liquidity buffers are stable.</p>
        </div>
      </div>
    `;
    await sleep(2500);

    // Turn 2
    const p2 = "{prompts[1]}";
    for (let i = 1; i <= p2.length; i++) {{
      promptInput.textContent = p2.slice(0, i);
      promptInput.style.color = '#1e293b';
      await sleep(15);
    }}
    await sleep(400);
    promptInput.textContent = 'Ask a question or enter a prompt...';
    promptInput.style.color = '#94a3b8';

    msgCont.innerHTML += `
      <div class="user-msg">${{p2}}</div>
      <div class="agent-msg">
        <div class="agent-avatar">{icon}</div>
        <div class="agent-content">
          <div class="status-pill"><div class="spinner"></div> Grounding with Google Search & Live Crypto Market Telemetry...</div>
          <div style="font-weight:600; margin-bottom:8px; color:#0f172a;">🌐 Market Grounding & Protocol Best Practices</div>
          <p>Comparing our metrics against current crypto industry standards (Binance, Uniswap v3, and Curve):</p>
          <ul style="padding-left:18px; margin:8px 0; line-height:1.6;">
            <li><strong>Slippage & Depth:</strong> Our 2% order book depth outperforms average tier-1 peers by <strong>14.2%</strong>.</li>
            <li><strong>Risk Mitigation:</strong> Real-time oracle updates prevent stale pricing and sandwich attacks.</li>
            <li><strong>Auditability:</strong> Full transparent lineage verified via BigQuery.</li>
          </ul>
        </div>
      </div>
    `;
    document.getElementById('chatPane').scrollTop = 600;
    await sleep(2500);

    // Turn 3: Visual Artifact
    const p3 = "{prompts[2]}";
    for (let i = 1; i <= p3.length; i++) {{
      promptInput.textContent = p3.slice(0, i);
      promptInput.style.color = '#1e293b';
      await sleep(15);
    }}
    await sleep(400);
    promptInput.textContent = 'Ask a question or enter a prompt...';
    promptInput.style.color = '#94a3b8';

    msgCont.innerHTML += `
      <div class="user-msg">${{p3}}</div>
      <div class="agent-msg">
        <div class="agent-avatar">{icon}</div>
        <div class="agent-content">
          <div class="status-pill">✓ Visual Analytics Artifact Rendered</div>
          <div style="font-weight:600; margin-bottom:8px; color:#0f172a;">📈 Visual Comparison: {clean_title} vs Market Benchmark</div>
          <div class="chart-box">
            <svg width="100%" height="180" viewBox="0 0 650 180">
              <rect x="50" y="30" width="120" height="110" fill="#0284c7" rx="4"/>
              <text x="110" y="20" text-anchor="middle" fill="#0284c7" font-size="12" font-weight="600">Protocol (99.8%)</text>
              <rect x="220" y="60" width="120" height="80" fill="#94a3b8" rx="4"/>
              <text x="280" y="50" text-anchor="middle" fill="#64748b" font-size="12" font-weight="600">Industry Avg (85.4%)</text>
              <rect x="390" y="80" width="120" height="60" fill="#cbd5e1" rx="4"/>
              <text x="450" y="70" text-anchor="middle" fill="#94a3b8" font-size="12" font-weight="600">L2 Peers (74.1%)</text>
              <line x1="30" y1="140" x2="550" y2="140" stroke="#cbd5e1" stroke-width="2"/>
            </svg>
          </div>
        </div>
      </div>
    `;
    document.getElementById('chatPane').scrollTop = 1200;
    await sleep(2500);

    // Turn 4: Canvas Presentation Mode
    const p4 = "{prompts[3]}";
    for (let i = 1; i <= p4.length; i++) {{
      promptInput.textContent = p4.slice(0, i);
      promptInput.style.color = '#1e293b';
      await sleep(15);
    }}
    await sleep(400);
    promptInput.textContent = 'Ask a question or enter a prompt...';
    promptInput.style.color = '#94a3b8';

    document.getElementById('canvasPane').style.display = 'flex';
    document.getElementById('chatPane').scrollTop = 1500;
    await sleep(1500);

    // Flip through Canvas slides
    moveCursor(1400, 1020);
    renderSlide(1);
    await sleep(2200);

    moveCursor(1520, 1020);
    renderSlide(2);
    await sleep(2200);

    moveCursor(1640, 1020);
    renderSlide(3);
    await sleep(2200);

    moveCursor(1760, 1020);
    renderSlide(4);
    await sleep(2500);

    // Smooth Overview Scroll
    moveCursor(450, 500);
    document.getElementById('chatPane').scrollTop = 0;
    await sleep(2000);
    document.getElementById('chatPane').scrollTop = 1500;
    await sleep(2000);
  }};
</script>
</body>
</html>
"""
    return html

async def record_agent_video(agent_name: str, reg_agent: dict):
    domain = reg_agent.get('domain', 'defi')
    output_dir = REPO_ROOT / 'demos' / 'gemini-enterprise' / domain
    output_dir.mkdir(parents=True, exist_ok=True)
    mp4_target = output_dir / f"{agent_name}.mp4"
    
    html_content = generate_gemini_enterprise_html(agent_name, reg_agent)
    
    temp_dir = Path(tempfile.mkdtemp(prefix=f"ge_rec_{agent_name}_"))
    temp_html = temp_dir / "index.html"
    temp_html.write_text(html_content, encoding='utf-8')
    
    from playwright.async_api import async_playwright
    
    print(f"🎬 Recording 1080p Web3 Agent UI walkthrough for: [{domain}] {agent_name}...")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            executable_path='/opt/google/chrome/chrome',
            headless=True,
            args=['--no-sandbox', '--disable-gpu', '--window-size=1920,1080']
        )
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            record_video_dir=str(temp_dir),
            record_video_size={'width': 1920, 'height': 1080}
        )
        page = await context.new_page()
        await page.goto(f"file://{temp_html.resolve()}")
        await page.wait_for_load_state("domcontentloaded")
        
        # Trigger sequence
        await page.evaluate("window.runDemoSequence()")
        await asyncio.sleep(26.0) # total duration of high-fidelity animation sequence
        
        await page.close()
        await context.close()
        await browser.close()
        
    # Find recorded webm
    webm_files = list(temp_dir.glob("*.webm"))
    if not webm_files:
        print(f"❌ Error: No webm recorded for {agent_name}")
        return
        
    webm_file = webm_files[0]
    
    # Convert with ffmpeg to high-quality MP4 (H.264, yuv420p)
    cmd = [
        'ffmpeg', '-y',
        '-i', str(webm_file),
        '-c:v', 'libx264',
        '-pix_fmt', 'yuv420p',
        '-preset', 'fast',
        '-crf', '22',
        str(mp4_target)
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    shutil.rmtree(temp_dir, ignore_errors=True)
    print(f"✅ Created 1080p MP4: {mp4_target} ({mp4_target.stat().st_size // 1024} KB)")

async def main():
    registry_file = REPO_ROOT / '_shared' / 'table_registry.yaml'
    with open(registry_file, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    agents_map = data.get('agents', {})
    
    target_agent = sys.argv[1] if len(sys.argv) > 1 else None
    
    if target_agent and target_agent in agents_map:
        await record_agent_video(target_agent, agents_map[target_agent])
    else:
        for name, agent in agents_map.items():
            await record_agent_video(name, agent)

if __name__ == '__main__':
    asyncio.run(main())
