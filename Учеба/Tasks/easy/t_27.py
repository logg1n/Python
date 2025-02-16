import re


def split_str(str):
    text = "Это предложение! А это вопрос? Или просто точка. Бла бла бла"
    pattern = r"[!?.]+"
    return re.split(pattern, text)


if __name__ == "__main__":
    text = ""
    print(split_str(text))
