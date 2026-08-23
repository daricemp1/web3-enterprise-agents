# Deployment Lifecycle & Deduplication Audit Report: Defi

**Generated:** `2026-08-23 05:57:53 UTC`

---

## Execution Summary

| # | Agent Name | Display Name | Before State | Cleanup Actions | After State | Demo Recorded | Status |
|---|---|---|---|---|---|---|---|
| 1 | `dex_amm_liquidity` | DEFI: AMM Liquidity & Impermanent Loss | ⚠️ 1 Engine(s), 0 Cards (Unpublished) | Deleted 1 engine(s), 0 card(s) | ✅ 1147566333223763968 | — | SUCCESS |
| 2 | `lending_liquidation_risk` | DEFI: Lending Health & Liquidation Risk | ❌ Missing Runtime & Card | Deleted 0 engine(s), 0 card(s) | ✅ 3520963336848015360 | — | SUCCESS |
| 3 | `yield_staking_optimizer` | DEFI: Liquid Staking & Yield Optimizer | ❌ Missing Runtime & Card | Deleted 0 engine(s), 0 card(s) | ✅ 3946553501634527232 | — | SUCCESS |
| 4 | `bridge_outflow_monitor` | DEFI: Cross-Chain Bridge & Outflow Monitor | ❌ Missing Runtime & Card | Deleted 0 engine(s), 0 card(s) | ✅ 1413278711238623232 | — | SUCCESS |

---

## Metrics & Invariant Summary
- **Total Agents Evaluated:** 4
- **Active & Healthy (1:1 Bound):** 4
- **Needing Deployment / Missing Runtime:** 0
- **Demo Videos Available:** 0
- **Duplicate Invariants Detected:** 0

---

## 🌿 Isolated Git Worktree Execution Command
To deploy or redeploy this domain in an isolated worktree:
```bash
git worktree add .worktrees/deploy_defi -b deploy_defi
cd .worktrees/deploy_defi
uv run python _shared/scripts/deploy_agent_lifecycle.py --domain defi --record-demo
```
