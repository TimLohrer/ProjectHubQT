from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

class Project(QFrame):
	def __init__(self):
		"""This is a standart ProjectHub visual project element.

			Args:
		"""
		super().__init__() # init QWidget (parent class)

		self.setObjectName("project")
		self.setFixedWidth(150)

		title_label = QLabel("ProjectHub")

		layout = QVBoxLayout(self)
		layout.setAlignment(Qt.AlignTop)
		layout.addWidget(title_label)
