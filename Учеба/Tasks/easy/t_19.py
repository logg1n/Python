# st1 = {1, 2, 3, 4, 5}
# st2 = {4, 5, 6, 7, 8}


def get_common_elements(s1: set, s2: set):
    return s1.intersection(s2)


if __name__ == "__main__":
    print(get_common_elements({1, 2, 3, 4, 5}, {4, 5, 6, 7, 8}))
