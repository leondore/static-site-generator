import unittest

from textnode import (
    TextNode,
    text_type_bold,
    text_type_italic,
    text_type_link,
)


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a bold node", text_type_bold)
        node2 = TextNode("This is a bold node", text_type_bold)
        self.assertEqual(node, node2)

    def test_eq_with_url(self):
        node = TextNode("This is a link node", text_type_link, "https://google.com/")
        node2 = TextNode("This is a link node", text_type_link, "https://google.com/")
        self.assertEqual(node, node2)

    def test_not_eq_type(self):
        node = TextNode("This is a text node", text_type_italic)
        node2 = TextNode("This is a text node", text_type_bold)
        self.assertNotEqual(node, node2)

    def test_not_eq_text(self):
        node = TextNode("This is a bold node", text_type_bold)
        node2 = TextNode("This is also a bold node", text_type_bold)
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a link node", text_type_link, "https://google.com/")
        self.assertEqual(
            repr(node), "TextNode(This is a link node, link, https://google.com/)"
        )


if __name__ == "__main__":
    unittest.main()
