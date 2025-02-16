# a = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89];
# b = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]


def find_identical_elements(val1, val2):
    return list(set([x for x in val1 if x in val2]))


if __name__ == "__main__":
    print(
        find_identical_elements(
            [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89],
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
        )
    )
