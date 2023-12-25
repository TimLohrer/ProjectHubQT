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

class CreateProject(QWidget):
    def __init__(self, window):
        """This is a standart ProjectHub visual task element.

			Args:
		"""
        super().__init__() # init QWidget (parent class)

        self.db_handler = DatabaseHandler("__database__/database.db")

        # configuring self ...
        self.setFixedSize(600, 300)
        self.window = window
        self.project = ProjectStruct(id=0)
        self.gray_create_button = False

        # creating elements
        self.main_layout = QVBoxLayout()
        self.title_bar = TitleBar(self, f"Create Project", False, False)

        self.name_text = QLineEdit(self.project.name)

        self.description_label = QLabel("Description")
        self.description_text = QTextEdit(self.project.description)

        self.create_button = QPushButton("Create")

        # configuring the elements
        self.main_layout.setAlignment(Qt.AlignTop)

        self.name_text.textChanged.connect(self.update_name)
        self.name_text.setPlaceholderText("Enter a name...")

        self.description_text.setAlignment(Qt.AlignTop)
        self.description_text.setLineWrapMode(QTextEdit.WidgetWidth)
        self.description_text.setPlaceholderText("Enter a description...")
        self.description_text.textChanged.connect(self.update_description)

        self.create_button.enterEvent = lambda event: self.setCursor(Qt.PointingHandCursor)
        self.create_button.leaveEvent = lambda event: self.setCursor(Qt.ArrowCursor)
        self.create_button.clicked.connect(self.create)

        # styling
        self.setStyleSheet(f"background-color: { Colors.background }; color: white;")

        self.name_text.setStyleSheet("font-size: 25px; font-weight: bold; border: 0px;")

        field_name_css = "font-size: 13px; font-weight: bold; padding: 0px; margin: 0px;"

        self.description_label.setFixedHeight(20)
        self.description_label.setStyleSheet(field_name_css)
        self.description_text.setStyleSheet(f"padding: 5px; border-radius: 5px; font-size: 14px; background-color: { Colors.second_background };")
        self.description_text.setFixedHeight(100)

        self.create_button.setStyleSheet(f"background-color: { Colors.green }; color: { Colors.background }; font-weight: bold; border-radius: 5px; padding: 5px;")
        self.create_button.setFixedHeight(33)
        self.create_button.setFixedWidth(80)

        # adding elements
        self.setLayout(self.main_layout)
        self.main_layout.addWidget(self.title_bar)
        self.main_layout.addWidget(self.name_text)
        self.main_layout.addSpacing(5)
        self.main_layout.addWidget(self.description_label)
        self.main_layout.addWidget(self.description_text)
        self.main_layout.addSpacing(10)
        self.main_layout.addWidget(self.create_button, 0, Qt.AlignBottom)

        # set create button to gray initially
        self.check_create_button_visibility()

    def update_name(self, new_name):
        self.project.name = new_name
        self.check_create_button_visibility()

    def update_description(self):
        self.project.description = self.description_text.toPlainText()
        self.check_create_button_visibility()

    def check_create_button_visibility(self):
        gray = self.project.name == ""
        opacity = QGraphicsOpacityEffect()
        if not gray:
            opacity.setOpacity(1.0)
        else:
            opacity.setOpacity(0.75)
        self.create_button.setGraphicsEffect(opacity)
        return not gray

    def create(self):
        if not self.check_create_button_visibility():
            return
        self.db_handler.projects.create(
			name=self.project.name,
			description=self.project.description,
        )
        self.window.update_workpace()
        self.hide()