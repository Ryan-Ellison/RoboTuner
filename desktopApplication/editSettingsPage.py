import sys
from profile import Profile

from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QLabel, QGridLayout, QWidget

# Subclass QMainWindow to customize application's profile setting menu
class profileInputWindow(QMainWindow):

    def __init__(self) -> None:
        super().__init__()
        # Define the title of the application
        self.setWindowTitle("RoboTuner Settings")

        # Create a button and a variable that tracks if the button is toggled
        self.saveButton = QPushButton("Save Profile")
        self.clearButton = QPushButton("Reset Profile")

        # Link the button with created functions and toggle variable
        self.saveButton.clicked.connect(self.saveProfile)
        self.clearButton.clicked.connect(self.setTextBoxesToProfile)

        # Create a textbox and label for slide max length
        self.slideMaxLengthInput = QLineEdit()
        self.slideMaxLengthLabel = QLabel()
        self.slideMaxLengthLabel.setText("Max slide length (in)")

        # Create a textbox and label for slide min length
        self.slideMinLengthInput = QLineEdit()
        self.slideMinLengthLabel = QLabel()
        self.slideMinLengthLabel.setText("Min slide length (in)")

        # Create a textbox and label for slide max speed
        self.slideMaxSpeedInput = QLineEdit()
        self.slideMaxSpeedLabel = QLabel()
        self.slideMaxSpeedLabel.setText("Max slide speed (in/sec)")

        # Create a textbox and label for slide min speed
        self.slideMinSpeedInput = QLineEdit()
        self.slideMinSpeedLabel = QLabel()
        self.slideMinSpeedLabel.setText("Min slide speed before error thrown (in/sec)")

        # Set text boxes to initial values
        self.loadProfile()

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
        layout.addWidget(self.clearButton, 4, 0)   
        layout.addWidget(self.saveButton, 4, 1)

        # Utilize the layout as a widget
        container = QWidget()
        container.setLayout(layout)

        # Place the layout in the app window
        self.setCentralWidget(container)

    # Helper function to set all slide fields to initial values
    def setTextBoxesToProfile(self):
        profile = self.profile

        maxLength, minLength, maxSpeed, minSpeed = profile.getStringValues()

        self.slideMaxLengthInput.setText(maxLength)
        self.slideMinLengthInput.setText(minLength)
        self.slideMaxSpeedInput.setText(maxSpeed)
        self.slideMinSpeedInput.setText(minSpeed)


    # Foundation to save 
    # Not working version of profile system, temporary testing solution
    def saveProfile(self):
        profile = self.profile
        profile.slideMaxLength = self.slideMaxLengthInput.text()
        profile.slideMinLength = self.slideMinLengthInput.text()
        profile.slideMaxSpeed = self.slideMaxSpeedInput.text()
        profile.slideMinSpeed = self.slideMinSpeedInput.text()
        
    # Sets profile data as initial values for all fields
    # Testing solution until profile data structure is made
    def loadProfile(self):
        self.profile = Profile()
        self.setTextBoxesToProfile()

app = QApplication(sys.argv)

window = profileInputWindow()
window.show()

app.exec()