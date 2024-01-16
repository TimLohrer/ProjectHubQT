from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QDate
from copy import copy

from config.Colors import Colors
from components.TitleBar import TitleBar
from config.Type import Type
from config.Status import Status
from config.Priority import Priority

class TaskDetails(QWidget):
    def __init__(self, task, asignee, window):
        """This is a standart ProjectHub visual task element.

			Args:
		"""
        super().__init__() # init QWidget (parent class)

        self.db_handler = window.db_handler

        # configuring self ...
        self.setFixedSize(800, 800)
        self.window = window
        self.original_task = copy(task)
        self.task = copy(task)
        self.show_save_button = False
        self.creator = self.db_handler.users.fetch(id=self.task.creator_id)[0]
        self.original_asignee = copy(asignee).username if asignee is not None else ""
        self.asignee = copy(asignee).username if asignee is not None else ""
        self.projects = self.db_handler.projects.fetch()
        self.project = None
        for project in self.projects:
            if project.id == self.task.project_id:
                self.project = project

        # creating elements
        self.main_layout = QVBoxLayout()
        self.title_bar = TitleBar(self, f"Edit Task", False, False)

        self.title_text = QLineEdit(self.task.title)

        self.description_label = QLabel("Description")
        self.description_text = QTextEdit(self.task.description)

        self.project_label = QLabel("Project")
        self.project_selector = QComboBox(self)
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
        self.asignee_text = QLineEdit(str(self.asignee))

        self.creator_label = QLabel("Creator")
        self.creator_text = QLabel(str(self.creator.username))

        self.delete_button = QPushButton("Delete")
        self.save_button = QPushButton("Save")

        # configuring the elements
        self.main_layout.setAlignment(Qt.AlignTop)

        self.title_text.textChanged.connect(self.update_title)
        self.title_text.setPlaceholderText("Enter a title...")

        self.description_text.setAlignment(Qt.AlignTop)
        self.description_text.setLineWrapMode(QTextEdit.WidgetWidth)
        self.description_text.setPlaceholderText("Enter a description...")
        self.description_text.textChanged.connect(self.update_description)

        self.project_selector.setCurrentText(self.project.name)
        self.project_selector.enterEvent = lambda event: self.setCursor(Qt.PointingHandCursor)
        self.project_selector.leaveEvent = lambda event: self.setCursor(Qt.ArrowCursor)
        self.project_selector.currentIndexChanged.connect(self.update_project)

        self.type_selector.setCurrentText(Type().emojify(task.type) + " " + Type().stringify(task.type))
        self.type_selector.enterEvent = lambda event: self.setCursor(Qt.PointingHandCursor)
        self.type_selector.leaveEvent = lambda event: self.setCursor(Qt.ArrowCursor)
        self.type_selector.currentIndexChanged.connect(self.update_type)

        self.status_selector.setCurrentText(Status().emojify(task.status) + " " + Status().stringify(task.status))
        self.status_selector.enterEvent = lambda event: self.setCursor(Qt.PointingHandCursor)
        self.status_selector.leaveEvent = lambda event: self.setCursor(Qt.ArrowCursor)
        self.status_selector.currentIndexChanged.connect(self.update_status)

        self.priority_selector.setCurrentText(Priority().emojify(task.priority) + " " + Priority().stringify(task.priority))
        self.priority_selector.enterEvent = lambda event: self.setCursor(Qt.PointingHandCursor)
        self.priority_selector.leaveEvent = lambda event: self.setCursor(Qt.ArrowCursor)
        self.priority_selector.currentIndexChanged.connect(self.update_priority)

        self.due_date_text.textChanged.connect(self.update_due_date)
        self.due_date_text.setPlaceholderText("Enter a due date...")

        self.asignee_text.textChanged.connect(self.update_asignee)
        self.asignee_text.setPlaceholderText("Enter a username...")

        self.creator_text.enterEvent = lambda event: self.setCursor(Qt.ForbiddenCursor)
        self.creator_text.leaveEvent = lambda event: self.setCursor(Qt.ArrowCursor)

        self.delete_button.enterEvent = lambda event: self.setCursor(Qt.PointingHandCursor)
        self.delete_button.leaveEvent = lambda event: self.setCursor(Qt.ArrowCursor)
        self.delete_button.clicked.connect(self.delete)

        self.save_button.enterEvent = lambda event: self.setCursor(Qt.PointingHandCursor)
        self.save_button.leaveEvent = lambda event: self.setCursor(Qt.ArrowCursor)
        self.save_button.clicked.connect(self.save)

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

        self.delete_button.setStyleSheet(f"background-color: { Colors.red }; color: { Colors.background }; font-weight: bold; border-radius: 5px; padding: 5px;")
        self.delete_button.setFixedHeight(33)
        self.delete_button.setFixedWidth(90)

        self.save_button.setStyleSheet(f"background-color: { Colors.green }; color: { Colors.background }; font-weight: bold; border-radius: 5px; padding: 5px;")
        self.save_button.setFixedHeight(33)
        self.save_button.setFixedWidth(80)
        self.save_button.hide()

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
        self.main_layout.addWidget(self.delete_button, 0, Qt.AlignBottom)
        self.main_layout.addWidget(self.save_button, 0, Qt.AlignBottom)

    def update_title(self, new_title):
        self.task.title = new_title
        self.check_save_button_visibility()

    def update_description(self):
        self.task.description = self.description_text.toPlainText()
        self.check_save_button_visibility()

    def update_project(self):
        try:
            self.task.project_id = self.db_handler.projects.fetch(name=self.project_selector.currentText())[0].id
            self.check_save_button_visibility()
        except Exception as e:
            print(e)

    def update_type(self):
        self.task.type = Type.parse(" ".join(self.type_selector.currentText().split(" ")[1:]))
        self.check_save_button_visibility()

    def update_status(self):
        self.task.status = Status.parse(" ".join(self.status_selector.currentText().split(" ")[1:]))
        self.check_save_button_visibility()

    def update_priority(self):
        self.task.priority = Priority.parse(" ".join(self.priority_selector.currentText().split(" ")[1:]))
        self.check_save_button_visibility()

    def update_due_date(self, new_due_date):
        if new_due_date == "":
            new_due_date = None # set empty due date to None to match previous state (NULL in db)
        self.task.due_date = new_due_date
        self.check_save_button_visibility()

    def update_asignee(self, new_asignee):
        if new_asignee == "":
            new_asignee = -1 # set asignee to -1 -> No Asignee
        self.asignee = new_asignee
        self.check_save_button_visibility()

    def check_save_button_visibility(self):
        hide = (self.task.title == self.original_task.title and self.task.title != "") and (self.task.description == self.original_task.description) and (self.task.project_id == self.original_task.project_id) and (self.task.type == self.original_task.type) and (self.task.status == self.original_task.status) and (self.task.priority == self.original_task.priority) and (self.task.due_date == self.original_task.due_date) and (self.asignee == self.original_asignee)
        if not hide:
            self.save_button.show()
        else:
            self.save_button.hide()

    def validate_inputs(self) -> bool:
        if self.asignee == "":
            self.asignee = -1
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

    def save(self):
        if not self.validate_inputs():
            return
        self.db_handler.tasks.update(
            id=self.task.id,
            project_id=self.task.project_id,
			asignee_id=self.task.asignee_id,
			title=self.task.title,
			description=self.task.description,
			type=self.task.type,
			status=self.task.status,
			priority=self.task.priority,
			due_date=self.task.due_date
		)
        self.window.update_workpace()
        self.hide()

    def delete(self):
        self.db_handler.tasks.delete(id=self.task.id)
        self.window.update_workpace()
        self.hide()
