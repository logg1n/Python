try:
    text = input("Введите текст: ")
except EOFError:
    print("Ошибка при вводе данных. Пожалуйста, попробуйте снова.")
else:
    try:
        with open("user_data.txt", "a", encoding="utf-8") as file:
            file.write(text + "\n")
    except IOError as e:
        print(f"Ошибка при работе с файлом: {e}")
    else:
        print("Текст успешно записан в файл user_data.txt.")
