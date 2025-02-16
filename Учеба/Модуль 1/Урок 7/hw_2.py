import random

students = [
    "Аня",
    "Борис",
    "Виктор",
    "Галина",
    "Дима",
    "Елена",
    "Жанна",
    "Игорь",
    "Кира",
    "Леонид",
    "Маша",
    "Наташа",
    "Олег",
    "Петр",
    "Рита",
    "Сергей",
    "Таня",
    "Ульяна",
    "Федор",
    "Христина",
    "Юрий",
    "Яна",
]


def select_students(students_list, num_of_students):
    if num_of_students > len(students_list):
        return "Недостаточно студентов в списке для выбора."

    selected_students = random.sample(students_list, num_of_students)
    return selected_students


num_to_select = 5
selected = select_students(students, num_to_select)

if isinstance(selected, list):
    print("Имена выбранных студентов для ответа на уроке:")
    for student in selected:
        print(student)
else:
    print(selected)
