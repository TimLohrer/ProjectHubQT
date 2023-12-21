from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

from database.handler import DatabaseHandler
from config.Colors import Colors

class Sidebar(QFrame):
	def __init__(self, projects):
		"""This is a standart ProjectHub visual sidebar element.

            Args:
                projects (list<Projects>) (=[<empty list>])
        """
		super().__init__() # init QFrame (parent class)
		self.db_handler = DatabaseHandler("__database__/database.db")

        # configuring self ...
		self.setObjectName("sidebar")

        # creating elements
		self.main_layout = QVBoxLayout(self)

		self.title_label = QLabel("ProjectHub")
		self.create_task_button = QPushButton("Create Task")
		self.scroll_area = QScrollArea(self)
		self.projects_container_widget = QWidget(self.scroll_area)
		self.projects_container_layout = QVBoxLayout(self.projects_container_widget)

        # configuring the elements
		self.main_layout.setAlignment(Qt.AlignTop)
		self.create_task_button.clicked.connect(self.createTask)
		self.scroll_area.setWidgetResizable(True)
		self.scroll_area.setFixedWidth(200)
		self.scroll_area.setMinimumHeight(350)

		#styling
		self.title_label.setStyleSheet(f"color: { Colors.blue }; font-size: 30px; font-weight: bold; margin-bottom: 10px;")
		self.create_task_button.setStyleSheet(f"background-color: { Colors.green }; color: { Colors.background }; font-weight: bold; border-radius: 5px; padding: 10px;")
		self.scroll_area.setStyleSheet("QScrollArea { margin-top: 10px; }")

		# adding projects
		self.main_layout.addWidget(self.title_label)
		self.main_layout.addWidget(self.create_task_button)
		self.main_layout.addWidget(self.scroll_area)

		for project in projects:
			self.projects_container_layout.addWidget(project)

	def createTask(self):
		self.db_handler.tasks.create(1, 1, 1, "ABC", "DEV", "TASK", "BACKLOG", "VERY_HIGH", 0)
