from PyQt5.QtWidgets import (
    QPushButton, QMainWindow, QWidget, QGridLayout, QTabWidget
)
from PyQt5.QtCore import pyqtSignal, QRect

from dashboard.db import DataBase

TABS_MAPPING = {
    "add_data": 2,
    "create_figure": 1,
}


class MainWindow(QMainWindow):

    switch_window = pyqtSignal()
    show_login_window = pyqtSignal(object)

    def __init__(self, username: str, tab_name: str = "add_data"):
        """
        Using the main window the user can add new data and plot a figure
        :param username: logged-in user name.
        :param tab_name: tab that must be opened.
        """
        QMainWindow.__init__(self)
        self.setWindowTitle("QS Dashboard")

        self.username = username
        self.db = DataBase(username)

        self.resize(800, 600)
        self.tabs = QTabWidget()

        self.init_add_data_tab()
        self.init_create_figure_tab()

        if tab_name not in TABS_MAPPING:
            raise ValueError(f"Invalid name of tab: '{tab_name}'")

        QTabWidget.setCurrentIndex(self.tabs, TABS_MAPPING[tab_name])
        self.setCentralWidget(self.tabs)

    def init_add_data_tab(self):
        self.add_data_tab = QWidget()
        self.tabs.addTab(self.add_data_tab, "Add Data")

        self.widget = QWidget(self.add_data_tab)

        grid_layout = QGridLayout()
        self.widget.setLayout(grid_layout)

        button = QPushButton("Grid Button")
        grid_layout.addWidget(button, 0, 0)

    def init_create_figure_tab(self):
        self.create_figure_tab = QWidget()
        self.tabs.addTab(self.create_figure_tab, "Create Figure")

        self.widget = QWidget(self.create_figure_tab)

        self.button = QPushButton("Logout", self.widget)
        self.button.setEnabled(True)
        self.button.setGeometry(QRect(10, 200, 150, 50))
        self.button.clicked.connect(self.handle_logout)

    def on_click(self):
        print('Simple Button was pushed')

    def handle_logout(self):
        self.show_login_window.emit(self)
