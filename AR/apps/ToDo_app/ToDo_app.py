import numpy as np
import cv2

from gui.elements.dropdown import Dropdown
from gui.elements.number_box import NumberBox
from apps.app_base import FixedAspectApp, FreeResizeApp
from gui.color_manager import *
from gui.draw import *
from other_utilities import *
from hand_detection_models import *
from gui.keyboard import Keyboard
from apps.ToDo_app.ToDo_manager import ToDoManager, Task

class ToDoApp(FreeResizeApp):
    def __init__(self, name: str, display_name: str, icon_path: str):
        super().__init__(name, display_name, icon_path)
        self.manager = ToDoManager()
        self.new_task_title = ""

    def draw(self, image: np.ndarray, gestures: DetectionModel):
        # Draw tasks
        y_offset = 50
        for task in self.manager.get_tasks():
            color = (0, 255, 0) if task.completed else (255, 0, 0)
            cv2.putText(image, task.title, (50, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
            y_offset += 40

        # Draw input for new task
        cv2.putText(image, f"New Task: {self.new_task_title}", (50, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    def handle_gesture(self, gesture: DetectionModel):
        # Example: Add a new task when a specific gesture is detected
        if gesture.left_hand.clicked:
            self.manager.add_task(Task(title=self.new_task_title))
            self.new_task_title = ""