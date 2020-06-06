from PyQt5.QtWidgets import (
    QDialog, QPushButton, QComboBox, QLineEdit, QGridLayout, QLabel
)
from PyQt5.QtCore import pyqtSignal

from dashboard.utils.user import AVAILABLE_METRICS


class MeasurementWindow(QDialog):
    """
    Add a single measurement
    """
    show_main_window = pyqtSignal(str, str, object)

    def __init__(self, parent=None):
        super(MeasurementWindow, self).__init__(parent)

        self.setWindowTitle('Sign Up')
        self.resize(400, 300)

        layout = QGridLayout()

        self.line_edit_measure_name = QLineEdit()
        self.line_edit_measure_name.setPlaceholderText('Enter measurement name')
        self.line_edit_measure_name.setMaxLength(30)
        self.line_edit_measure_name.setFixedHeight(35)
        layout.addWidget(self.line_edit_measure_name, 0, 0, 1, 3)

        self.line_edit_value = QLineEdit()
        self.line_edit_value.setPlaceholderText('Enter measurement value')
        self.line_edit_value.setMaxLength(30)
        self.line_edit_value.setFixedHeight(35)
        layout.addWidget(self.line_edit_value, 1, 0, 1, 3)

        # self.acceptabele_metrics_label = QLabel('Choose measurement metric from available:')
        # layout.addWidget(self.acceptabele_metrics_label, 2, 0, 1, 3)

        self.acceptabele_metrics = QComboBox()
        self.acceptabele_metrics.addItems(['-- choose metric --'] + sorted(AVAILABLE_METRICS))
        layout.addWidget(self.acceptabele_metrics, 2, 0, 1, 3)

        self.line_edit_day = QLineEdit()
        self.line_edit_day.setPlaceholderText('Enter measurement day')
        self.line_edit_day.setMaxLength(30)
        self.line_edit_day.setFixedHeight(35)
        layout.addWidget(self.line_edit_day, 3, 0, 1, 3)

        button_signup = QPushButton('Add measurement')
        button_signup.clicked.connect(self.handle_measurement_addition)
        layout.addWidget(button_signup, 4, 0, 1, 3)

        button_login = QPushButton('Cancel')
        button_login.clicked.connect(self.handle_cancel)
        layout.addWidget(button_login, 5, 0, 1, 3)

        self.setLayout(layout)

    def handle_cancel(self):
        self.close()

    def handle_measurement_addition(self):
        measure_name = self.line_edit_measure_name.text()
        measure_value = self.line_edit_value.text()
        metric = self.acceptabele_metrics.currentText()
        day = self.line_edit_day.text()
        firstname = self.line_edit_firstname.text()
        gender = self.gender

        messages = []
        valid_password, msg_password = check_password(password)
        if not valid_password:
            messages.append("Password:")
            messages.append(self.transform_message(msg_password))

        valid_username, msg_username = check_username(username)
        if not valid_username:
            messages.append("Username:")
            messages.append(self.transform_message(msg_username))

        valid_firstname, msg_firstname = check_firstname(firstname)
        if not valid_firstname:
            messages.append("Firstname:")
            messages.append(self.transform_message(msg_firstname))

        if gender is None:
            messages.append("Gender:")
            messages.append(self.transform_message(
                "Please choose your gender"
            ))

        create_user_flag = (
                valid_password and
                valid_firstname and
                valid_firstname and
                valid_username and
                gender is not None
        )

        if create_user_flag:
            create_new_user(
                username=username,
                password=password,
                firstname=firstname,
                gender=gender
            )
            self.show_login_window.emit(self)
        else:
            msg_box = QMessageBox()
            msg_box.setText("\n".join(messages))
            msg_box.exec_()

    def gender_button_state(self):
        gender_button = self.sender()
        if gender_button.isChecked():
            self.gender = gender_button.gender
