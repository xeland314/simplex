from PySide6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar
)
from matplotlib.figure import Figure


class PlotWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Crear figura y canvas
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        # Crear toolbar asociada al canvas
        self.toolbar = NavigationToolbar(self.canvas, self)

        # Layout vertical
        layout = QVBoxLayout(self)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
