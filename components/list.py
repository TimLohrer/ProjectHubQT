from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

class List(QWidget):
    def __init__(self, tasks=[]):
        """This is a standart ProjectHub visual list element.

            Args:
                task (list<Task>) (=[<empty list>])
        """
        super().__init__() # init QWidget (parent class)

        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setFixedWidth(350)

        container_widget = QWidget(scroll_area)
        container_layout = QVBoxLayout(container_widget)
        container_layout.setAlignment(Qt.AlignTop)

        for task in tasks:
            container_layout.addWidget(task)

        scroll_area.setWidget(container_widget)

        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignTop)
        main_layout.addWidget(scroll_area)
