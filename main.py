# native libaries
import sys

# all further libaries (even if not used in this file)
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon, QFont
import time

# porject inter import
from __init__ import *

def fetch_projects(window: object) -> list:
    # convert each item from database into pyhton object
    return [Project(window, project, project.id == window.PROJECT_ID) for project in db_handler.projects.fetch_all()]

def fetch_tasks(window: object, status: str) -> list:
    # convert each item from database into pyhton object
    return [Task(task) for task in db_handler.tasks.fetch_by(window.PROJECT_ID, status)]

class Window(QMainWindow):
    """This is a standart ProjectHub visual window element."""
    def __init__(self):
        super().__init__()

        # variables
        self.USER_ID = 1
        self.PROJECT_ID = 1

        # configuring self ...
        self.setObjectName("window")
        self.setWindowTitle("ProjectHub")

        self.resize(1800, 900)

        # initial creation of the ui
        self.window_widget     = QWidget()
        self.vertical_layout   = QVBoxLayout()
        self.central_widget    = QWidget()
        self.horizontal_layout = QHBoxLayout()
        self.title_bar         = TitleBar(self)

        # build workspace
        self.create_workspace()

        # configuring new elements
        self.setCentralWidget(self.window_widget)
        self.vertical_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # adding: layouts
        self.window_widget.setLayout(self.vertical_layout)
        self.central_widget.setLayout(self.horizontal_layout)

        # adding: titlebar & workspace
        self.vertical_layout.addWidget(self.title_bar)
        self.vertical_layout.addWidget(self.central_widget)

        # adding: sidebar
        self.horizontal_layout.addWidget(self.sidebar)

        # adding: columns
        self.horizontal_layout.addWidget(self.list_widget_0)
        self.horizontal_layout.addWidget(self.list_widget_1)
        self.horizontal_layout.addWidget(self.list_widget_2)
        self.horizontal_layout.addWidget(self.list_widget_3)

        # styling
        self.setStyleSheet(f"margin: 0px; padding: 0px; border: 0px; outline: 0px; background-color: { Colors.background }; color: white;")

    def create_workspace(self):
        # creating / redefining elements
        self.sidebar = Sidebar(fetch_projects(self))

        self.list_widget_0 = TaskList(f"{Status.emojify(Status.BACKLOG)} {Status.stringify(Status.BACKLOG)}", fetch_tasks(self, Status.BACKLOG))
        self.list_widget_1 = TaskList(f"{Status.emojify(Status.TODO)} {Status.stringify(Status.TODO)}",       fetch_tasks(self, Status.TODO))
        self.list_widget_2 = TaskList(f"{Status.emojify(Status.IN_PROGRESS)} {Status.stringify(Status.IN_PROGRESS)}", fetch_tasks(self, Status.IN_PROGRESS))
        self.list_widget_3 = TaskList(f"{Status.emojify(Status.DONE)} {Status.stringify(Status.DONE)}",       fetch_tasks(self, Status.DONE))


    def switch_project(self, new_project):
        self.PROJECT_ID = new_project
        self.create_workspace()



def main():
    """Mainloop of the pyqt5 based ProjectHub project-managing software"""
    # application and window built
    application = QApplication(sys.argv)
    application.setWindowIcon(QIcon('assets/icon.ico'))
    application.setFont(QFont("Roboto"))
    main_window = Window()

    # create timer
    timer = QTimer()
    timer.timeout.connect(main_window.create_workspace)
    timer.start(1000)

    # display window
    main_window.show()

    # application exit ...
    sys.exit(application.exec_())

if __name__ == '__main__':
    # create db handler
    db_handler = DatabaseHandler("__database__/database.db")

    # start mainloop
    main()
