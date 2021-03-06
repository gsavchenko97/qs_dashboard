from PyQt5.QtWidgets import QApplication
from .controller import Controller


def main():
    app = QApplication([])
    controller = Controller()
    controller.show_login_window()
    app.exec_()


if __name__ == "__main__":
    main()
