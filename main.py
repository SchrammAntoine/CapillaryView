import sys
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QSplitter,QFrame
from PyQt5.QtCore import Qt

from Widget.PlotWidget import MplWidget
from Widget.TreeView import FileSelector
from Widget.Parameter import ParameterPanel

import numpy as np
from pathlib import Path

from Parser.ABIFReader import ABIFReader
from functools import lru_cache

@lru_cache
def ParseFile(file_name) :
    reader = ABIFReader(file_name)
    output = {
        "1"    : reader.getData('DATA',1),
        "2"    : reader.getData('DATA',2),
        "3"    : reader.getData('DATA',3),
        "4"    : reader.getData('DATA',4)#,
#        "Satd" : reader.getData('Satd',1)
    }
    return output


class MyWidget(QWidget):
    def __init__(self, data_dir):
        super().__init__()

        # Set window properties
        self.setWindowTitle("Capillary Viewer")
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        window_width = screen_geometry.width()
        self.setGeometry(screen_geometry)
        # Create widgets
        self.file_widget = FileSelector(
            parent = self,
            manager = self,
            start_dir = data_dir
        )
        self.plot_widget = MplWidget(
            parent = self,
            manager = self,
            custom_button_labels = ["1","2","3","4"]
        )
        self.parameter_widget = ParameterPanel(
            parent = self,
            manager = self
        )

        # Create splitter and add widgets
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.file_widget)
        splitter.addWidget(self.plot_widget)
        splitter.addWidget(self.parameter_widget)

        ## set initial width of self.file_widget and self.parameter_widget to 20% of window width
        splitter.setSizes([
            int(0.2 * window_width),  # file_widget
            int(0.7 * window_width),  # plot_widget
            int(0.1 * window_width)   # parameter_widget
        ])
        splitter.setStyleSheet("""
            QSplitter::handle {
                background-color: #AAAAAA;
            }
        """)

        # Optional: set initial sizes for the splitter widgets
        #splitter.setSizes([200, 600])

        # Use layout to hold splitter
        layout = QHBoxLayout()
        layout.addWidget(splitter)
        self.setLayout(layout)

    def reset_view(self) :
        self.plot_widget.ax.set_xlim(self.home_xlim)
        self.plot_widget.ax.set_ylim(self.home_ylim)

    def update_plot(self) :
        states = self.plot_widget.get_states()
        files = self.file_widget.get_selected_files()
        parameters = self.parameter_widget.get_parameters()

        valid_states = [ channel for channel in states if states[channel] ]

        dataset = dict()
        for file in files :
            try :
                content = ParseFile(file)
            except Exception :
                continue
            data = {}
            for key in valid_states : data[key] = content[key]
            dataset[file] = data

        self.plot_widget.clear_plot()
        for file_name, data in dataset.items() :

            path = Path(file_name)
            file_stem = path.stem
            last_folder = path.parent.name
            name = f"{last_folder}_{file_stem}"

            for channel, intensities in data.items() :
                label = file_name

                intensities = np.array(intensities, dtype=float)

                start = parameters["start"]
                end = parameters["end"]
                intensities = intensities[start:end]

                if parameters["apply_median_scaling"] :
                    median = np.median(intensities)
                    intensities /= median

                self.plot_widget.ax.plot(
                    intensities,
                    label=f"{name}_channel={channel}"
                )

        self.plot_widget.ax.set_xlabel("Frames (#)")
        self.plot_widget.ax.set_ylabel("Fluorescence Intensity (AU)")
        self.home_ylim = self.plot_widget.ax.get_ylim()
        self.home_xlim = self.plot_widget.ax.get_xlim()
        self.plot_widget.draw()





def main():
    home_dir = Path.home()
    app = QApplication(sys.argv)
    window = MyWidget(
        data_dir = home_dir
    )
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
