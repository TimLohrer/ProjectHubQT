import sys
from PyQt5.QtWidgets import *

from __init__ import *

class TaskContent():
    def __init__(self, title, description):
        self.title = title
        self.description = description


def main():
    app = QApplication(sys.argv)
    main_window = QMainWindow()
    
    list_widget = StatusList(None, [TaskContent("Test TItle", "Test Text")]*3)
    main_window.setCentralWidget(list_widget)

    main_window.setMinimumSize(1800, 1000)
    main_window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()