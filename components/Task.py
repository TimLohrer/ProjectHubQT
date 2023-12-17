from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from config.Colors import Colors

class Task(QFrame):
    def __init__(self, title, description):
        """This is a standart ProjectHub visual task element.

			Args:
		"""
        super().__init__() # init QWidget (parent class)

        # configuring self ...
        self.setObjectName("task")
        self.setFixedSize(330, 100)
        self.setStyleSheet("QFrame#task { background-color: ; border-radius: 5px; }")

        # creating elements
        main_layout = QVBoxLayout(self)

        title_label = QLabel(title)
        description_label = QLabel(description)

        # configuring the elements
        main_layout.setAlignment(Qt.AlignTop)
        # main_layout.setContentsMargins(10, 10, 10, 10)
        # main_layout.setSpacing(50)

        # adding tasks
        main_layout.addWidget(title_label)
        main_layout.addWidget(description_label)
