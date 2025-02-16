def has_one_divisor(n):
    count = 0
    for i in range(2, n):
        if n % i == 0:
            count += 1
        if count > 1:
            return False
    return count == 1


if __name__ == "__main__":
    numbers = [4, 8, 9, 10, 15]
    results = {number: has_one_divisor(number) for number in numbers}

    print(results)
