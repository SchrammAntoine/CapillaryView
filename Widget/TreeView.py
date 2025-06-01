
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTreeView, QLabel,
    QPushButton, QFileDialog, QHBoxLayout
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QDir, QModelIndex, Qt
from PyQt5.QtWidgets import QFileSystemModel


class FileSelector(QWidget):
    def __init__(self, parent=None, manager=None, start_dir=None):
        super().__init__(parent)
        self.manager = manager
        self.setWindowTitle("File Selector Widget")
        self.resize(600, 450)

        self.selected_files = []

        # Layout
        layout = QVBoxLayout(self)

        # Top bar: Select root directory
        top_bar = QHBoxLayout()
        self.select_root_btn = QPushButton("Select Root Directory")
        self.select_root_btn.clicked.connect(self.select_root_directory)
        top_bar.addWidget(self.select_root_btn)
        layout.addLayout(top_bar)

        # File system model
        self.model = QFileSystemModel()
        self.model.setRootPath(QDir.rootPath())
        self.model.setFilter(QDir.AllDirs | QDir.NoDotAndDotDot | QDir.Files)

        # Tree view
        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(start_dir or QDir.homePath()))
        self.tree.setSelectionMode(QTreeView.ExtendedSelection)  # Enable Shift/Ctrl selection
        self.tree.selectionModel().selectionChanged.connect(self.on_selection_changed)
        self.tree.setHeaderHidden(False)

        # Hide unnecessary columns
        for i in range(1, 4):
            self.tree.hideColumn(i)

        layout.addWidget(self.tree)

    def on_selection_changed(self, selected, deselected):
        self.selected_files = []
        indexes = self.tree.selectionModel().selectedIndexes()

        # Collect only file paths (not directories)
        for index in indexes:
            if index.column() == 0 and not self.model.isDir(index):
                self.selected_files.append(self.model.filePath(index))

        self.manager.update_plot()

    def select_root_directory(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select Root Directory", QDir.homePath())
        if dir_path:
            self.model.setRootPath(dir_path)
            self.tree.setRootIndex(self.model.index(dir_path))

    def get_selected_files(self):
        return self.selected_files


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileSelector(
        parent = None,
        start_dir = "/home/administrateur/Documents/PythonProjects/CapillaryViewer"
    )
    window.show()
    sys.exit(app.exec_())
