import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        node = LeafNode(
            "a",
            "This is a link",
            {"href": "http://google.com/", "target": "_blank"},
        )
        self.assertEqual(
            node.to_html(),
            '<a href="http://google.com/" target="_blank">This is a link</a>',
        )

    def test_to_html_raw(self):
        node = LeafNode(
            None,
            "This is raw text",
        )
        self.assertEqual(node.to_html(), "This is raw text")


if __name__ == "__main__":
    unittest.main()
