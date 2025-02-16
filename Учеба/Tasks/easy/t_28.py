# Нужно полуить главную диагональ  [ 11, 22, 33,44, 55 ]


def get_diagonal(arr):
    res = []
    for i, a in enumerate(arr):
        res.append(a[i])

    return res


if __name__ == "__main__":
    arr = [
        [11, 12, 13, 14, 15],
        [21, 22, 23, 24, 25],
        [31, 32, 33, 34, 35],
        [41, 42, 43, 44, 45],
        [51, 52, 53, 54, 55],
    ]

    print(get_diagonal(arr))
