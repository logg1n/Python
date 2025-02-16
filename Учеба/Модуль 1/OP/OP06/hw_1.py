# ------------------------
# Урок 5, Задача 3
# ------------------------
def bank(m, y):
    sum = m
    for _ in range(y):
        sum += sum * (10 / 100)
    return round(sum, 2)


if __name__ == "__main__":
    while True:
        try:
            money = float(input("Введите сумму вклада: "))
            years = int(input("Введите продолжительность вклада в годах: "))
            break
        except ValueError:
            print("Неверный ввод. Пожалуйста, введите число.")

    try:
        result = bank(money, years)
        print(f"Итоговая сумма: {result}")
    except Exception as e:
        print(f"Произошла ошибка при вычислениях: {e}")
