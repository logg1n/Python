def func(l: list):
    # получение диагонали
    for i, a in enumerate(l):
        a[:i] = [0] * i


if __name__ == "__main__":
    ls = [
        [11, 12, 13, 14, 15],
        [21, 22, 23, 24, 25],
        [31, 32, 33, 34, 35],
        [41, 42, 43, 44, 45],
        [51, 52, 53, 54, 55],
    ]
    func(ls)
    for a in ls:
        print(a)
