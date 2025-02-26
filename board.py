from task import Task
from storage import Storage

class Board:
    def __init__(self):
        self.storage = Storage()
        self.tasks = self.storage.load_tasks()

    def add_task(self, task):
        self.tasks.append(task)
        self.storage.save_tasks(self.tasks)
        print(f"Task added: {task}")

    def move_task(self, task_id, new_status):
        for task in self.tasks:
            if task.id == task_id:
                task.status = new_status
                self.storage.save_tasks(self.tasks)
                print(f"Moved task {task_id} to {new_status}")
                return
        print(f"Task {task_id} not found!")

    def list_tasks(self):
        for task in self.tasks:
            print(task)

    def filter_tasks(self, status):
        return [task for task in self.tasks if task.status == status]

    def sort_tasks(self, tasks, sort_by):
        if sort_by == "priority":
            priority_order = {"high" : 1, "medium" : 2, "low" : 3}
            return sorted(tasks, key=lambda task : priority_order.get(task.priority, 4))
        elif sort_by == "title":
            return sorted(tasks, key=lambda task : task.title.lower())
        return tasks
