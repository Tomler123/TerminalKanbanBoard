class Task:
    def __init__(self, task_id, title, status="TODO", priority="medium"):
        self.id = task_id
        self.title = title
        self.status = status
        self.priority = priority

    def __repr__(self):
        return f"[{self.id}] {self.title} ({self.status})"
