import sys
import typing
from PyQt6 import QtCore

from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton

# Subclass QMainWindow to customize application's main window
class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("RoboTuner")

        self.isButtonChecked = True
        self.button = QPushButton("Press Here :)")
        self.button.setCheckable(True)
        self.button.clicked.connect(self.buttonClicked)
        self.button.clicked.connect(self.buttonToggled)
        self.button.setChecked(self.isButtonChecked)

        self.setCentralWidget(self.button)

    def buttonClicked(self):
        print("Clicked")
    
    def buttonToggled(self):
        self.isButtonChecked = self.button.isChecked()
        self.button.setText(str(self.isButtonChecked))
        print(self.isButtonChecked)

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()