import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Tuple, Union

@dataclass
class Task:
    title: str
    completed: bool = False

class ToDoManager:
    def __init__(self):
        self.tasks: List[Task] = []
        self._file_path = Path(__file__).parent / "ToDo_app_data.json"
        #self.load_tasks()

    def add_task(self, task: Task):
        self.tasks.append(task)
        self.save_tasks()

    def remove_task(self, task: Task):
        self.tasks.remove(task)
        self.save_tasks()

    def toggle_task(self, task: Task):
        task.completed = not task.completed
        self.save_tasks()

    def get_tasks(self) -> List[Task]:
        return self.tasks

    def save_tasks(self):
        with open(self._file_path, "w") as file:
            json.dump([asdict(task) for task in self.tasks], file, indent=4)

    def load_tasks(self):
        if self._file_path.exists():
            with open(self._file_path, "r") as file:
                data = json.load(file)
                self.tasks = [Task(**task) for task in data]