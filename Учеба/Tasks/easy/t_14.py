def find_firt_num(num):
    return int(str(num)[0])


def get_first_num(number):
    while number >= 10:
        number //= 10
    return number


if __name__ == "__main__":
    print(find_firt_num(323878))
    print(get_first_num(323878))
