import sys
from instrumentProfiles import InstrumentProfile
from datetime import datetime
from functools import cmp_to_key
from pathlib import Path
import shutil
import re

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
    QVBoxLayout,
    QFileDialog
)
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
        self.createProfileButton = QPushButton("Create Profile")
        self.deleteProfileButton = QPushButton("Delete Current Profile")
        self.renameProfileButton = QPushButton("Rename Current Profile")
        self.sortOrderButton = QPushButton("Sort By Date")
        self.sortByName = True
        self.exportProfileButton = QPushButton("Export Profiles")
        self.importProfileButton = QPushButton("Import Profiles")

        # Link the button with created functions and toggle variable
        self.saveButton.clicked.connect(self.saveProfile)
        self.clearButton.clicked.connect(self.setTextBoxesToProfile)
        self.createProfileButton.clicked.connect(self.createProfile)
        self.deleteProfileButton.clicked.connect(self.confirmDeleteProfile)
        self.renameProfileButton.clicked.connect(self.renameProfile)
        self.sortOrderButton.clicked.connect(self.swapSortOrder)
        self.sortOrderButton.setCheckable(True)
        self.exportProfileButton.clicked.connect(self.exportProfiles)
        self.importProfileButton.clicked.connect(self.importProfiles)
        

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
        self.profile = None
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
        layout.addWidget(self.sortOrderButton, 4, 2)
        layout.addWidget(self.createProfileButton, 5, 0)
        layout.addWidget(self.deleteProfileButton, 5, 1)
        layout.addWidget(self.renameProfileButton, 5, 2)
        layout.addWidget(self.exportProfileButton, 6, 0)
        layout.addWidget(self.importProfileButton, 6, 1)

        # Utilize the layout as a widget
        container = QWidget()
        container.setLayout(layout)

        # Place the layout in the app window
        self.setCentralWidget(container)

    # Imports profiles
    def importProfiles(self):
        homeDir = str(Path.home())
        fname = QFileDialog.getOpenFileName(self, "Import from:", homeDir)[0]
        if fname == '':
            return
        file = open(file=fname, mode="r")

        if not self.verifyProfileFile(file):
            self.generateWarningDialog("Invalid File", "Invalid file.\nPlease choose another file.")
            return
        newProfiles = self.readProfilesFromFile(fname)
        for profile in newProfiles.keys():
            if profile in self.profiles.keys():
                continue
            self.profiles[profile] = newProfiles[profile]

        self.updateProfilesFiles()
        self.loadProfiles()
        file.close()
    
    # Verifies the shared file contains profile data with valid formatting
    def verifyProfileFile(self, file):
        namePattern = r"^.+$"
        settingsPattern = r'^(\d+,){3}\d+\n$'
        datePattern = r"^(\d{1,2}/){2}\d{2} (\d{2}:){2}\d{2}(\n)?$"
        lines = file.readlines()
        for i in range(0, len(lines), 3):
            nameMatch = re.findall(namePattern, lines[i])
            settingsMatch = re.match(settingsPattern, str(lines[i + 1]))
            dateMatch = re.match(datePattern, lines[i + 2])
            if not (nameMatch and settingsMatch and dateMatch):
                print(lines[i], nameMatch)
                print(lines[i + 1], settingsMatch)
                print(lines[i + 2], dateMatch)
                return False
        return True

    # Exports the profiles file to target location
    def exportProfiles(self):
        homeDir = str(Path.home())
        dname = QFileDialog.getExistingDirectory(self, "Export to:", homeDir)
        profilesPath = str(Path(__file__).parent) + "/.profiles.txt"
        shutil.copy2(profilesPath, dname)

    # Swaps the sorting order and repopulates the dropdown
    def swapSortOrder(self, toggled):
        if toggled:
            self.sortOrderButton.setText("Sort By Name")
            self.sortByName = False
        else:
            self.sortOrderButton.setText("Sort By Date")
            self.sortByName = True
        self.populateDropdown()

    # Rename the current profile
    def renameProfile(self):
        name, confirmed = QInputDialog.getText(self, 'New Profile Name', 'Enter the new profile\'s name:')
        if confirmed:
            if name in self.profiles.keys():
                self.generateWarningDialog("Name Taken!", "This name is already in use.\nPlease choose another name.")
            else:
                self.profiles[name] = self.profiles.pop(self.profile.name)
                self.profile.name = name
                self.populateDropdown()
                self.updateProfilesFiles()

    # Update the current set profile when a new one is selected from the dropdown
    def changeProfile(self, _):
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
   
    # Function to create a profile
    def createProfile(self):
        name, confirmed = QInputDialog.getText(self, 'New Profile Name', 'Enter the new profile\'s name:')
        if confirmed:
            if name in self.profiles.keys():
                self.generateWarningDialog("Name Taken!", "This name is already in use.\nPlease choose another name.")
            else:
                profile = InstrumentProfile(name)
                self.profile = profile
                self.profiles[name] = profile
                self.populateDropdown()
                self.updateProfilesFiles()

    # Function to confirm the user wants to delete the current profile
    def confirmDeleteProfile(self):
        deleteProfileWarning = QDialog()
        deleteProfileWarning.setWindowTitle("Confirm Profile Deletion")

        warningButtons = QDialogButtonBox.StandardButton.Yes | QDialogButtonBox.StandardButton.No

        # accept and reject connections close the dialog box
        buttonBox = QDialogButtonBox(warningButtons)
        buttonBox.accepted.connect(deleteProfileWarning.accept)
        buttonBox.rejected.connect(deleteProfileWarning.reject)

        # Delete the profile only when confirmation is accepted
        buttonBox.accepted.connect(self.deleteProfile)

        deleteProfileWarning.layout = QVBoxLayout()
        deleteProfileWarning.layout.addWidget(QLabel("Are you sure you want to delete this profile?"))
        deleteProfileWarning.layout.addWidget(buttonBox)
        deleteProfileWarning.setLayout(deleteProfileWarning.layout)

        deleteProfileWarning.exec()
    
    # Function to delete the current profile
    def deleteProfile(self):
        if len(self.profiles) == 1:
            self.generateWarningDialog("Not Enough Profiles", "If you delete this profile there won't be any left.\nPlease create a new profile before deleting this one.")
        else:
            self.profiles.pop(self.profile.name, InstrumentProfile("-99"))
            if self.profileDropdown.itemText(0) == self.profile.name:
                self.profile = self.profiles[self.profileDropdown.itemText(1)]
            else:
                self.profile = self.profiles[self.profileDropdown.itemText(0)]
            self.updateProfilesFiles()
            self.populateDropdown()

    # Updates the profile class object and calls to update the save file
    def saveProfile(self):
        profile = self.profile
        profile.slideMaxLength = self.slideMaxLengthInput.text()
        profile.slideMinLength = self.slideMinLengthInput.text()
        profile.slideMaxSpeed = self.slideMaxSpeedInput.text()
        profile.slideMinSpeed = self.slideMinSpeedInput.text()
        profile.dateEdited = datetime.now()

        self.updateProfilesFiles()
        
    # Loads the first profile if there are any already made, otherwise makes a default
    def loadProfiles(self):
        self.profiles = self.readProfilesFromFile()
        if len(self.profiles) == 0:
            self.profile = InstrumentProfile("Default")
            self.updateProfilesFiles()
        else:
            self.profile = self.profiles[list(self.profiles.keys())[0]]
        self.setTextBoxesToProfile()

    # Reads through the profile save file and constructs all profiles
    def readProfilesFromFile(self, file="desktopApplication/.profiles.txt") -> dict[str, InstrumentProfile]:
        profiles = dict()
        try:
            openFile = open(file, "r")
            print("file found")
        except IOError:
            openFile = open(file, "w+")
            print("file not found")
        else:
            lines = openFile.readlines()
            for i in range(0, len(lines), 3):
                name = lines[i].strip()
                slideSettings = lines[i + 1].split(',')
                slideSettings = [slideSettings[i].strip() for i in range(len(slideSettings))]
                dateString = lines[i + 2].strip()
                date = datetime.strptime(dateString, '%d/%m/%y %H:%M:%S')
                profile = InstrumentProfile(name)
                profile.setValuesAndDate(slideSettings, date)
                profiles[name] = profile
        finally:
            openFile.close()
            return profiles

    # Writes all existing profiles to the save file
    def updateProfilesFiles(self, file="desktopApplication/.profiles.txt"):
        openFile = open(file, "w")
        for profileName in sorted(list(self.profiles.keys()), key=lambda s: s.casefold()):
            profile = self.profiles[profileName]
            openFile.write(profile.generateSaveFileText())
        openFile.close()

    # Adds all profiles to the dropdown menu
    def populateDropdown(self):
        self.profileDropdown.clear()
        if self.sortByName:
            print("sorting by name")
            self.profileDropdown.addItems(sorted(list(self.profiles.keys()), key=lambda s: s.casefold()))
        else:
            print("sorting by date")
            self.profileDropdown.addItems(sorted(list(self.profiles.keys()), key=cmp_to_key(self.orderByDate)))
        self.profileDropdown.setCurrentText(self.profile.name)
        self.setTextBoxesToProfile()

    # Comparator function to allow sorting by date
    def orderByDate(self, profileName1, profileName2):
        profile1 = self.profiles[profileName1]
        profile2 = self.profiles[profileName2]
        if profile1.dateEdited < profile2.dateEdited:
            return 1
        elif profile1.dateEdited > profile2.dateEdited:
            return -1
        else:
            return 0

    # Create a warning dialog with specified window title and message
    def generateWarningDialog(self, windowTitle, message):
        warning = QDialog()
        warning.setWindowTitle(windowTitle)
        
        warningButton = QDialogButtonBox.StandardButton.Ok

        buttonBox = QDialogButtonBox(warningButton)
        buttonBox.accepted.connect(warning.accept)

        warning.layout = QVBoxLayout()
        warning.layout.addWidget(QLabel(message))
        warning.layout.addWidget(buttonBox)
        warning.setLayout(warning.layout)

        warning.exec()

""" 
app = QApplication(sys.argv)

window = ProfileInputWindow()
window.show()

app.exec() """