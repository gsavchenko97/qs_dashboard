from PyQt5.QtWidgets import QPushButton, QMainWindow, QWidget, QGridLayout
from PyQt5.QtCore import pyqtSignal, QRect


class MainWindow(QMainWindow):

    switch_window = pyqtSignal()

    def __init__(self):
        QMainWindow.__init__(self)
        # self.setWindowTitle("QS Dashboard")
        self.setWindowTitle("Draft")

        self.resize(800, 600)
        self.widget = QWidget(self)

        self.button = QPushButton("Simple Button", self.widget)
        self.button.setEnabled(True)
        self.button.setGeometry(QRect(10, 200, 150, 50))
        self.button.clicked.connect(self.on_click)

        grid_layout = QGridLayout()
        self.widget.setLayout(grid_layout)

        button = QPushButton("Grid Button")
        grid_layout.addWidget(button, 0, 0)

        self.setCentralWidget(self.widget)

    def on_click(self):
        print('Simple Button was pushed')
