PERC = 10 / 100  # Persent 10%


def bank(m, y):
    sum = m
    for i in range(y):
        sum += sum * PERC

    return round(sum, 2)


if __name__ == "__main__":
    money = float(input("Введите сумму вклада: "))
    years = int(input("Введите продолжительность вклада в годах: "))
    print(bank(money, years))
