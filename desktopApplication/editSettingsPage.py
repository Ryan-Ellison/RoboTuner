import sys
from profile import Profile

from PyQt6.QtWidgets import QComboBox, QMainWindow, QPushButton, QLineEdit, QLabel, QGridLayout, QWidget
from PyQt6.QtGui import QIntValidator

# Subclass QMainWindow to customize application's profile setting menu
class ProfileInputWindow(QMainWindow):

    def __init__(self) -> None:
        super().__init__()
        # Define the title of the application
        self.setWindowTitle("RoboTuner Settings")

        # Create a button and a variable that tracks if the button is toggled
        self.saveButton = QPushButton("Save Profile")
        self.clearButton = QPushButton("Discard Changes")

        # Link the button with created functions and toggle variable
        self.saveButton.clicked.connect(self.saveProfile)
        self.clearButton.clicked.connect(self.setTextBoxesToProfile)

        intRange = QIntValidator()
        intRange.setBottom(0)
        intRange.setTop(9)

        # Create a textbox and label for slide max length
        self.slideMaxLengthInput = QLineEdit()
        self.slideMaxLengthInput.setValidator(intRange)
        self.slideMaxLengthLabel = QLabel()
        self.slideMaxLengthLabel.setText("Max slide length (in)")

        # Create a textbox and label for slide min length
        self.slideMinLengthInput = QLineEdit()
        self.slideMinLengthInput.setValidator(intRange)
        self.slideMinLengthLabel = QLabel()
        self.slideMinLengthLabel.setText("Min slide length (in)")

        # Create a textbox and label for slide max speed
        self.slideMaxSpeedInput = QLineEdit()
        self.slideMaxSpeedInput.setValidator(intRange)
        self.slideMaxSpeedLabel = QLabel()
        self.slideMaxSpeedLabel.setText("Max slide speed (in/sec)")

        # Create a textbox and label for slide min speed
        self.slideMinSpeedInput = QLineEdit()
        self.slideMinSpeedInput.setValidator(intRange)
        self.slideMinSpeedLabel = QLabel()
        self.slideMinSpeedLabel.setText("Min slide speed before error thrown (in/sec)")

        # Set text boxes to initial values
        self.loadProfiles()

        # Create and populate the dropdown menu for profiles
        self.profileDropdown = QComboBox()
        self.profileDropdown.activated.connect(self.changeProfile)
        self.populateDropdown()

        # Create the layout for the app
        layout = QGridLayout()
        layout.addWidget(self.profileDropdown, 0, 2)
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

    # Update the current set profile when a new one is selected from the dropdown
    def changeProfile(self, index):
        profile = self.profileDropdown.currentText()
        self.profile = self.profiles[profile]
        self.setTextBoxesToProfile()

    # Helper function to set all slide fields to initial values
    def setTextBoxesToProfile(self):
        maxLength, minLength, maxSpeed, minSpeed = self.profile.getStringValues()
        self.slideMaxLengthInput.setText(maxLength)
        self.slideMinLengthInput.setText(minLength)
        self.slideMaxSpeedInput.setText(maxSpeed)
        self.slideMinSpeedInput.setText(minSpeed)


    # Updates the profile class object and calls to update the save file
    def saveProfile(self):
        profile = self.profile
        profile.slideMaxLength = self.slideMaxLengthInput.text()
        profile.slideMinLength = self.slideMinLengthInput.text()
        profile.slideMaxSpeed = self.slideMaxSpeedInput.text()
        profile.slideMinSpeed = self.slideMinSpeedInput.text()

        self.updateProfilesFiles()
        
    # Loads the first profile if there are any already made, otherwise makes a default
    def loadProfiles(self):
        self.profiles = self.readProfilesFromFile()
        if len(self.profiles) == 0:
            self.profile = Profile("Default")
            self.updateProfilesFiles()
        else:
            self.profile = self.profiles[list(self.profiles.keys())[0]]
        self.setTextBoxesToProfile()

    # Reads through the profile save file and constructs all profiles
    def readProfilesFromFile(self, file="desktopApplication/.profiles.txt") -> dict[str, Profile]:
        profiles = dict()
        try:
            openFile = open(file, "r")
            print("file found")
        except IOError:
            openFile = open(file, "w+")
            print("file not found")
        else:
            lines = openFile.readlines()
            for i in range(0, len(lines), 2):
                name = lines[i].strip()
                slideSettings = lines[i + 1].split(',')
                slideSettings = [slideSettings[i].strip() for i in range(len(slideSettings))]
                profile = Profile(name)
                profile.setAllValues(slideSettings)
                profiles[name] = profile
        finally:
            openFile.close()
            return profiles

    # Writes all existing profiles to the save file
    def updateProfilesFiles(self, file="desktopApplication/.profiles.txt"):
        openFile = open(file, "w")
        for profile in list(self.profiles.values()):
            openFile.write(profile.generateSaveFileText())
        openFile.close()

    # Adds all profiles to the dropdown menu
    def populateDropdown(self):
        self.profileDropdown.clear()
        self.profileDropdown.addItems(sorted(list(self.profiles.keys())))


""" 
app = QApplication(sys.argv)

window = ProfileInputWindow()
window.show()

app.exec() """