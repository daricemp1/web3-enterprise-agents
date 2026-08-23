#!/usr/bin/env python3
import re
from pathlib import Path

REPO_ROOT = Path('/usr/local/google/home/daricemahtab/web3-enterprise-agents')

# 1. Fix grid alignment in generate_portal_site.py
gps_file = REPO_ROOT / '_shared' / 'scripts' / 'generate_portal_site.py'
if gps_file.exists():
    c = gps_file.read_text(encoding='utf-8')
    c = c.replace(
        '.agent-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(420px, 1fr)); gap: 24px; }',
        '.agent-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(420px, 1fr)); gap: 24px; align-items: start; }'
    )
    # Also ensure modal video wrapper takes clean 16:9 full width
    c = c.replace(
        '.modal-video-wrapper { position: relative; width: 100%; background: #000; border-radius: 14px; overflow: hidden; border: 1px solid var(--border-color); box-shadow: 0 12px 30px rgba(0, 0, 0, 0.5); }',
        '.modal-video-wrapper { position: relative; width: 100%; background: #000; border-radius: 14px; overflow: hidden; border: 1px solid var(--border-color); box-shadow: 0 12px 30px rgba(0, 0, 0, 0.5); aspect-ratio: 16 / 9; }'
    )
    c = c.replace(
        '.modal-video { width: 100%; height: auto; display: block; max-height: 640px; }',
        '.modal-video { width: 100%; height: 100%; object-fit: cover; display: block; }'
    )
    gps_file.write_text(c, encoding='utf-8')
    print("generate_portal_site.py updated with align-items: start and aspect-ratio: 16/9")

# 2. Update record_simulated_demo.py with larger, High-DPI UI scaling (1.3x font sizes & dimensions)
rec_file = REPO_ROOT / '_shared' / 'scripts' / 'record_simulated_demo.py'
if rec_file.exists():
    rc = rec_file.read_text(encoding='utf-8')
    
    # Update sidebar width and font sizes
    rc = rc.replace('width: 260px;', 'width: 320px;')
    rc = rc.replace('font-size: 14px;', 'font-size: 17px;')
    rc = rc.replace('font-size: 14.5px;', 'font-size: 18px;')
    rc = rc.replace('font-size: 13.5px;', 'font-size: 16px;')
    rc = rc.replace('font-size: 15px;', 'font-size: 18px;')
    rc = rc.replace('font-size: 16px;', 'font-size: 20px;')
    rc = rc.replace('font-size: 32px;', 'font-size: 38px;')
    rc = rc.replace('width: 320px;\n    background: #ffffff;\n    border: 1px solid #e2e8f0;\n    border-radius: 16px;',
                    'width: 440px;\n    background: #ffffff;\n    border: 1px solid #e2e8f0;\n    border-radius: 18px;')
    rc = rc.replace('width: 620px;', 'width: 740px;')
    rc = rc.replace('max-width: 820px;\n    height: 52px;', 'max-width: 960px;\n    height: 62px;')
    
    rec_file.write_text(rc, encoding='utf-8')
    print("record_simulated_demo.py updated with High-DPI UI scaling")

