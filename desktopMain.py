import sys
import typing
from PyQt6 import QtCore

from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QLabel, QGridLayout, QWidget

# Subclass QMainWindow to customize application's main window
class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        # Define the title of the application
        self.setWindowTitle("RoboTuner")

        # Create a button and a variable that tracks if the button is toggled
        self.isButtonChecked = True
        self.button = QPushButton("Press Here :)")
        self.button.setCheckable(True)

        # Link the button with created functions and toggle variable
        self.button.clicked.connect(self.buttonClicked)
        self.button.clicked.connect(self.buttonToggled)
        self.button.setChecked(self.isButtonChecked)

        # Create a textbox and label for slide max length
        self.slideMaxLengthInput = QLineEdit()
        self.slideMaxLengthInput.setText("4")
        self.slideMaxLengthLabel = QLabel()
        self.slideMaxLengthLabel.setText("Max slide length (in)")

        # Create a textbox and label for slide min length
        self.slideMinLengthInput = QLineEdit()
        self.slideMinLengthInput.setText("0")
        self.slideMinLengthLabel = QLabel()
        self.slideMinLengthLabel.setText("Min slide length (in)")

        # Create a textbox and label for slide max speed
        self.slideMaxSpeedInput = QLineEdit()
        self.slideMaxSpeedInput.setText("4")
        self.slideMaxSpeedLabel = QLabel()
        self.slideMaxSpeedLabel.setText("Max slide speed (in/sec)")

        # Create a textbox and label for slide min speed
        self.slideMinSpeedInput = QLineEdit()
        self.slideMinSpeedInput.setText("2")
        self.slideMinSpeedLabel = QLabel()
        self.slideMinSpeedLabel.setText("Min slide speed before error thrown (in/sec)")

        # Create the layout for the app
        layout = QGridLayout()
        layout.addWidget(self.slideMaxLengthLabel, 0, 0)
        layout.addWidget(self.slideMaxLengthInput, 0, 1)
        layout.addWidget(self.slideMinLengthLabel, 1, 0)
        layout.addWidget(self.slideMinLengthInput, 1, 1)
        layout.addWidget(self.slideMaxSpeedLabel, 2, 0)
        layout.addWidget(self.slideMaxSpeedInput, 2, 1)
        layout.addWidget(self.slideMinSpeedLabel, 3, 0)
        layout.addWidget(self.slideMinSpeedInput, 3, 1)
        layout.addWidget(self.button, 4, 1)   

        # Utilize the layout as a widget
        container = QWidget()
        container.setLayout(layout)

        # Place the layout in the app window
        self.setCentralWidget(container)

    def buttonClicked(self):
        print("Clicked")
    
    # Toggles the button when clicked
    def buttonToggled(self):
        self.isButtonChecked = self.button.isChecked()
        self.button.setText(str(self.isButtonChecked))
        print(self.isButtonChecked)

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()