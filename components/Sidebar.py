from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

class Sidebar(QFrame):
	def __init__(self, projects=[]):
		"""This is a standart ProjectHub visual sidebar element.

            Args:
                projects (list<Projects>) (=[<empty list>])
        """
		super().__init__() # init QWidget (parent class)

		self.setObjectName("sidebar")
		self.setFixedWidth(150)

		title_label = QLabel("ProjectHub")

		layout = QVBoxLayout(self)
		layout.setAlignment(Qt.AlignTop)
		layout.addWidget(title_label)