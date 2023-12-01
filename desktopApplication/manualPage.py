
import sys

from PyQt6.QtWidgets import (
    QComboBox,
    QMainWindow,
    QPushButton,
    QLineEdit,
    QLabel,
    QGridLayout,
    QWidget,
    QInputDialog,
    QDialog,
    QDialogButtonBox,
    QVBoxLayout, QApplication, QTabWidget,
    QDockWidget,
    QListWidget,
    QTextEdit,
    QScrollArea 
)
from PyQt6.QtGui import QIntValidator


# Subclass QMainWindow to customize application's profile setting menu
class ManualWindow(QMainWindow):

    def __init__(self) -> None:
        super().__init__()
        # Define the title of the application
        self.setWindowTitle("Manual")

        layout = QGridLayout()

        self.setFixedWidth(1000)
        self.setFixedHeight(1000)

        self.tabs = QTabWidget()
        self.index = QWidget()
        self.assembly = QWidget()
        self.configuration = QWidget()
        self.usage = QWidget()
        self.tabs.resize(1000,1000)

        self.indexLabel = QLabel()
        self.indexLabel.setText("Hello There!")

        self.tabs.addTab(self.index, "Index")
        self.tabs.addTab(self.assembly, "Assembly")
        self.tabs.addTab(self.configuration, "Configuration")
        self.tabs.addTab(self.usage, "Usage")

        #add content to index tab
        self.index.layout = QGridLayout()
        self.indexLabel = QLabel()
        self.indexLabel.setText("Hello There!")
        self.index.layout.addWidget(self.indexLabel)
        self.index.setLayout(self.index.layout)


        layout.addWidget(self.tabs)
        self.setLayout(layout)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        #add content to assembly tab
        self.assembly.layout = QGridLayout()

        #Component List Header
        self.assemblyLabel = QLabel()
        self.assemblyLabel.setText("<b>List of Components:</b>")
        self.assembly.layout.addWidget(self.assemblyLabel, 0, 0)
        self.assembly.layout.setRowStretch(0, 0)
        self.assembly.setLayout(self.assembly.layout)

        self.assemblyText = QTextEdit()
        self.assemblyText.append("Hello")
        self.assembly.layout.addWidget(self.assemblyText, 1, 1)

        #Component List
        self.assemblyItemList = QListWidget()
        self.assemblyItemList.insertItem(0, "List")
        self.assembly.layout.addWidget(self.assemblyItemList, 1, 0)
        self.assembly.layout.setRowStretch(1, 25)

        #Assembly Instructions Header
        self.assemblyLabel = QLabel()
        self.assemblyLabel.setText("<b>Hardware Assembly Instructions:</b>")
        self.assembly.layout.addWidget(self.assemblyLabel, 2, 0)
        self.assembly.layout.setRowStretch(0, 0)

        #Hardware Assembly Instructions
        self.assemblyText = QTextEdit()
        self.assemblyText.append("1. Scream incredibly loung\n2. Probably start crying\n3. Finish crying and get a move on")
        self.assembly.layout.addWidget(self.assemblyText, 3, 0)
        self.assembly.layout.setRowStretch(3, 50)





app = QApplication(sys.argv)
window = ManualWindow()
window.show()

app.exec()