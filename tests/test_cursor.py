"""Web derivatives preserve supplied geometry; only the attached cursor blinks."""
import re
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
ASSETS='docs/assets/brand'
MASTER='primary'
class Cursor(unittest.TestCase):
    def test_reduced_motion_uses_static_picture_source(self):
        for name in ['overrides/partials/wordmark.html']:
            markup=(ROOT / name).read_text()
            self.assertIn('media="(prefers-reduced-motion: reduce)"',markup)
            self.assertEqual(markup.count('<picture'),markup.count('wordmark-web-'))

    def test_web_derivatives_only_add_cursor_style(self):
        for theme in ('dark','light'):
            original=(ROOT / ASSETS / f'{MASTER}-{theme}.svg').read_text()
            web=(ROOT / ASSETS / f'wordmark-web-{theme}.svg').read_text() if (ROOT / ASSETS / f'wordmark-web-{theme}.svg').exists() else ''
            self.assertIn('#techdox-cursor { animation: techdox-cursor 1.2s step-end infinite; }',web)
            self.assertIn('@media (prefers-reduced-motion: reduce)',web)
            self.assertIn('#techdox-cursor { animation: none; opacity: 1; }',web)
            self.assertEqual(re.sub(r'<style>.*?</style>','',web,flags=re.S).replace(' id="techdox-cursor"', ''), original)
            self.assertEqual(web.count('id="techdox-cursor"'),1)
            self.assertEqual(web.count('<rect '),1)
if __name__=='__main__': unittest.main()
