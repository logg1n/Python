import re

TEXT = """"
        Lorem ipsum dolor sit amet,
        consectetur adipiscing elit, 
        sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
        Ut enim ad minim veniam, 
        quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. 
        Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. 
        Excepteur sint occaecat cupidatat non proident, 
        sunt in culpa qui officia deserunt mollit anim id est laborum.
        """


def split_text(text):
    delimiters = r"[,\s;.!?]+"

    result = re.split(delimiters, text)
    result = [word for word in result if word]

    return result


def is_prefix_a(str):
    return [w for w in str if w[0] == "a"]


if __name__ == "__main__":
    print(is_prefix_a(split_text(TEXT)))
