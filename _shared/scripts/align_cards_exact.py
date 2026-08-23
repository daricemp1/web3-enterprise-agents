#!/usr/bin/env python3
import json
import yaml
from pathlib import Path

REPO_ROOT = Path('/usr/local/google/home/daricemahtab/web3-enterprise-agents')

CLEAN_DESCRIPTIONS = {
    "order_book_depth": "Analyzes bid-ask spread efficiency, top-of-book depth, order book imbalance, and slippage across major spot and perpetual trading pairs to optimize institutional order routing.",
    "proof_of_reserves": "Verifies centralized exchange collateralization by comparing on-chain wallet holdings against declared customer liabilities in real-time to alert on solvency drift.",
    "whale_custody_flows": "Tracks institutional deposits, treasury movements, and exchange hot/cold wallet rebalancing to detect large-scale liquidity shifts before market impact.",
    "l2_sequencer_throughput": "Monitors Layer-2 rollup sequencer health, transaction batch compression, EIP-4844 blob gas consumption, and L1 settlement costs to ensure uninterrupted network throughput.",
    "validator_rpc_health": "Evaluates global RPC node latency, block proposal sync, validator attestation effectiveness, and peer counts to prevent consensus degradation and slashing.",
    "mev_arbitrage_radar": "Identifies frontrunning, sandwich attacks, backrunning arbitrage, and block builder priority fees to protect liquidity pools and traders from predatory MEV extraction.",
    "dex_amm_liquidity": "Analyzes automated market maker (AMM) pool depths, 24-hour volume-to-TVL ratios, fee generation, and impermanent loss to optimize liquidity provider yield.",
    "lending_liquidation_risk": "Tracks collateralization ratios, borrow utilization rates, health factor distributions, and impending underwater positions across major decentralized lending markets.",
    "yield_staking_optimizer": "Compares liquid staking token (LST) yields, reward distribution APRs, and peg discounts to optimize risk-adjusted capital deployment across DeFi vaults.",
    "bridge_outflow_monitor": "Tracks cross-chain bridge transfer velocity, lock-and-mint vs burn liquidity imbalances, and alerts on anomalous multi-chain capital flight."
}

# Update table_registry.yaml
reg_file = REPO_ROOT / '_shared' / 'table_registry.yaml'
if reg_file.exists():
    with open(reg_file, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    for name, desc in CLEAN_DESCRIPTIONS.items():
        if name in data.get('agents', {}):
            data['agents'][name]['description'] = desc
    with open(reg_file, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, sort_keys=False, allow_unicode=True)
    print("Updated table_registry.yaml descriptions")

