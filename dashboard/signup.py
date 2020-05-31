from PyQt5.QtWidgets import (QDialog, QPushButton, QRadioButton, QLineEdit, QGridLayout)
from PyQt5.QtCore import pyqtSignal


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
        self.line_edit_username.setFixedHeight(35)
        layout.addWidget(self.line_edit_username, 0, 0, 1, 3)

        self.line_edit_firstname = QLineEdit()
        self.line_edit_firstname.setPlaceholderText('Enter your first name')
        self.line_edit_firstname.setFixedHeight(35)
        layout.addWidget(self.line_edit_firstname, 1, 0, 1, 3)

        self.line_edit_password = QLineEdit()
        self.line_edit_password.setPlaceholderText('Enter your new password')
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
        # TODO: Create a new user with the given information
        # username = self.line_edit_username.text()
        # TODO: Check the password for the minimum requirements
        # password = self.line_edit_password.text()
        # firstname = self.line_edit_firstname.text()
        # gender = self.gender
        self.show_login_window.emit(self)

    def gender_button_state(self):
        gender_button = self.sender()
        if gender_button.isChecked():
            self.gender = gender_button.gender
