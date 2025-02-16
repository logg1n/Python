# + - * ** / // %
OPERATION = [
    "Сложение",
    "Вычитание",
    "Умножение",
    "Возведение в степень 2",
    "Деление",
    "Целая часть от деления",
    "Остаток от деления",
]


def solve():
    val_1 = int(input("Введите 1-ое значение: "))
    val_2 = int(input("Введите 2-ое значение: "))

    return [
        val_1 + val_2,
        val_1 - val_2,
        val_1 * val_2,
        val_1**val_2,
        val_1 / val_2,
        val_1 // val_2,
        val_1 % val_2,
    ]


if __name__ == "__main__":
    for k, o in zip(solve(), OPERATION):
        print("-------------------------------")
        print(f"{o}: {k}")
