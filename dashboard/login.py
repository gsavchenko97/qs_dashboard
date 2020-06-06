from PyQt5.QtWidgets import (
    QDialog, QPushButton, QLineEdit, QGridLayout, QMessageBox
)
from PyQt5.QtCore import pyqtSignal

from dashboard.utils.user import (
    match_username_password, MAX_PASSWORD_LENGTH, MAX_USERNAME_LENGTH
)


class Login(QDialog):
    """
    Log In form
    """
    show_main_window = pyqtSignal(str, str, object)
    show_signup_window = pyqtSignal(object)

    def __init__(self, parent=None):
        super(Login, self).__init__(parent)
        self.setWindowTitle('Log In')
        self.resize(400, 200)

        layout = QGridLayout()

        self.line_edit_username = QLineEdit()
        self.line_edit_username.setPlaceholderText('Username')
        self.line_edit_username.setMaxLength(MAX_USERNAME_LENGTH)
        self.line_edit_username.setFixedHeight(35)
        layout.addWidget(self.line_edit_username, 0, 0, 1, 3)

        self.line_edit_password = QLineEdit()
        self.line_edit_password.setPlaceholderText('Password')
        self.line_edit_password.setMaxLength(MAX_PASSWORD_LENGTH)
        self.line_edit_password.setFixedHeight(35)
        layout.addWidget(self.line_edit_password, 1, 0, 1, 3)

        button_login = QPushButton('Log In')
        button_login.clicked.connect(self.handle_login)
        layout.addWidget(button_login, 2, 0, 1, 1)

        button_signup = QPushButton('Sign Up')
        button_signup.clicked.connect(self.handle_signup)
        layout.addWidget(button_signup, 2, 1, 1, 1)

        button_signup = QPushButton('Exit')
        button_signup.clicked.connect(self.handle_exit)
        layout.addWidget(button_signup, 2, 2, 1, 1)

        self.setLayout(layout)

    def handle_login(self):
        username = self.line_edit_username.text()
        password = self.line_edit_password.text()

        def fake_check():
            return username == '' and password == ''
        # if fake_check():
        if match_username_password(username, password) or fake_check():
            self.show_main_window.emit(username, "add_data", self)
        else:
            msg = QMessageBox()
            msg.setText("Incorrect Username or Password")
            msg.exec_()

    def handle_signup(self):
        self.show_signup_window.emit(self)

    def handle_exit(self):
        self.close()
