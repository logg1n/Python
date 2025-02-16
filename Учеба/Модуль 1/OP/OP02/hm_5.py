def convert():
    exchange = float(input("Введите курс валют BTC/USDT: "))

    while True:
        print("\n1.Конвертировать\n2.Выход\n")
        option = int(input("Выберите действие: "))

        if option == 1:
            usdt = float(input("Введите сумму в USDT: "))
            print(f"{usdt} USDT = {usdt / exchange} BTC\n")
        if option == 2:
            break


if __name__ == "__main__":
    convert()
