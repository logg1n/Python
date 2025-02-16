def arithmetic(val1, val2, oper):
    if oper == "+":
        return val1 + val2
    elif oper == "-":
        return val1 - val2
    elif oper == "*":
        return val1 * val2
    elif oper == "/":
        if val2 != 0:
            return val1 / val2
        else:
            return "Деление на ноль!"
    else:
        return "Неизвестная операция"


def set_data():
    val1 = int(input("Введите 1-ое значение: "))
    val2 = int(input("Введите 2-ое значение: "))
    operation = input("Введите операцию: ")
    print()
    print(arithmetic(val1, val2, operation))


if __name__ == "__main__":
    set_data()
