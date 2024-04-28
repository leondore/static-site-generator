import unittest

from parentnode import ParentNode
from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_to_html_nested(self):
        p1_node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        p2_node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(
                    "a", "Link", {"href": "http://google.com/", "target": "_blank"}
                ),
                LeafNode("i", "italic text"),
            ],
        )
        parent_node = ParentNode(
            "div", [p1_node, p2_node], {"class": "pt-1 bg-zinc-200"}
        )
        self.assertEqual(
            parent_node.to_html(),
            '<div class="pt-1 bg-zinc-200"><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p><p><b>Bold text</b><a href="http://google.com/" target="_blank">Link</a><i>italic text</i></p></div>',
        )


if __name__ == "__main__":
    unittest.main()
