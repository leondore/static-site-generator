import unittest
from inline import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
)


class TestInline(unittest.TestCase):
    def test_split_bold(self):
        node = TextNode("This is **bolded** text", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)

        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is ", text_type_text),
                TextNode("bolded", text_type_bold),
                TextNode(" text", text_type_text),
            ],
        )

    def test_split_multiword_tag(self):
        node = TextNode("This is **BOLDED AND UPPERCASE** text", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)

        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is ", text_type_text),
                TextNode("BOLDED AND UPPERCASE", text_type_bold),
                TextNode(" text", text_type_text),
            ],
        )

    def test_split_multiple_tags(self):
        node = TextNode(
            "This is **bolded** text, and some more **bolded** text", text_type_text
        )
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)

        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is ", text_type_text),
                TextNode("bolded", text_type_bold),
                TextNode(" text, and some more ", text_type_text),
                TextNode("bolded", text_type_bold),
                TextNode(" text", text_type_text),
            ],
        )

    def test_split_italic(self):
        node = TextNode("This is *italic* text", text_type_text)
        new_nodes = split_nodes_delimiter([node], "*", text_type_italic)

        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is ", text_type_text),
                TextNode("italic", text_type_italic),
                TextNode(" text", text_type_text),
            ],
        )

    def test_split_code(self):
        node = TextNode("This is `code` text", text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", text_type_code)

        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is ", text_type_text),
                TextNode("code", text_type_code),
                TextNode(" text", text_type_text),
            ],
        )

    def test_extract_images(self):
        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"

        image_elements = extract_markdown_images(text)

        self.assertListEqual(
            image_elements,
            [
                (
                    "image",
                    "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
                ),
                (
                    "another",
                    "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png",
                ),
            ],
        )

    def test_extract_links(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"

        link_elements = extract_markdown_links(text)

        self.assertListEqual(
            link_elements,
            [
                ("link", "https://www.example.com"),
                ("another", "https://www.example.com/another"),
            ],
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png) and that is it",
            text_type_text,
        )
        new_nodes = split_nodes_image([node])

        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with an ", text_type_text),
                TextNode(
                    "image",
                    text_type_image,
                    "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
                ),
                TextNode(" and ", text_type_text),
                TextNode(
                    "another",
                    text_type_image,
                    "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png",
                ),
                TextNode(" and that is it", text_type_text),
            ],
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://google.com/) and [another](https://boot.dev/) and that is it",
            text_type_text,
        )
        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with a ", text_type_text),
                TextNode(
                    "link",
                    text_type_link,
                    "https://google.com/",
                ),
                TextNode(" and ", text_type_text),
                TextNode(
                    "another",
                    text_type_link,
                    "https://boot.dev/",
                ),
                TextNode(" and that is it", text_type_text),
            ],
        )

    def test_text_to_textnodes(self):
        nodes = text_to_textnodes(
            "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
        )
        self.assertListEqual(
            [
                TextNode("This is ", text_type_text),
                TextNode("text", text_type_bold),
                TextNode(" with an ", text_type_text),
                TextNode("italic", text_type_italic),
                TextNode(" word and a ", text_type_text),
                TextNode("code block", text_type_code),
                TextNode(" and an ", text_type_text),
                TextNode(
                    "image",
                    text_type_image,
                    "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
                ),
                TextNode(" and a ", text_type_text),
                TextNode("link", text_type_link, "https://boot.dev"),
            ],
            nodes,
        )
