"""Check migrated routes, local assets and fragment links in a Jekyll build."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import json
import sys
import re

root = Path(sys.argv[1] if len(sys.argv) > 1 else '_site').resolve()
base = sys.argv[2].rstrip('/') if len(sys.argv) > 2 else ''

class Page(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.ids = set()
        self.links = []
        self.feed(html)
    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if 'id' in attrs:
            self.ids.add(attrs['id'])
        for key in ('href', 'src', 'poster'):
            if key in attrs:
                self.links.append(attrs[key])

pages = {p: Page(p.read_text()) for p in root.rglob('*.html')}
errors = []
content_root = Path(__file__).parent.parent / 'content'
for path in content_root.rglob('*.md'):
    if re.search(r'<[A-Za-z/]|{{|{%', path.read_text()):
        errors.append(f'HTML or Liquid in content: {path}')
if list(content_root.rglob('*.html')):
    errors.append('HTML files found in the content folder')
manifest = json.loads((Path(__file__).parent / 'migration.json').read_text())
for entry in manifest:
    if not (root / entry['route'].lstrip('/') / 'index.html').exists():
        errors.append('Missing route: ' + entry['route'])
for path, page in pages.items():
    for link in page.links:
        parts = urlsplit(link)
        if parts.scheme or parts.netloc:
            continue
        local = unquote(parts.path)
        if local.startswith('/'):
            if base and not (local == base or local.startswith(base + '/')):
                errors.append('Missing base path: ' + link)
                continue
            local = local[len(base):] if base else local
            dest = root / local.lstrip('/')
        else:
            dest = path.parent / local if local else path
        dest = dest.resolve()
        if dest.is_dir():
            dest /= 'index.html'
        if not dest.exists():
            errors.append(f'{path.relative_to(root)}: missing {link}')
        elif parts.fragment and dest in pages and unquote(parts.fragment) not in pages[dest].ids:
            errors.append(f'{path.relative_to(root)}: missing fragment {link}')
    if '{{' in path.read_text() or '{%' in path.read_text():
        errors.append(f'Unrendered Liquid: {path.relative_to(root)}')
if errors:
    raise SystemExit('\n'.join(sorted(set(errors))))
print(f'Validated {len(manifest)} migrated routes and links/assets/fragments in {len(pages)} pages (baseurl={base!r}).')
