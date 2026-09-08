"""Catalogue contract tests; run with python -m unittest discover -s tests."""
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED = {'index.md', 'about.md', 'tags.md', 'support.md', 'racknerd.md',
            'docker-containers.md', 'networking-overview.md', 'logging-overview.md',
            'general-guides.md', 'homelab-rebuild/index.md'}


class CatalogueTests(unittest.TestCase):
    def hook(self):
        path = ROOT / 'hooks/catalogue.py'
        self.assertTrue(path.exists(), 'Missing catalogue validation hook')
        spec = importlib.util.spec_from_file_location('catalogue', path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_mkdocs_hooks_publish_browse_and_article_contract(self):
        from types import SimpleNamespace
        from tempfile import TemporaryDirectory
        from html.parser import HTMLParser
        hook = self.hook()
        self.assertTrue(hasattr(hook, 'on_config'), 'Missing MkDocs catalogue integration')
        with TemporaryDirectory() as site_dir:
            config = {'docs_dir': str(ROOT / 'docs'), 'site_dir': site_dir, 'extra': {},
                      'nav': [{'Home': 'index.md'}, {'All Guides': []}]}
            hook.on_config(config)
            self.assertEqual(config['extra']['tx_guide_count'], len(hook.RECORDS))
            self.assertEqual(sum(t['count'] for t in config['extra']['tx_topics']), len(hook.RECORDS))
            self.assertTrue(all(t['url'] == 'topics/' + t['slug'] + '/' for t in hook.TOPICS))
            page = SimpleNamespace(file=SimpleNamespace(src_uri='guides/index.md'), url='guides/', meta={})
            rendered = hook.on_page_markdown('<!-- tx:catalogue -->', page, config, None)
            class Links(HTMLParser):
                def __init__(self):
                    super().__init__()
                    self.cards, self.ids = [], set()
                def handle_starttag(self, tag, attrs):
                    attrs = dict(attrs)
                    if 'id' in attrs: self.ids.add(attrs['id'])
                    if tag == 'a' and 'tx-guide-card' in attrs.get('class', '').split():
                        self.cards.append(attrs)
            parser = Links()
            parser.feed(rendered)
            self.assertIn('placeholder="Search guides" disabled', rendered, 'No-JS filters must not look functional')
            self.assertEqual(len(parser.cards), len(hook.RECORDS))
            self.assertTrue({'guide-query', 'guide-topic', 'guide-type', 'guide-reset', 'guide-count', 'guide-empty'} <= parser.ids)
            npm = next(c for c in parser.cards if c['href'] == '../npm/')
            self.assertEqual(npm['data-topic'], 'networking')
            self.assertIn('npm', npm['data-search'].lower())
            page.file.src_uri, page.url = 'topics/networking.md', 'topics/networking/'
            topic_html = hook.on_page_markdown('<!-- tx:catalogue topic=networking -->', page, config, None)
            parser = Links(); parser.feed(topic_html)
            self.assertTrue(parser.cards)
            self.assertTrue(all(c['data-topic'] == 'networking' for c in parser.cards))
            self.assertIn('../../npm/', topic_html)
            page.file.src_uri, page.url = 'npm.md', 'npm/'
            original = '# Original title\n\n## Preserve this anchor\n\n```yaml\nexact: true\n```'
            self.assertEqual(hook.on_page_markdown(original, page, config, None), original)
            hook.on_page_context({}, page, config, None)
            self.assertEqual(page.meta['tx_guide']['title'], 'Nginx Proxy Manager')
            self.assertNotIn('verified', page.meta['tx_guide'])
            self.assertLessEqual(len(page.meta['tx_related']), 3)
            self.assertNotIn('npm/', [g['url'] for g in page.meta['tx_related']])
            self.assertTrue(all(g['topic'] == 'networking' for g in page.meta['tx_related']))
            hook.on_post_build(config)
            exported = json.loads((Path(site_dir) / 'assets/guides.json').read_text())
            self.assertEqual(len(exported), len(hook.RECORDS))
            self.assertEqual(set(exported[0]), {'title', 'description', 'url', 'topic', 'topic_label', 'tags', 'aliases', 'type'})
            self.assertTrue(all(not g['url'].startswith('/') for g in exported))

    def test_series_sidebar_is_generated_from_metadata(self):
        hook = self.hook()
        config = {'docs_dir': str(ROOT / 'docs'), 'extra': {}, 'nav': [{'Homelab Rebuild': []}]}
        hook.on_config(config)
        entries = config['nav'][0]['Homelab Rebuild']
        self.assertTrue(entries, 'Series sidebar must come from catalogue metadata')
        self.assertEqual(entries[0], {'Overview': 'homelab-rebuild/index.md'})
        self.assertEqual(list(entries[1].values()), ['homelab-rebuild/opnsense-zimaboard.md'])
        self.assertEqual(list(entries[-1].values()), ['homelab-rebuild/architecture.md'])
        self.assertEqual(len(entries) - 1, sum('series' in g for g in hook.RECORDS))

    def test_series_navigation_stays_in_ordered_series(self):
        from types import SimpleNamespace
        hook = self.hook()
        hook.on_config({'docs_dir': str(ROOT / 'docs'), 'extra': {}, 'nav': []})
        page = SimpleNamespace(file=SimpleNamespace(src_uri='homelab-rebuild/dns-stack.md'), meta={})
        hook.on_page_context({}, page, {}, None)
        self.assertIn('tx_series', page.meta, 'Missing ordered series navigation')
        series = page.meta['tx_series']
        self.assertEqual(series['previous']['url'], 'homelab-rebuild/opnsense-zimaboard/')
        self.assertEqual(series['next']['url'], 'homelab-rebuild/wireguard-vpn/')
        page.file.src_uri = 'homelab-rebuild/opnsense-zimaboard.md'
        hook.on_page_context({}, page, {}, None)
        self.assertIsNone(page.meta['tx_series']['previous'])

    def test_validated_records_reject_invalid_metadata(self):
        hook = self.hook()
        data = json.loads((ROOT / 'data/guides.json').read_text())
        records = hook.validate(data, ROOT / 'docs')
        self.assertEqual(len(records), len(data['guides']))
        for record in records:
            self.assertEqual(record['url'], record['path'][:-3] + '/')
            self.assertTrue(record['topic_label'])
            self.assertNotIn('verified', record)
        import copy
        for field, value in [('topic', 'unknown'), ('path', '../secret.md'),
                             ('title', ''), ('type', 'unknown'), ('aliases', 'NPM'),
                             ('verified', '2026-01-01')]:
            invalid = copy.deepcopy(data)
            invalid['guides'][0][field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                hook.validate(invalid, ROOT / 'docs')
        duplicate = copy.deepcopy(data)
        duplicate['guides'].append(duplicate['guides'][0])
        with self.assertRaises(ValueError):
            hook.validate(duplicate, ROOT / 'docs')
        missing = copy.deepcopy(data)
        missing['guides'].pop()
        with self.assertRaises(ValueError):
            hook.validate(missing, ROOT / 'docs')

    def test_every_real_guide_has_exactly_one_metadata_record(self):
        path = ROOT / 'data/guides.json'
        self.assertTrue(path.exists(), 'Missing authoritative guide catalogue')
        data = json.loads(path.read_text())
        expected = {p.relative_to(ROOT / 'docs').as_posix()
                    for p in (ROOT / 'docs').rglob('*.md')
                    if p.relative_to(ROOT / 'docs').as_posix() not in EXCLUDED
                    and p.relative_to(ROOT / 'docs').parts[0] not in ('guides', 'topics')}
        paths = [g['path'] for g in data['guides']]
        self.assertEqual(set(paths), expected)
        self.assertEqual(len(paths), len(set(paths)))


if __name__ == '__main__':
    unittest.main()
