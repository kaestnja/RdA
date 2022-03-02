import sys

from PyQt5.QtWidgets import *


class HelloWorld(QDialog):
    def __init__(self):
        QDialog.__init__(self)

        # layout = QVBoxLayout()
        # layout = QHBoxLayout()
        layout = QGridLayout()

        self.label = QLabel("Hello World!")
        line_edit = QLineEdit()
        button = QPushButton("Close")

        layout.addWidget(self.label, 0, 0)
        layout.addWidget(line_edit, 0, 1)
        layout.addWidget(button, 1, 1)

        self.setLayout(layout)

        button.clicked.connect(self.close)
        # line_edit.textChanged.connect(label.setText)
        line_edit.textChanged.connect(self.changeTextLabel)

    def changeTextLabel(self, text):
        self.label.setText(text)


app = QApplication(sys.argv)
dialog = HelloWorld()
dialog.show()
sys.exit(app.exec_())
