# Deployment Lifecycle & Deduplication Audit Report: Infra

**Generated:** `2026-08-23 05:57:53 UTC`

---

## Execution Summary

| # | Agent Name | Display Name | Before State | Cleanup Actions | After State | Demo Recorded | Status |
|---|---|---|---|---|---|---|---|
| 1 | `l2_sequencer_throughput` | INFRA: L2 Sequencer & Blob Gas Throughput | ❌ Missing Runtime & Card | Deleted 0 engine(s), 0 card(s) | ✅ 4743690635679105024 | — | SUCCESS |
| 2 | `validator_rpc_health` | INFRA: RPC Latency & Validator Health | ❌ Missing Runtime & Card | Deleted 0 engine(s), 0 card(s) | ✅ 260357206631776256 | — | SUCCESS |
| 3 | `mev_arbitrage_radar` | INFRA: MEV & Sandwich Attack Radar | ❌ Missing Runtime & Card | Deleted 0 engine(s), 0 card(s) | ✅ 6014831630504427520 | — | SUCCESS |

---

## Metrics & Invariant Summary
- **Total Agents Evaluated:** 3
- **Active & Healthy (1:1 Bound):** 3
- **Needing Deployment / Missing Runtime:** 0
- **Demo Videos Available:** 0
- **Duplicate Invariants Detected:** 0

---

## 🌿 Isolated Git Worktree Execution Command
To deploy or redeploy this domain in an isolated worktree:
```bash
git worktree add .worktrees/deploy_infra -b deploy_infra
cd .worktrees/deploy_infra
uv run python _shared/scripts/deploy_agent_lifecycle.py --domain infra --record-demo
```
