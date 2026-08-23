# Web3 Enterprise Agents

> **Google Agent Development Kit (ADK) Agents for Web3**  
> 10 Declarative On-Chain & Market Intelligence Agents across 3 Strategic Web3 Domains (**CEX**, **INFRA**, **DEFI**).

---

## 🌟 System Overview

**Web3 Enterprise Agents** is an enterprise-grade AI assistant ecosystem powered by the **Google Agent Development Kit (ADK)** for **Web3 Enterprise Intelligence**. It provides protocol founders, liquidity managers, risk officers, and DeFi traders with autonomous, natural-language business intelligence grounded in **Google BigQuery on-chain data** and **Google Search live market intelligence**.

```
User Prompt (Web3 Agent Platform)
       │
       ▼
Root Orchestrator Agent (LlmAgent / gemini-3.5-flash)
       │
       ├──► Data Insights Sub-Agent ──────► BigQuery CA API (On-Chain SQL, TVL Forecasts, Whale Anomalies)
       │                                     └── Authorized Dataset: web3_enterprise_agents
       │                                     └── Chart Generator (render_chart -> PNG)
       │
       └──► Market Context Sub-Agent ────► Google Search Grounding (Live token prices, governance forums)
       │
       ▼
Synthesized Executive Briefing / Canvas Presentation
```

---

## 🏛️ Strategic Domains & 10 Deployed Agents

| Domain | Domain ID | Agent Name | Focus Area & Key Metrics |
| :--- | :---: | :--- | :--- |
| **Centralized Exchanges & Trading** | `cex` | **Order Book Depth & Spread Analytics** | Bid-ask spreads, 2% depth, order book imbalance, institutional trade slippage. |
| | | **Proof of Reserves (PoR) & Solvency** | On-chain reserve verification, customer liability coverage, cold storage ratio. |
| | | **Whale Inflows & Custody Transfers** | Large exchange deposit alerts, hot/cold wallet rebalancing, reserve drawdowns. |
| **Blockchain Infrastructure & L2** | `infra` | **L2 Sequencer & Blob Gas Throughput** | Rollup TPS, EIP-4844 blob gas usage, batch verification latency, L1 settlement cost. |
| | | **RPC Latency & Validator Health** | Multi-region RPC endpoint latency, validator attestation rate, slash risk alerts. |
| | | **MEV & Sandwich Attack Radar** | Maximal extractable value (MEV) bundles, sandwich loss detection, builder bribes. |
| **Decentralized Finance & Protocols**| `defi` | **AMM Liquidity & Impermanent Loss** | Pool TVL, 24h volume/TVL capital efficiency, fee generation, impermanent loss. |
| | | **Lending Health & Liquidation Risk** | Collateralization ratios, health factor distribution, bad debt prevention. |
| | | **Liquid Staking & Yield Optimizer** | Liquid staking yields (LSTs), vault reward APRs, risk-adjusted yield comparison. |
| | | **Cross-Chain Bridge & Outflow Monitor** | Bridge transfer velocity, pool utilization %, anomalous cross-chain flight. |

---

## 🚀 Quickstart & Development

### 1. Prerequisites
- Python 3.10+
- [uv](https://docs.astral.sh/uv/) (Python package manager)
- Google Cloud SDK (`gcloud` and `bq`)

### 2. Setup
```bash
# Sync dependencies
uv sync

# Verify ADK installation
uv run --frozen adk --help
```

### 3. Local Simulation & Web Chat
```bash
# Test an individual agent in the terminal
uv run --frozen adk run domains/defi/agents/dex_amm_liquidity

# Launch the local Web UI to chat with all 10 agents
uv run --frozen adk web domains/
```

### 4. BigQuery Data Ingestion
```bash
# Load seed CSV data into BigQuery for an agent
uv run --frozen python _shared/scripts/load_agent_data.py \
    --domain defi --name dex_amm_liquidity \
    --project <YOUR_GCP_PROJECT_ID> --dataset web3_enterprise_agents
```

### 5. Deployment & Gemini Enterprise Registration
```bash
# Automated 7-stage deployment & verification
uv run --frozen python _shared/scripts/deploy_agent_lifecycle.py \
    --domain defi --agent-name dex_amm_liquidity \
    --project-id <YOUR_GCP_PROJECT_ID>
```

---

## 📁 Repository Structure

```
web3-enterprise-agents/
├── _shared/
│   ├── instructions/             # Persona, Web3 safety/grounding, output formatting
│   ├── templates/logical_agent/  # ADK agent skeleton template
│   ├── table_registry.yaml       # Central catalog (3 domains, 10 agents)
│   └── scripts/                  # Scaffolding, data loader, IAM, deploy, and demo scripts
├── domains/
│   ├── cex/agents/               # 3 CEX agents
│   ├── infra/agents/             # 3 Infrastructure agents
│   └── defi/agents/              # 4 DeFi agents
├── pyproject.toml / uv.lock      # Project & ADK dependencies
└── README.md                     # Main documentation
```
