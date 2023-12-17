from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

from config.Colors import Colors

class TitleBar(QWidget):
    def __init__(self):
        super().__init__()

        # configuring self ...
        self.setAutoFillBackground(True)
        self.initial_pos = None

        # creating elements
        self.horizontal_layout = QHBoxLayout()
        self.title = QLabel("ProjectHub")

        # configuring new elements
        self.horizontal_layout.setContentsMargins()
        self.horizontal_layout.setSpacing(2)
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # adding element
        self.setLayout(self.horizontal_layout)
        self.horizontal_layout.addWidget(self.title)

        # styling
        self.title.setStyleSheet(
            """font-weight: bold;
            border: 2px solid black;
            border-radius: 12px;
            margin: 2px;
            """
        )