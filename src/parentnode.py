from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Raw nodes can't be parent nodes.")

        if self.children is None:
            raise ValueError("Parent nodes require children.")

        opening = f"<{self.tag}{self.props_to_html()}>"
        closing = f"</{self.tag}>"
        children_html = "".join([child.to_html() for child in self.children])

        return opening + children_html + closing

    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"
