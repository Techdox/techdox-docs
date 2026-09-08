"""Verify built icons and genuine per-page OG cards, including warm-cache builds."""
from hashlib import sha256
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
from PIL import Image, ImageChops, ImageFont
from material.plugins.social.plugin import SocialPlugin

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'site'

class Head(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.meta = {}
        self.links = []
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'meta':
            self.meta[attrs.get('property', attrs.get('name'))] = attrs.get('content')
        elif tag == 'link':
            self.links.append(attrs)

cards = []
logo = Image.open(ROOT / 'docs/assets/brand/icon-512.png').convert('RGBA').resize((144, 144))
for route in ['', 'npm/', 'homelab-rebuild/dns-stack/']:
    head = Head((SITE / route / 'index.html').read_text())
    assert any(link.get('rel') == 'apple-touch-icon' and link['href'].endswith('assets/brand/icon-180.png') for link in head.links)
    assert any(link.get('rel') == 'icon' and link['href'].endswith('assets/brand/favicon.ico') for link in head.links)
    assert any(link.get('rel') == 'icon' and link['href'].endswith('assets/brand/icon-32.png') for link in head.links)
    image_path = SITE / urlparse(head.meta['og:image']).path.lstrip('/')
    card = Image.open(image_path).convert('RGBA')
    assert card.size == (1200, 630)
    assert card.getpixel((0, 0)) == (9, 12, 18, 255), 'stale/non-kit social background'
    expected = Image.new('RGBA', (144, 144), '#090c12')
    expected.alpha_composite(logo)
    assert ImageChops.difference(card.crop((972, 60, 1116, 204)), expected).convert('RGB').getbbox() is None, 'OG must contain supplied kit icon, not old TECH/DOX mark'
    assert head.meta['og:title'] and head.meta['og:description']
    # Use the pinned renderer with an explicitly local kit-derived Hanken font.
    # Comparing pixels catches both Roboto fallback and stale warm-cache cards.
    title = head.meta['og:title'].removesuffix(' - Techdox Docs')
    font_path = ROOT / 'assets/social-brand-kit-v2/fonts/Hanken Grotesk/Bold.ttf'
    assert sha256(font_path.read_bytes()).hexdigest() == 'e2e24b5626761a850ad71cb0e8836deaa62fd8c73e2e86bfe97a5b6e284fa7e8'
    font = ImageFont.truetype(str(font_path), 92)
    assert font.getname()[0] == 'Hanken Grotesk'
    renderer = SocialPlugin()
    renderer.color = {'text': '#f4f7fb'}
    title_image = Image.new('RGBA', (826, 328), '#090c12')
    title_image.alpha_composite(renderer._render_text((826, 328), font, title, 3, 30))
    assert ImageChops.difference(card.crop((64, 160, 890, 488)), title_image).convert('RGB').getbbox() is None, 'OG title must actually render in bundled Hanken 800'
    regular_path = font_path.with_name("Regular.ttf")
    assert sha256(regular_path.read_bytes()).hexdigest() == "0a4cb26adfce0ba2d7a9fb9f1458f03bddef3e4dc915e7c5b7982a9c879cb095"
    description = Image.new("RGBA", (826, 80), "#090c12")
    description.alpha_composite(renderer._render_text((826, 80), ImageFont.truetype(str(regular_path), 28), head.meta["og:description"], 2, 14))
    assert ImageChops.difference(card.crop((68, 512, 894, 592)), description).convert("RGB").getbbox() is None, "OG description must render in bundled Hanken 400"
    renderer._executor.shutdown()
    cards.append((head.meta['og:title'], sha256(card.crop((64, 160, 890, 488)).tobytes()).hexdigest()))
assert len({title for title, _ in cards}) == 3, 'keep actual per-page titles'
assert len({pixels for _, pixels in cards}) == 3, 'titles must differ in actual artwork, not just metadata'
print('Built brand: icons and supplied OG mark verified on 3 distinct page cards:', cards)
