# [
#     ['x', 'x', 'x'],
#     ['x', 'x', 'x'],
#     ['x', 'x', 'x'],
# ]


def create_arr(s, l, sym):
    arr_o = []

    for _ in range(s):
        arr_i = []
        for _ in range(l):
            arr_i.append(sym)
        arr_o.append(arr_i)

    return arr_o


if __name__ == "__main__":
    size = 3
    len = 3
    sym = "x"

    print(create_arr(size, len, sym))
