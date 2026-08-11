#!/usr/bin/env python3
"""
deploy_agent_lifecycle.py - Idempotent Agent Deployment, Cleanup & Verification Engine

Provides an automated 7-stage lifecycle for retail enterprise agents:
1. Audit Stage: Capture pre-deploy baseline across Vertex AI and Gemini Enterprise.
2. Cleanup Stage: Idempotently delete legacy/dangling reasoning engines & duplicate GE cards.
3. Backend Deploy Stage: Package and deploy via `adk deploy agent_engine` to us-central1.
4. GE Publishing Stage: Register runtime in Gemini Enterprise with `agents-cli publish`.
5. Deduplication Gate: Assert exactly 1 reasoning engine and 1 registered card (0 duplicates).
6. Demo Recording Stage (Optional): Record 1080p demo via `record_agent_demo.py` & update README.
7. Reporting Stage: Generate domain-scoped Before vs. After Delta Reports.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
import requests
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


@dataclass
class AgentDeployConfig:
    """Encapsulates all deployment configuration for an agent."""
    domain: str
    agent_name: str
    agent_id: str
    display_name: str
    description: str
    project_id: str
    region: str = "us-central1"
    gemini_enterprise_app_id: str = ""
    agent_dir: Path = field(default_factory=lambda: Path("."))


def resolve_agent_config(
    domain: str,
    agent_name: str,
    project_id: str | None = None,
    ge_app_id: str | None = None,
    repo_root: Path = REPO_ROOT,
    load_env: bool = True
) -> AgentDeployConfig:
    """Resolves deployment configuration for an agent from table_registry and .env files."""
    registry_path = repo_root / "_shared" / "table_registry.yaml"
    agent_dir = repo_root / "domains" / domain / "agents" / agent_name
    
    if not registry_path.exists():
        raise FileNotFoundError(f"Table registry not found at: {registry_path}")
    if not agent_dir.exists():
        raise FileNotFoundError(f"Agent directory not found at: {agent_dir}")
        
    with open(registry_path, "r", encoding="utf-8") as f:
        registry = yaml.safe_load(f) or {}
        
    agent_meta = registry.get("agents", {}).get(agent_name, {})
    agent_id = agent_meta.get("agent_id", "")
    display_name = agent_meta.get("display_name", f"{domain.title()}: {agent_name.replace('_', ' ').title()}")
    
    # Read description from root_agent.yaml if present
    description = display_name
    root_agent_path = agent_dir / "root_agent.yaml"
    if root_agent_path.exists():
        try:
            with open(root_agent_path, "r", encoding="utf-8") as f:
                root_data = yaml.safe_load(f) or {}
                description = root_data.get("description", display_name)
        except Exception:
            pass
            
    # Load environment hierarchically: agent .env -> _shared .env -> root .env
    if load_env:
        if (agent_dir / ".env").exists():
            load_dotenv(agent_dir / ".env")
        if (repo_root / "_shared" / ".env").exists():
            load_dotenv(repo_root / "_shared" / ".env")
        if (repo_root / ".env").exists():
            load_dotenv(repo_root / ".env")
        
    resolved_proj = (
        project_id
        or os.environ.get("PROJECT_ID")
        or os.environ.get("GOOGLE_CLOUD_PROJECT")
    )
    if not resolved_proj:
        raise ValueError("PROJECT_ID or GOOGLE_CLOUD_PROJECT must be set in .env or passed via --project-id")
        
    resolved_app = (
        ge_app_id
        or os.environ.get("GEMINI_ENTERPRISE_APP_ID", "")
    )
    # Normalize short engine ID to full Discovery Engine resource name
    if resolved_app and not resolved_app.startswith("projects/"):
        resolved_app = f"projects/{resolved_proj}/locations/global/collections/default_collection/engines/{resolved_app}"
    
    return AgentDeployConfig(
        domain=domain,
        agent_name=agent_name,
        agent_id=agent_id,
        display_name=display_name,
        description=description,
        project_id=resolved_proj,
        region="us-central1",
        gemini_enterprise_app_id=resolved_app,
        agent_dir=agent_dir
    )


class GcpControlPlaneClient:
    """Interacts directly with Vertex AI Agent Engine and Discovery Engine APIs."""
    
    def __init__(self, token: str | None = None):
        self._token = token

    def get_token(self) -> str:
        """Acquires GCP OAuth2 Bearer token using Google Application Default Credentials (ADC)."""
        if self._token:
            return self._token
        try:
            import google.auth
            import google.auth.transport.requests
            credentials, _ = google.auth.default(
                scopes=["https://www.googleapis.com/auth/cloud-platform"]
            )
            auth_req = google.auth.transport.requests.Request()
            credentials.refresh(auth_req)
            self._token = credentials.token
            if self._token:
                return self._token
        except Exception as e:
            raise RuntimeError(
                f"Failed to acquire Google Application Default Credentials (ADC): {e}\n"
                "Please run: gcloud auth application-default login"
            )

        raise RuntimeError("Could not acquire GCP authentication token from ADC.")

    def _headers(self, project_id: str) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.get_token()}",
            "x-goog-user-project": project_id,
            "Content-Type": "application/json"
        }

    def list_reasoning_engines(self, project_id: str, region: str = "us-central1") -> list[dict]:
        """Lists all deployed Vertex AI Reasoning Engines in the specified region."""
        url = f"https://{region}-aiplatform.googleapis.com/v1beta1/projects/{project_id}/locations/{region}/reasoningEngines"
        try:
            resp = requests.get(url, headers=self._headers(project_id), timeout=30)
            if resp.status_code == 200:
                return resp.json().get("reasoningEngines", [])
            else:
                print(f"⚠️ [Vertex AI] list_reasoning_engines HTTP {resp.status_code}: {resp.text[:200]}", file=sys.stderr)
        except Exception as e:
            print(f"⚠️ [Vertex AI] list_reasoning_engines connection error: {e}", file=sys.stderr)
        return []

    def delete_reasoning_engine(self, engine_resource_name: str, project_id: str) -> bool:
        """Deletes a Vertex AI Reasoning Engine."""
        region = "us-central1"
        url = f"https://{region}-aiplatform.googleapis.com/v1beta1/{engine_resource_name}"
        try:
            resp = requests.delete(url, headers=self._headers(project_id), timeout=30)
            return resp.status_code in [200, 202, 204]
        except Exception as e:
            print(f"⚠️ [Vertex AI] delete_reasoning_engine error: {e}", file=sys.stderr)
            return False

    def list_ge_agents(self, app_id: str, project_id: str) -> list[dict]:
        """Lists all registered assistant agents in Gemini Enterprise / Discovery Engine."""
        if not app_id:
            return []
        endpoint = "https://discoveryengine.googleapis.com"
        url = f"{endpoint}/v1alpha/{app_id}/assistants/default_assistant/agents"
        try:
            resp = requests.get(url, headers=self._headers(project_id), timeout=30)
            if resp.status_code == 200:
                return resp.json().get("agents", [])
            else:
                print(f"⚠️ [Discovery Engine] list_ge_agents HTTP {resp.status_code}: {resp.text[:200]}", file=sys.stderr)
        except Exception as e:
            print(f"⚠️ [Discovery Engine] list_ge_agents connection error: {e}", file=sys.stderr)
        return []

    def delete_ge_agent(self, agent_resource_name: str, project_id: str) -> bool:
        """Deletes a registered agent card from Gemini Enterprise Discovery Engine."""
        endpoint = "https://discoveryengine.googleapis.com"
        url = f"{endpoint}/v1alpha/{agent_resource_name}"
        try:
            resp = requests.delete(url, headers=self._headers(project_id), timeout=30)
            return resp.status_code in [200, 202, 204]
        except Exception:
            return False


class AgentLifecycleEngine:
    """Orchestrates the 7-stage deployment, cleanup, and verification lifecycle."""

    def __init__(self, client: GcpControlPlaneClient):
        self.client = client

    def match_resources(self, config: AgentDeployConfig, all_engines: list[dict], all_cards: list[dict]) -> dict:
        """Matches reasoning engines and GE assistant cards for the given agent."""
        target_name = config.display_name.strip().lower()
        matching_engines = [
            e for e in all_engines
            if e.get("displayName", "").strip().lower() == target_name
        ]
        matching_cards = [
            c for c in all_cards
            if c.get("displayName", "").strip().lower() == target_name
        ]
        return {
            "matching_engines": matching_engines,
            "matching_cards": matching_cards
        }

    def clean(self, config: AgentDeployConfig, matching_engines: list[dict], matching_cards: list[dict]) -> dict:
        """Idempotently purges existing cards and reasoning engines."""
        deleted_cards = []
        deleted_engines = []
        
        for card in matching_cards:
            card_name = card.get("name", "")
            if card_name and self.client.delete_ge_agent(card_name, config.project_id):
                deleted_cards.append(card_name)
                time.sleep(2.0)
                
        for eng in matching_engines:
            eng_name = eng.get("name", "")
            if eng_name and self.client.delete_reasoning_engine(eng_name, config.project_id):
                deleted_engines.append(eng_name)
                time.sleep(2.0)
                
        return {
            "deleted_cards": deleted_cards,
            "deleted_engines": deleted_engines
        }

    def deploy_backend(self, config: AgentDeployConfig) -> str:
        """Deploys the agent reasoning engine to Vertex AI via `adk deploy`."""
        cmd = [
            "adk", "deploy", "agent_engine",
            "--project", config.project_id,
            "--region", config.region,
            "--display_name", config.display_name,
            "--description", config.description
        ]
        res = subprocess.run(cmd, cwd=str(config.agent_dir), capture_output=True, text=True, check=True)
        
        meta_path = config.agent_dir / "deployment_metadata.json"
        if meta_path.exists():
            try:
                with open(meta_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    re_id = data.get("remote_agent_engine_id") or data.get("resource_name")
                    if re_id:
                        return re_id
            except Exception:
                pass
        raise RuntimeError(f"Could not extract deployed Reasoning Engine ID from {meta_path}. Output: {res.stdout}")

    def publish_ge(self, config: AgentDeployConfig, reasoning_engine_id: str) -> None:
        """Publishes the deployed reasoning engine to Gemini Enterprise."""
        cmd = [
            "agents-cli", "publish", "gemini-enterprise",
            "--registration-type", "adk",
            "--agent-runtime-id", reasoning_engine_id,
            "--gemini-enterprise-app-id", config.gemini_enterprise_app_id,
            "--display-name", config.display_name,
            "--description", config.description
        ]
        subprocess.run(cmd, cwd=str(config.agent_dir), check=True)

    def record_demo(self, config: AgentDeployConfig, speed: str = "normal", resolution: str = "1080p") -> None:
        """Invokes the Playwright demo recorder engine."""
        cmd = [
            "uv", "run", "python", "_shared/scripts/record_agent_demo.py",
            "--domain", config.domain,
            "--name", config.agent_name,
            "--speed", speed,
            "--resolution", resolution
        ]
        subprocess.run(cmd, cwd=str(REPO_ROOT), check=True)

    def verify_deduplication(self, config: AgentDeployConfig, expected_engine_id: str) -> bool:
        """Verifies exactly 1 reasoning engine and 1 registered card exist and are bound."""
        engines = self.client.list_reasoning_engines(config.project_id, config.region)
        cards = self.client.list_ge_agents(config.gemini_enterprise_app_id, config.project_id)
        matched = self.match_resources(config, engines, cards)
        
        if len(matched["matching_engines"]) != 1:
            raise AssertionError(f"Expected exactly 1 Reasoning Engine, found {len(matched['matching_engines'])}")
        if len(matched["matching_cards"]) != 1:
            raise AssertionError(f"Expected exactly 1 GE Card, found {len(matched['matching_cards'])}")
            
        card_re = (
            matched["matching_cards"][0]
            .get("adkAgentDefinition", {})
            .get("provisionedReasoningEngine", {})
            .get("reasoningEngine", "")
        )
        if expected_engine_id not in card_re:
            raise AssertionError(f"Bound engine '{card_re}' does not match expected '{expected_engine_id}'")
        return True


def group_results_by_domain(results: list[dict]) -> dict[str, list[dict]]:
    """Groups execution results by domain."""
    grouped: dict[str, list[dict]] = {}
    for r in results:
        dom = r.get("domain", "general")
        grouped.setdefault(dom, []).append(r)
    return grouped


def get_domain_report_path(domain: str, repo_root: Path = REPO_ROOT) -> Path:
    """Returns the standardized domain-specific audit report path."""
    return repo_root / "docs" / "reports" / f"{domain}_audit.md"


def generate_delta_report(
    results: list[dict],
    domain: str | None = None,
    output_path: Path | None = None
) -> str:
    """Generates a structured Before vs. After Markdown audit report."""
    now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    domain_title = domain.replace("_", " ").title() if domain else "All Domains"
    
    lines = [
        f"# Deployment Lifecycle & Deduplication Audit Report: {domain_title}",
        f"",
        f"**Generated:** `{now_str}`",
        f"",
        "---",
        f"",
        "## Execution Summary",
        f"",
        "| # | Agent Name | Display Name | Before State | Cleanup Actions | After State | Demo Recorded | Status |",
        "|---|---|---|---|---|---|---|---|"
    ]
    
    for idx, r in enumerate(results, 1):
        lines.append(
            f"| {idx} | `{r['agent_name']}` | {r['display_name']} | {r['before_state']} | {r['cleanup_actions']} | {r['after_state']} | {r.get('demo_recorded', '—')} | {r['status']} |"
        )
        
    healthy_count = sum(1 for r in results if r.get("status") in ["SUCCESS", "HEALTHY"])
    needs_deploy_count = sum(1 for r in results if r.get("status") in ["NEEDS_DEPLOY", "FAILED"])
    duplicate_count = sum(1 for r in results if "Duplicate" in r.get("before_state", "") or r.get("status") == "NEEDS_CLEANUP")
    demo_ready_count = sum(1 for r in results if "Ready" in r.get("demo_recorded", "") or "Recorded" in r.get("demo_recorded", "") or "1080p" in r.get("demo_recorded", ""))

    lines.extend([
        "",
        "---",
        "",
        "## Metrics & Invariant Summary",
        f"- **Total Agents Evaluated:** {len(results)}",
        f"- **Active & Healthy (1:1 Bound):** {healthy_count}",
        f"- **Needing Deployment / Missing Runtime:** {needs_deploy_count}",
        f"- **Demo Videos Available:** {demo_ready_count}",
        f"- **Duplicate Invariants Detected:** {duplicate_count}",
        ""
    ])
    
    if domain:
        lines.extend([
            "---",
            "",
            "## 🌿 Isolated Git Worktree Execution Command",
            "To deploy or redeploy this domain in an isolated worktree:",
            "```bash",
            f"git worktree add .worktrees/deploy_{domain} -b deploy_{domain}",
            f"cd .worktrees/deploy_{domain}",
            f"uv run python _shared/scripts/deploy_agent_lifecycle.py --domain {domain} --record-demo",
            "```",
            ""
        ])
        
    content = "\n".join(lines)
    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(content, encoding="utf-8")
    return content


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parses CLI arguments."""
    parser = argparse.ArgumentParser(
        description="Idempotent Agent Deployment, Cleanup & Verification Engine"
    )
    parser.add_argument("--domain", type=str, help="Target retail domain (e.g. supply_chain)")
    parser.add_argument("--name", type=str, help="Specific agent name (e.g. inbound_freight_optimization)")
    parser.add_argument("--all", action="store_true", help="Process all registered agents across all 9 domains")
    parser.add_argument("--audit-only", action="store_true", help="Perform discovery audit and report without modifying resources")
    parser.add_argument("--record-demo", action="store_true", help="Automatically record 1080p multi-turn demo after successful verification")
    parser.add_argument("--demo-speed", type=str, choices=["normal", "fast"], default="normal", help="Pacing speed for demo recording (default: normal)")
    parser.add_argument("--demo-resolution", type=str, choices=["1080p", "720p"], default="1080p", help="Resolution for demo recording (default: 1080p)")
    parser.add_argument("--project-id", type=str, help="Override GCP Project ID")
    parser.add_argument("--gemini-enterprise-app-id", type=str, help="Override Gemini Enterprise App ID")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """CLI Entrypoint for the lifecycle engine."""
    args = parse_args(argv)
    registry_path = REPO_ROOT / "_shared" / "table_registry.yaml"
    with open(registry_path, "r", encoding="utf-8") as f:
        registry = yaml.safe_load(f) or {}
        
    agents_map = registry.get("agents", {})
    
    # Filter target agents
    targets: list[tuple[str, str]] = []
    if args.name:
        domain = args.domain
        if not domain:
            for ag_name, meta in agents_map.items():
                if ag_name == args.name:
                    domain = meta.get("domain")
                    break
        if not domain:
            print(f"❌ Error: Agent '{args.name}' not found in registry.", file=sys.stderr)
            return 1
        targets.append((domain, args.name))
    elif args.domain:
        for ag_name, meta in agents_map.items():
            if meta.get("domain") == args.domain:
                targets.append((args.domain, ag_name))
    elif args.all:
        for ag_name, meta in agents_map.items():
            targets.append((meta.get("domain"), ag_name))
    else:
        print("❌ Error: Must specify --name, --domain, or --all.", file=sys.stderr)
        return 1

    client = GcpControlPlaneClient()
    engine = AgentLifecycleEngine(client=client)
    
    print("=" * 80)
    print(f"🚀 AGENT DEPLOYMENT LIFECYCLE ENGINE: {len(targets)} Target Agent(s)")
    print(f"Mode: {'AUDIT ONLY' if args.audit_only else 'DEPLOY & VERIFY'}")
    print("=" * 80)
    
    all_results: list[dict] = []
    
    # Pre-fetch control plane state once upfront for fast audit
    cached_engines: list[dict] | None = None
    cached_cards: list[dict] | None = None
    
    for domain, ag_name in targets:
        print(f"\n▶ Processing [{domain}] `{ag_name}`...")
        try:
            config = resolve_agent_config(
                domain=domain,
                agent_name=ag_name,
                project_id=args.project_id,
                ge_app_id=args.gemini_enterprise_app_id
            )
        except Exception as e:
            print(f"❌ Config Error for {ag_name}: {e}")
            all_results.append({
                "domain": domain,
                "agent_name": ag_name,
                "display_name": ag_name,
                "before_state": "❌ Config Error",
                "cleanup_actions": "None",
                "after_state": "❌ Skipped",
                "status": "FAILED"
            })
            continue

        # 1. Audit
        if cached_engines is None or not args.audit_only:
            cached_engines = client.list_reasoning_engines(config.project_id, config.region)
        if cached_cards is None or not args.audit_only:
            cached_cards = client.list_ge_agents(config.gemini_enterprise_app_id, config.project_id)
            
        all_engines = cached_engines
        all_cards = cached_cards
        matched = engine.match_resources(config, all_engines, all_cards)
        num_engines = len(matched["matching_engines"])
        num_cards = len(matched["matching_cards"])
        
        before_state = f"{num_engines} Engine(s), {num_cards} GE Card(s)"
        if num_engines == 0:
            before_state = "❌ No Backend Engine"
        elif num_cards > 1:
            before_state = f"⚠️ {num_cards} Duplicate GE Cards"

        demo_file = REPO_ROOT / "demos" / "gemini-enterprise" / domain / f"{ag_name}.mp4"
        demo_status = "🎬 1080p Ready" if demo_file.exists() else "—"
        
        audit_status = "HEALTHY"
        if num_engines == 0:
            audit_status = "NEEDS_DEPLOY"
        elif num_cards > 1:
            audit_status = "NEEDS_CLEANUP"

        print(f"   📋 Audit: {before_state} | Demo: {demo_status}")
        
        if args.audit_only:
            all_results.append({
                "domain": domain,
                "agent_name": ag_name,
                "display_name": config.display_name,
                "before_state": before_state,
                "cleanup_actions": "Audit Only",
                "after_state": before_state,
                "demo_recorded": demo_status,
                "status": audit_status
            })
            continue
            
        # 2. Cleanup
        clean_res = engine.clean(config, matched["matching_engines"], matched["matching_cards"])
        cleanup_desc = f"Deleted {len(clean_res['deleted_engines'])} engine(s), {len(clean_res['deleted_cards'])} card(s)"
        print(f"   🧹 Cleanup: {cleanup_desc}")
        
        # 3. Backend Deploy
        try:
            print(f"   🚀 Deploying backend to Vertex AI ({config.region})...")
            new_engine_id = engine.deploy_backend(config)
            print(f"   ✓ Deployed Reasoning Engine: {new_engine_id}")
        except Exception as e:
            print(f"   ❌ Deploy failed: {e}")
            all_results.append({
                "domain": domain,
                "agent_name": ag_name,
                "display_name": config.display_name,
                "before_state": before_state,
                "cleanup_actions": cleanup_desc,
                "after_state": "❌ Deploy Failed",
                "status": "FAILED"
            })
            continue
            
        # 4. GE Publish
        try:
            print(f"   📢 Publishing to Gemini Enterprise ({config.gemini_enterprise_app_id})...")
            engine.publish_ge(config, new_engine_id)
            print("   ✓ Published to Gemini Enterprise")
        except Exception as e:
            print(f"   ❌ Publish failed: {e}")
            # Rollback engine
            engine.client.delete_reasoning_engine(new_engine_id, config.project_id)
            all_results.append({
                "domain": domain,
                "agent_name": ag_name,
                "display_name": config.display_name,
                "before_state": before_state,
                "cleanup_actions": cleanup_desc,
                "after_state": "❌ Publish Failed (Rolled Back)",
                "status": "FAILED"
            })
            continue
            
        # 5. Verification
        try:
            print("   🔍 Verifying deduplication & binding...")
            engine.verify_deduplication(config, new_engine_id)
            print("   ✅ Verified 100% healthy: 1 engine, 1 card, 0 duplicates")
            after_state = f"✅ {new_engine_id.split('/')[-1]}"
            status = "SUCCESS"
        except Exception as e:
            print(f"   ❌ Verification failed: {e}")
            after_state = f"❌ Verification Failed: {e}"
            status = "FAILED"
            
        demo_status = "—"
        # 6. Optional Demo Recording
        if status == "SUCCESS" and args.record_demo:
            try:
                print(f"   🎬 Recording demo ({args.demo_speed} speed, {args.demo_resolution})...")
                engine.record_demo(config, speed=args.demo_speed, resolution=args.demo_resolution)
                demo_status = f"🎬 {args.demo_resolution} ({args.demo_speed})"
                print("   ✅ Demo recorded successfully")
            except Exception as e:
                print(f"   ⚠️ Demo recording failed: {e}")
                demo_status = "⚠️ Recording Error"
                
        all_results.append({
            "domain": domain,
            "agent_name": ag_name,
            "display_name": config.display_name,
            "before_state": before_state,
            "cleanup_actions": cleanup_desc,
            "after_state": after_state,
            "demo_recorded": demo_status,
            "status": status
        })

    # Generate domain-scoped reports
    grouped_by_domain = group_results_by_domain(all_results)
    for dom, dom_results in grouped_by_domain.items():
        report_path = get_domain_report_path(dom)
        generate_delta_report(dom_results, domain=dom, output_path=report_path)
        print(f"\n📁 Saved Domain Audit Report: {report_path}")
        
    # Also print console summary
    print("\n" + "=" * 80)
    print(generate_delta_report(all_results, domain=args.domain))
    print("=" * 80)
    
    return 0 if (args.audit_only or all(r.get("status") == "SUCCESS" for r in all_results)) else 1


if __name__ == "__main__":
    sys.exit(main())
