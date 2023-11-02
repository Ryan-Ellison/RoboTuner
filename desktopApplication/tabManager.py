import sys
import os
from editSettingsPage import ProfileInputWindow
from landingPage import LandingPage
from cadFilesPage import CADFilesWindow
from noteDisplayPage import NoteDisplayPage
from hardwareSpecificationsPage import HardwareSpecificationsPage

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTabWidget,
)

class TabManager(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("RoboTuner")

        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.TabPosition.North)
        self.tabs.setMovable(False)
        self.tabs.setDocumentMode(True)

        self.landingPage = LandingPage()
        self.profileInputWindow = ProfileInputWindow()
        self.cadFilesWindow = CADFilesWindow()
        self.noteDiplayPage = NoteDisplayPage()
        self.hardwareSpecificationsPage = HardwareSpecificationsPage()

        # self.timer = QTimer(self)

        self.tabs.addTab(self.landingPage, "Landing Page")
        self.tabs.addTab(self.profileInputWindow, "Edit settings")
        self.tabs.addTab(self.cadFilesWindow, "CAD Files")
        self.tabs.addTab(self.noteDiplayPage, "Display Note")
        self.tabs.addTab(self.hardwareSpecificationsPage, "Hardware Specifications")

        # self.tabs.tabBarClicked.connect(self.tabSelected)

        self.setCentralWidget(self.tabs)
    
    """
    def tabSelected(self):
        if self.tabs.currentIndex() == 3:
            self.timer.setSingleShot(False)
            self.timer.timeout.connect(self.noteDiplayPage.callPitch)
            self.timer.start(200)
        else:
            self.timer.setSingleShot(True)
    """

# PATH = "/Users/ryanellison/VSCode Projects/RoboTuner/"

# sys.path.insert(0, PATH)
# os.chdir(PATH)

app = QApplication(sys.argv)

window = TabManager()
window.show()

app.exec()