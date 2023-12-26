from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

from config.Colors import Colors
from components.CreateTask import CreateTask
from components.CreateProject import CreateProject
from components.SwitchAccount import SwitchAccount

class Sidebar(QFrame):
	def __init__(self, window: object, projects: list):
		"""This is a standart ProjectHub visual sidebar element.

            Args:
                projects (list<Projects>) (=[<empty list>])
        """
		super().__init__() # init QFrame (parent class)
		self.db_handler = window.db_handler
		self.window = window
		self.user = self.db_handler.users.fetch(id=self.window.USER_ID)[0]

        # configuring self ...
		self.setObjectName("sidebar")

        # creating elements
		self.main_layout = QVBoxLayout(self)

		self.title_label = QLabel("ProjectHub")
		self.create_task_button = QPushButton("Create Task")
		self.create_project_button = QPushButton("Create Project")
		self.scroll_area = QScrollArea(self)
		self.projects_container_widget = QWidget(self.scroll_area)
		self.projects_container_layout = QVBoxLayout(self.projects_container_widget)
		self.user_label = QLabel(f"{ self.user.firstname } { self.user.surname }")
		self.switch_account_button = QPushButton("Switch Account")

        # configuring the elements
		self.main_layout.setAlignment(Qt.AlignTop)
		self.create_task_button.clicked.connect(self.create_task)
		self.create_project_button.clicked.connect(self.create_project)
		self.scroll_area.setWidgetResizable(True)
		self.scroll_area.setFixedWidth(200)
		self.scroll_area.setMinimumHeight(350)
		self.switch_account_button.clicked.connect(self.switch_account)

		#styling
		self.title_label.setStyleSheet(f"color: { Colors.blue }; font-size: 30px; font-weight: bold; margin-bottom: 10px;")
		self.create_task_button.setStyleSheet(f"background-color: { Colors.green }; color: { Colors.background }; font-weight: bold; border-radius: 5px; padding: 10px;")
		self.create_project_button.setStyleSheet(f"background-color: { Colors.blue }; color: white; font-weight: bold; border-radius: 5px; padding: 10px;")
		self.scroll_area.setStyleSheet("QScrollArea { margin-top: 10px; }")
		self.user_label.setStyleSheet(f"color: white; font-size: 20px; font-weight: bold; margin-bottom: 10px;")
		self.switch_account_button.setStyleSheet(f"background-color: { Colors.blue }; color: white; font-weight: bold; border-radius: 5px; padding: 10px;")

		# adding projects
		self.main_layout.addWidget(self.title_label)
		self.main_layout.addWidget(self.create_task_button)
		self.main_layout.addSpacing(3)
		self.main_layout.addWidget(self.create_project_button)
		self.main_layout.addWidget(self.scroll_area)
		self.main_layout.addWidget(self.user_label, 0, Qt.AlignBottom)
		self.main_layout.addWidget(self.switch_account_button, 0, Qt.AlignBottom)

		for project in projects:
			self.projects_container_layout.addWidget(project)

	def create_task(self):
		create_task = CreateTask(self.window)
		create_task.show()

	def create_project(self):
		create_project = CreateProject(self.window)
		create_project.show()

	def switch_account(self):
		switch_account = SwitchAccount(self.window)
		switch_account.show()