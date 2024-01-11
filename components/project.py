from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSignal

from config.Colors import Colors
from components.ProjectDetails import ProjectDetails

class Project(QFrame):
	def __init__(self, window: object, project: object, active: bool = False):
		"""This is a standart ProjectHub visual project element.

			Args:
		"""
		super().__init__() # init QFrame (parent class)
		self.project = project
		self.window = window

        # configuring self ...
		self.setObjectName("project")
		self.setFixedWidth(200)
		self.setFixedHeight(35)

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

    # DON'T TOUCH: this needs to stay in camel as pyqt is trying to access QFrame.mouseReleaseEvent
	def mousePressEvent(self, event):
		if event.button() == Qt.LeftButton:
			self.window.switch_project(self.project.id)
		elif event.button() == Qt.RightButton:
			details = ProjectDetails(self.project, self.window)
			details.show()

