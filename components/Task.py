from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from config.Colors import Colors
import math
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

        # creating elements
        self.main_layout = QVBoxLayout()
        self.title_label = QLabel(task.title)
        self.description_label = QLabel(task.description)
        self.details = TaskDetails(task)

        # configuring the elements
        self.main_layout.setAlignment(Qt.AlignTop)

        # adding elements
        self.setLayout(self.main_layout)
        self.main_layout.addWidget(self.title_label)
        self.main_layout.addWidget(self.description_label)

    def show_details(self):
        self.details.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.details.show()

    def mousePressEvent(self, event):
        self.show_details()
