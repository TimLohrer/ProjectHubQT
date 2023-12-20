from PyQt5.QtWidgets import *

class EditableLabel(QWidget):
    def __init__(self, content=''):
        """This is a standart ProjectHub visual label element.

			Args: content
		"""
        super().__init__() # init QWidget (parent class)

        # configuring self
        self.edit_mode = False

        # creating elements
        self.label = QLabel(content)
        self.edit_line = QLineEdit()
        self.save_button = QPushButton('Save')
        self.save_button.clicked.connect(self.save_text)
        self.edit_line.hide()
        self.save_button.hide()

        # configuring elements
        self.label.mousePressEvent = self.toggle_edit_mode

        # adding elements
        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.edit_line)
        layout.addWidget(self.save_button)

    def toggle_edit_mode(self, event=None):
        self.edit_mode = not self.edit_mode

        if self.edit_mode:
            self.edit_line.setText(self.label.text())
            self.label.hide()
            self.edit_line.show()
            self.save_button.show()
        else:
            self.label.setText(self.edit_line.text())
            self.label.show()
            self.edit_line.hide()
            self.save_button.hide()

    def save_text(self):
        self.toggle_edit_mode()

    def get_text(self):
        return self.label.text()

    def set_text(self, text):
        self.label.setText(text)
        self.edit_line.setText(text)