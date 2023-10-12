import sys
import shutil
from PyQt6.QtCore import (
    QDir,
    QCoreApplication,
)
from PyQt6.QtGui import (
    QGuiApplication,
    QFileSystemModel,
)
from PyQt6.QtWidgets import (
    QApplication,
    QComboBox, 
    QMainWindow, 
    QListView,
    QTreeView,
    QAbstractItemView,
    QPushButton, 
    QLineEdit, 
    QLabel, 
    QGridLayout, 
    QWidget, 
    QInputDialog, 
    QDialog, 
    QDialogButtonBox, 
    QVBoxLayout,
    QHBoxLayout
)

class CADFilesWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.fileListView = QListView()
        self.fileBrowserView = QTreeView()

        # 
        self.cadPath = QDir("desktopApplication/CADFiles/").absolutePath()

        self.fileModel = QFileSystemModel()
        self.fileModel.setRootPath(self.cadPath)

        self.fileListView.setModel(self.fileModel)
        self.fileListView.setRootIndex(self.fileModel.index(self.cadPath))
        self.fileListView.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)

        self.dirModel = QFileSystemModel()
        self.dirModel.setRootPath(QDir.homePath())
        
        self.fileBrowserView.setModel(self.dirModel)
        self.fileBrowserView.expanded.connect(self.resizeNameColumn)

        self.saveFilesAtLocation = QPushButton("Save Files")
        self.saveFilesAtLocation.clicked.connect(self.saveFiles)

        layout = QHBoxLayout()
        browserLayout = QVBoxLayout()
        browserLayout.addWidget(self.fileBrowserView)
        browserLayout.addWidget(self.saveFilesAtLocation)
        layout.addWidget(self.fileListView, 1)
        layout.addLayout(browserLayout, 3)
        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

    def saveFiles(self):
        selected = self.getSelected()
        targetPath = self.dirModel.filePath(self.fileBrowserView.currentIndex())
        for file in selected:
            filePath = self.cadPath + file
            shutil.copy2(filePath, targetPath)

    def resizeNameColumn(self):
        self.fileBrowserView.resizeColumnToContents(0)

    def getSelected(self) -> list[str]:
        selected = []
        for index in self.fileListView.selectedIndexes():
            selected.append(self.fileModel.data(index))
        return selected


# app = QApplication(sys.argv)

# window = CADFilesWindow()
# window.show()

# app.exec()