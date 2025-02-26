import json
import os
from task import Task

class Storage:
    FILE_PATH = "data/tasks.json"

    def load_tasks(self):
        if not os.path.exists(self.FILE_PATH):
            print("Path does not exist")
            return []

        try:
            with open(self.FILE_PATH, "r") as f:
                data = f.read().strip()
                if not data:
                    print("Data not found")
                    return []
                return [Task(task["id"], task["title"], task["status"], task["priority"]) for task in json.loads(data)]
        except (json.JSONDecodeError, FileNotFoundError):
            print("LOAD TASK ERROR")
            return []

    def save_tasks(self, tasks):
        os.makedirs(os.path.dirname(self.FILE_PATH), exist_ok=True)
        with open(self.FILE_PATH, "w") as f:
            json.dump([task.__dict__ for task in tasks], f, indent=4)
