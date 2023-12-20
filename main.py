# native libaries
import sys

# all further libaries (even if not used in this file)
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFont

# porject inter import
from __init__ import *

def fetch_projects(active_project_id) -> list:
    # convert each item from database into pyhton object
    return [Project(project, project.id == active_project_id) for project in db_handler.projects.fetch_all()]

def fetch_tasks(project_id: int, status: str) -> list:
    # convert each item from database into pyhton object
    return [Task(task) for task in db_handler.tasks.fetch_condition(project_id, status)]

class Window(QMainWindow):
    """This is a standart ProjectHub visual window element."""
    def __init__(self):
        super().__init__()
        # !!! === TEMP === (subject of change)
        self.USER_ID = 1
        self.PROJECT_ID = 1

        # configuring self ...
        self.setObjectName("window")
        self.setWindowTitle("ProjectHub")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        self.resize(1800, 900)

        self.create_ui()

        # styling
        self.setStyleSheet(f"margin: 0px; padding: 0px; border: 0px; outline: 0px; background-color: { Colors.background }; color: white;")

    def create_ui(self):
        # creating elements
        window_widget     = QWidget()
        vertical_layout   = QVBoxLayout()
        central_widget    = QWidget()
        horizontal_layout = QHBoxLayout()
        title_bar         = TitleBar(self)
        sidebar           = Sidebar(fetch_projects(self.PROJECT_ID), self.create_ui, self.switch_project)
        list_widget_0     = TaskList(Status().stringify("BACKLOG").upper(),     fetch_tasks(project_id=self.PROJECT_ID, status=Status.BACKLOG))
        list_widget_1     = TaskList(Status().stringify("TODO").upper(),        fetch_tasks(project_id=self.PROJECT_ID, status=Status.TODO))
        list_widget_2     = TaskList(Status().stringify("IN_PROGRESS").upper(), fetch_tasks(project_id=self.PROJECT_ID, status=Status.IN_PROGRESS))
        list_widget_3     = TaskList(Status().stringify("DONE").upper(),        fetch_tasks(project_id=self.PROJECT_ID, status=Status.DONE))

        # configuring new elements
        vertical_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # adding: sidebar
        horizontal_layout.addWidget(sidebar)

        # adding: columns
        horizontal_layout.addWidget(list_widget_0)
        horizontal_layout.addWidget(list_widget_1)
        horizontal_layout.addWidget(list_widget_2)
        horizontal_layout.addWidget(list_widget_3)

        # adding elements
        window_widget.setLayout(vertical_layout)
        central_widget.setLayout(horizontal_layout)

        # adding: titlebar & workspace
        vertical_layout.addWidget(title_bar)
        vertical_layout.addWidget(central_widget)

        # saving and updating ui
        self.setCentralWidget(window_widget)
        self.vertical_layout   = vertical_layout
        self.central_widget    = central_widget
        self.horizontal_layout = horizontal_layout

    def switch_project(self, new_project):
        # !!! check if exists
        self.PROJECT_ID = new_project
        self.create_ui()

def main():
    """Mainloop of the pyqt5 based ProjectHub project-managing software"""
    # application and window built
    application = QApplication(sys.argv)
    application.setWindowIcon(QIcon('assets/icon.ico'))
    application.setFont(QFont("Roboto"))
    main_window = Window()

    # display window
    main_window.show()

    # application exit ...
    sys.exit(application.exec_())

if __name__ == '__main__':
    # setup database connection and handling
    db_handler = DatabaseHandler("__database__/database.db")

    # start mainloop
    main()
