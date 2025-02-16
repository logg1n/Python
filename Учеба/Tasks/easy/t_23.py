NUMS = [
    [
        [11, 12, 13],
        [14, 15, 16],
        [17, 17, 19],
    ],
    [
        [21, 22, 23],
        [24, 25, 26],
        [27, 27, 29],
    ],
    [
        [31, 32, 33],
        [34, 35, 36],
        [37, 37, 39],
    ],
]


def sum_elements(lst):
    total = 0
    for item in lst:
        if isinstance(item, list):
            total += sum_elements(item)
        else:
            total += item
    return total


if __name__ == "__main__":
    print(sum_elements(NUMS))
