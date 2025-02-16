# 'abcdeabc'


def rem_duplicates(str):
    result = []
    s = set()

    for ch in str:
        if ch not in s:
            result.append(ch)
            s.add(ch)

    return "".join(result)


if __name__ == "__main__":
    print(rem_duplicates(str="abcdeabc"))
