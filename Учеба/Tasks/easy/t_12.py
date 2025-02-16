def is_operation(val1, val2):
    if val1 * val2 >= 1000:
        return val1 * val2
    else:
        return val1 + val2


if __name__ == "__main__":
    print(is_operation(50, 20))
    print(is_operation(30, 20))
