import re

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
)


def text_to_textnodes(text):
    nodes = [TextNode(text, text_type_text)]
    nodes = split_nodes_delimiter(nodes, "**", text_type_bold)
    nodes = split_nodes_delimiter(nodes, "*", text_type_italic)
    nodes = split_nodes_delimiter(nodes, "`", text_type_code)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


def split_nodes_delimiter(nodes, delimiter, text_type):
    new_nodes = []

    for node in nodes:
        if node.text_type is not text_type_text:
            new_nodes.append(node)
            continue

        text_nodes = []
        text_parts = node.text.split(delimiter)

        if len(text_parts) % 2 == 0:
            raise ValueError("Invalid markdown")

        for i in range(len(text_parts)):
            if text_parts[i] == "":
                continue
            if i % 2 == 0:
                text_nodes.append(TextNode(text_parts[i], text_type_text))
            else:
                text_nodes.append(TextNode(text_parts[i], text_type))

        new_nodes.extend(text_nodes)

    return new_nodes


def split_nodes_image(nodes):
    new_nodes = []

    for node in nodes:
        if node.text_type is not text_type_text:
            new_nodes.append(node)
            continue

        images = extract_markdown_images(node.text)
        if len(images) == 0:
            new_nodes.append(node)
            continue

        remaining_text = node.text
        for image in images:
            text_parts = remaining_text.split(f"![{image[0]}]({image[1]})", 1)

            if len(text_parts) != 2:
                raise ValueError("Invalid markdown")

            if text_parts[0] != "":
                new_nodes.append(TextNode(text_parts[0], text_type_text))

            new_nodes.append(TextNode(image[0], text_type_image, image[1]))
            remaining_text = text_parts[1]

        if len(remaining_text) != 0:
            new_nodes.append(TextNode(remaining_text, text_type_text))

    return new_nodes


def split_nodes_link(nodes):
    new_nodes = []

    for node in nodes:
        if node.text_type is not text_type_text:
            new_nodes.append(node)
            continue

        links = extract_markdown_links(node.text)
        if len(links) == 0:
            new_nodes.append(node)
            continue

        remaining_text = node.text
        for link in links:
            text_parts = remaining_text.split(f"[{link[0]}]({link[1]})", 1)

            if len(text_parts) != 2:
                raise ValueError("Invalid markdown")

            if text_parts[0] != "":
                new_nodes.append(TextNode(text_parts[0], text_type_text))

            new_nodes.append(TextNode(link[0], text_type_link, link[1]))
            remaining_text = text_parts[1]

        if len(remaining_text) != 0:
            new_nodes.append(TextNode(remaining_text, text_type_text))

    return new_nodes


def extract_markdown_images(text):
    regex = r"!\[(.*?)\]\((.*?)\)"
    matches = re.findall(regex, text)
    return matches


def extract_markdown_links(text):
    regex = r"\[(.*?)\]\((.*?)\)"
    matches = re.findall(regex, text)
    return matches
