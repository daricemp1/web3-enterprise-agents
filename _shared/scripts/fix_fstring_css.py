from pathlib import Path

p = Path('/usr/local/google/home/daricemahtab/web3-enterprise-agents/_shared/scripts/generate_portal_site.py')
c = p.read_text(encoding='utf-8')

# Fix unescaped single braces in arch CSS block
import re

def escape_css_braces(match):
    block = match.group(0)
    # Replace single { with {{ and single } with }} where not already doubled
    block = re.sub(r'(?<!\{)\{(?!\{)', '{{', block)
    block = re.sub(r'(?<!\})\}(?!\})', '}}', block)
    return block

c = re.sub(r'/\* Architecture Blueprint Modal matching Retail Parity \*/[\s\S]*?(?=/\* Footer \*/)', escape_css_braces, c)
p.write_text(c, encoding='utf-8')
print("Escaped CSS braces in generate_portal_site.py")
