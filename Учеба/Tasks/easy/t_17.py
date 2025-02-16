# [1, 2, 3, 4, 5]


def get_sum_square(list):
    return sum([num**2 for num in list])


if __name__ == "__main__":
    print(get_sum_square(list=[1, 2, 3, 4, 5]))
