from textnode import TextNode, TextType

def main():
    node1 = TextNode("This is a link", TextType["LINK"], "https://google.com")
    print(node1)


if __name__ == "__main__":
    main()
