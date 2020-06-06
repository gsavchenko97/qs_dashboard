from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QScrollArea
from PyQt5.QtCore import Qt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


import matplotlib
matplotlib.use('Qt5Agg')


class FigureCanvas(FigureCanvasQTAgg):
    def __init__(self, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(FigureCanvas, self).__init__(fig)
        self.axes.plot([0, 1, 2, 3, 4], [10, 1, 20, 3, 40])


class CreateFigure(QWidget):
    def __init__(self):
        super(CreateFigure, self).__init__()

        hbox = QHBoxLayout(self)

        scroll, widget, vbox = QScrollArea(), QWidget(), QVBoxLayout()
        for i in range(1, 50):
            object = QLabel("TextLabel")
            vbox.addWidget(object)
        widget.setLayout(vbox)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setWidgetResizable(True)
        scroll.setWidget(widget)
        hbox.addWidget(scroll)

        sc = FigureCanvas(width=5, height=4, dpi=100)
        hbox.addWidget(sc)

        self.setGeometry(500, 500, 750, 750)
