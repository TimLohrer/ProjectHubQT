import time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QDate
from copy import copy

from config.Colors import Colors
from components.TitleBar import TitleBar
from config.structs import UserStruct

class CreateUser(QWidget):
    def __init__(self, window):
        """This is a standart ProjectHub visual task element.

			Args:
		"""
        super().__init__() # init QWidget (parent class)

        self.db_handler = window.db_handler

        # configuring self ...
        self.setFixedSize(500, 375)
        self.window = window
        self.user = UserStruct(id=0)
        self.gray_create_button = False

        # creating elements
        self.main_layout = QVBoxLayout()
        self.title_bar = TitleBar(self, f"Create User", False, False)

        self.firstname_label = QLabel("First Name")
        self.firstname_text = QLineEdit(self.user.firstname)

        self.surname_label = QLabel("Last Name")
        self.surname_text = QLineEdit(self.user.surname)

        self.username_label = QLabel("Username")
        self.username_text = QLineEdit(self.user.surname)

        self.email_label = QLabel("Email")
        self.email_text = QLineEdit(self.user.surname)

        self.create_button = QPushButton("Create")

        # configuring the elements
        self.main_layout.setAlignment(Qt.AlignTop)

        self.firstname_text.textChanged.connect(self.update_firstname)
        self.firstname_text.setPlaceholderText("e.g. John")

        self.surname_text.setPlaceholderText("e.g. Doe")
        self.surname_text.textChanged.connect(self.update_surname)

        self.username_text.setPlaceholderText("e.g. johndoe (must be unique)")
        self.username_text.textChanged.connect(self.update_username)

        self.email_text.setPlaceholderText("e.g. john.doe@example.com (must be unique)")
        self.email_text.textChanged.connect(self.update_email)

        self.create_button.enterEvent = lambda event: self.setCursor(Qt.PointingHandCursor)
        self.create_button.leaveEvent = lambda event: self.setCursor(Qt.ArrowCursor)
        self.create_button.clicked.connect(self.create)

        # styling
        self.setStyleSheet(f"background-color: { Colors.background }; color: white;")

        field_name_css = "font-size: 13px; font-weight: bold; padding: 0px; margin: 0px;"

        self.firstname_label.setFixedHeight(20)
        self.firstname_label.setStyleSheet(field_name_css)
        self.firstname_text.setStyleSheet(f"border: 0px; padding: 5px; border-radius: 5px; font-size: 12px; background-color: { Colors.second_background };")
        self.firstname_text.setFixedHeight(30)

        self.surname_label.setFixedHeight(20)
        self.surname_label.setStyleSheet(field_name_css)
        self.surname_text.setStyleSheet(f"border: 0px; padding: 5px; border-radius: 5px; font-size: 12px; background-color: { Colors.second_background };")
        self.surname_text.setFixedHeight(30)

        self.username_label.setFixedHeight(20)
        self.username_label.setStyleSheet(field_name_css)
        self.username_text.setStyleSheet(f"border: 0px; padding: 5px; border-radius: 5px; font-size: 12px; background-color: { Colors.second_background };")
        self.username_text.setFixedHeight(30)

        self.email_label.setFixedHeight(20)
        self.email_label.setStyleSheet(field_name_css)
        self.email_text.setStyleSheet(f"border: 0px; padding: 5px; border-radius: 5px; font-size: 12px; background-color: { Colors.second_background };")
        self.email_text.setFixedHeight(30)

        self.create_button.setStyleSheet(f"background-color: { Colors.green }; color: { Colors.background }; font-weight: bold; border-radius: 5px; padding: 5px;")
        self.create_button.setFixedHeight(33)
        self.create_button.setFixedWidth(80)

        # adding elements
        self.setLayout(self.main_layout)
        self.main_layout.addWidget(self.title_bar)
        self.main_layout.addWidget(self.firstname_label)
        self.main_layout.addWidget(self.firstname_text)
        self.main_layout.addSpacing(2)
        self.main_layout.addWidget(self.surname_label)
        self.main_layout.addWidget(self.surname_text)
        self.main_layout.addSpacing(2)
        self.main_layout.addWidget(self.username_label)
        self.main_layout.addWidget(self.username_text)
        self.main_layout.addSpacing(2)
        self.main_layout.addWidget(self.email_label)
        self.main_layout.addWidget(self.email_text)
        self.main_layout.addSpacing(15)
        self.main_layout.addWidget(self.create_button, 0, Qt.AlignBottom)

        # set create button to gray initially
        self.check_create_button_visibility()

    def update_firstname(self, new_firstname):
        self.user.firstname = new_firstname
        self.check_create_button_visibility()

    def update_surname(self, new_surname):
        self.user.surname = new_surname
        self.check_create_button_visibility()

    def update_username(self, new_username):
        self.user.username = new_username
        self.check_create_button_visibility()

    def update_email(self, new_email):
        self.user.email = new_email
        self.check_create_button_visibility()

    def check_create_button_visibility(self):
        gray = (self.user.firstname == "") or (self.user.surname == "") or (self.user.username == "") or (self.user.email == "" or "@" not in self.user.email or "." not in self.user.email)
        opacity = QGraphicsOpacityEffect()
        if not gray:
            opacity.setOpacity(1.0)
        else:
            opacity.setOpacity(0.75)
        self.create_button.setGraphicsEffect(opacity)
        return not gray

    def validate_inputs(self) -> bool:
        if len(self.db_handler.users.fetch(username=self.user.username)) != 0:
            return False
        elif len(self.db_handler.users.fetch(email=self.user.email)) != 0:
            return False
        else:
            return True

    def create(self):
        if not self.check_create_button_visibility() or not self.validate_inputs():
            return
        self.db_handler.users.create(
            firstname=self.user.firstname,
            surname=self.user.surname,
            username=self.user.username,
            email=self.user.email
        )
        self.window.switch_user(self.db_handler.users.fetch(username=self.user.username)[0].id)
        self.hide()