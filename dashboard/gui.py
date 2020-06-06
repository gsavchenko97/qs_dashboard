from PyQt5.QtWidgets import (
    QPushButton, QMainWindow, QWidget, QGridLayout, QTabWidget,
    QFileDialog)
from PyQt5.QtCore import pyqtSignal, QRect

from dashboard.db import DataBase
from dashboard.figure import CreateFigure

TABS_MAPPING = {
    "add_data": 2,
    "create_figure": 1,
}


class MainWindow(QMainWindow):
    switch_window = pyqtSignal()
    show_login_window = pyqtSignal(object)
    show_data_loading_window = pyqtSignal(str, object)
    show_data_saving_window = pyqtSignal(str, object)
    show_measurement_adding_window = pyqtSignal(object)
    show_conv_rule_adding_window = pyqtSignal(object)

    def __init__(self, username: str, tab_name: str = "add_data"):
        """
        Using the main window the user can add new data and plot a figure
        :param username: logged-in user name.
        :param tab_name: tab that must be opened.
        """
        QMainWindow.__init__(self)
        self.setWindowTitle(f"QS Dashboard: {username}")

        self.username = username
        self.db = DataBase(username=username)

        self.resize(800, 600)
        self.tabs = QTabWidget()

        self.init_add_data_tab()

        figure = CreateFigure(self)
        self.tabs.addTab(figure, "---> Plots <---")

        if tab_name not in TABS_MAPPING:
            raise ValueError(f"Invalid name of tab: '{tab_name}'")

        QTabWidget.setCurrentIndex(self.tabs, TABS_MAPPING[tab_name])
        self.setCentralWidget(self.tabs)

    # @property
    # def db(self):
    #     return DataBase(self.username)
    #
    # @db.setter
    # def db(self, database):
    #     """If database is changed you need to update it on disk"""
    #     raise NotImplementedError()

    def init_add_data_tab(self):
        self.add_data_tab = QWidget()
        self.tabs.addTab(self.add_data_tab, "---> Data <---")

        self.widget = QWidget(self.add_data_tab)

        grid_layout = QGridLayout()

        button = QPushButton("Load Data", self.widget)
        button.setGeometry(QRect(10, 200, 150, 50))
        button.clicked.connect(self.handle_data_loading)
        grid_layout.addWidget(button, 0, 0)

        button = QPushButton("Add Measurement", self.widget)
        button.setGeometry(QRect(10, 200, 150, 50))
        button.clicked.connect(self.handle_measurement_adding)
        grid_layout.addWidget(button, 1, 0)

        button = QPushButton("Add metrics convertation rule", self.widget)
        button.setGeometry(QRect(10, 200, 150, 50))
        button.clicked.connect(self.handle_conv_rule_adding)
        grid_layout.addWidget(button, 2, 0)

        button = QPushButton("Save Data", self.widget)
        button.setGeometry(QRect(10, 200, 150, 50))
        button.clicked.connect(self.handle_data_saving)
        grid_layout.addWidget(button, 3, 0)

        button = QPushButton("Logout", self.widget)
        button.setEnabled(True)
        button.setGeometry(QRect(10, 200, 150, 50))
        button.clicked.connect(self.handle_logout)
        grid_layout.addWidget(button, 4, 0)

        self.widget.setLayout(grid_layout)

    def on_click(self):
        print('Simple Button was pushed')

    def handle_logout(self):
        self.show_login_window.emit(self)

    def handle_data_loading(self):
        print('loading data')
        self.show_data_loading_window.emit(self.username, self)

    def handle_data_saving(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Save file",
            "",
            "All Files (*);;Text Files (*.txt)", options=options
        )
        if filename:
            print('saving data to', filename)
            self.db.save_to_dataframe(filename)

    def handle_measurement_adding(self):
        print('adding measurement data')
        self.show_measurement_adding_window.emit(self)

    def handle_conv_rule_adding(self):
        self.show_conv_rule_adding_window.emit(self)
