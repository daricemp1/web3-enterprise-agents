import asyncio
from pathlib import Path
from playwright.async_api import async_playwright
import subprocess
import shutil

async def test():
    temp_dir = Path("/tmp/test_rec")
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    html = """<!DOCTYPE html>
<html>
<head>
<style>
  html, body {
    margin: 0;
    padding: 0;
    width: 100vw;
    height: 100vh;
    background: #0f172a;
    color: white;
    font-family: sans-serif;
    display: flex;
    box-sizing: border-box;
    border: 10px solid #38bdf8;
  }
  .sidebar { width: 280px; background: #1e293b; height: 100%; padding: 20px; }
  .content { flex: 1; padding: 40px; background: #0f172a; }
</style>
</head>
<body>
  <div class="sidebar"><h2>Web3 Agents</h2></div>
  <div class="content"><h1>Full Width 1080p View</h1></div>
</body>
</html>
"""
    html_file = temp_dir / "test.html"
    html_file.write_text(html, encoding="utf-8")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            executable_path='/opt/google/chrome/chrome',
            headless=True,
            args=['--no-sandbox', '--disable-gpu', '--window-size=1920,1080', '--force-device-scale-factor=1']
        )
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            device_scale_factor=1.0,
            record_video_dir=str(temp_dir),
            record_video_size={'width': 1920, 'height': 1080}
        )
        page = await context.new_page()
        await page.goto(f"file://{html_file.resolve()}")
        await asyncio.sleep(2.0)
        await page.close()
        await context.close()
        await browser.close()

    webm = list(temp_dir.glob("*.webm"))[0]
    out_mp4 = temp_dir / "test.mp4"
    subprocess.run(['ffmpeg', '-y', '-i', str(webm), '-c:v', 'libx264', '-pix_fmt', 'yuv420p', str(out_mp4)], check=True)
    subprocess.run(['ffmpeg', '-y', '-i', str(out_mp4), '-vframes', '1', '-update', '1', '/tmp/test_frame.png'], check=True)
    print("Test frame created at /tmp/test_frame.png")

asyncio.run(test())
