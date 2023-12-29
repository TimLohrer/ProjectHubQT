from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QDate

from config.Colors import Colors
from components.TitleBar import TitleBar
from components.CreateUser import CreateUser

class SwitchAccount(QWidget):
    def __init__(self, window):
        """This is a standart ProjectHub visual task element.

			Args:
		"""
        super().__init__() # init QWidget (parent class)

        self.db_handler = window.db_handler

        # configuring self ...
        self.setFixedSize(400, 400)
        self.window = window

        self.users = [UserItem(self.window, self, user, user.id == self.window.USER_ID) for user in self.db_handler.users.fetch()]

        # creating elements
        self.main_layout = QVBoxLayout()
        self.title_bar = TitleBar(self, "Switch Account", False, False)
        self.scroll_area = QScrollArea(self)
        self.users_container_widget = QWidget(self.scroll_area)
        self.users_container_layout = QVBoxLayout(self.users_container_widget)
        self.create_user_button = QPushButton("Create User")

        # configuring the elements
        self.main_layout.setAlignment(Qt.AlignTop)
        self.users_container_layout.setAlignment(Qt.AlignTop)
        self.scroll_area.setFixedWidth(400)
        self.scroll_area.setFixedHeight(300)
        self.create_user_button.clicked.connect(self.create_user)

        #styling
        self.setStyleSheet(f"background-color: { Colors.background }; color: white;")
        self.scroll_area.setStyleSheet("QScrollArea { margin-top: 10px; border: none }")
        self.create_user_button.setStyleSheet(f"background-color: { Colors.green }; color: { Colors.background }; font-weight: bold; border-radius: 5px; padding: 10px;")

		# adding elements
        self.setLayout(self.main_layout)
        self.main_layout.addWidget(self.title_bar)
        self.main_layout.addWidget(self.scroll_area)
        self.main_layout.addWidget(self.create_user_button, 0, Qt.AlignBottom)

        for user in self.users:
            self.users_container_layout.addWidget(user)
            self.users_container_layout.addSpacing(1)

    def create_user(self):
        create_user = CreateUser(self.window)
        create_user.show()
        self.hide()

class UserItem(QWidget):
    def __init__(self, window, parent_window, user, active: bool = False):
        """This is a standart ProjectHub visual task element.

			Args:
		"""
        super().__init__() # init QWidget (parent class)

        if user.id == 0:
            self.hide()
            return

        # configuring self ...
        self.setFixedSize(400, 50)
        self.window = window
        self.parent_window = parent_window
        self.user = user
        self.active = active

        # creating elements
        self.main_layout = QVBoxLayout()
        self.full_name_label = QLabel(f"{ self.user.firstname } { self.user.surname }")
        self.details_label = QLabel(f"{ self.user.username } <{ self.user.email }>")

        # configuring elements
        # self.enterEvent = lambda event: self.setCursor(Qt.PointingHandCursor if not self.active else Qt.ArrowCursor)
        # self.leaveEvent = lambda event: self.setCursor(Qt.ArrowCursor)

        # styling
        self.main_layout.setAlignment(Qt.AlignTop)
        self.full_name_label.setStyleSheet(f"color: { Colors.blue if self.active else 'white' }; font-size: 17px; font-weight: bold;")
        self.details_label.setStyleSheet(f"color: { Colors.blue if self.active else 'gray' }; font-size: 12px;")

        # adding projects
        self.setLayout(self.main_layout)
        self.main_layout.addWidget(self.full_name_label)
        self.main_layout.addSpacing(2)
        self.main_layout.addWidget(self.details_label)

    # DON'T TOUCH: this needs to stay in camel as pyqt is trying to access QFrame.mouseReleaseEvent
    def mouseReleaseEvent(self, event):
        if not self.active:
            self.window.switch_user(self.user.id)
            self.parent_window.hide()
