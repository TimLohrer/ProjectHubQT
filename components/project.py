from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSignal

from config.Colors import Colors

class Project(QFrame):
	# Create custom event emitter
	clicked = pyqtSignal(int)

	def __init__(self, project, active = False):
		"""This is a standart ProjectHub visual project element.

			Args:
		"""
		super().__init__() # init QWidget (parent class)

        # configuring self ...
		self.setObjectName("project")
		self.setFixedWidth(200)
		self.project = project

        # creating elements
		self.main_layout = QVBoxLayout(self)

		self.title_label = QLabel(project.name)

        # configuring the elements
		self.main_layout.setAlignment(Qt.AlignTop)

		# styling
		background_color = Colors.blue if active else Colors.second_background
		self.setStyleSheet(f"background-color: { background_color }; border-radius: 5px;")
		self.title_label.setStyleSheet("font-size: 14px; font-weight: bold;")

        # adding tasks
		self.main_layout.addWidget(self.title_label)

	def mousePressEvent(self, event):
		self.clicked.emit(self.project.id)
