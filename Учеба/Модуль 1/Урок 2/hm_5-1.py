import requests


def get_exchange_rate():
    response = requests.get(
        "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    )
    data = response.json()
    return data["bitcoin"]["usd"]


def convert():
    exchange_rate = get_exchange_rate()
    print(f"Текущий курс BTC/USDT: {exchange_rate:.8f}")

    while True:
        print("\n1. Конвертировать\n2. Выход")
        option = int(input("Выберите действие: "))

        if option == 1:
            usdt = float(input("Введите сумму в USDT: "))
            btc = usdt / exchange_rate  # Используем деление для конвертации
            print(f"{usdt} USDT = {btc:.8f} BTC")  # Ограничиваем до 8 десятичных знаков
        elif option == 2:
            break


if __name__ == "__main__":
    convert()
