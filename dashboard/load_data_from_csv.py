from PyQt5.QtWidgets import (
    QDialog, QPushButton, QRadioButton, QLineEdit, QGridLayout, QMessageBox,
    QVBoxLayout, QLabel,
    QFileDialog)
from PyQt5.QtCore import pyqtSignal

from dashboard.utils.user import (
    create_new_user,
    check_password, check_username, check_firstname
)


class LoadDataWindow(QDialog):
    """
    Loading data from csv
    """
    show_main_window = pyqtSignal(str, str, object)

    def __init__(self, username, parent=None):

        super(LoadDataWindow, self).__init__(parent)
        self.username = username

        layout = QGridLayout()

        self.description_lbl = QLabel("Choose csv-like file to download to"
                                      "download data from:")
        layout.addWidget(self.description_lbl)

        self.choose_file_btn = QPushButton("Choose file")
        self.choose_file_btn.clicked.connect(self.choose_data_file)
        layout.addWidget(self.choose_file_btn, 0, 0, 1, 3)

        self.status_lbl = QLabel("File not chosen!")
        layout.addWidget(self.description_lbl, 1, 0, 1, 3)

        self.cancel_btn = QPushButton("Ok")
        self.cancel_btn.clicked.connect(self.handle_ok())
        layout.addWidget(self.cancel_btn, 2, 0, 1, 2)

        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.handle_cancel())
        layout.addWidget(self.cancel_btn, 2, 2, 1, 1)

        self.setWindowTitle("Choose file")
        self.resize(400, 300)

        self.setLayout(layout)

    def handle_ok(self):


    def handle_cancel(self):
        self.show_main_window.emit(self.username, 'add_data', self)

    def choose_data_file(self):
        filename, _ = QFileDialog.getOpenFileName(
            None,
            caption='Open file',
            directory='',
            filter="(*.csv *.tsv)")
        self.status_lbl.setText(filename)
