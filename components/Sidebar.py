from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

from config.Color import Colors

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
		create_task_button = QPushButton("Create Task")
		scroll_area = QScrollArea(self)
		projects_container_widget = QWidget(scroll_area)
		projects_container_layout = QVBoxLayout(projects_container_widget)

        # configuring the elements
		main_layout.setAlignment(Qt.AlignTop)
		scroll_area.setWidgetResizable(True)
		scroll_area.setFixedWidth(170)
		scroll_area.setMinimumHeight(350)

		#styling
		title_label.setStyleSheet("font-size: 28px; font-weight: bold; margin-bottom: 10px")
		create_task_button.setStyleSheet("background-color: " + Colors.green + "; border-radius: 5px; padding: 10px")
		scroll_area.setStyleSheet("border: 0px, background-color: transparent")

		# adding projects
		main_layout.addWidget(title_label)
		main_layout.addWidget(create_task_button)
		main_layout.addWidget(scroll_area)

		for project in projects:
			projects_container_layout.addWidget(project)
