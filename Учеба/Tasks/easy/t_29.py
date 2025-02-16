def prime_factors(n):
    i = 2
    factors = []
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)
    return factors


# Запрашиваем у пользователя целое число
number = int(input("Введите целое число: "))

# Получаем простые множители
factors = prime_factors(number)

# Выводим результат
print(f"Простые множители числа {number}: {factors}")
