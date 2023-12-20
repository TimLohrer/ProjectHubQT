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

        if len(self.task.title) > 35:
            self.task.title = self.task.title[0:35] + "..."
        if len(self.task.description) > 105:
            self.task.description = self.task.description[0:105] + "..."

        # creating elements
        self.main_layout = QVBoxLayout()
        self.title_label = QLabel(self.task.title)
        self.description_label = QLabel(self.task.description)
        self.type_icon = ""
        match self.task.type:
            case Type.TASK:
                type_icon = "📋"
            case Type.PROBLEM:
                type_icon = "⚠️"
            case Type.INITIATIVE:
                type_icon = "💡"
            case _:
                type_icon = Type().stringify(self.task.type)
        self.priority_icon = ""
        match self.task.priority:
            case Priority.VERY_LOW:
                priority_icon = "🔵"
            case Priority.LOW:
                priority_icon = "🟣"
            case Priority.MEDIUM:
                priority_icon = "🟡"
            case Priority.HIGH:
                priority_icon = "🟠"
            case Priority.VERY_HIGH:
                priority_icon = "🔴"
            case _:
                priority_icon = Priority().stringify(self.task.priority)
        self.info_label = QLabel(f"Type: <b>{ type_icon }</b>  |  Priority: <b>{ priority_icon }</b>  |  Asignee: <b>{ self.task.asignee_id }</b>")

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
