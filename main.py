# native libaries
import sys
import time

# all further libaries (even if not used in this file)
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon, QFont

# porject inter import
from __init__ import *

def fetch_projects(window: object) -> list:
    # convert each item from database into pyhton object
    return [Project(window, project, project.id == window.PROJECT_ID) for project in db_handler.projects.fetch()]

def fetch_tasks(window: object, status: str) -> list:
    # convert each item from database into pyhton object
    return [Task(task, window) for task in db_handler.tasks.fetch(project_id=window.PROJECT_ID, status=status)]

class Window(QMainWindow):
    """This is a standart ProjectHub visual window element."""
    def __init__(self):
        super().__init__()
        self.db_handler = DatabaseHandler("__database__/database.db")

        # variables
        self.USER_ID = 1
        self.PROJECT_ID = 1
        self.LAST_UPDATE = time.time()

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

        # configuring new elements
        self.setCentralWidget(self.window_widget)
        self.vertical_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # adding: layouts
        self.window_widget.setLayout(self.vertical_layout)
        self.central_widget.setLayout(self.horizontal_layout)

        # adding: titlebar & workspace
        self.vertical_layout.addWidget(self.title_bar)
        self.vertical_layout.addWidget(self.central_widget)

        # creating and adding elements of the actual workspace
        self.create_workspace()

        # styling
        self.setStyleSheet(f"margin: 0px; padding: 0px; border: 0px; outline: 0px; background-color: { Colors.background }; color: white;")

        # timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.__handle_updates)
        self.timer.start(1000)

    def __handle_updates(self):
        update = self.db_handler.check_update(self.LAST_UPDATE)

        if update[0]:
            print("Recived remote update request. Updating UI now...")
            self.update_workpace()
            self.LAST_UPDATE = update[1]

    def create_workspace(self):
        # workspace: sidebar
        self.sidebar = Sidebar(self, fetch_projects(self))

        # workspace: lists
        self.list_widget_0 = TaskList(f"{ Status.emojify(Status.BACKLOG) } { Status.stringify(Status.BACKLOG) }", fetch_tasks(self, Status.BACKLOG))
        self.list_widget_1 = TaskList(f"{ Status.emojify(Status.TODO) } { Status.stringify(Status.TODO) }",       fetch_tasks(self, Status.TODO))
        self.list_widget_2 = TaskList(f"{ Status.emojify(Status.IN_PROGRESS) } { Status.stringify(Status.IN_PROGRESS) }", fetch_tasks(self, Status.IN_PROGRESS))
        self.list_widget_3 = TaskList(f"{ Status.emojify(Status.DONE) } { Status.stringify(Status.DONE) }",       fetch_tasks(self, Status.DONE))

        # adding: sidebar
        self.horizontal_layout.addWidget(self.sidebar)

        # adding: columns
        self.horizontal_layout.addWidget(self.list_widget_0)
        self.horizontal_layout.addWidget(self.list_widget_1)
        self.horizontal_layout.addWidget(self.list_widget_2)
        self.horizontal_layout.addWidget(self.list_widget_3)

    def update_workpace(self):
        # removing widgets workspace: sidebar
        self.horizontal_layout.removeWidget(self.sidebar)

        # removing widgets workspace: lists
        self.horizontal_layout.removeWidget(self.list_widget_0)
        self.horizontal_layout.removeWidget(self.list_widget_1)
        self.horizontal_layout.removeWidget(self.list_widget_2)
        self.horizontal_layout.removeWidget(self.list_widget_3)

        # creating and adding elements of new workspace
        self.create_workspace()

    def switch_project(self, new_project):
        self.PROJECT_ID = new_project
        self.update_workpace()

    def switch_user(self, new_user):
        self.USER_ID = new_user
        self.update_workpace()



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
    # create db handler
    db_handler = DatabaseHandler("__database__/database.db")

    # start mainloop
    main()
