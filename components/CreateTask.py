import time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QDate
from copy import copy

from config.Colors import Colors
from components.TitleBar import TitleBar
from config.Type import Type
from config.Status import Status
from config.Priority import Priority
from config.structs import TaskStruct
from database.handler import DatabaseHandler

class CreateTask(QWidget):
    def __init__(self, window):
        """This is a standart ProjectHub visual task element.

			Args:
		"""
        super().__init__() # init QWidget (parent class)

        self.db_handler = DatabaseHandler("__database__/database.db")

        # configuring self ...
        self.setFixedSize(800, 800)
        self.window = window
        self.task = TaskStruct(id=0, project_id=0, creator_id=self.window.USER_ID, create_date=0)
        self.gray_create_button = False
        self.asignee = -1
        self.projects = self.db_handler.projects.fetch()

        # creating elements
        self.main_layout = QVBoxLayout()
        self.title_bar = TitleBar(self, f"Create Task", False, False)

        self.title_text = QLineEdit(self.task.title)

        self.description_label = QLabel("Description")
        self.description_text = QTextEdit(self.task.description)

        self.project_label = QLabel("Project")
        self.project_selector = QComboBox(self)
        self.project_selector.addItem("Select a project...")
        for project in self.projects:
            self.project_selector.addItem(project.name)

        self.type_label = QLabel("Type")
        self.type_selector = QComboBox(self)
        self.type_selector.addItem(Type.emojify(Type.TASK)       + " Task")
        self.type_selector.addItem(Type.emojify(Type.PROBLEM)    + " Problem")
        self.type_selector.addItem(Type.emojify(Type.INITIATIVE) + " Initiative")

        self.status_label = QLabel("Status")
        self.status_selector = QComboBox(self)
        self.status_selector.addItem(Status.emojify(Status.BACKLOG)     + " Backlog")
        self.status_selector.addItem(Status.emojify(Status.TODO)        + " ToDo")
        self.status_selector.addItem(Status.emojify(Status.IN_PROGRESS) + " In Progress")
        self.status_selector.addItem(Status.emojify(Status.DONE)        + " Done")

        self.priority_label = QLabel("Priority")
        self.priority_selector = QComboBox(self)
        self.priority_selector.addItem(Priority.emojify(Priority.VERY_HIGH) + " Very High")
        self.priority_selector.addItem(Priority.emojify(Priority.HIGH)      + " High")
        self.priority_selector.addItem(Priority.emojify(Priority.MEDIUM)    + " Medium")
        self.priority_selector.addItem(Priority.emojify(Priority.LOW)       + " Low")
        self.priority_selector.addItem(Priority.emojify(Priority.VERY_LOW)  + " Very Low")

        self.due_date_label = QLabel("Due Date")
        self.due_date_text = QLineEdit(self.task.due_date)

        self.asignee_label = QLabel("Asignee")
        self.asignee_text = QLineEdit("")

        self.creator_label = QLabel("Creator")
        self.creator_text = QLabel("You")

        self.create_button = QPushButton("Create")

        # configuring the elements
        self.main_layout.setAlignment(Qt.AlignTop)

        self.title_text.textChanged.connect(self.update_title)
        self.title_text.setPlaceholderText("Enter a title...")

        self.description_text.setAlignment(Qt.AlignTop)
        self.description_text.setLineWrapMode(QTextEdit.WidgetWidth)
        self.description_text.setPlaceholderText("Enter a description...")
        self.description_text.textChanged.connect(self.update_description)

        self.type_selector.setCurrentText("Select a project...")
        self.project_selector.enterEvent = lambda event: self.setCursor(Qt.PointingHandCursor)
        self.project_selector.leaveEvent = lambda event: self.setCursor(Qt.ArrowCursor)
        self.project_selector.currentIndexChanged.connect(self.update_project)

        self.type_selector.setCurrentText(Type().emojify(self.task.type) + " " + Type().stringify(self.task.type))
        self.type_selector.enterEvent = lambda event: self.setCursor(Qt.PointingHandCursor)
        self.type_selector.leaveEvent = lambda event: self.setCursor(Qt.ArrowCursor)
        self.type_selector.currentIndexChanged.connect(self.update_type)

        self.status_selector.setCurrentText(Status().emojify(self.task.status) + " " + Status().stringify(self.task.status))
        self.status_selector.enterEvent = lambda event: self.setCursor(Qt.PointingHandCursor)
        self.status_selector.leaveEvent = lambda event: self.setCursor(Qt.ArrowCursor)
        self.status_selector.currentIndexChanged.connect(self.update_status)

        self.priority_selector.setCurrentText(Priority().emojify(self.task.priority) + " " + Priority().stringify(self.task.priority))
        self.priority_selector.enterEvent = lambda event: self.setCursor(Qt.PointingHandCursor)
        self.priority_selector.leaveEvent = lambda event: self.setCursor(Qt.ArrowCursor)
        self.priority_selector.currentIndexChanged.connect(self.update_priority)

        self.due_date_text.textChanged.connect(self.update_due_date)
        self.due_date_text.setPlaceholderText("Enter a due date...")

        self.asignee_text.textChanged.connect(self.update_asignee)
        self.asignee_text.setPlaceholderText("Enter a username...")

        self.creator_text.enterEvent = lambda event: self.setCursor(Qt.ForbiddenCursor)
        self.creator_text.leaveEvent = lambda event: self.setCursor(Qt.ArrowCursor)

        self.create_button.enterEvent = lambda event: self.setCursor(Qt.PointingHandCursor)
        self.create_button.leaveEvent = lambda event: self.setCursor(Qt.ArrowCursor)
        self.create_button.clicked.connect(self.create)

        # styling
        self.setStyleSheet(f"background-color: { Colors.background }; color: white;")
        dropdown_css = """
            QComboBox {
                background-color: {{ second-background }};
                border-radius: 5px;
                padding: 5px;
                font-size: 15px;
            }

            QComboBox::drop-down {
                border: 0px;
            }

            QComboBox QAbstractItemView {
                background-color: {{ second-background }};
                selection-background-color: {{ second-background }};
                selection-color: {{ blue }};
                outline: 0px;
                border: 0px;
                padding: 5px;
            }
        """
        self.title_text.setStyleSheet("font-size: 25px; font-weight: bold; border: 0px;")

        field_name_css = "font-size: 13px; font-weight: bold; padding: 0px; margin: 0px;"

        self.description_label.setFixedHeight(20)
        self.description_label.setStyleSheet(field_name_css)
        self.description_text.setStyleSheet(f"padding: 5px; border-radius: 5px; font-size: 14px; background-color: { Colors.second_background };")
        self.description_text.setFixedHeight(100)

        dropdown_css = dropdown_css.replace("{{ background }}", Colors.background).replace("{{ second-background }}", Colors.second_background).replace("{{ blue }}", Colors.blue)

        self.project_label.setFixedHeight(20)
        self.project_label.setStyleSheet(field_name_css)
        self.project_selector.setStyleSheet(dropdown_css)

        self.type_label.setFixedHeight(20)
        self.type_label.setStyleSheet(field_name_css)
        self.type_selector.setStyleSheet(dropdown_css)

        self.status_label.setFixedHeight(20)
        self.status_label.setStyleSheet(field_name_css)
        self.status_selector.setStyleSheet(dropdown_css)

        self.priority_label.setFixedHeight(20)
        self.priority_label.setStyleSheet(field_name_css)
        self.priority_selector.setStyleSheet(dropdown_css)

        self.due_date_label.setFixedHeight(20)
        self.due_date_label.setStyleSheet(field_name_css)
        self.due_date_text.setStyleSheet(f"border: 0px; padding: 5px; border-radius: 5px; font-size: 12px; background-color: { Colors.second_background };")
        self.due_date_text.setFixedHeight(30)

        self.asignee_label.setFixedHeight(20)
        self.asignee_label.setStyleSheet(field_name_css)
        self.asignee_text.setStyleSheet(f"border: 0px; padding: 5px; border-radius: 5px; font-size: 12px; background-color: { Colors.second_background };")
        self.asignee_text.setFixedHeight(30)

        self.creator_label.setFixedHeight(20)
        self.creator_label.setStyleSheet(field_name_css)
        self.creator_text.setStyleSheet(f"border: 0px; padding: 5px; border-radius: 5px; font-size: 12px; background-color: { Colors.second_background };")
        self.creator_text.setFixedHeight(30)
        opacity = QGraphicsOpacityEffect()
        opacity.setOpacity(0.75)
        self.creator_text.setGraphicsEffect(opacity)

        self.create_button.setStyleSheet(f"background-color: { Colors.green }; color: { Colors.background }; font-weight: bold; border-radius: 5px; padding: 5px;")
        self.create_button.setFixedHeight(33)
        self.create_button.setFixedWidth(80)

        # adding elements
        self.setLayout(self.main_layout)
        self.main_layout.addWidget(self.title_bar)
        self.main_layout.addWidget(self.title_text)
        self.main_layout.addSpacing(2)
        self.main_layout.addWidget(self.description_label)
        self.main_layout.addWidget(self.description_text)
        self.main_layout.addSpacing(5)
        self.main_layout.addWidget(self.project_label)
        self.main_layout.addWidget(self.project_selector)
        self.main_layout.addSpacing(5)
        self.main_layout.addWidget(self.type_label)
        self.main_layout.addWidget(self.type_selector)
        self.main_layout.addSpacing(2)
        self.main_layout.addWidget(self.status_label)
        self.main_layout.addWidget(self.status_selector)
        self.main_layout.addSpacing(2)
        self.main_layout.addWidget(self.priority_label)
        self.main_layout.addWidget(self.priority_selector)
        self.main_layout.addSpacing(2)
        self.main_layout.addWidget(self.due_date_label)
        self.main_layout.addWidget(self.due_date_text)
        self.main_layout.addSpacing(2)
        self.main_layout.addWidget(self.asignee_label)
        self.main_layout.addWidget(self.asignee_text)
        self.main_layout.addSpacing(2)
        self.main_layout.addWidget(self.creator_label)
        self.main_layout.addWidget(self.creator_text)
        self.main_layout.addSpacing(10)
        self.main_layout.addWidget(self.create_button, 0, Qt.AlignBottom)

        # set create button to gray initially
        self.check_create_button_visibility()

    def update_title(self, new_title):
        self.task.title = new_title
        self.check_create_button_visibility()

    def update_description(self):
        self.task.description = self.description_text.toPlainText()
        self.check_create_button_visibility()

    def update_project(self):
        if self.project_selector.currentText() == "Select a project...":
            self.task.project_id = 0
            self.check_create_button_visibility()
        try:
            self.task.project_id = self.db_handler.projects.fetch(name=self.project_selector.currentText())[0].id
            self.check_create_button_visibility()
        except Exception as e:
            print(e)

    def update_type(self):
        self.task.type = Type.parse(" ".join(self.type_selector.currentText().split(" ")[1:]))
        self.check_create_button_visibility()

    def update_status(self):
        self.task.status = Status.parse(" ".join(self.status_selector.currentText().split(" ")[1:]))
        self.check_create_button_visibility()

    def update_priority(self):
        self.task.priority = Priority.parse(" ".join(self.priority_selector.currentText().split(" ")[1:]))
        self.check_create_button_visibility()

    def update_due_date(self, new_due_date):
        if new_due_date == "":
            new_due_date = None # set empty due date to None to match previous state (NULL in db)
        self.task.due_date = new_due_date
        self.check_create_button_visibility()

    def update_asignee(self, new_asignee):
        if new_asignee == "":
            new_asignee = -1 # set asignee to -1 if empty to raise error on create if it stays empty
        self.asignee = new_asignee
        self.check_create_button_visibility()

    def check_create_button_visibility(self):
        gray = (self.task.title == "") or (self.task.project_id == 0)
        opacity = QGraphicsOpacityEffect()
        if not gray:
            opacity.setOpacity(1.0)
        else:
            opacity.setOpacity(0.75)
        self.create_button.setGraphicsEffect(opacity)
        return not gray

    def validate_inputs(self) -> bool:
        if self.asignee == -1:
            self.task.asignee_id = self.asignee
            return True
        try:
            asignee = self.db_handler.users.fetch(username=self.asignee)[0]
            self.task.asignee_id = asignee.id
            return True
        except Exception as e:
            print(e)
            return False

    def create(self):
        if not self.validate_inputs() or not self.check_create_button_visibility():
            return
        self.task.create_date = time.time()
        self.db_handler.tasks.create(
            project_id=self.task.project_id,
			creator_id=self.task.creator_id,
			asignee_id=self.task.asignee_id,
			title=self.task.title,
			description=self.task.description,
			type=self.task.type,
			status=self.task.status,
			priority=self.task.priority,
			due_date=self.task.due_date,
            create_date=time.time()
        )
        self.window.update_workpace()
        self.hide()