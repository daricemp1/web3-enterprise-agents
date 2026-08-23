#!/usr/bin/env python3
import re
from pathlib import Path

REPO_ROOT = Path('/usr/local/google/home/daricemahtab/web3-enterprise-agents')
gps_file = REPO_ROOT / '_shared' / 'scripts' / 'generate_portal_site.py'

content = gps_file.read_text(encoding='utf-8')

# 1. Add Architecture Blueprint CSS
arch_css = """
    /* Architecture Blueprint Modal matching Retail Parity */
    .arch-tier {
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 14px;
      padding: 20px 22px;
      position: relative;
    }
    .arch-tier-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 16px;
      padding-bottom: 10px;
      border-bottom: 1px solid var(--border-faint);
    }
    .arch-tier-title {
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 1.05rem;
      font-weight: 700;
      color: var(--text-primary);
    }
    .arch-tier-badge {
      font-size: 0.72rem;
      font-weight: 700;
      padding: 3px 10px;
      border-radius: 6px;
      background: rgba(56, 189, 248, 0.12);
      border: 1px solid rgba(56, 189, 248, 0.28);
      color: #38bdf8;
      font-family: 'JetBrains Mono', monospace;
    }
    .arch-tier-badge.green {
      background: rgba(52, 211, 153, 0.12);
      border-color: rgba(52, 211, 153, 0.28);
      color: #34d399;
    }
    .arch-tier-badge.purple {
      background: rgba(167, 139, 250, 0.12);
      border-color: rgba(167, 139, 250, 0.28);
      color: #a78bfa;
    }
    .arch-cards-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 12px;
    }
    .arch-card-item {
      background: var(--bg-surface);
      border: 1px solid var(--border-color);
      border-radius: 10px;
      padding: 14px 16px;
      display: flex;
      flex-direction: column;
      gap: 4px;
    }
    .arch-card-title {
      font-size: 0.88rem;
      font-weight: 700;
      color: var(--text-primary);
    }
    .arch-card-desc {
      font-size: 0.78rem;
      color: var(--text-secondary);
      line-height: 1.45;
    }
    .arch-flow-arrow {
      text-align: center;
      color: var(--accent-blue);
      font-size: 1rem;
      margin: 4px 0;
    }
    .arch-split-row {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 16px;
    }
    .arch-sub-tier {
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 14px;
      padding: 18px 20px;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }
    .arch-pillars-box {
      background: var(--bg-surface);
      border: 1px solid var(--border-color);
      border-radius: 12px;
      padding: 18px 22px;
      display: flex;
      flex-direction: column;
      gap: 10px;
      margin-top: 4px;
    }
    .arch-pillars-title {
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 0.95rem;
      font-weight: 700;
      color: var(--accent-indigo);
    }
    .arch-pillar-item {
      font-size: 0.82rem;
      color: var(--text-secondary);
      line-height: 1.5;
    }
    .arch-pillar-item strong {
      color: var(--text-primary);
    }
"""

content = content.replace("/* Footer */", arch_css + "\n    /* Footer */")

# 2. Replace Architecture Modal HTML
old_arch_modal = """  <!-- Architecture Modal -->
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
  </div>"""

new_arch_modal = """  <!-- Architecture Blueprint Modal matching Retail 4-Tier Topology -->
  <div class="modal-backdrop" id="archModal">
    <div class="modal-dialog" style="max-width: 1040px; max-height: 92vh;">
      <div class="modal-header">
        <div class="modal-header-left">
          <h2 style="font-family: 'Google Sans'; font-size: 1.45rem; font-weight: 700;">📐 Web3 Enterprise Multi-Agent Architecture</h2>
          <span style="font-size: 0.8rem; color: var(--text-muted);">Enterprise 4-Tier Google ADK & Vertex AI Multi-Agent Topology</span>
        </div>
        <button class="modal-close" id="archClose">✕</button>
      </div>
      
      <div class="modal-body" style="gap: 14px;">
        
        <!-- Tier 1: Client & Presentation Layer -->
        <div class="arch-tier">
          <div class="arch-tier-header">
            <div class="arch-tier-title"><span>💬</span> Tier 1: Client & Presentation Layer</div>
            <span class="arch-tier-badge">Web3 Agent Platform</span>
          </div>
          <div class="arch-cards-grid">
            <div class="arch-card-item">
              <div class="arch-card-title">Discovery Engine Assistant</div>
              <div class="arch-card-desc">10 Registered Enterprise Web3 Agents searchable via natural language chat</div>
            </div>
            <div class="arch-card-item">
              <div class="arch-card-title">Real-Time SSE Streaming</div>
              <div class="arch-card-desc">Live multi-turn token streaming & dynamic markdown formatting</div>
            </div>
            <div class="arch-card-item">
              <div class="arch-card-title">Web3 Canvas Presentations</div>
              <div class="arch-card-desc">Automated 4-slide executive decks generated directly from queries</div>
            </div>
          </div>
        </div>

        <div class="arch-flow-arrow">▼</div>

        <!-- Tier 2: Orchestration & Multi-Agent Reasoning -->
        <div class="arch-tier">
          <div class="arch-tier-header">
            <div class="arch-tier-title"><span>🧠</span> Tier 2: Orchestration & Multi-Agent Reasoning</div>
            <span class="arch-tier-badge">Vertex AI Agent Engine</span>
          </div>
          <div class="arch-cards-grid" style="grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));">
            <div class="arch-card-item">
              <div class="arch-card-title">Declarative ADK Framework</div>
              <div class="arch-card-desc">Zero-boilerplate root orchestrators (<code>root_agent.yaml</code>)</div>
            </div>
            <div class="arch-card-item">
              <div class="arch-card-title">Vertex AI Reasoning Engines</div>
              <div class="arch-card-desc"><code>us-central1</code> hosting containers with auto-scaling & memory management</div>
            </div>
            <div class="arch-card-item">
              <div class="arch-card-title">Global Model Inference</div>
              <div class="arch-card-desc"><code>gemini-3.5-flash</code> with low latency via global inference endpoint</div>
            </div>
            <div class="arch-card-item">
              <div class="arch-card-title">Lifecycle Callbacks</div>
              <div class="arch-card-desc">IAM token scoping, date injection & dataset context binding</div>
            </div>
          </div>
        </div>

        <div class="arch-flow-arrow">▼</div>

        <!-- Tier 3: Dual Sub-Agent Split Row -->
        <div class="arch-split-row">
          
          <!-- Sub-Agent 3A -->
          <div class="arch-sub-tier" style="border-top: 3px solid #34d399;">
            <div class="arch-tier-header" style="margin-bottom: 0;">
              <div class="arch-tier-title" style="font-size: 0.95rem;"><span>📊</span> Sub-Agent 3A: BigQuery Data Insights</div>
              <span class="arch-tier-badge green">Conversational Analytics</span>
            </div>
            <div class="arch-card-item">
              <div class="arch-card-title">Natural Language to SQL Engine</div>
              <div class="arch-card-desc">Conversational Analytics API executes parameterized SQL directly</div>
            </div>
            <div class="arch-card-item">
              <div class="arch-card-title">Built-in ML Models</div>
              <div class="arch-card-desc">BigQuery forecasting, anomaly detection & contribution analysis</div>
            </div>
            <div class="arch-card-item">
              <div class="arch-card-title">Matplotlib Chart Generator</div>
              <div class="arch-card-desc">Serverless visual chart rendering (<code>render_chart</code>)</div>
            </div>
          </div>

          <!-- Sub-Agent 3B -->
          <div class="arch-sub-tier" style="border-top: 3px solid #38bdf8;">
            <div class="arch-tier-header" style="margin-bottom: 0;">
              <div class="arch-tier-title" style="font-size: 0.95rem;"><span>🌐</span> Sub-Agent 3B: Market Context & Grounding</div>
              <span class="arch-tier-badge">Google Search Grounding</span>
            </div>
            <div class="arch-card-item">
              <div class="arch-card-title">Real-Time Web Grounding</div>
              <div class="arch-card-desc">Live Google Search verification for fresh protocol news & trends</div>
            </div>
            <div class="arch-card-item">
              <div class="arch-card-title">External Benchmarks</div>
              <div class="arch-card-desc">DeFi Llama, Etherscan, CoinGecko, Dune & L2Beat on-chain stats</div>
            </div>
            <div class="arch-card-item">
              <div class="arch-card-title">Protocol Intelligence</div>
              <div class="arch-card-desc">Live market pricing, MEV radar tracking & liquidity depth analytics</div>
            </div>
          </div>

        </div>

        <div class="arch-flow-arrow">▼</div>

        <!-- Tier 4: Enterprise Web3 Data Lakehouse -->
        <div class="arch-tier">
          <div class="arch-tier-header">
            <div class="arch-tier-title"><span>🗄️</span> Tier 4: Enterprise Web3 Data Lakehouse</div>
            <span class="arch-tier-badge purple">Google Cloud BigQuery</span>
          </div>
          <div class="arch-cards-grid">
            <div class="arch-card-item">
              <div class="arch-card-title">Enterprise Dataset</div>
              <div class="arch-card-desc"><code>web3_enterprise_agents</code> multi-domain on-chain schema</div>
            </div>
            <div class="arch-card-item">
              <div class="arch-card-title">20 Partitioned Tables</div>
              <div class="arch-card-desc">Structured namespace: <code>&lt;domain_id&gt;_&lt;agent_id&gt;_&lt;table_name&gt;</code></div>
            </div>
            <div class="arch-card-item">
              <div class="arch-card-title">IAM Table Allowlisting</div>
              <div class="arch-card-desc">Strict per-agent service account dataset authorization</div>
            </div>
          </div>
        </div>

        <!-- Key Architectural Pillars -->
        <div class="arch-pillars-box">
          <div class="arch-pillars-title"><span>🚀</span> Key Architectural Pillars</div>
          <div class="arch-pillar-item">
            <strong>Declarative ADK Architecture:</strong> Zero-code orchestrator models bind BigQuery tools and Google Search tools with strict domain separation.
          </div>
          <div class="arch-pillar-item">
            <strong>Global Low-Latency Inference:</strong> <code>gemini-3.5-flash</code> global routing delivers ~30% faster time-to-first-token than regional clusters.
          </div>
          <div class="arch-pillar-item">
            <strong>Dual Sub-Agent Pattern:</strong> Quantitative BigQuery queries and qualitative market grounding execute in specialized sub-agent contexts for hallucination-free answers.
          </div>
        </div>

      </div>
      
      <div class="modal-footer">
        <button class="btn-header btn-primary-header" id="archOk">Close Blueprint</button>
      </div>
    </div>
  </div>"""

content = content.replace(old_arch_modal, new_arch_modal)

gps_file.write_text(content, encoding='utf-8')
print("Successfully updated Architecture Blueprint modal in generate_portal_site.py!")
