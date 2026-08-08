#!/usr/bin/env python3
"""Generic Agent Demo Video Recorder for Gemini Enterprise.

Automates opening Gemini Enterprise in Google Chrome using an authenticated Chrome profile,
focuses on the main prompt input box, types '@' followed by the agent name, selects the agent
card that appears above the prompt box, executes the 3 curated prompts from the agent's
README.md sequentially (waiting for each full response to appear on screen before proceeding),
performs a smooth mouse scroll to the top and all the way to the bottom, and records a 1080p demo
video saved as MP4 under demos/gemini-enterprise/<domain>/<agent_name>.mp4.
"""

import argparse
import asyncio
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path
from dotenv import load_dotenv
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from _shared.scripts.prompt_parser import parse_agent_prompts, resolve_agent_domain

# Load environment configuration
load_dotenv(REPO_ROOT / "_shared" / ".env")
load_dotenv(REPO_ROOT / ".env")
DEFAULT_GE_URL = os.getenv("GEMINI_ENTERPRISE_URL", "")
DEFAULT_CHROME_USER_DATA_DIR = Path.home() / ".config" / "google-chrome-demo-recorder"
DEFAULT_SOURCE_CHROME_DIR = Path.home() / ".config" / "google-chrome"
DEFAULT_CHROME_PROFILE_DIR = os.getenv("CHROME_PROFILE_DIR", "Profile 2")
DEFAULT_CHROME_PROFILE_NAME = os.getenv("CHROME_PROFILE_NAME", "Default Profile")


def sync_chrome_profile():
    """Syncs user Chrome profile into demo recorder directory to avoid singleton locks."""
    if not DEFAULT_CHROME_USER_DATA_DIR.exists():
        DEFAULT_CHROME_USER_DATA_DIR.mkdir(parents=True, exist_ok=True)
        print("🔄 Performing initial Chrome profile sync...", flush=True)
        cmd = [
            "rsync", "-av", "--delete",
            "--exclude=Singleton*",
            "--exclude=*Cache*",
            "--exclude=*Crash*",
            "--exclude=BrowserMetrics*",
            str(DEFAULT_SOURCE_CHROME_DIR) + "/",
            str(DEFAULT_CHROME_USER_DATA_DIR) + "/"
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        # Fast sync of Local State and Profile Preferences/Cookies
        for f in ["Local State"]:
            src_f = DEFAULT_SOURCE_CHROME_DIR / f
            tgt_f = DEFAULT_CHROME_USER_DATA_DIR / f
            if src_f.exists():
                shutil.copy2(src_f, tgt_f)
        p_src = DEFAULT_SOURCE_CHROME_DIR / DEFAULT_CHROME_PROFILE_DIR
        p_tgt = DEFAULT_CHROME_USER_DATA_DIR / DEFAULT_CHROME_PROFILE_DIR
        p_tgt.mkdir(parents=True, exist_ok=True)
        for item in ["Preferences", "Secure Preferences", "Cookies", "Network"]:
            src_item = p_src / item
            tgt_item = p_tgt / item
            if src_item.is_file():
                shutil.copy2(src_item, tgt_item)


def get_agent_display_name(agent_name: str, domain: str) -> str:
    """Gets human-readable display name from root_agent.yaml or table_registry.yaml."""
    root_agent_file = REPO_ROOT / "domains" / domain / "agents" / agent_name / "root_agent.yaml"
    if root_agent_file.exists():
        try:
            data = yaml.safe_load(root_agent_file.read_text(encoding="utf-8"))
            if "display_name" in data:
                return data["display_name"]
        except Exception:
            pass
    return agent_name.replace("_", " ").title()


def convert_webm_to_mp4(webm_path: Path, mp4_path: Path) -> bool:
    """Converts recorded webm video to high-quality universal MP4 using ffmpeg."""
    try:
        print(f"🔄 Converting {webm_path.name} to MP4 format...", flush=True)
        cmd = [
            "ffmpeg", "-y",
            "-i", str(webm_path),
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "22",
            "-pix_fmt", "yuv420p",
            str(mp4_path)
        ]
        res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return res.returncode == 0
    except Exception as e:
        print(f"⚠️ FFmpeg conversion error: {e}", flush=True)
        return False


async def wait_for_response_completion(
    page,
    turn_index: int,
    timeout_seconds: int = 120,
    read_pause: float = 6.0
):
    """Waits for the streaming response of turn_index to fully render and the Stop button to change back to Action."""
    print(f"⏳ Waiting for Response {turn_index} to appear and complete streaming on screen...", flush=True)
    
    visible_stops = page.locator("button[aria-label*='Stop' i]:visible, button:has(mat-icon:has-text('stop')):visible")
    
    # Phase 1: Wait up to 15s for generation to start (Stop button appears in prompt bar)
    gen_started = False
    for _ in range(30):
        if await visible_stops.count() > 0:
            gen_started = True
            break
        await asyncio.sleep(0.5)
        
    if gen_started:
        print(f"   ✓ Generation {turn_index} active (Stop button active in prompt bar).", flush=True)
        
    # Phase 2: Wait for generation to finish (Stop button disappears / changes back to Action)
    start_time = asyncio.get_event_loop().time()
    while True:
        is_stop_active = (await visible_stops.count()) > 0
        elapsed = asyncio.get_event_loop().time() - start_time
        if not is_stop_active:
            print(f"   ✓ Response {turn_index} generation completed after {elapsed:.1f}s (Stop button returned to Action).", flush=True)
            break
        if elapsed > timeout_seconds:
            print(f"   ⚠️ Reached {timeout_seconds}s timeout waiting for Response {turn_index}. Proceeding...", flush=True)
            break
        await asyncio.sleep(1.0)
        
    # Phase 3: Short DOM stabilization
    await asyncio.sleep(1.5)
    
    # Phase 4: Reading pause
    print(f"📖 Reading pause ({read_pause:.1f}s) for Response {turn_index}...", flush=True)
    await asyncio.sleep(read_pause)
    print(f"✅ Turn {turn_index} response successfully displayed.\n", flush=True)


async def smooth_mouse_scroll_walkthrough(page):
    """Performs a smooth mouse scroll to the top of the conversation and then down to the bottom."""
    print("\n📜 Performing smooth mouse scroll walkthrough of full conversation...", flush=True)
    
    # Center mouse on viewport
    await page.mouse.move(960, 540)
    await asyncio.sleep(0.5)
    
    print("   ⬆️ Smoothly scrolling mouse up to the top...", flush=True)
    for _ in range(30):
        await page.mouse.wheel(0, -250)
        await asyncio.sleep(0.06)
        
    print("   ⏸️ Pausing at top (3.0s) to showcase agent pill and Turn 1 response...", flush=True)
    await asyncio.sleep(3.0)
    
    print("   ⬇️ Smoothly scrolling mouse down to the bottom...", flush=True)
    for _ in range(30):
        await page.mouse.wheel(0, 250)
        await asyncio.sleep(0.06)
        
    print("   ⏸️ Pausing at bottom (3.0s) to showcase final charts and recommendations...", flush=True)
    await asyncio.sleep(3.0)


async def record_single_agent_demo(
    agent_name: str,
    domain: str,
    prompts: list[str],
    output_dir: Path,
    speed: str = "normal",
    video_format: str = "mp4",
    headless: bool = False,
    chrome_profile_dir: str = DEFAULT_CHROME_PROFILE_DIR,
    ge_url: str = DEFAULT_GE_URL,
    dry_run: bool = False
) -> Path:
    """Executes full flow: opens GE, types @agent, selects card above prompt box, executes 3 prompts with response sync, scrolls top to bottom, records MP4."""
    domain_output_dir = output_dir / domain
    domain_output_dir.mkdir(parents=True, exist_ok=True)
    target_video_file = domain_output_dir / f"{agent_name}.{video_format}"
    
    display_name = get_agent_display_name(agent_name, domain)
    # Extract search title without domain prefix
    agent_clean_title = display_name.split(":")[-1].strip() if ":" in display_name else display_name
    keywords = [w for w in agent_name.split("_") if len(w) > 2]
    mention_keyword = keywords[0].title() if keywords else agent_clean_title
    
    print("\n" + "=" * 60, flush=True)
    print(f"🎬 RECORDING DEMO: {display_name} ({agent_name})", flush=True)
    print(f"📁 Domain: {domain}", flush=True)
    print(f"🎯 Target Video: {target_video_file}", flush=True)
    print(f"👤 Chrome Profile: {chrome_profile_dir} ({DEFAULT_CHROME_PROFILE_NAME})", flush=True)
    print(f"⚡ Pacing Speed: {speed}", flush=True)
    print(f"🎞️ Output Format: {video_format.upper()}", flush=True)
    print("📝 Prompts to Execute:", flush=True)
    for idx, p in enumerate(prompts, 1):
        print(f"   {idx}. {p}", flush=True)
    print("=" * 60, flush=True)
    
    if dry_run:
        print("🔍 [DRY-RUN] Validation passed. Skipping browser launch.", flush=True)
        return target_video_file

    sync_chrome_profile()
    
    from playwright.async_api import async_playwright
    
    temp_video_dir = domain_output_dir / f".tmp_video_{agent_name}_{int(time.time())}"
    temp_video_dir.mkdir(parents=True, exist_ok=True)
    
    keystroke_delay = 25 if speed == "normal" else 0
    mention_delay = 60 if speed == "normal" else 10
    read_pause = 6.0 if speed == "normal" else 2.5
    action_pause = 2.0 if speed == "normal" else 0.8

    async with async_playwright() as p:
        print("🌐 Launching Google Chrome with authenticated session...", flush=True)
        context = await p.chromium.launch_persistent_context(
            user_data_dir=str(DEFAULT_CHROME_USER_DATA_DIR),
            channel="chrome",
            headless=headless,
            record_video_dir=str(temp_video_dir),
            record_video_size={"width": 1920, "height": 1080},
            viewport={"width": 1536, "height": 864},
            device_scale_factor=1.25,
            ignore_default_args=["--password-store=basic", "--use-mock-keychain"],
            args=[
                f"--profile-directory={chrome_profile_dir}",
                "--password-store=detect",
                "--force-device-scale-factor=1.25",
                "--disable-blink-features=AutomationControlled",
                "--no-default-browser-check",
                "--start-maximized"
            ]
        )
        
        page = context.pages[0] if context.pages else await context.new_page()
        
        try:
            print(f"🔗 Navigating to Gemini Enterprise: {ge_url}", flush=True)
            await page.goto(ge_url, wait_until="domcontentloaded", timeout=45000)
            await asyncio.sleep(4.0)
            
            # --- STEP 1: Focus on main home prompt input box ---
            print("👉 Step 1: Focusing on main prompt input box...", flush=True)
            prompt_box = page.locator("div[contenteditable='true']:visible, textarea:visible").first
            await prompt_box.wait_for(state="visible", timeout=20000)
            await prompt_box.click()
            await asyncio.sleep(action_pause)

            # --- STEP 2: Type @ followed by agent name ---
            mention_text = f"@{mention_keyword}"
            print(f"👉 Step 2: Typing mention query \"{mention_text}\" in prompt box...", flush=True)
            await prompt_box.press_sequentially(mention_text, delay=mention_delay)
            await asyncio.sleep(1.5)

            # --- STEP 3: Select agent card showing up above the prompt box ---
            print(f"👉 Step 3: Selecting agent card for '{display_name}' above prompt box...", flush=True)
            agent_card_selectors = [
                f"[role='option']:visible:has-text('{agent_clean_title}')",
                f"[role='option']:visible:has-text('{mention_keyword}')",
                f"mat-option:visible:has-text('{agent_clean_title}')",
                f".mention-item:visible:has-text('{agent_clean_title}')",
                f"[class*='mention']:visible:has-text('{agent_clean_title}')",
                f"[role='option']:visible"
            ]

            selected = False
            for sel in agent_card_selectors:
                el = page.locator(sel).first
                if await el.is_visible():
                    print(f"   ✓ Found agent card above prompt box: {sel}", flush=True)
                    await el.click()
                    selected = True
                    break

            if not selected:
                print("   ℹ️ Fallback: Pressing Enter to select agent suggestion.", flush=True)
                await prompt_box.press("Enter")

            await asyncio.sleep(action_pause)
            print("   ✓ Agent successfully selected and pinned in prompt box.", flush=True)

            # --- STEP 4: Execute 3 prompts sequentially with response sync ---
            print("👉 Step 4: Executing 3 prompts sequentially with response synchronization...", flush=True)
            for turn_idx, prompt_text in enumerate(prompts, 1):
                print(f"\n--- Turn {turn_idx}/3 ---", flush=True)
                print(f"💬 Typing Prompt {turn_idx}: \"{prompt_text}\"", flush=True)
                
                input_box = page.locator("div[contenteditable='true']:visible, textarea:visible").last
                await input_box.wait_for(state="visible", timeout=25000)
                await input_box.click()
                await asyncio.sleep(0.5)
                
                if speed == "normal":
                    await input_box.press_sequentially(prompt_text, delay=keystroke_delay)
                else:
                    await input_box.fill(prompt_text)
                    
                await asyncio.sleep(0.8)
                
                print(f"📤 Submitting Prompt {turn_idx}...", flush=True)
                send_btn = page.locator("button[aria-label*='Send' i], button[aria-label*='Submit' i]").first
                if turn_idx == 1 and await send_btn.is_visible():
                    await send_btn.click()
                else:
                    await input_box.press("Enter")
                
                # Active wait for response to appear on screen and finish streaming
                await wait_for_response_completion(page, turn_index=turn_idx, read_pause=read_pause)
                print(f"✅ Turn {turn_idx} response successfully displayed.", flush=True)
                
            print("\n🎉 All 3 responses have been received and verified on screen!", flush=True)
            
            # --- STEP 5: Mouse scroll walkthrough from top to bottom ---
            await smooth_mouse_scroll_walkthrough(page)
            
            print("\n🏁 Finalizing video recording session...", flush=True)
            await asyncio.sleep(2.0)
            
        except Exception as e:
            print(f"❌ Recording error: {e}", flush=True)
        finally:
            await context.close()
            print("🚪 Browser closed.", flush=True)
            
    recorded_videos = list(temp_video_dir.glob("*.webm"))
    if recorded_videos:
        raw_video = recorded_videos[0]
        if video_format == "mp4":
            converted = convert_webm_to_mp4(raw_video, target_video_file)
            if not converted:
                print("⚠️ Falling back to raw WebM file.", flush=True)
                shutil.move(str(raw_video), str(domain_output_dir / f"{agent_name}.webm"))
                target_video_file = domain_output_dir / f"{agent_name}.webm"
        else:
            shutil.move(str(raw_video), str(target_video_file))
            
        shutil.rmtree(str(temp_video_dir), ignore_errors=True)
        print(f"\n🎥 Video successfully saved to: {target_video_file} ({target_video_file.stat().st_size / 1024 / 1024:.2f} MB)", flush=True)
    else:
        print("⚠️ No video file generated.", flush=True)
        
    return target_video_file


def main():
    parser = argparse.ArgumentParser(description="Generic Agent Demo Video Recorder for Gemini Enterprise")
    parser.add_argument("--name", type=str, help="Target agent name (e.g. cart_checkout_analytics)")
    parser.add_argument("--domain", type=str, help="Target retail domain (e.g. e_commerce). Auto-discovered if omitted.")
    parser.add_argument("--all", action="store_true", help="Record all agents in the specified domain (or all domains)")
    parser.add_argument("--speed", choices=["normal", "fast"], default="normal", help="Pacing speed (default: normal)")
    parser.add_argument("--format", choices=["mp4", "webm"], default="mp4", help="Video output format (default: mp4)")
    parser.add_argument("--headless", action="store_true", help="Run browser in headless mode (default is headed)")
    parser.add_argument("--output-dir", type=Path, default=REPO_ROOT / "demos" / "gemini-enterprise", help="Base output directory for recorded videos")
    parser.add_argument("--profile", type=str, default=DEFAULT_CHROME_PROFILE_DIR, help="Chrome profile directory name (default: Profile 2)")
    parser.add_argument("--url", type=str, default=DEFAULT_GE_URL, help="Gemini Enterprise URL (default: GEMINI_ENTERPRISE_URL env var)")
    parser.add_argument("--dry-run", action="store_true", help="Validate prompt parsing without launching the browser")
    
    args = parser.parse_args()
    
    if not args.dry_run and not args.url:
        parser.error("GEMINI_ENTERPRISE_URL must be set in .env or passed via --url")
        
    if not args.name and not args.all:
        parser.error("Must provide either --name <agent_name> or --all")
        
    agents_to_record = []
    
    if args.name:
        domain = args.domain or resolve_agent_domain(args.name, REPO_ROOT)
        readme = REPO_ROOT / "domains" / domain / "agents" / args.name / "README.md"
        prompts = parse_agent_prompts(readme)
        agents_to_record.append((args.name, domain, prompts))
    elif args.all:
        if args.domain:
            agent_dirs = sorted((REPO_ROOT / "domains" / args.domain / "agents").glob("*"))
            for ad in agent_dirs:
                if ad.is_dir() and (ad / "README.md").exists():
                    prompts = parse_agent_prompts(ad / "README.md")
                    agents_to_record.append((ad.name, args.domain, prompts))
        else:
            agent_dirs = sorted(REPO_ROOT.glob("domains/*/agents/*"))
            for ad in agent_dirs:
                if ad.is_dir() and (ad / "README.md").exists():
                    domain = ad.parent.parent.name
                    prompts = parse_agent_prompts(ad / "README.md")
                    agents_to_record.append((ad.name, domain, prompts))
                    
    print(f"📋 Found {len(agents_to_record)} agent(s) to record.", flush=True)
    
    for agent_name, domain, prompts in agents_to_record:
        asyncio.run(
            record_single_agent_demo(
                agent_name=agent_name,
                domain=domain,
                prompts=prompts,
                output_dir=args.output_dir,
                speed=args.speed,
                video_format=args.format,
                headless=args.headless,
                chrome_profile_dir=args.profile,
                ge_url=args.url,
                dry_run=args.dry_run
            )
        )


if __name__ == "__main__":
    main()
