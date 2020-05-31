from PyQt5.QtWidgets import QApplication
from dashboard.controller import Controller


if __name__ == "__main__":
    app = QApplication([])
    controller = Controller()
    # controller.show_dialog_window()
    controller.show_login_window()
    app.exec_()
