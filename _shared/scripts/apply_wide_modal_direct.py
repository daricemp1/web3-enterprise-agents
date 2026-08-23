#!/usr/bin/env python3
import re
from pathlib import Path

REPO_ROOT = Path('/usr/local/google/home/daricemahtab/web3-enterprise-agents')
gps_file = REPO_ROOT / '_shared' / 'scripts' / 'generate_portal_site.py'

content = gps_file.read_text(encoding='utf-8')

# 1. Replace the modal CSS block cleanly
css_pattern = r'/\* Video Modal \*/[\s\S]*?(?=/\* Footer \*/)'
new_modal_css = """/* Video Modal matching Retail layout exactly */
    .modal-backdrop {{ position: fixed; inset: 0; background: var(--modal-overlay); z-index: 100; display: none; align-items: center; justify-content: center; padding: 24px; backdrop-filter: blur(8px); }}
    .modal-dialog {{ background: var(--bg-card); border: 1px solid var(--border-faint); border-radius: 18px; width: 100%; max-width: 1200px; max-height: 94vh; display: flex; flex-direction: column; box-shadow: var(--shadow-modal); overflow: hidden; }}
    .modal-header {{ display: flex; justify-content: space-between; align-items: flex-start; padding: 24px 28px 18px; border-bottom: 1px solid var(--border-color); }}
    .modal-header-left {{ display: flex; flex-direction: column; gap: 8px; }}
    .modal-badges-row {{ display: flex; gap: 8px; align-items: center; }}
    .modal-title {{ font-family: 'Google Sans', sans-serif; font-size: 1.55rem; font-weight: 700; color: var(--text-primary); line-height: 1.25; }}
    .modal-close {{ width: 36px; height: 36px; border-radius: 8px; background: rgba(255, 255, 255, 0.06); border: 1px solid var(--border-color); color: var(--text-secondary); display: flex; align-items: center; justify-content: center; font-size: 1.15rem; cursor: pointer; transition: all 0.15s ease; }}
    .modal-close:hover {{ background: var(--bg-surface); color: var(--text-primary); border-color: var(--border-focus); }}
    .modal-body {{ padding: 24px 28px; overflow-y: auto; display: flex; flex-direction: column; gap: 20px; }}
    .modal-video-wrapper {{ position: relative; width: 100%; background: #000; border-radius: 14px; overflow: hidden; border: 1px solid var(--border-color); box-shadow: 0 12px 30px rgba(0, 0, 0, 0.5); aspect-ratio: 16 / 9; }}
    .modal-video {{ width: 100%; height: 100%; object-fit: contain; background: #000; display: block; }}
    .modal-meta-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; background: var(--bg-surface); border: 1px solid var(--border-color); border-radius: 10px; padding: 18px 22px; }}
    .modal-meta-item {{ display: flex; flex-direction: column; gap: 4px; }}
    .modal-meta-label {{ font-size: 0.72rem; font-weight: 700; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.05em; }}
    .modal-meta-value {{ font-size: 0.95rem; font-weight: 600; color: var(--text-primary); }}
    .modal-sequence-box {{ background: var(--bg-surface); border: 1px solid var(--border-color); border-radius: 10px; padding: 22px 24px; }}
    .modal-sequence-title {{ font-size: 0.95rem; font-weight: 700; color: var(--accent-indigo); margin-bottom: 12px; }}
    .modal-turns-list {{ list-style: none; display: flex; flex-direction: column; gap: 10px; font-size: 0.9rem; color: var(--text-secondary); line-height: 1.55; }}
    .modal-turns-list strong {{ color: var(--text-primary); }}
    .modal-footer {{ padding: 18px 28px; border-top: 1px solid var(--border-color); display: flex; justify-content: flex-end; gap: 12px; background: var(--bg-card); }}
    .btn-download {{ display: inline-flex; align-items: center; gap: 6px; padding: 10px 18px; border-radius: 8px; font-size: 0.9rem; font-weight: 600; color: var(--text-primary); text-decoration: none; border: 1px solid var(--border-color); background: var(--bg-surface); transition: all 0.15s ease; }}
    .btn-download:hover {{ border-color: var(--border-focus); color: var(--accent-blue); }}
    .btn-open-showcase {{ display: inline-flex; align-items: center; gap: 6px; padding: 10px 22px; border-radius: 8px; font-size: 0.9rem; font-weight: 700; color: #0f172a; background: var(--accent-blue); text-decoration: none; transition: all 0.15s ease; }}
    .btn-open-showcase:hover {{ background: var(--accent-blue-hover); color: #ffffff; }}
    
    """

content = re.sub(css_pattern, new_modal_css, content)

# 2. Replace the modal HTML block cleanly
html_pattern = r'<!-- Video Modal -->[\s\S]*?(?=<!-- Site Footer -->)'
new_modal_html = """<!-- Video Modal matching Retail Layout Exactly -->
  <div class="modal-backdrop" id="videoModal">
    <div class="modal-dialog">
      <div class="modal-header">
        <div class="modal-header-left">
          <div class="modal-badges-row">
            <span id="modalDomainBadge" class="badge-domain"></span>
            <span id="modalRegionBadge" class="badge-region"></span>
          </div>
          <h2 id="modalAgentTitle" class="modal-title">Agent Demo</h2>
        </div>
        <button class="modal-close" id="modalCloseBtn">✕</button>
      </div>
      <div class="modal-body">
        
        <!-- Video Player -->
        <div class="modal-video-wrapper">
          <video id="modalVideo" class="modal-video" controls autoplay muted playsinline preload="auto">
            <source src="" type="video/mp4">
            Your browser does not support HTML5 video.
          </video>
        </div>

        <!-- Meta Grid -->
        <div class="modal-meta-grid">
          <div class="modal-meta-item">
            <span class="modal-meta-label">Resolution</span>
            <span class="modal-meta-value">1080p Full HD (1920×1080)</span>
          </div>
          <div class="modal-meta-item">
            <span class="modal-meta-label">Model Reasoning</span>
            <span class="modal-meta-value">Gemini 3.5 Flash (Global)</span>
          </div>
          <div class="modal-meta-item">
            <span class="modal-meta-label">Platform UI</span>
            <span class="modal-meta-value">Web3 Agent Platform</span>
          </div>
          <div class="modal-meta-item">
            <span class="modal-meta-label">Data Execution</span>
            <span class="modal-meta-value">BigQuery Conversational Analytics</span>
          </div>
        </div>

        <!-- Demonstration Workflow Sequence -->
        <div class="modal-sequence-box">
          <div class="modal-sequence-title">🎬 Demonstration Workflow Sequence</div>
          <ul class="modal-turns-list" id="modalTurnsList">
            <!-- Injected via JavaScript -->
          </ul>
        </div>

      </div>
      <div class="modal-footer">
        <a id="modalDownloadBtn" href="#" download class="btn-download">⬇ Download MP4</a>
        <a id="modalShowcaseBtn" href="#" target="_blank" class="btn-open-showcase">🚀 Open Full Showcase Player</a>
      </div>
    </div>
  </div>

  """

content = re.sub(html_pattern, new_modal_html, content)

# 3. Ensure openVideoModal sets the clean title
content = content.replace(
    'modalAgentTitle.textContent = `${agent.icon} ${agent.display_name}`;',
    'modalAgentTitle.textContent = agent.display_name;'
)

gps_file.write_text(content, encoding='utf-8')
print("Successfully applied wide modal CSS and HTML to generate_portal_site.py")
