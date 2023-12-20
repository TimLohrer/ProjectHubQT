from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from copy import copy

from config.Colors import Colors
from components.TitleBar import TitleBar
from config.Type import Type
from config.Status import Status
from config.Priority import Priority
from database.handler import DatabaseHandler

class TaskDetails(QWidget):
    def __init__(self, task):
        """This is a standart ProjectHub visual task element.

			Args:
		"""
        super().__init__() # init QWidget (parent class)

        self.db_hander = DatabaseHandler("__database__/database.db")

        # configuring self ...
        self.setFixedSize(800, 800)
        self.original_task = copy(task)
        self.task = copy(task)
        self.show_save_button = False

        # creating elements
        self.main_layout = QVBoxLayout()
        self.title_bar = TitleBar(self, f"Edit Task", False, False)

        self.type_selector = QComboBox(self)
        self.type_selector.addItem('Task')
        self.type_selector.addItem('Problem')
        self.type_selector.addItem('Initiative')

        self.title_label = QLineEdit(task.title)
        self.description_text = QTextEdit(task.description)

        self.status_selector = QComboBox(self)
        self.status_selector.addItem('Backlog')
        self.status_selector.addItem('ToDo')
        self.status_selector.addItem('In Progress')
        self.status_selector.addItem('Done')

        self.priority_selector = QComboBox(self)
        self.priority_selector.addItem('Very High')
        self.priority_selector.addItem('High')
        self.priority_selector.addItem('Medium')
        self.priority_selector.addItem('Low')
        self.priority_selector.addItem('Very Low')

        self.save_button = QPushButton("Save")

        # configuring the elements
        self.main_layout.setAlignment(Qt.AlignTop)
        self.title_label.textChanged.connect(self.title_changed)
        self.title_label.setPlaceholderText("Enter a title...")
        self.description_text.setAlignment(Qt.AlignTop)
        self.description_text.setLineWrapMode(QTextEdit.WidgetWidth)
        self.description_text.setPlaceholderText("Enter a description...")
        self.description_text.textChanged.connect(self.description_changed)
        self.type_selector.setCurrentText(Type().stringify(task.type))
        self.type_selector.currentIndexChanged.connect(self.update_type)
        self.status_selector.setCurrentText(Status().stringify(task.status))
        self.status_selector.currentIndexChanged.connect(self.update_status)
        self.priority_selector.setCurrentText(Priority().stringify(task.priority))
        self.priority_selector.currentIndexChanged.connect(self.update_priority)

        # styling
        self.setStyleSheet(f"background-color: { Colors.background }; color: white;")
        dropdown_css = """
            QComboBox {
                background-color: {{ second-background }};
                border-radius: 5px;
                padding: 5px;
                min-width: 3em;
                width: 20px;
            }

            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
            }

            QComboBox QAbstractItemView {
                background-color: {{ second-background }};
                selection-background-color: {{ second-background }};
                selection-color: {{ blue }};
                width: 20px;
                height: 30px;
            }
        """
        dropdown_css = dropdown_css.replace("{{ background }}", Colors.background).replace("{{ second-background }}", Colors.second_background).replace("{{ blue }}", Colors.blue)
        self.type_selector.setStyleSheet(dropdown_css)
        self.status_selector.setStyleSheet(dropdown_css)
        self.priority_selector.setStyleSheet(dropdown_css)
        self.title_label.setStyleSheet("font-size: 25px; font-weight: w600; border: 0px")
        self.description_text.setStyleSheet(f"padding: 5px; border-radius: 5px; font-size: 14px; background-color: { Colors.second_background };")
        self.description_text.setFixedHeight(100)
        self.save_button.setStyleSheet(f"background-color: { Colors.green }; color: { Colors.background }; font-weight: bold; border-radius: 5px; padding: 10px;")
        self.save_button.setFixedHeight(50)
        self.save_button.hide()

        # adding elements
        self.setLayout(self.main_layout)
        self.main_layout.addWidget(self.title_bar)
        self.main_layout.addWidget(self.title_label)
        self.main_layout.addWidget(self.description_text)
        self.main_layout.addWidget(self.type_selector)
        self.main_layout.addWidget(self.status_selector)
        self.main_layout.addWidget(self.priority_selector)
        self.main_layout.addWidget(self.save_button)

    def title_changed(self, new_title):
        self.task.title = new_title
        self.check_save_button_visibility()

    def description_changed(self):
        self.task.description = self.description_text.toPlainText()
        self.check_save_button_visibility()

    def update_type(self):
        self.task.type = Type().parse(self.type_selector.currentText())
        self.check_save_button_visibility()

    def update_status(self):
        self.task.status = Status().parse(self.status_selector.currentText())
        self.check_save_button_visibility()

    def update_priority(self):
        self.task.priority = Priority().parse(self.priority_selector.currentText())
        self.check_save_button_visibility()

    def check_save_button_visibility(self):
        hide = (self.task.title == self.original_task.title and self.task.title != "") and (self.task.description == self.original_task.description) and (self.task.type == self.original_task.type) and (self.task.status == self.original_task.status) and (self.task.priority == self.original_task.priority) and (self.task.asignee_id == self.original_task.asignee_id)
        if not hide:
            self.save_button.show()
        else:
            self.save_button.hide()