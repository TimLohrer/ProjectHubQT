import time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QDate
from copy import copy

from config.Colors import Colors
from components.TitleBar import TitleBar
from config.Type import Type
from config.Status import Status
from config.Priority import Priority
from config.structs import ProjectStruct
from database.handler import DatabaseHandler

class ProjectDetails(QWidget):
    def __init__(self, project, window):
        """This is a standart ProjectHub visual task element.

			Args:
		"""
        super().__init__() # init QWidget (parent class)

        self.db_handler = window.db_handler

        # configuring self ...
        self.setFixedSize(600, 350)
        self.window = window
        self.project = copy(project)
        self.original_project = copy(project)
        self.gray_save_button = False

        # creating elements
        self.main_layout = QVBoxLayout()
        self.title_bar = TitleBar(self, f"Edit Project", False, False)

        self.name_label = QLabel("Name")
        self.name_text = QLineEdit(self.project.name)

        self.description_label = QLabel("Description")
        self.description_text = QTextEdit(self.project.description)

        self.delete_button = QPushButton("Delete")
        self.save_button = QPushButton("Save")

        # configuring the elements
        self.main_layout.setAlignment(Qt.AlignTop)

        self.name_text.textChanged.connect(self.update_name)
        self.name_text.setPlaceholderText("Enter a name...")

        self.description_text.setAlignment(Qt.AlignTop)
        self.description_text.setLineWrapMode(QTextEdit.WidgetWidth)
        self.description_text.setPlaceholderText("Enter a description...")
        self.description_text.textChanged.connect(self.update_description)

        self.delete_button.enterEvent = lambda event: self.setCursor(Qt.PointingHandCursor)
        self.delete_button.leaveEvent = lambda event: self.setCursor(Qt.ArrowCursor)
        self.delete_button.clicked.connect(self.delete)

        self.save_button.enterEvent = lambda event: self.setCursor(Qt.PointingHandCursor)
        self.save_button.leaveEvent = lambda event: self.setCursor(Qt.ArrowCursor)
        self.save_button.clicked.connect(self.save)

        # styling
        self.setStyleSheet(f"background-color: { Colors.background }; color: white;")

        field_name_css = "font-size: 13px; font-weight: bold; padding: 0px; margin: 0px;"

        self.name_label.setFixedHeight(20)
        self.name_label.setStyleSheet(field_name_css)
        self.name_text.setStyleSheet("font-size: 25px; font-weight: bold; border: 0px;")

        self.description_label.setFixedHeight(20)
        self.description_label.setStyleSheet(field_name_css)
        self.description_text.setStyleSheet(f"padding: 5px; border-radius: 5px; font-size: 14px; background-color: { Colors.second_background };")
        self.description_text.setFixedHeight(100)

        self.delete_button.setStyleSheet(f"background-color: { Colors.red }; color: { Colors.background }; font-weight: bold; border-radius: 5px; padding: 5px;")
        self.delete_button.setFixedHeight(33)
        self.delete_button.setFixedWidth(90)

        self.save_button.setStyleSheet(f"background-color: { Colors.green }; color: { Colors.background }; font-weight: bold; border-radius: 5px; padding: 5px;")
        self.save_button.setFixedHeight(33)
        self.save_button.setFixedWidth(80)

        # adding elements
        self.setLayout(self.main_layout)
        self.main_layout.addWidget(self.title_bar)
        self.main_layout.addWidget(self.name_label)
        self.main_layout.addWidget(self.name_text)
        self.main_layout.addSpacing(5)
        self.main_layout.addWidget(self.description_label)
        self.main_layout.addWidget(self.description_text)
        self.main_layout.addSpacing(10)
        self.main_layout.addWidget(self.delete_button, 0, Qt.AlignBottom)
        self.main_layout.addWidget(self.save_button, 0, Qt.AlignBottom)

        # set create button to gray initially
        self.check_save_button_visibility()

        if len(self.db_handler.projects.fetch()) < 2:
            self.delete_button.hide()

    def update_name(self, new_name):
        self.project.name = new_name
        self.check_save_button_visibility()

    def update_description(self):
        self.project.description = self.description_text.toPlainText()
        self.check_save_button_visibility()

    def check_save_button_visibility(self):
        hide = (self.project.name == self.original_project.name and self.project.name != "") and (self.project.description == self.original_project.description)
        if not hide:
            self.save_button.show()
        else:
            self.save_button.hide()

    def save(self):
        self.db_handler.projects.update(
            id=self.project.id,
			name=self.project.name,
			description=self.project.description
        )
        self.window.update_workpace()
        self.hide()

    def delete(self):
        self.db_handler.projects.delete(id=self.project.id)
        if self.window.PROJECT_ID == self.project.id:
            new_project_id = self.db_handler.projects.fetch()[0].id
            self.window.PROJECT_ID = new_project_id
        self.window.update_workpace()
        self.hide()