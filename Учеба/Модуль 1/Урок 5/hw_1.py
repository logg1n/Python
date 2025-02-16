def sum_range(start, end):
    total = 0
    for number in range(start, end + 1):
        total += number
    return total


start = int(input("Введите начальное значение (start): "))
end = int(input("Введите конечное значение (end): "))

result = sum_range(start, end)
print(f"Сумма всех целых чисел от {start} до {end} включительно: {result}")
