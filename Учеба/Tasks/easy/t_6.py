def season(m):
    if m in [12, 1, 2]:
        return "зима"
    elif m in [3, 4, 5]:
        return "весна"
    elif m in [6, 7, 8]:
        return "лето"
    elif m in [9, 10, 11]:
        return "осень"
    else:
        return "Некорректный номер месяца"


if __name__ == "__main__":
    month = int(input("Введите номкр месяца (1-12): "))
    season(month)
