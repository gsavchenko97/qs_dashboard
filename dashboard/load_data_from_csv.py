from PyQt5.QtWidgets import (
    QDialog, QPushButton, QGridLayout, QLabel, QFileDialog
)
from PyQt5.QtCore import pyqtSignal
import pandas as pd

from dashboard.db import convert_csv_to_db_and_metrics
from dashboard.utils.user import DF_COLUMNS


class LoadDataWindow(QDialog):
    """
    Loading data from csv file
    """
    show_main_window = pyqtSignal(str, str, object)

    def __init__(self, username, parent=None):
        super(LoadDataWindow, self).__init__(parent)
        self.username = username
        self.filename = ""

        layout = QGridLayout()

        self.description_lbl = QLabel(
            "Choose csv-like file to download to download data from:"
        )
        layout.addWidget(self.description_lbl, 0, 0, 1, 3)

        self.choose_file_btn = QPushButton("Choose file")
        self.choose_file_btn.clicked.connect(self.choose_data_file)
        layout.addWidget(self.choose_file_btn, 1, 0, 1, 3)

        self.status_lbl = QLabel("No file chosen")
        layout.addWidget(self.status_lbl, 2, 0, 1, 3)

        self.cancel_btn = QPushButton("Ok")
        self.cancel_btn.clicked.connect(self.handle_ok)
        layout.addWidget(self.cancel_btn, 3, 0, 1, 2)

        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.handle_cancel)
        layout.addWidget(self.cancel_btn, 3, 2, 1, 1)

        self.setWindowTitle("Choose file")
        self.resize(400, 80)

        self.setLayout(layout)
        self.parent = parent

    def handle_ok(self):
        print(self.filename)

        df = pd.read_csv(self.filename, sep=",")
        metrics = df["metric"].unique()
        available_metrics = set(self.parent.AVAILABLE_METRICS)
        fail = False

        print(len(set(metrics).difference(available_metrics)))
        print(df.columns, DF_COLUMNS)

        if len(set(DF_COLUMNS).difference(set(df.columns))) > 0:
            fail = True
        elif len(set(metrics).difference(available_metrics)) > 0:
            fail = True

        if fail:
            self.status_lbl.setText(
                "PLease choose another file with acceptable values"
            )
        else:
            db, metrics = convert_csv_to_db_and_metrics(df)
            self.parent.db.db = db
            self.parent.metrics = metrics
            self.show_main_window.emit(self.username, "add_data", self)

    def handle_cancel(self):
        self.show_main_window.emit(self.username, "add_data", self)

    def choose_data_file(self):
        filename, _ = QFileDialog.getOpenFileName(
            None,
            caption="Open file",
            directory="",
            filter="(*.csv *.tsv)",
        )
        self.filename = filename
        self.status_lbl.setText(filename)
