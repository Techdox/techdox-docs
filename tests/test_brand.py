"""Brand identity regressions; browser.cjs covers rendered layout/accessibility."""
import hashlib
import json
from html.parser import HTMLParser
from pathlib import Path
import unittest
from jinja2 import Environment, FileSystemLoader

ROOT = Path(__file__).resolve().parents[1]

class Elements(HTMLParser):
    def __init__(self, markup):
        super().__init__()
        self.elements = []
        self.feed(markup)

    def handle_starttag(self, tag, attrs):
        self.elements.append((tag, dict(attrs)))

class BrandTests(unittest.TestCase):
    def test_supplied_assets_remain_byte_identical_to_kit(self):
        manifest = json.loads((ROOT / "tests/brand-assets.json").read_text())
        for name, expected in manifest.items():
            with self.subTest(asset=name):
                self.assertEqual(hashlib.sha256((ROOT / name).read_bytes()).hexdigest(), expected)

    def test_header_uses_outlined_theme_wordmarks_with_separate_destinations(self):
        env = Environment(loader=FileSystemLoader(ROOT / 'overrides'), autoescape=True)
        env.filters['url'] = lambda path: '/' + path
        markup = env.get_template('partials/header.html').render(config={'plugins': [], 'theme': {}})
        elements = Elements(markup).elements
        images = [a for tag, a in elements if tag == 'img']
        self.assertEqual({a['src'] for a in images}, {
            '/assets/brand/primary-dark.svg', '/assets/brand/primary-light.svg'})
        links = {a.get('aria-label'): a['href'] for tag, a in elements if tag == 'a'}
        self.assertEqual(links['Techdox main site'], 'https://techdox.nz')
        self.assertEqual(links['Docs home'], '/')
        for image in images:
            self.assertEqual(image['alt'], '')  # The link supplies the accessible name.
            svg = (ROOT / 'docs' / image['src'].lstrip('/')).read_text()
            self.assertIn('<path', svg)
            self.assertNotIn('<text', svg)
            self.assertNotIn('<animate', svg)
            self.assertIn('#f4f7fb' if 'dark.svg' in image['src'] else '#090c12', svg)
        self.assertNotIn('tx-cursor', markup)

    def test_browser_icons_and_generated_social_cards_use_kit_identity(self):
        config = (ROOT / 'mkdocs.yml').read_text()
        self.assertIn('logo: assets/brand/icon-512.png', config)
        self.assertIn('favicon: assets/brand/favicon.ico', config)
        self.assertIn('background_color: "#090c12"', config)
        self.assertIn('color: "#f4f7fb"', config)
        head = (ROOT / 'overrides/main.html').read_text()
        self.assertIn('rel="apple-touch-icon"', head)
        self.assertIn('assets/brand/icon-180.png', head)
        self.assertIn('assets/brand/icon-32.png', head)
        self.assertNotIn('blog-og.png', head, 'keep genuine per-guide social titles')

    def test_canonical_tokens_are_loaded_before_semantic_theme_adaptations(self):
        config = (ROOT / 'mkdocs.yml').read_text()
        self.assertIn('  - stylesheets/techdox.css\n  - stylesheets/extra.css', config)
        css = (ROOT / 'docs/stylesheets/extra.css').read_text()
        dark = css.split('[data-md-color-scheme="slate"]{', 1)[1].split('}', 1)[0]
        light = css.split('[data-md-color-scheme="default"]{', 1)[1].split('}', 1)[0]
        for semantic, token in {'bg':'bg', 'raised':'raised', 'panel':'panel', 'soft':'soft', 'text':'text', 'muted':'muted', 'link':'bright', 'cyan':'cyan', 'border':'line', 'blue':'blue'}.items():
            self.assertIn(f'--tx-{semantic}:var(--td-{token})', dark)
        self.assertIn('--tx-bg:#f8fafc', light)
        self.assertIn('--tx-link:#2259b5', light)
        self.assertIn('--tx-control:#7c8ca3', light)
        self.assertNotIn('#293345', css)
        self.assertIn('--td-line: #293445', (ROOT / 'docs/stylesheets/techdox.css').read_text())

    def test_social_cards_use_bundled_hanken_without_runtime_font_downloads(self):
        config = (ROOT / 'mkdocs.yml').read_text()
        self.assertIn('font_family: "Hanken Grotesk"', config)
        self.assertIn('cache_dir: assets/social-brand-kit-v2', config)
        for style in ['Regular', 'Bold']:
            self.assertTrue((ROOT / 'assets/social-brand-kit-v2/fonts/Hanken Grotesk' / (style + '.ttf')).is_file())
        self.assertTrue((ROOT / 'assets/social-brand-kit-v2/fonts/Hanken Grotesk/OFL.txt').is_file())

if __name__ == '__main__':
    unittest.main()
