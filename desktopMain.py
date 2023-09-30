import sys
import typing
from PyQt6 import QtCore

from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QLabel, QVBoxLayout, QWidget

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

        # Create a texbox and link it with the button
        self.input = QLineEdit()
        self.input.textChanged.connect(self.button.setText)

        # Create the layout for the app
        layout = QVBoxLayout()
        layout.addWidget(self.input)
        layout.addWidget(self.button)   

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