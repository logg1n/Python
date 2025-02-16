def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None


try:
    v1 = int(input("Введите 1-е число: "))
    v2 = int(input("Введите 2-е число: "))
except ValueError:
    print("Ups")
    exit()


print(safe_divide(v1, v2))
