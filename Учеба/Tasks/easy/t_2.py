def check_polindrome():
    str = input("Введите строку палиндром: ")
    cl_str = "".join([ch for ch in str if ch.isalpha()]).lower()
    print()

    if cl_str == cl_str[::-1]:
        print("Строка является палиндромом.")
    else:
        print("Строка не является палиндромом.")


if __name__ == "__main__":
    check_polindrome()
