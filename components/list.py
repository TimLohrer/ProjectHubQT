from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

class List(QWidget):
    def __init__(self, tasks=[]):
        """This is a standart ProjectHub visual list element.

            Args:
                task (list<Task>) (=[<empty list>])
        """
        super().__init__() # init QWidget (parent class)

        # configuring self ...
        self.setObjectName("list")

        # creating elements
        main_layout = QVBoxLayout(self)
        scroll_area = QScrollArea(self)

        container_widget = QWidget(scroll_area)
        container_layout = QVBoxLayout(container_widget)

        # configuring the elements
        main_layout.setAlignment(Qt.AlignTop)
        scroll_area.setWidgetResizable(True)
        scroll_area.setFixedWidth(350)
        container_layout.setAlignment(Qt.AlignTop)

        # adding tasks
        main_layout.addWidget(scroll_area)

        for task in tasks:
            container_layout.addWidget(task)

