from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

from config.Colors import Colors

class Project(QFrame):
	def __init__(self, title, description, active = False):
		"""This is a standart ProjectHub visual project element.

			Args:
		"""
		super().__init__() # init QWidget (parent class)

        # configuring self ...
		self.setObjectName("project")
		self.setFixedWidth(200)

        # creating elements
		main_layout = QVBoxLayout(self)

		title_label = QLabel(title)

        # configuring the elements
		main_layout.setAlignment(Qt.AlignTop)

		# styling
		background_color = Colors.blue if active else Colors.second_background
		self.setStyleSheet(f"background-color: { background_color }; border-radius: 5px;")
		title_label.setStyleSheet("font-size: 14px; font-weight: bold;")

        # adding tasks
		main_layout.addWidget(title_label)
