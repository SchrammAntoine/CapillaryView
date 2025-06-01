import sys
from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QCheckBox, QVBoxLayout,
    QFormLayout, QApplication, QGroupBox
)

class ParameterPanel(QWidget):
    def __init__(self, parent=None, manager=None):
        super().__init__(parent)
        self.manager = manager
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # --- Region Of Interest Group ---
        roi_group = QGroupBox("Region Of Interest")
        roi_layout = QFormLayout()
        self.start_input = QLineEdit()
        self.end_input = QLineEdit()
        self.start_input.textChanged.connect(self.on_parameter_update)
        self.end_input.textChanged.connect(self.on_parameter_update)
        roi_layout.addRow("Start:", self.start_input)
        roi_layout.addRow("End:", self.end_input)
        roi_group.setLayout(roi_layout)
        main_layout.addWidget(roi_group)
        roi_group.setFixedHeight(100)

        # --- Median Scaling ---
        median_scaling_group = QGroupBox("Median Rescaling")
        median_scaling_layout = QFormLayout()
        self.median_scaling_checkbox = QCheckBox("Apply")
        self.median_scaling_checkbox.stateChanged.connect(self.on_parameter_update)
        median_scaling_layout.addRow("", self.median_scaling_checkbox)
        median_scaling_group.setLayout(median_scaling_layout)
        main_layout.addWidget(median_scaling_group)
        median_scaling_group.setFixedHeight(60)

        main_layout.addStretch()
        self.setLayout(main_layout)

    def on_parameter_update(self) :
        self.manager.update_plot()

    def get_parameters(self):
        """Return the current values of the parameters as a dictionary."""
        try:
            start = int(self.start_input.text())
        except ValueError:
            start = 0
        try:
            end = int(self.end_input.text())
        except ValueError:
            end = -1

        return {
            "start": start,
            "end": end,
            "apply_median_scaling": self.median_scaling_checkbox.isChecked()
        }

# For testing purposes
if __name__ == "__main__":
    app = QApplication(sys.argv)
    panel = ParameterPanel()
    panel.show()
    sys.exit(app.exec_())
