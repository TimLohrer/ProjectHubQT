# native libaries
import sys

# all further libaries (even if not used in this file)
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

# porject inter import
from __init__ import *

def fetch_projects(active_project_id) -> list:
    # convert each item from database into pyhton object
    return [Project(project, project.id == active_project_id) for project in db_handler.projects.fetch_all()]

def fetch_tasks(user_id: int, project_id: int, status: str) -> list:
    # convert each item from database into pyhton object
    return [Task(task) for task in db_handler.tasks.fetch_condition(user_id, project_id, status)]

class Window(QMainWindow):
    """This is a standart ProjectHub visual window element."""
    def __init__(self):
        super().__init__()
        # === TEMP === (subject of change)
        USER_ID = 1
        PROJECT_ID = 1

        # configuring self ...
        self.setObjectName("window")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        self.resize(1800, 900)

        # creating elements
        self.window_widget     = QWidget()
        self.vertical_layout   = QVBoxLayout()
        self.central_widget    = QWidget()
        self.horizontal_layout = QHBoxLayout()

        self.title_bar = TitleBar(self)
        self.sidebar = Sidebar(fetch_projects(PROJECT_ID))
        self.list_widget_0 = TaskList("BACKLOG", fetch_tasks(USER_ID, PROJECT_ID, status=Status.BACKLOG))
        self.list_widget_1 = TaskList("TODO",    fetch_tasks(USER_ID, PROJECT_ID, status=Status.TODO))
        self.list_widget_2 = TaskList("IN PROGRESS", fetch_tasks(USER_ID, PROJECT_ID, status=Status.IN_PROGRESS))
        self.list_widget_3 = TaskList("DONE",    fetch_tasks(USER_ID, PROJECT_ID, status=Status.DONE))

        # configuring new elements
        self.vertical_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # adding elements
        self.setCentralWidget(self.window_widget)
        self.window_widget.setLayout(self.vertical_layout)
        self.central_widget.setLayout(self.horizontal_layout)

        # adding: titlebar and workspace
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

def main():
    """Mainloop of the pyqt5 based ProjectHub project-managing software"""
    # application and window built
    application = QApplication(sys.argv)
    application.setWindowIcon(QIcon('assets/icon.ico'))
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
