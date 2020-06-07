from PyQt5.QtWidgets import (
    QPushButton, QMainWindow, QWidget, QGridLayout, QTabWidget,
    QFileDialog, QHBoxLayout, QVBoxLayout, QListWidget, QListWidgetItem)
from PyQt5.QtCore import pyqtSignal, QRect

from qs_dashboard.db import DataBase
from qs_dashboard.figure import CreateFigure


TABNAME2IDX = {
    "add_data": 0,
    "create_figure": 1,
}
IDX2TABNAME = {idx: name for name, idx in TABNAME2IDX.items()}


class MainWindow(QMainWindow):
    """
    MainWindow class. It stores database.
    """
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
        self.setWindowTitle(_("QS Dashboard") + f": {username}")

        self.username = username
        self.db = DataBase(username=username)
        print(self.db.DB_FOLDER)

        self.resize(800, 600)
        self.tabs = QTabWidget()
        self.tabs.currentChanged.connect(self.tab_click)
        self.init_add_data_tab()

        self.figure = CreateFigure(self)
        self.tabs.addTab(self.figure, _("---> Plots <---"))

        if tab_name not in TABNAME2IDX:
            raise ValueError(f"Invalid name of tab: '{tab_name}'")

        QTabWidget.setCurrentIndex(self.tabs, TABNAME2IDX[tab_name])
        self.setCentralWidget(self.tabs)

    def tab_click(self, i: int):
        if IDX2TABNAME[i] == "create_figure":
            self.figure.update_list()

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
        self.tabs.addTab(self.add_data_tab, _("---> Data <---"))

        # self.widget = QWidget(self.add_data_tab)

        self.hbox = QHBoxLayout(self.add_data_tab)

        lwidget, lvbox = QWidget(), QVBoxLayout()
        self.list_widget = QListWidget()
        self.list_widget_conv_rules = QListWidget()
        self.update_metrics_list()
        lvbox.addWidget(self.list_widget)
        lvbox.addWidget(self.list_widget_conv_rules)

        lwidget.setLayout(lvbox)
        self.hbox.addWidget(lwidget)

        rwidget, grid_layout = QWidget(), QGridLayout()
        button = QPushButton(_("Load Data"))
        button.setGeometry(QRect(10, 200, 150, 50))
        button.clicked.connect(self.handle_data_loading)
        grid_layout.addWidget(button, 0, 0)

        button = QPushButton(_("Add Measurement"))
        button.setGeometry(QRect(10, 200, 150, 50))
        button.clicked.connect(self.handle_measurement_adding)
        grid_layout.addWidget(button, 1, 0)

        button = QPushButton(_("Add metrics convertation rule"))
        button.setGeometry(QRect(10, 200, 150, 50))
        button.clicked.connect(self.handle_conv_rule_adding)
        grid_layout.addWidget(button, 2, 0)

        button = QPushButton(_("Save Data"))
        button.setGeometry(QRect(10, 200, 150, 50))
        button.clicked.connect(self.handle_data_saving)
        grid_layout.addWidget(button, 3, 0)

        button = QPushButton(_("Logout"))
        button.setEnabled(True)
        button.setGeometry(QRect(10, 200, 150, 50))
        button.clicked.connect(self.handle_logout)
        grid_layout.addWidget(button, 4, 0)

        rwidget.setLayout(grid_layout)
        self.hbox.addWidget(rwidget)

    @property
    def user_df(self):
        return self.db.to_dataframe()

    def update_metrics_list(self):
        self.list_widget.clear()
        self.list_widget_conv_rules.clear()
        df = self.user_df
        if "measurement_name" in df.columns:
            metrics = (
                    [_("Added measurements:")] +
                    list(df.measurement_name.unique())
            )
            for metric in metrics:
                QListWidgetItem(metric, self.list_widget)
        converter_rules = self.db.metrics_converter
        QListWidgetItem(
            _("Added convertation rules:"),
            self.list_widget_conv_rules
        )
        for (from_metric, to_metric), val in converter_rules.items():
            QListWidgetItem(
                f'{from_metric} / {to_metric} = {round(val, 5)}',
                self.list_widget_conv_rules
            )

    @staticmethod
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
        filename, trash = QFileDialog.getSaveFileName(
            self,
            _("Save file"),
            "",
            _("All Files (*);;Text Files (*.txt)"), options=options
        )
        if filename:
            print('saving data to', filename)
            self.db.save_to_dataframe(filename)

    def handle_measurement_adding(self):
        print('adding measurement data')
        self.show_measurement_adding_window.emit(self)

    def handle_conv_rule_adding(self):
        self.show_conv_rule_adding_window.emit(self)
