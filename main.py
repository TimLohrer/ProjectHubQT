# native libaries
import sys

# all further libaries (even if not used in this file)
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

# porject inter import
from __init__ import *

def fetch_projects() -> list:
    # convert each item from database into pyhton object
    return [Project(project[1], project[2]) for project in db_handler.projects.fetch_all()]

def fetch_tasks(user_id: int, project_id: int, list_type: str) -> list:
    # convert each item from database into pyhton object
    return [Task(task[4], task[5]) for task in db_handler.tasks.fetch_condition(user_id, project_id, list_type)]

def main():
    """Mainloop of the pyqt5 based ProjectHub project-managing software"""
    # === IMPORTANT ===
    USER_ID = 1
    PROJECT_ID = 1

    # application and window built
    application = QApplication(sys.argv)
    main_window = QMainWindow()

    horizontal_layout = QHBoxLayout()
    central_widget = QWidget()

    # window conf
    main_window.resize(1800, 900)
    main_window.setWindowTitle("ProjectHub")

    # creating elements
    sidebar = Sidebar(fetch_projects())
    list_widget_0 = List(fetch_tasks(USER_ID, PROJECT_ID, list_type="BACK")) # BACK = backlog
    list_widget_1 = List(fetch_tasks(USER_ID, PROJECT_ID, list_type="TODO")) #_TODO = todo
    list_widget_2 = List(fetch_tasks(USER_ID, PROJECT_ID, list_type="INPR")) # INPR = in progress
    list_widget_3 = List(fetch_tasks(USER_ID, PROJECT_ID, list_type="DONE")) # DONE = done

    # adding elements
    main_window.setCentralWidget(central_widget)
    central_widget.setLayout(horizontal_layout)

    horizontal_layout.addWidget(sidebar)
    horizontal_layout.addWidget(list_widget_0)
    horizontal_layout.addWidget(list_widget_1)
    horizontal_layout.addWidget(list_widget_2)
    horizontal_layout.addWidget(list_widget_3)

    # display window
    main_window.show()

    # application exit ...
    sys.exit(application.exec_())

if __name__ == '__main__':
    # setup database connection and handling
    db_handler = DatabaseHandler("__database__/database.db")

    # start mainloop
    main()
