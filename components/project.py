from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

class Project(QFrame):
	def __init__(self, title, description):
		"""This is a standart ProjectHub visual project element.

			Args:
		"""
		super().__init__() # init QWidget (parent class)

        # configuring self ...
		self.setObjectName("project")
		self.setFixedWidth(165)

        # creating elements
		main_layout = QVBoxLayout(self)

		title_label = QLabel(title)
		description_label = QLabel(description)

        # configuring the elements
		main_layout.setAlignment(Qt.AlignTop)

        # adding tasks
		main_layout.addWidget(title_label)
		main_layout.addWidget(description_label)
