from typing import Any

from qs_dashboard.dialog import DialogWindow
from qs_dashboard.gui import MainWindow
from qs_dashboard.login import Login
from qs_dashboard.measurement import (
    MeasurementWindow,
    MeasurementConvertRuleWindow,
)
from qs_dashboard.signup import Signup
from qs_dashboard.load_data_from_csv import LoadDataWindow


class Controller:
    """
    Allows to manage multiple windows of the application
    """

    def show_login_window(self, parent_window: Any = None):
        """
        Opens log in window and closes the parent window.
        The parent window must be closed to avoid a situation
        where two windows are opened at the same time.
        :param parent_window: window that called this method.
        """
        self.login_window = Login()
        self.login_window.show_main_window.connect(self.show_main_window)
        self.login_window.show_signup_window.connect(self.show_signup_window)
        if parent_window is not None:
            parent_window.close()
        self.login_window.show()

    def show_signup_window(self, parent_window: Any = None):
        """
        Opens sign up window and closes the parent window.
        The parent window must be closed to avoid a situation
        where two windows are opened at the same time.
        :param parent_window: window that called this method.
        """
        self.signup_window = Signup()
        self.signup_window.show_login_window.connect(self.show_login_window)
        if parent_window is not None:
            parent_window.close()
        self.signup_window.show()

    def show_dialog_window(self):
        """
        Opens dialog window.
        """
        self.dialog_window = DialogWindow()
        self.dialog_window.switch_window.connect(self.show_main_window)
        self.dialog_window.show()

    def show_main_window(
        self, username: str, tab_name: str, parent_window: Any
    ):
        """
        Opens main window and closes the parent window.
        The parent window must be closed to avoid a situation
        where two windows are opened at the same time.
        :param username: logged-in user name.
        :param tab_name: tab that must be opened,
            because the main window has multiple tabs.
        :param parent_window: window that called this method.
        """
        self.main_window = MainWindow(username=username, tab_name=tab_name)
        self.main_window.switch_window.connect(self.show_dialog_window)
        self.main_window.show_login_window.connect(self.show_login_window)
        self.main_window.show_data_loading_window.connect(
            self.show_load_data_window
        )
        self.main_window.show_measurement_adding_window.connect(
            self.show_add_measurement_window
        )
        self.main_window.show_conv_rule_adding_window.connect(
            self.show_add_conv_rules_window
        )
        parent_window.close()
        self.main_window.show()

    def show_load_data_window(self, username: str):
        """
        Opens dialog window for data loading from csv-like file
        :param username:
        :return:
        """
        self.load_data_window = LoadDataWindow(
            username=username, parent=self.main_window
        )
        self.load_data_window.show_main_window.connect(self.show_main_window)
        self.load_data_window.show()

    def show_add_measurement_window(self):
        """
        Opens dialog window for data loading from csv-like file
        """
        self.add_measurement_window = MeasurementWindow(
            parent=self.main_window
        )
        self.add_measurement_window.show_main_window.connect(
            self.show_main_window
        )
        self.add_measurement_window.show()

    def show_add_conv_rules_window(self):
        """
        Opens dialog window for data loading from csv-like file
        """
        self.add_conv_rules_window = MeasurementConvertRuleWindow(
            parent=self.main_window
        )
        self.add_conv_rules_window.show_main_window.connect(
            self.show_main_window
        )
        self.add_conv_rules_window.show()
