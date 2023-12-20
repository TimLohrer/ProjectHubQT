from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import math
from copy import copy

from config.Colors import Colors
from config.Type import Type
from config.Priority import Priority
from components.TaskDetails import TaskDetails

class Task(QFrame):
    def __init__(self, task):
        """This is a standart ProjectHub visual task element.

			Args:
		"""
        super().__init__() # init QWidget (parent class)

        # configuring self ...
        self.setObjectName("task")
        self.setFixedSize(330, 100)
        self.setStyleSheet(f"background-color: {Colors.blue}; border-radius: 5px;")
        self.original_task = copy(task)
        self.task = copy(task)

        if len(self.task.title) > 40:
            self.task.title = self.task.title[0:40] + "..."
        if len(self.task.description) > 115:
            self.task.description = self.task.description[0:115] + "..."

        # creating elements
        self.main_layout = QVBoxLayout()
        self.title_label = QLabel(self.task.title)
        self.description_label = QLabel(self.task.description)
        self.info_label = QLabel(f"Type: <b>{ Type().stringify(self.task.type) }</b>  |  Priority: <b>{ Priority().stringify(self.task.priority) }</b>  |  User: <b>{ self.task.asignee_id }</b>")

        # configuring the elements
        self.main_layout.setAlignment(Qt.AlignTop)
        self.description_label.setAlignment(Qt.AlignTop)
        self.description_label.setWordWrap(True)

        # styling
        self.title_label.setStyleSheet("font-size: 15px; font-weight: bold;")
        self.description_label.setStyleSheet("font-size: 12px;")
        self.description_label.setFixedHeight(40)
        self.info_label.setStyleSheet("font-size: 13px;")

        # adding elements
        self.setLayout(self.main_layout)
        self.main_layout.addWidget(self.title_label)
        self.main_layout.addWidget(self.description_label)
        self.main_layout.addWidget(self.info_label)

    def mousePressEvent(self, event):
        details = TaskDetails(self.original_task)
        details.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        details.show()
