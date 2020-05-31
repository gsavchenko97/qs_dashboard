from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QDialog
from PyQt5.QtCore import pyqtSignal


class DialogWindow(QDialog):
    """
    Creates a dialog box in order to ask the user what he wants to do
        1. Add new data
        2. Create a new figure based on already added data
    """

    switch_window = pyqtSignal(str, object)

    def __init__(self, parent=None):
        super(DialogWindow, self).__init__(parent)
        self.resize(300, 100)

        layout = QVBoxLayout()

        self.add_data_button = QPushButton("Add Data")
        self.add_data_button.clicked.connect(self.add_data)
        layout.addWidget(self.add_data_button)

        self.create_fig_button = QPushButton("Create Figure")
        self.create_fig_button.clicked.connect(self.create_figure)
        layout.addWidget(self.create_fig_button)

        self.exit_button = QPushButton("Exit")
        self.exit_button.clicked.connect(self.exit_clicked)
        layout.addWidget(self.exit_button)

        self.setLayout(layout)

    def add_data(self):
        self.switch_window.emit("add_data", self)

    def create_figure(self):
        self.switch_window.emit("create_figure", self)

    def exit_clicked(self):
        self.close()
