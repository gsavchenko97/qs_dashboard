from typing import Any, List

from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QListWidget, QListWidgetItem
)

from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg, NavigationToolbar2QT
)
from matplotlib.figure import Figure
import matplotlib
matplotlib.use('Qt5Agg')


class FigureCanvas(FigureCanvasQTAgg):
    def __init__(self, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(FigureCanvas, self).__init__(fig)
        # self.axes.plot([0, 1, 2, 3, 4], [10, 1, 20, 3, 40])

    def update_plot(self, x_values: List, y_values: List, title: str):
        self.axes.cla()
        self.axes.plot(x_values, y_values, "r")
        self.axes.set_title(title)
        self.draw()


class CreateFigure(QWidget):
    def __init__(self, parent: Any):
        super(CreateFigure, self).__init__()
        self.parent = parent
        self.hbox = QHBoxLayout(self)

        lwidget, lvbox = QWidget(), QVBoxLayout()

        self.list_widget = QListWidget()
        self.update_list()
        self.list_widget.itemClicked.connect(self.plot_figure_clicked)

        lvbox.addWidget(self.list_widget)
        lwidget.setLayout(lvbox)
        self.hbox.addWidget(lwidget)

        self.figure = FigureCanvas(width=5, height=4, dpi=100)
        toolbar = NavigationToolbar2QT(self.figure, self, coordinates=False)
        rwidget, rvbox = QWidget(), QVBoxLayout()
        rvbox.addWidget(toolbar)
        rvbox.addWidget(self.figure)
        rwidget.setLayout(rvbox)

        self.hbox.addWidget(rwidget)

        # self.setGeometry(500, 500, 750, 750)

    def update_list(self):
        self.list_widget.clear()
        df = self.user_df
        if "measurement_name" in df.columns:
            for metric in df.measurement_name.unique():
                QListWidgetItem(metric, self.list_widget)

    @property
    def user_df(self):
        return self.parent.db.to_dataframe()

    def plot_figure_clicked(self, item):
        metric = item.text()
        mask = self.user_df["measurement_name"] == metric
        local_df = self.user_df[mask]
        values = local_df.value.to_list()
        target_values = [x for x in values if x >= 0]
        mean_value = sum(target_values) / len(target_values)
        values = [mean_value if x < 0 else x for x in values]
        y_label = local_df.metric.values[0]
        title = _("%s in %s per day") % (metric, y_label)
        self.figure.update_plot(
            local_df.day.to_list(), values, title
        )
