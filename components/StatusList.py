from PyQt5.QtWidgets import *
from components.Task import Task

class StatusList(QWidget):
    def __init__(self, parent=None, tasks=[]):
        super().__init__(parent)

        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)

        container_widget = QWidget(scroll_area)
        container_layout = QVBoxLayout(container_widget)

        for task in tasks:
            rounded_box = Task(task.title, task.description)
            container_layout.addWidget(rounded_box)

        scroll_area.setWidget(container_widget)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll_area)