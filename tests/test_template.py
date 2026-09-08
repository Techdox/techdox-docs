"""Article metadata labels distinguish edits from technical verification."""
from pathlib import Path
import unittest
from jinja2 import Environment
ROOT = Path(__file__).resolve().parents[1]
class TemplateTests(unittest.TestCase):
    def test_source_dates_are_visibly_labelled_as_edits(self):
        path = ROOT / 'overrides/partials/source-file.html'
        self.assertTrue(path.exists(), 'Date template needs explicit labels')
        template = Environment(autoescape=True).from_string(path.read_text())
        result = template.render(page={'meta':{'git_revision_date_localized':'Yesterday','git_creation_date_localized':'Last year'}})
        self.assertIn('Edited', result)
        self.assertIn('Published', result)
        self.assertNotIn('verified', result.lower())
if __name__ == '__main__':
    unittest.main()
