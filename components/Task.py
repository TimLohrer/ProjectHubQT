from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import math
from copy import copy

from config.Colors import Colors
from config.Type import Type
from config.Priority import Priority
from components.TaskDetails import TaskDetails
from database.handler import DatabaseHandler

class Task(QFrame):
    def __init__(self, task, window):
        """This is a standart ProjectHub visual task element.

			Args:
		"""
        super().__init__() # init QFrame (parent class)

        self.db_handler = window.db_handler

        # configuring self ...
        self.setObjectName("task")
        self.setFixedSize(330, 100)
        self.setStyleSheet(f"background-color: {Colors.blue}; border-radius: 5px;")
        self.window = window
        self.original_task = copy(task)
        self.task = copy(task)
        self.asignee = None
        self.asignee_name = ""
        self.current_user = self.db_handler.users.fetch(id=self.window.USER_ID)[0]
        try:
            self.asignee = self.db_handler.users.fetch(id=self.task.asignee_id)[0]
        except Exception as e:
            pass

        if len(self.task.title) > 35:
            self.task.title = self.task.title[0:35] + "..."
        if len(self.task.description) > 105:
            self.task.description = self.task.description[0:105] + "..."
        if not self.asignee:
             self.asignee_name = "No Asignee"
        elif len(f"{ self.asignee.firstname } { self.asignee.surname }") > 17:
            self.asignee_name = f"{ self.asignee.firstname } { self.asignee.surname }"[0:17] + "..."
        elif self.asignee.id == self.current_user.id:
            self.asignee_name = "You"
        else:
            self.asignee_name = f"{ self.asignee.firstname } { self.asignee.surname }"

        # creating elements
        self.main_layout = QVBoxLayout()
        self.title_label = QLabel(self.task.title)
        self.description_label = QLabel(self.task.description)
        self.info_label = QLabel(f"Type: { Type().emojify(self.task.type) }  |  Priority: { Priority().emojify(self.task.priority) }  |  Asignee: <b>{ self.asignee_name }</b>")

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
        details = TaskDetails(self.original_task, self.asignee, self.window)
        details.show()
