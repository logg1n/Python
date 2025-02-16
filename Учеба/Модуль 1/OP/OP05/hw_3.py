def bank(m, y):
    sum = m
    for _ in range(y):
        sum += sum * (10 / 100)

    return round(sum, 2)


if __name__ == "__main__":
    money = float(input("Введите сумму вклада: "))
    years = int(input("Введите продолжительность вклада в годах: "))
    print(bank(money, years))
