import sys

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

        self.welcome = QLabel()
        self.welcome.setText("Landing Page")

        self.setCentralWidget(self.welcome)

"""
app = QApplication(sys.argv)

window = LandingPage()
window.show()

app.exec()
"""