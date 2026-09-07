"""Check built local routes/assets/anchors and preserve the pre-overhaul URL baseline."""
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit, unquote
import sys
ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'site'
class Document(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.ids = set()
        self.links = []
        self.feed(html)
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get('id'):
            self.ids.add(a['id'])
        value = a.get('href') if tag == 'a' else a.get('src') if tag in ('script', 'img') else a.get('href') if tag == 'link' and a.get('rel') in ('stylesheet', 'preload', 'icon') else None
        if value:
            self.links.append(value)
def file_for(url):
    path = unquote(urlsplit(url).path).lstrip('/')
    return SITE / (path + 'index.html' if not path or path.endswith('/') else path)
def main():
    if not (SITE / 'index.html').exists():
        raise SystemExit('Build the site first: mkdocs build --strict')
    documents = {p:Document(p.read_text(encoding='utf-8')) for p in SITE.rglob('*.html')}
    problems = []
    for p, doc in documents.items():
        rel = p.relative_to(SITE).as_posix()
        base = 'https://docs.techdox.nz/' + (rel[:-10] if rel.endswith('index.html') else rel)
        for href in doc.links:
            url = urlsplit(urljoin(base, href))
            if url.scheme not in ('http', 'https') or url.netloc != 'docs.techdox.nz':
                continue
            target = file_for(url.geturl())
            if not target.exists():
                problems.append('{} -> missing {}'.format(rel, href))
            elif url.fragment and target in documents and unquote(url.fragment) not in documents[target].ids:
                problems.append('{} -> missing anchor {}'.format(rel, href))
    legacy = json.loads((ROOT / 'tests/legacy-routes.json').read_text())
    for route, anchors in legacy.items():
        target = file_for(route)
        if target not in documents:
            problems.append('Legacy route missing: ' + route)
            continue
        for anchor in anchors:
            if anchor not in documents[target].ids:
                problems.append('Legacy anchor missing: ' + route + '#' + anchor)
    result = {'html_pages':len(documents),'legacy_routes':len(legacy),'problems':sorted(set(problems))}
    print(json.dumps(result, indent=2))
    return 1 if problems else 0
if __name__ == '__main__':
    sys.exit(main())
