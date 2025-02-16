import tkinter as tk
from tkinter import messagebox
import json


def add_task():
    task = task_entry.get()
    if task:
        frame = tk.Frame(task_list_box, bg="#F7DC6F", bd=1, relief="solid")
        label = tk.Label(
            frame, text=task, bg="#F7DC6F", fg="#34495E", font=("Arial", 12)
        )
        label.pack(side=tk.LEFT, padx=10)
        delete_btn = tk.Button(
            frame,
            text="Удалить",
            command=lambda: frame.destroy(),
            bg="#E74C3C",
            fg="#FFFFFF",
            font=("Arial", 10),
        )
        delete_btn.pack(side=tk.RIGHT, padx=5)
        mark_btn = tk.Button(
            frame,
            text="Выполнено",
            command=lambda: mark_task(frame, label),
            bg="#3498DB",
            fg="#FFFFFF",
            font=("Arial", 10),
        )
        mark_btn.pack(side=tk.RIGHT, padx=5)
        frame.pack(pady=5, fill="x")
        tasks.append({"text": task, "completed": False})
        task_entry.delete(0, tk.END)
        update_task_counter()


def mark_task(frame, label):
    frame.configure(bg="light green")
    label.configure(bg="light green")
    for task in tasks:
        if task["text"] == label.cget("text"):
            task["completed"] = True
    update_task_counter()


def save_tasks():
    with open("tasks.json", "w") as file:
        json.dump(tasks, file)
    messagebox.showinfo("Сохранение задач", "Ваши задачи сохранены.")


def load_tasks():
    try:
        with open("tasks.json", "r") as file:
            loaded_tasks = json.load(file)
        for task in loaded_tasks:
            frame = tk.Frame(task_list_box, bg="#F7DC6F", bd=1, relief="solid")
            label = tk.Label(
                frame, text=task["text"], bg="#F7DC6F", fg="#34495E", font=("Arial", 12)
            )
            label.pack(side=tk.LEFT, padx=10)
            delete_btn = tk.Button(
                frame,
                text="Удалить",
                command=lambda: frame.destroy(),
                bg="#E74C3C",
                fg="#FFFFFF",
                font=("Arial", 10),
            )
            delete_btn.pack(side=tk.RIGHT, padx=5)
            mark_btn = tk.Button(
                frame,
                text="Выполнено",
                command=lambda: mark_task(frame, label),
                bg="#3498DB",
                fg="#FFFFFF",
                font=("Arial", 10),
            )
            mark_btn.pack(side=tk.RIGHT, padx=5)
            if task["completed"]:
                mark_task(frame, label)
            frame.pack(pady=5, fill="x")
            tasks.append(task)
        update_task_counter()
    except FileNotFoundError:
        messagebox.showwarning("Загрузка задач", "Файл с задачами не найден.")


def update_task_counter():
    total_tasks = len(tasks)
    completed_tasks = sum(1 for task in tasks if task["completed"])
    task_counter_label.config(
        text=f"Всего задач: {total_tasks} | Выполнено: {completed_tasks}"
    )


root = tk.Tk()
root.title("Task List")
root.configure(background="#F2F3F4")

tasks = []

style = {"bg": "#F2F3F4", "fg": "#34495E", "font": ("Arial", 12), "padx": 10, "pady": 5}

# Верхняя часть интерфейса для добавления задач
frame_top = tk.Frame(root, bg="#F2F3F4")
frame_top.pack(pady=10)

text1 = tk.Label(frame_top, text="Введите вашу задачу", **style)
text1.pack(side=tk.LEFT, padx=5)

task_entry = tk.Entry(
    frame_top, width=40, bg="#E6B0AA", fg="#34495E", font=("Arial", 12)
)
task_entry.pack(side=tk.LEFT, padx=5)

add_task_btn = tk.Button(
    frame_top,
    text="Добавить задачу",
    command=add_task,
    bg="#48C9B0",
    fg="#FFFFFF",
    font=("Arial", 12),
)
add_task_btn.pack(side=tk.LEFT, padx=5)

# Средняя часть интерфейса для списка задач
frame_middle = tk.Frame(root, bg="#F2F3F4")
frame_middle.pack(pady=10)

text2 = tk.Label(frame_middle, text="Список задач", **style)
text2.pack()

task_list_box = tk.Frame(frame_middle, bg="#F2F3F4")
task_list_box.pack(pady=5, fill="both", expand=True)

# Нижняя часть интерфейса для кнопок управления
frame_bottom = tk.Frame(root, bg="#F2F3F4")
frame_bottom.pack(pady=10)

save_btn = tk.Button(
    frame_bottom,
    text="Сохранить задачи",
    command=save_tasks,
    bg="#F39C12",
    fg="#FFFFFF",
    font=("Arial", 12),
)
save_btn.pack(side=tk.LEFT, padx=5)

load_btn = tk.Button(
    frame_bottom,
    text="Загрузить задачи",
    command=load_tasks,
    bg="#8E44AD",
    fg="#FFFFFF",
    font=("Arial", 12),
)
load_btn.pack(side=tk.LEFT, padx=5)

task_counter_label = tk.Label(root, text="", **style)
task_counter_label.pack(pady=5)
update_task_counter()

root.mainloop()
