from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from config.Colors import Colors
from components.TitleBar import TitleBar
from config.Status import Status
from config.Type import Type
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

        # creating elements
        self.main_layout = QVBoxLayout()
        self.title_bar = TitleBar(self, "", False, False)

        self.type_selector = QComboBox(self)
        self.type_selector.addItem('Task')
        self.type_selector.addItem('Problem')
        self.type_selector.addItem('Initiative')

        self.title_label = QLabel(task.title)
        self.description_label = QLabel(task.description)

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

        # configuring the elements
        self.main_layout.setAlignment(Qt.AlignTop)
        self.type_selector.setCurrentText(Type().beautify(task.type))
        self.status_selector.setCurrentText(Status().beautify(task.status))
        self.priority_selector.setCurrentText(Priority().beautify(task.priority))

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

            QComboBox::down-arrow {
                visibility: hidden;
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
        self.title_label.setStyleSheet("font-size: 25px; font-weight: w600;")
        self.description_label.setStyleSheet(f"padding: 5px; border-radius: 5px; font-size: 15px; background-color: { Colors.second_background };")

        # adding elements
        self.setLayout(self.main_layout)
        self.main_layout.addWidget(self.title_bar)
        self.main_layout.addWidget(self.title_label)
        self.main_layout.addWidget(self.description_label)
        self.main_layout.addWidget(self.type_selector)
        self.main_layout.addWidget(self.status_selector)
        self.main_layout.addWidget(self.priority_selector)
