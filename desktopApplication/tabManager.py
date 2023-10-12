import sys
from editSettingsPage import ProfileInputWindow
from landingPage import LandingPage
from cadFilesPage import CADFilesWindow

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTabWidget,
)

class TabManager(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("RoboTuner")

        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.TabPosition.North)
        tabs.setMovable(True)
        tabs.setDocumentMode(True)

        tabs.addTab(LandingPage(), "Landing Page")
        tabs.addTab(ProfileInputWindow(), "Edit settings")
        tabs.addTab(CADFilesWindow(), "CAD Files")

        self.setCentralWidget(tabs)

app = QApplication(sys.argv)

window = TabManager()
window.show()

app.exec()