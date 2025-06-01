import sys


from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QVBoxLayout


import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

import numpy as np


class CustomNavigationToolbar(NavigationToolbar):
    def __init__(self, canvas, parent, manager, custom_button_labels = [] ):
        super().__init__(canvas, parent)
        self.manager = manager
        # Add custom buttons
        self.addSeparator()

        self.states = dict()
        for label in custom_button_labels :
            self.add_custom_button(label)
            self.states[label] = True

    def add_custom_button(self, label):
        checkbox = QCheckBox(label)
        checkbox.setChecked(True)
        checkbox.setFixedSize(50, 25)
        checkbox.toggled.connect(lambda checked, l=label: self.on_checkbox_toggled(l, checked))
        self.addWidget(checkbox)

    def on_checkbox_toggled(self, label, checked):
        self.states[label] = checked
        self.manager.update_plot()

    def home(self, *args):
        """Override the Home button to reset to a custom state."""
        self.manager.reset_view()
        self.canvas.draw()

class MplWidget(QWidget):
    def __init__(self, parent=None, manager=None, custom_button_labels = [] ):
        super().__init__(parent)
        self.manager = manager
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)

        self.toolbar = CustomNavigationToolbar(
            canvas = self.canvas,
            parent = self,
            manager = manager,
            custom_button_labels = custom_button_labels
        )

        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)

        self.setLayout(layout)

    def plot_data(self, x, y):
        self.ax.plot(x, y)
        self.canvas.draw()

    def draw(self) :
        self.canvas.draw()

    def get_ax(self) :
        return ax


    def clear_plot(self):
        self.ax.clear()
        self.canvas.draw()

    def get_states(self) :
        return self.toolbar.states

if __name__ == '__main__':

    from PyQt5.QtWidgets import QMainWindow
    from PyQt5.QtWidgets import QApplication

    class MainWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("Matplotlib with Custom Toolbar Buttons")
            self.mplwidget = MplWidget(self)
            self.setCentralWidget(self.mplwidget)
            self.resize(800, 600)

            x = np.linspace(0, 10, 100)
            y = np.sin(x)
            self.mplwidget.plot_data(x,y)

            x = np.linspace(0, 10, 100)
            y = np.cos(x)
            self.mplwidget.plot_data(x,y)

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
