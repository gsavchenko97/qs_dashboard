from dashboard.dialog import DialogWindow
from dashboard.gui import MainWindow


class Controller:
    """
    Allows to manage multiple windows of the application
    """
    def show_dialog_window(self):
        self.dialog_window = DialogWindow()
        self.dialog_window.switch_window.connect(self.show_main_window)
        self.dialog_window.show()

    def show_main_window(self, tab_num: int):
        self.main_window = MainWindow(tab_num)
        self.main_window.switch_window.connect(self.show_dialog_window)
        self.dialog_window.close()
        self.main_window.show()
