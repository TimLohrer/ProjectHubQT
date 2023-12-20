from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from config.Colors import Colors

class TaskList(QWidget):
    def __init__(self, name, tasks=[]):
        """This is a standart ProjectHub visual list element.

            Args:
                task (list<Task>) (=[<empty list>])
        """
        super().__init__() # init QWidget (parent class)

        # configuring self ...
        self.setObjectName("list")

        # creating elements
        self.main_layout = QVBoxLayout(self)
        self.scroll_area = QScrollArea(self)

        self.list_title = QLabel(name + f" ({ len(tasks) })")
        self.container_widget = QWidget(self.scroll_area)
        self.container_layout = QVBoxLayout(self.container_widget)

        # configuring the elements
        self.main_layout.setAlignment(Qt.AlignTop)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFixedWidth(350)
        self.container_layout.setAlignment(Qt.AlignTop)

        # styling
        self.scroll_area.setStyleSheet(f"background-color: { Colors.second_background }; border-radius: 7.5px")
        self.list_title.setStyleSheet("font-size: 15px; font-weight: w500;")

        # adding widgets
        self.main_layout.addWidget(self.list_title)
        self.main_layout.addWidget(self.scroll_area)

        for task in tasks:
            self.container_layout.addWidget(task)

