#!/usr/bin/env python3
import re
from pathlib import Path

REPO_ROOT = Path('/usr/local/google/home/daricemahtab/web3-enterprise-agents')
gps_file = REPO_ROOT / '_shared' / 'scripts' / 'generate_portal_site.py'

content = gps_file.read_text(encoding='utf-8')

css_pattern = r'/\* Video Modal matching Retail layout exactly \*/[\s\S]*?(?=/\* Footer \*/)'
retail_modal_css = """/* Video Modal matching Retail layout exactly */
    .modal-backdrop {{ position: fixed; inset: 0; background: var(--modal-overlay); z-index: 100; display: none; align-items: center; justify-content: center; padding: 24px; backdrop-filter: blur(8px); }}
    .modal-dialog {{ background: var(--bg-card); border: 1px solid var(--border-faint); border-radius: 18px; width: 100%; max-width: 960px; max-height: 90vh; display: flex; flex-direction: column; box-shadow: var(--shadow-modal); overflow: hidden; }}
    .modal-header {{ display: flex; justify-content: space-between; align-items: flex-start; padding: 22px 26px 16px; border-bottom: 1px solid var(--border-color); flex-shrink: 0; }}
    .modal-header-left {{ display: flex; flex-direction: column; gap: 8px; }}
    .modal-badges-row {{ display: flex; gap: 8px; align-items: center; }}
    .modal-title {{ font-family: 'Google Sans', sans-serif; font-size: 1.45rem; font-weight: 700; color: var(--text-primary); line-height: 1.25; }}
    .modal-close {{ width: 36px; height: 36px; border-radius: 8px; background: rgba(255, 255, 255, 0.06); border: 1px solid var(--border-color); color: var(--text-secondary); display: flex; align-items: center; justify-content: center; font-size: 1.15rem; cursor: pointer; transition: all 0.15s ease; }}
    .modal-close:hover {{ background: var(--bg-surface); color: var(--text-primary); border-color: var(--border-focus); }}
    .modal-body {{ padding: 22px 26px; overflow-y: auto; display: flex; flex-direction: column; gap: 20px; flex: 1; }}
    .modal-video-wrapper {{ position: relative; width: 100%; min-height: 480px; flex-shrink: 0; background: #000; border-radius: 12px; overflow: hidden; border: 1px solid var(--border-color); box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5); aspect-ratio: 16 / 9; }}
    .modal-video {{ width: 100%; height: 100%; object-fit: cover; background: #000; display: block; }}
    .modal-meta-grid {{ flex-shrink: 0; display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; background: var(--bg-surface); border: 1px solid var(--border-color); border-radius: 10px; padding: 16px 20px; }}
    .modal-meta-item {{ display: flex; flex-direction: column; gap: 4px; }}
    .modal-meta-label {{ font-size: 0.72rem; font-weight: 700; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.05em; }}
    .modal-meta-value {{ font-size: 0.92rem; font-weight: 600; color: var(--text-primary); }}
    .modal-sequence-box {{ flex-shrink: 0; background: var(--bg-surface); border: 1px solid var(--border-color); border-radius: 10px; padding: 20px 22px; }}
    .modal-sequence-title {{ font-size: 0.95rem; font-weight: 700; color: var(--accent-indigo); margin-bottom: 12px; }}
    .modal-turns-list {{ list-style: none; display: flex; flex-direction: column; gap: 10px; font-size: 0.88rem; color: var(--text-secondary); line-height: 1.55; }}
    .modal-turns-list strong {{ color: var(--text-primary); }}
    .modal-footer {{ padding: 16px 26px; border-top: 1px solid var(--border-color); display: flex; justify-content: flex-end; gap: 12px; background: var(--bg-card); flex-shrink: 0; }}
    .btn-download {{ display: inline-flex; align-items: center; gap: 6px; padding: 9px 16px; border-radius: 8px; font-size: 0.88rem; font-weight: 600; color: var(--text-primary); text-decoration: none; border: 1px solid var(--border-color); background: var(--bg-surface); transition: all 0.15s ease; }}
    .btn-download:hover {{ border-color: var(--border-focus); color: var(--accent-blue); }}
    .btn-open-showcase {{ display: inline-flex; align-items: center; gap: 6px; padding: 9px 20px; border-radius: 8px; font-size: 0.88rem; font-weight: 700; color: #0f172a; background: var(--accent-blue); text-decoration: none; transition: all 0.15s ease; }}
    .btn-open-showcase:hover {{ background: var(--accent-blue-hover); color: #ffffff; }}
    
    """

content = re.sub(css_pattern, retail_modal_css, content)
gps_file.write_text(content, encoding='utf-8')
print("Successfully updated generate_portal_site.py with exact Retail scrolling modal!")
