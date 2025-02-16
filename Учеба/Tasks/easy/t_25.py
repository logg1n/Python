# 10-1000


def is_even_num_prelast():
    for n in range(10, 1000):
        if int(str(n)[-2]) % 2 == 0:
            print(n)


def get_even_num_prelast():
    for n in range(10, 1000):
        if ((n // 10) % 10) % 2 == 0:
            print(n)


if __name__ == "__main__":
    #    is_even_num_prelast()
    get_even_num_prelast()
