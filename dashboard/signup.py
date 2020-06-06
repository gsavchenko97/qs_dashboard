from PyQt5.QtWidgets import (
    QDialog, QPushButton, QRadioButton, QLineEdit, QGridLayout, QMessageBox
)
from PyQt5.QtCore import pyqtSignal

from dashboard.utils.user import (
    create_new_user,
    check_password, check_username, check_firstname,
    MAX_PASSWORD_LENGTH, MAX_USERNAME_LENGTH, MAX_FIRSTNAME_LENGTH
)


class Signup(QDialog):
    """
    Sign Up form
    """
    show_login_window = pyqtSignal(object)

    def __init__(self, parent=None):
        super(Signup, self).__init__(parent)

        self.gender = None

        self.setWindowTitle('Sign Up')
        self.resize(400, 300)

        layout = QGridLayout()

        self.line_edit_username = QLineEdit()
        self.line_edit_username.setPlaceholderText('Enter your username')
        self.line_edit_username.setMaxLength(MAX_USERNAME_LENGTH)
        self.line_edit_username.setFixedHeight(35)
        layout.addWidget(self.line_edit_username, 0, 0, 1, 3)

        self.line_edit_firstname = QLineEdit()
        self.line_edit_firstname.setPlaceholderText('Enter your first name')
        self.line_edit_firstname.setMaxLength(MAX_FIRSTNAME_LENGTH)
        self.line_edit_firstname.setFixedHeight(35)
        layout.addWidget(self.line_edit_firstname, 1, 0, 1, 3)

        self.line_edit_password = QLineEdit()
        self.line_edit_password.setPlaceholderText('Enter your new password')
        self.line_edit_password.setMaxLength(MAX_PASSWORD_LENGTH)
        self.line_edit_password.setFixedHeight(35)
        layout.addWidget(self.line_edit_password, 2, 0, 1, 3)

        self.male_button = QRadioButton("Male")
        self.male_button.gender = "Male"
        self.male_button.toggled.connect(lambda: self.gender_button_state())
        layout.addWidget(self.male_button, 3, 0, 1, 1)

        self.female_button = QRadioButton("Female")
        self.female_button.gender = "Female"
        self.female_button.toggled.connect(lambda: self.gender_button_state())
        layout.addWidget(self.female_button, 3, 1, 1, 1)

        button_signup = QPushButton('Sign Up')
        button_signup.clicked.connect(self.handle_signup)
        layout.addWidget(button_signup, 4, 0, 1, 3)

        button_login = QPushButton('Log In to Existing Account')
        button_login.clicked.connect(self.handle_login)
        layout.addWidget(button_login, 5, 0, 1, 3)

        self.setLayout(layout)

    def handle_login(self):
        self.show_login_window.emit(self)

    def handle_signup(self):
        username = self.line_edit_username.text()
        password = self.line_edit_password.text()
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

        msg_box = QMessageBox()
        msg_box.setText("\n".join(messages))
        msg_box.exec_()

        if valid_password and valid_firstname and valid_firstname and valid_username and gender is not None:
            create_new_user(
                username=username,
                password=password,
                firstname=firstname,
                gender=gender
            )

        self.show_login_window.emit(self)

    @staticmethod
    def transform_message(msg: str) -> str:
        return "\n".join("        " + m for m in msg.split("\n"))

    def gender_button_state(self):
        gender_button = self.sender()
        if gender_button.isChecked():
            self.gender = gender_button.gender
