from PyQt5.QtWidgets import QWidget, QPushButton
from PyQt5.QtCore import QRect


class Figure(QWidget):
    def __init__(self):
        super(Figure, self).__init__()
        self.button = QPushButton("Logout", self)
        self.button.setEnabled(True)
        self.button.setGeometry(QRect(10, 200, 150, 50))
