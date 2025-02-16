# [2-300]
# stop 237
# step n / 2 == 0


def get_even_nums(range):
    range_even = []

    for r in range:
        if r == 237:
            break

        if r % 2 == 0:
            range_even.append(r)

    return range_even


if __name__ == "__main__":
    print(get_even_nums(range=[r for r in range(2, 300)]))
