# native libaries
import sys

# all further libaries (even if not used in this file)
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

# porject inter import
from __init__ import *

def main():
    """Mainloop of the pyqt5 based ProjectHub project-managing software"""

    # application and window built
    application = QApplication(sys.argv)
    main_window = QMainWindow()

    central_widget  = QWidget()
    horizontal_layout = QHBoxLayout()

    # window conf
    main_window.resize(1170, 690)
    main_window.setWindowTitle("ProjectHub")

    # creating elements
    sidebar = Sidebar()
    list_widget_0 = List()
    list_widget_1 = List()
    list_widget_2 = List()

    # adding elements
    main_window.setCentralWidget(central_widget)
    central_widget.setLayout(horizontal_layout)

    horizontal_layout.addWidget(sidebar)
    horizontal_layout.addWidget(list_widget_0)
    horizontal_layout.addWidget(list_widget_1)
    horizontal_layout.addWidget(list_widget_2)

    # display window
    main_window.show()

    # application exit ...
    sys.exit(application.exec_())

if __name__ == '__main__':
    main()
