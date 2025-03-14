from unittest import TestCase
from markdown_manipulation import extract_markdown_title


class TestMarkdownManipulation(TestCase):
    def test_extract_title(self):
        md = """
this is text
# This is a markdown title 

This is more text

## This is not a markdown title

This is even more text

# This is another title
"""
        title: str = extract_markdown_title(md)
        self.assertEqual(title, "This is a markdown title")

    def test_extract_title_no_title(self):
        md = """
this is text

This is more text

## This is not a markdown title

This is even more text
"""
        self.assertRaises(ValueError, extract_markdown_title, md)
