from PyQt5.QtWidgets import (QDialog, QPushButton, QLineEdit, QGridLayout, QMessageBox)
from PyQt5.QtCore import pyqtSignal


class Login(QDialog):
    """
    Log In form
    """
    show_main_window = pyqtSignal(str, object)
    show_signup_window = pyqtSignal(object)

    def __init__(self, parent=None):
        super(Login, self).__init__(parent)
        self.setWindowTitle('Log In')
        self.resize(400, 200)

        layout = QGridLayout()

        self.line_edit_username = QLineEdit()
        self.line_edit_username.setPlaceholderText('Username')
        self.line_edit_username.setFixedHeight(35)
        layout.addWidget(self.line_edit_username, 0, 0, 1, 2)

        self.line_edit_password = QLineEdit()
        self.line_edit_password.setPlaceholderText('Password')
        self.line_edit_password.setFixedHeight(35)
        layout.addWidget(self.line_edit_password, 1, 0, 1, 2)

        button_login = QPushButton('Log In')
        button_login.clicked.connect(self.handle_login)
        layout.addWidget(button_login, 2, 0, 1, 1)

        button_signup = QPushButton('Sign Up')
        button_signup.clicked.connect(self.handle_signup)
        layout.addWidget(button_signup, 2, 1, 1, 1)

        self.setLayout(layout)

    def handle_login(self):
        msg = QMessageBox()

        def fake_check():
            return self.line_edit_username.text() == '' and self.line_edit_password.text() == ''

        if fake_check():
            self.show_main_window.emit("add_data", self)
        else:
            msg.setText("Incorrect Username or Password")
            msg.exec_()

    def handle_signup(self):
        self.show_signup_window.emit(self)
