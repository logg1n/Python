from datetime import date
from typing import List


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class TaskManager(metaclass=Singleton):
    class Task:
        def __init__(self, description: str, deadline: date):
            self.description = description
            self.deadline = deadline
            self.status = False

        def mark_completed(self):
            self.status = True

        def __str__(self):
            status = "Выполнено" if self.status else "Не выполнено"
            return f"{self.description} (Дедлайн: {self.deadline}, Статус: {status})"

    def __init__(self):
        self.tasks: List[TaskManager.Task] = []

    def add_task(self, description: str, deadline: date):
        task = self.Task(description, deadline)
        self.tasks.append(task)

    def mark_task_completed(self, index: int):
        if 0 <= index < len(self.tasks):
            self.tasks[index].mark_completed()
        else:
            print("Некорректный индекс задачи")

    def get_current_tasks(self) -> List["TaskManager.Task"]:
        return [task for task in self.tasks if not task.status]


task_manager = TaskManager()

task_manager.add_task("Сделать домашнее задание", date(2025, 2, 18))
task_manager.add_task("Сделать дополнительное задание", date(2025, 2, 19))

task_manager.mark_task_completed(0)

print("\nНе выполненые задачи:")
for task in task_manager.get_current_tasks():
    print(task)


# Не выполненые задачи:
# Сделать дополнительное задание (Дедлайн: 2025-02-19, Статус: Не выполнено)
