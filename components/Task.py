from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

class Task(QFrame):
    def __init__(self, title, description, parent=None):
        super().__init__(parent)

        self.setObjectName("task")

        title_label = QLabel(title)
        description_label = QLabel(description)

        layout = QVBoxLayout(self)
        layout.addWidget(title_label)
        layout.addWidget(description_label)

        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        self.setStyleSheet("QFrame#task { background-color: lightblue; border-radius: 5px; }")
