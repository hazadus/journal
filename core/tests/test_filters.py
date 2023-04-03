from django.test import TestCase

from core.templatetags.core_filters import get_dict_item_by_key, markdown


class CoreFiltersTest(TestCase):
    """
    Test all filters defined in `core_filters.py`.
    """

    def test_get_dict_item_by_key(self):
        """
        Ensure `get_dict_item_by_key` filter works as expected.
        """
        dictionary = {
            "test_key": "test_value",
        }
        self.assertEqual(get_dict_item_by_key(dictionary, key="test_key"), "test_value")

    def test_markdown(self):
        """
        Ensure that basic Markdown to HTML conversion works properly
        """
        self.assertEqual(markdown("**bold**"), "<p><strong>bold</strong></p>")
        self.assertEqual(markdown("_italic_"), "<p><em>italic</em></p>")
        self.assertEqual(markdown("# header1"), "<h1>header1</h1>")
        self.assertEqual(markdown("## header2"), "<h2>header2</h2>")
        self.assertEqual(markdown("### header3"), "<h3>header3</h3>")
        self.assertEqual(markdown("#### header4"), "<h4>header4</h4>")
        self.assertEqual(markdown("##### header5"), "<h5>header5</h5>")
        self.assertEqual(markdown("###### header6"), "<h6>header6</h6>")
