from PyQt5.QtWidgets import (
    QPushButton, QMainWindow, QWidget, QGridLayout, QTabWidget
)
from PyQt5.QtCore import pyqtSignal, QRect


class MainWindow(QMainWindow):

    switch_window = pyqtSignal()

    def __init__(self, tab_num: int = 2):
        QMainWindow.__init__(self)
        self.setWindowTitle("QS Dashboard")

        self.resize(800, 600)
        self.tabs = QTabWidget()

        self.init_add_data_tab()
        self.init_create_figure_tab()

        assert 1 <= tab_num <= 2, f"Invalid number of tab: {tab_num}"
        QTabWidget.setCurrentIndex(self.tabs, tab_num)

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

        self.button = QPushButton("Simple Button", self.widget)
        self.button.setEnabled(True)
        self.button.setGeometry(QRect(10, 200, 150, 50))
        self.button.clicked.connect(self.on_click)

    def on_click(self):
        print('Simple Button was pushed')
