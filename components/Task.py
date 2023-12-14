from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

class Task(QFrame):
    def __init__(self, title, description, parent=None):
        super().__init__(parent)

        self.setObjectName("task")
        self.setFixedSize(330, 100)

        title_label = QLabel(title)
        title_label.setObjectName("title")
        description_label = QLabel(description)
        description_label.setObjectName("description")

        title_label.setStyleSheet("QLabel#title { color: white; font-size: 16px; font-weight: bold; }")
        description_label.setStyleSheet("QLabel#description { color: white; font-size: 16px; font-weight: bold; }")

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)
        layout.addWidget(title_label)
        layout.addWidget(description_label)

        # layout.setContentsMargins(10, 10, 10, 10)
        # layout.setSpacing(50)

        self.setStyleSheet("QFrame#task { background-color: lightblue; border-radius: 5px; }")
