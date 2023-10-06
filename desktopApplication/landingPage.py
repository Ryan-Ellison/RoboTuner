import sys
from editSettingsPage import ProfileInputWindow

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QTabWidget,
    QWidget,
)

class LandingPage(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Landing Page")

        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.TabPosition.North)
        tabs.setMovable(True)
        tabs.setDocumentMode(True)

        tabs.addTab(ProfileInputWindow(), "Edit settings")
        tabs.addTab(ProfileInputWindow(), "other edit settings")

        self.setCentralWidget(tabs)

app = QApplication(sys.argv)

window = LandingPage()
window.show()

app.exec()