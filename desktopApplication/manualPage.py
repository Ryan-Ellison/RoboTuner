
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
    QVBoxLayout, QApplication, QTabWidget
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


app = QApplication(sys.argv)
window = ManualWindow()
window.show()

app.exec()