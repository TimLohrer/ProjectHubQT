from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

class Sidebar(QFrame):
  def __init__(self, parent=None):
    super().__init__(parent)

    self.setObjectName("sidebar")
    self.setFixedWidth(150)

    title_label = QLabel("ProjectHub")

    layout = QVBoxLayout(self)
    layout.setAlignment(Qt.AlignTop)
    layout.addWidget(title_label)