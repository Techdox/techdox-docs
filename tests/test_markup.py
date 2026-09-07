"""Regression checks for public documentation markup."""
from html.parser import HTMLParser
from pathlib import Path
import unittest
ROOT = Path(__file__).resolve().parents[1]
class SupportImages(HTMLParser):
    def __init__(self):
        super().__init__()
        self.unnamed = []
    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == 'img' and 'buymeacoffee.com' in (values.get('src') or '') and not (values.get('alt') or '').strip():
            self.unnamed.append(values['src'])
class MarkupTests(unittest.TestCase):
    def test_support_image_links_have_descriptive_names(self):
        missing = []
        for file in (ROOT / 'docs').rglob('*.md'):
            parser = SupportImages()
            parser.feed(file.read_text(encoding='utf-8'))
            if parser.unnamed:
                missing.append(str(file.relative_to(ROOT)))
        self.assertEqual(missing, [], 'Support image links need descriptive alternative text')
if __name__ == '__main__':
    unittest.main()
