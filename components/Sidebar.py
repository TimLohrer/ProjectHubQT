from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

class Sidebar(QFrame):
	def __init__(self, projects=[]):
		"""This is a standart ProjectHub visual sidebar element.

            Args:
                projects (list<Projects>) (=[<empty list>])
        """
		super().__init__() # init QWidget (parent class)

        # configuring self ...
		self.setObjectName("sidebar")

        # creating elements
		main_layout = QVBoxLayout(self)

		title_label = QLabel("ProjectHub")

        # configuring the elements
		main_layout.setAlignment(Qt.AlignTop)

		# adding projects
		main_layout.addWidget(title_label)

		for project in projects:
			main_layout.addWidget(project)
