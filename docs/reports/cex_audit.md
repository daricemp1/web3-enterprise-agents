# Deployment Lifecycle & Deduplication Audit Report: Cex

**Generated:** `2026-08-23 05:57:53 UTC`

---

## Execution Summary

| # | Agent Name | Display Name | Before State | Cleanup Actions | After State | Demo Recorded | Status |
|---|---|---|---|---|---|---|---|
| 1 | `order_book_depth` | CEX: Order Book Depth & Spread Analytics | ❌ Missing Runtime & Card | Deleted 0 engine(s), 0 card(s) | ✅ 5549272019025002496 | — | SUCCESS |
| 2 | `proof_of_reserves` | CEX: Proof of Reserves & Solvency | ❌ Missing Runtime & Card | Deleted 0 engine(s), 0 card(s) | ✅ 9139203871992709120 | — | SUCCESS |
| 3 | `whale_custody_flows` | CEX: Whale Inflows & Custody Transfers | ❌ Missing Runtime & Card | Deleted 0 engine(s), 0 card(s) | ✅ 6221997213363470336 | — | SUCCESS |

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
git worktree add .worktrees/deploy_cex -b deploy_cex
cd .worktrees/deploy_cex
uv run python _shared/scripts/deploy_agent_lifecycle.py --domain cex --record-demo
```
