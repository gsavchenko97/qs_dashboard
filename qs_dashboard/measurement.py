from PyQt5.QtWidgets import (
    QDialog, QPushButton, QComboBox, QLineEdit, QGridLayout, QMessageBox
)
from PyQt5.QtCore import pyqtSignal

from qs_dashboard.utils import AVAILABLE_METRICS
import re


def check_matching_to_chars(sting_val: str, allowed_char: str) -> bool:
    return bool(re.match(rf"^[{allowed_char}]+$", sting_val))


class MeasurementWindow(QDialog):
    """
    Add a single measurement
    """
    show_main_window = pyqtSignal(str, str, object)

    def __init__(self, parent=None):
        super(MeasurementWindow, self).__init__(parent)

        self.setWindowTitle('Add measurement')
        self.resize(400, 300)
        self.parent = parent

        layout = QGridLayout()

        self.line_edit_measure_name = QLineEdit()
        self.line_edit_measure_name.setPlaceholderText(_(
            "Enter measurement name"
        ))
        self.line_edit_measure_name.setMaxLength(30)
        self.line_edit_measure_name.setFixedHeight(35)
        layout.addWidget(self.line_edit_measure_name, 0, 0, 1, 3)

        self.line_edit_value = QLineEdit()
        self.line_edit_value.setPlaceholderText(_("Enter measurement value"))
        self.line_edit_value.setMaxLength(30)
        self.line_edit_value.setFixedHeight(35)
        layout.addWidget(self.line_edit_value, 1, 0, 1, 3)

        self.acceptabele_metrics = QComboBox()
        self.acceptabele_metrics.addItems(
            [_("-- choose metric --")] + sorted(AVAILABLE_METRICS)
        )
        layout.addWidget(self.acceptabele_metrics, 2, 0, 1, 3)

        self.line_edit_day = QLineEdit()
        self.line_edit_day.setPlaceholderText(_("Enter measurement day"))
        self.line_edit_day.setMaxLength(3.0)
        self.line_edit_day.setFixedHeight(35)
        layout.addWidget(self.line_edit_day, 3, 0, 1, 3)

        button_signup = QPushButton(_("Add measurement"))
        button_signup.clicked.connect(self.handle_measurement_addition)
        layout.addWidget(button_signup, 4, 0, 1, 3)

        button_login = QPushButton(_("Cancel"))
        button_login.clicked.connect(self.handle_cancel)
        layout.addWidget(button_login, 5, 0, 1, 3)

        self.setLayout(layout)

    @property
    def db(self):
        return self.parent.db

    def handle_cancel(self):
        self.close()

    def handle_measurement_addition(self):
        print('before:', self.db.db, self.db.metrics)
        measure_name = self.line_edit_measure_name.text()
        measure_value = self.line_edit_value.text()
        metric = self.acceptabele_metrics.currentText()

        day = self.line_edit_day.text()

        allowed_name_chars = "A-Za-z"
        allowed_value_chars = "0-9."

        valid_name = check_matching_to_chars(
            measure_name, allowed_name_chars
        )
        valid_value = check_matching_to_chars(
            measure_value, allowed_value_chars
        )
        valid_metric = metric != _("-- choose metric --")
        valid_day = check_matching_to_chars(day, r"\d")

        valid_day = int(day) > 0 if valid_day else False
        valid_value = float(measure_value) > 0.0 if valid_value else False

        add_measurement_flags = (
            valid_name and valid_value and valid_metric and valid_day
        )

        print([key[0] for key in self.db.metrics_converter.keys()])

        should_convert, from_metric = self.db.if_metric_convertation_need(
            measure_name, metric
        )
        rule_exist = (from_metric, metric) in self.db.metrics_converter.keys()
        if should_convert and not rule_exist:
            msg_box = QMessageBox()
            msg_box.setText(
                _("Please try first to add convertation rule\nfrom %s to %s") %
                (from_metric, metric)
            )
            msg_box.exec_()
        elif add_measurement_flags:
            measure_value = float(measure_value)
            day = int(day)
            self.db.add_measurement(
                measurement_name=measure_name,
                value=measure_value,
                metric=metric,
                day=day
            )
            self.db.save_db(self.db.db_path)
            self.db.save_metrics(self.db.metrics_path)
            self.parent.update_metrics_list()
            print('after:', self.db.db, self.db.metrics)
        else:
            msg_box = QMessageBox()
            msg_box.setText(
                _("Please fill correct values for:\n"
                "days: > 0, values: > 0, measurement_names: [A-Za-z]")
            )
            msg_box.exec_()
        self.close()


class MeasurementConvertRuleWindow(QDialog):
    """
    Add metrics convertation rules
    """
    show_main_window = pyqtSignal(str, str, object)

    def __init__(self, parent=None):
        super(MeasurementConvertRuleWindow, self).__init__(parent)

        self.setWindowTitle(_("Add measurement rule"))
        self.resize(400, 150)
        self.parent = parent

        layout = QGridLayout()

        self.acceptabele_metrics_from = QComboBox()
        self.acceptabele_metrics_from.addItems(
            [_("-- choose metric --")] + sorted(AVAILABLE_METRICS)
        )
        layout.addWidget(self.acceptabele_metrics_from, 0, 0, 1, 2)

        self.acceptabele_metrics_to = QComboBox()
        self.acceptabele_metrics_to.addItems(
            [_("-- choose metric --")] + sorted(AVAILABLE_METRICS)
        )
        layout.addWidget(self.acceptabele_metrics_to, 0, 1, 1, 2)

        self.line_edit_value_from = QLineEdit()
        self.line_edit_value_from.setPlaceholderText(_("Enter value"))
        self.line_edit_value_from.setMaxLength(30.0)
        self.line_edit_value_from.setFixedHeight(35)
        layout.addWidget(self.line_edit_value_from, 1, 0, 1, 1)

        self.line_edit_value_to = QLineEdit()
        self.line_edit_value_to.setPlaceholderText(_("Enter value"))
        self.line_edit_value_to.setMaxLength(30.0)
        self.line_edit_value_to.setFixedHeight(35)
        layout.addWidget(self.line_edit_value_to, 1, 2, 1, 1)

        button_signup = QPushButton(_("Add rule"))
        button_signup.clicked.connect(self.handle_conv_rule_addition)
        layout.addWidget(button_signup, 4, 0, 1, 3)

        button_login = QPushButton(_("Cancel"))
        button_login.clicked.connect(self.handle_cancel)
        layout.addWidget(button_login, 5, 0, 1, 3)

        self.setLayout(layout)

    def handle_cancel(self):
        self.close()

    def handle_conv_rule_addition(self):
        metric_from = self.acceptabele_metrics_from.currentText()
        metric_to = self.acceptabele_metrics_to.currentText()
        value_from = self.line_edit_value_from.text()
        value_to = self.line_edit_value_to.text()

        allowed_value_chars = "0-9."

        valid_pair = metric_from != metric_to
        valid_values = check_matching_to_chars(
            value_from, allowed_value_chars
        )
        valid_values = float(value_from) > 0 if valid_values else False
        if valid_values:
            valid_values = check_matching_to_chars(
                value_to, allowed_value_chars
            )
        else:
            valid_values = False
        valid_values = float(value_to) if valid_values else False

        add_conv_rule_flags = valid_pair and valid_values

        print('before', self.db.db, self.db.metrics_converter)
        if add_conv_rule_flags:
            value_from = float(value_from)
            value_to = float(value_to)
            self.db.add_metrics_convertion(
                metric_from, metric_to, value_from, value_to
            )
            self.parent.update_metrics_list()
            print('before', self.db.db, self.db.metrics_converter)
            self.close()
            # self.show_login_window.emit(self)
        else:
            msg_box = QMessageBox()
            msg_box.setText(
                _("Please fill correct values for:\n\
                metrics: must differ\n\
                values: > 0")
            )
            msg_box.exec_()
            self.close()
