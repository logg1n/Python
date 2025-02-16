def get_days_in_month(m):
    days_in_month = {
        1: 31,  # Январь
        2: 28,  # Февраль
        3: 31,  # Март
        4: 30,  # Апрель
        5: 31,  # Май
        6: 30,  # Июнь
        7: 31,  # Июль
        8: 31,  # Август
        9: 30,  # Сентябрь
        10: 31,  # Октябрь
        11: 30,  # Ноябрь
        12: 31,  # Декабрь
    }

    return days_in_month.get(m)


month = int(input("Введите номер месяца (1-12): "))

days = get_days_in_month(month)

print(f"Количество дней в месяце {month}: {days}")
