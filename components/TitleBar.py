# inspired by https://stackoverflow.com/questions/9377914/how-to-customize-title-bar-and-window-of-desktop-application
#  and https://www.pythonguis.com/tutorials/custom-title-bar-pyqt6/

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from config.Colors import Colors

class TitleBar(QWidget):
    def __init__(self, window, title: str = "ProjectHub", enable_min = True, enable_nor = True, enable_close = True):
        super().__init__()
        self.window = window

        # configuring self ...
        self.setAutoFillBackground(True)
        self.window.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.initial_pos = None

        # creating elements
        self.horizontal_layout = QHBoxLayout()
        self.title = QLabel(title)
        # action buttons
        self.min_button = QToolButton()
        self.nor_button = QToolButton()
        self.close_button = QToolButton()

        # configuring new elements
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.min_button.setIcon(QIcon('assets/min.png'))
        self.nor_button.setIcon(QIcon('assets/nor.png'))
        self.close_button.setIcon(QIcon('assets/close.png'))

        self.min_button.clicked.connect(self.window_show_minimized)
        self.nor_button.clicked.connect(self.window_show_normilized)
        self.close_button.clicked.connect(self.window.close)


        # adding element
        self.setLayout(self.horizontal_layout)
        self.horizontal_layout.addWidget(self.title)
        if enable_min: self.horizontal_layout.addWidget(self.min_button)
        if enable_nor: self.horizontal_layout.addWidget(self.nor_button)
        if enable_close: self.horizontal_layout.addWidget(self.close_button)

        # styling
        self.setFixedHeight(45)
        self.setStyleSheet(f"background-color: { Colors.second_background }; padding: 0px; border: 4px solid { Colors.second_background }")

        self.title.setStyleSheet("font-weight: 700; font-size: 12px;")
        

    def window_show_minimized(self):
        self.window.showMinimized()

    def window_show_normilized(self):
        if self.window.isMaximized():
            self.window.showNormal()
            self.nor_button.setIcon(QIcon('assets/nor.png'))
        else:
            self.window.showMaximized()
            self.nor_button.setIcon(QIcon('assets/max.png'))

    # DON'T TOUCH: this needs to stay in camel as pyqt is trying to access QWidget.mousePressEvent
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # normalizes the window if maximised
            if self.window.isMaximized():
                self.window.showNormal()
                self.nor_button.setIcon(QIcon('assets/nor.png'))

            # sets the starting position on press
            self.start_pos = event.globalPos() - self.window.frameGeometry().topLeft()
            event.accept() # stops from preventing further events

    # DON'T TOUCH: this needs to stay in camel as pyqt is trying to access QWidget.mouseMoveEvent
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and not self.window.isMaximized():
            # moves the window to the position of the cursor
            self.window.move(event.globalPos() - self.start_pos)

            # dragged against the upper edge
            if event.globalY() <= 0:
                self.window.showMaximized()
                self.nor_button.setIcon(QIcon('assets/max.png'))

            event.accept() # stops from preventing further events
