while True:
    user_input = input("Введите целое число: ")
    try:
        user_number = int(user_input)
        print(f"Вы ввели число: {user_number}")
        break
    except ValueError:
        print(
            "Невозможно преобразовать введенное значение в целое число. Попробуйте еще раз."
        )
