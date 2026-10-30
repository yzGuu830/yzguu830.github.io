"""Validate the built homepage, its local resources, and sitemap without dependencies."""
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
from xml.etree import ElementTree


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []
        self.text = []

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))

    def handle_data(self, data):
        self.text.append(data)


root = Path(sys.argv[1] if len(sys.argv) > 1 else '_site')
page = Page()
page.feed((root / 'index.html').read_text())
assert 'Projects' not in ''.join(page.text), 'Projects is still rendered'
expected_count = len(list((Path(__file__).resolve().parents[1] / '_research').glob('*.markdown')))
assert sum(a.get('class') == 'research-row' for _, a in page.tags) == expected_count
assert any(t == 'link' and a.get('rel') == 'canonical' and
           a.get('href') == 'https://yzguu830.github.io/' for t, a in page.tags)
images = []
for tag, attrs in page.tags:
    if tag == 'img':
        assert attrs.get('width') and attrs.get('height'), 'Missing image dimensions'
        images.append(root / urlsplit(attrs['src']).path.lstrip('/'))
    value = attrs.get('src') if tag == 'img' else attrs.get('href')
    if not value:
        continue
    url = urlsplit(value)
    if url.scheme or url.netloc or not url.path:
        continue
    target = root / unquote(url.path).lstrip('/')
    assert target.exists(), f'Missing resource: {value}'
assert sum(p.stat().st_size for p in images) < 500_000, 'Homepage images exceed 500 KB'
ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
locations = [e.text for e in ElementTree.parse(root / 'sitemap.xml').findall('.//s:loc', ns)]
assert locations == ['https://yzguu830.github.io/'], locations
assert not (root / 'CNAME').exists()
assert not (root / '_archive').exists()
assert not (root / 'images/vgpt.gif').exists()
print(f'PASS: {expected_count} research entries, valid resources, canonical and sitemap; images {sum(p.stat().st_size for p in images):,} bytes')
