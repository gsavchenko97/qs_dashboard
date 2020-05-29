from PyQt5.QtWidgets import QApplication
import sys
sys.path.append('..')
from dashboard.controller import Controller


if __name__ == "__main__":
    app = QApplication([])
    controller = Controller()
    controller.show_dialog_window()
    app.exec_()
