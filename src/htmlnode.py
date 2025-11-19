class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props == None:
            return ""
        props_string = ""
        for key, value in self.props.items():
            props_string = props_string + f' {key}="{value}"'
        return props_string
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self):
        if self.value == None:
            raise ValueError("invalid HTML: no value")
        if self.tag == None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
         return f"LeafNode({self.tag}, {self.value}, {self.props})"


if __name__ == "__main__":
    node = LeafNode("p", "Hello, world!")
    print(node.to_html())
    node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
    print(node2.to_html())
