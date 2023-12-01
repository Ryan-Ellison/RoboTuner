import sys
import os
from instrumentProfiles import InstrumentProfile
from datetime import datetime
from functools import cmp_to_key
from pathlib import Path
import paramiko
import shutil
import re
import time

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
    QFileDialog,
    QApplication,
    QRadioButton,
    QButtonGroup,
    QHBoxLayout
)
from PyQt6.QtGui import QIntValidator
from PyQt6.QtCore import QDir
 
class ImportExportWindow(QMainWindow):
    def __init__(self, runningWindow):
        super().__init__()

        self.runningWindow = runningWindow

        self.exportProfileButton = QPushButton("Export Profiles To Desktop")
        self.importProfileButton = QPushButton("Import Profiles From Desktop")
        self.exportProfilesToRPButton = QPushButton("Export Profiles To Device")
        self.importProfilesFromRPButton = QPushButton("Import Profiles From Device")
        self.confirmButton = QPushButton("Confirm Action")

        self.exportProfileButton.clicked.connect(self.runningWindow.exportProfiles)
        self.importProfileButton.clicked.connect(self.runningWindow.importProfiles)
        self.exportProfilesToRPButton.clicked.connect(self.runningWindow.exportProfilesToRaspberryPi)
        self.importProfilesFromRPButton.clicked.connect(self.runningWindow.importProfilesFromRaspberryPi)
        self.confirmButton.clicked.connect(self.confirmAction)

        self.connectionTypeRadioGroup = QButtonGroup(self)

        self.connectionLabel = QLabel("Connection Method:")
        self.desktopRadio = QRadioButton("Current Device", self)
        self.wifiRadio = QRadioButton("Wifi/Ethernet", self)
        self.bluetoothRadio = QRadioButton("Bluetooth", self)

        connectionColumn = QVBoxLayout()
        connectionColumn.addWidget(self.connectionLabel)

        connections = [self.desktopRadio, self.wifiRadio, self.bluetoothRadio]
        for connection in connections:
            self.connectionTypeRadioGroup.addButton(connection)
            connectionColumn.addWidget(connection)

        self.importExportGroup = QButtonGroup(self)
        self.importExportLabel = QLabel("Action:")
        self.importRadio = QRadioButton("Import Profiles", self)
        self.exportRadio = QRadioButton("Export Profiles", self)

        actionColumn = QVBoxLayout()
        actionColumn.addWidget(self.importExportLabel)

        actions = [self.importRadio, self.exportRadio]
        for action in actions:
            self.importExportGroup.addButton(action)
            actionColumn.addWidget(action)
        actionColumn.addWidget(QLabel(""))

        layout = QVBoxLayout()
        columns = QHBoxLayout()
        columns.addLayout(connectionColumn)
        columns.addLayout(actionColumn)
        layout.addLayout(columns)
        layout.addWidget(self.confirmButton)

        # Utilize the layout as a widget
        container = QWidget()
        container.setLayout(layout)

        # Place the layout in the app window
        self.setCentralWidget(container)

    def confirmAction(self):
        if self.importRadio.isChecked():
            if self.desktopRadio.isChecked():
                self.runningWindow.importProfiles()
            elif self.wifiRadio.isChecked():
                self.runningWindow.importProfilesFromRaspberryPi()
            elif self.bluetoothRadio.isChecked():
                self.runningWindow.generateWarningDialog("Bluetooth is in progress", "Bluetooth development is in progress")
            else:
                self.runningWindow.generateWarningDialog("Invalid Selection", "Invalid Selection")
        elif self.exportRadio.isChecked():
            if self.desktopRadio.isChecked():
                self.runningWindow.exportProfiles()
            elif self.wifiRadio.isChecked():
                self.runningWindow.exportProfilesToRaspberryPi()
            elif self.bluetoothRadio.isChecked():
                self.runningWindow.generateWarningDialog("Bluetooth is in progress", "Bluetooth development is in progress")
            else:
                self.runningWindow.generateWarningDialog("Invalid Selection", "Invalid Selection")
        else:
            self.runningWindow.generateWarningDialog("Invalid selection", "Invalid Selection")
        

# Subclass QMainWindow to customize application's profile setting menu
class ProfileInputWindow(QMainWindow):

    RASPBERRYPIPATH = "10.186.35.57"
    #RASPBERRYPIPATH = "192.168.4.28"

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
        self.updateRaspberryPiButton = QPushButton("Update Raspberry Pi")
        self.resetRaspberryPiButton = QPushButton("Reset Raspberry Pi Files")
        self.importExportProfilesButton = QPushButton("Import/Export Profiles To/From Device")

        self.importExportWindow = ImportExportWindow(self)

        # Link the button with created functions and toggle variable
        self.saveButton.clicked.connect(self.saveProfile)
        self.clearButton.clicked.connect(self.setTextBoxesToProfile)
        self.createProfileButton.clicked.connect(self.createProfile)
        self.deleteProfileButton.clicked.connect(self.confirmDeleteProfile)
        self.renameProfileButton.clicked.connect(self.renameProfile)
        self.sortOrderButton.clicked.connect(self.swapSortOrder)
        self.sortOrderButton.setCheckable(True)
        self.updateRaspberryPiButton.clicked.connect(self.updateRaspberryPi)
        self.resetRaspberryPiButton.clicked.connect(self.resetRaspberryPiConfirmation)
        self.importExportProfilesButton.clicked.connect(self.importExportProfiles)

        intRange = QIntValidator()
        intRange.setBottom(0)
        intRange.setTop(100)

        self.maxSpeedRange = QIntValidator()
        self.maxSpeedRange.setBottom(10)
        self.maxSpeedRange.setTop(100)

        # Create a textbox and label for slide max length
        self.slideMaxLengthInput = QLineEdit()
        self.slideMaxLengthInput.setValidator(intRange)
        self.slideMaxLengthLabel = QLabel()
        self.slideMaxLengthLabel.setText("Max slide length (mm)")

        # Create a textbox and label for slide min length
        self.slideMinLengthInput = QLineEdit()
        self.slideMinLengthInput .setValidator(intRange)
        self.slideMinLengthLabel = QLabel()
        self.slideMinLengthLabel.setText("Min slide length (mm)")

        # Create a textbox and label for slide max speed
        self.slideMaxSpeedInput = QLineEdit()
        self.slideMaxSpeedInput.setValidator(self.maxSpeedRange)
        self.slideMaxSpeedLabel = QLabel()
        self.slideMaxSpeedLabel.setText("Max slide speed (mm/sec)")

        # Create a textbox and label for slide min speed
        self.slideMinSpeedInput = QLineEdit()
        self.slideMinSpeedInput.setValidator(intRange)
        self.slideMinSpeedLabel = QLabel()
        self.slideMinSpeedLabel.setText("Min slide speed before error thrown (mm/sec)")

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
        layout.addWidget(self.updateRaspberryPiButton, 6, 2)
        layout.addWidget(self.resetRaspberryPiButton, 6, 0)
        layout.addWidget(self.importExportProfilesButton, 6, 1)

        # Utilize the layout as a widget
        container = QWidget()
        container.setLayout(layout)

        # Place the layout in the app window
        self.setCentralWidget(container)

    def importExportProfiles(self):
        self.importExportWindow.show()

    # Reset raspberry pi files
    def resetRaspberryPiConfirmation(self):
        resetPiWarning = QDialog()
        resetPiWarning.setWindowTitle("Reset Raspberry Pi")

        warningButtons = QDialogButtonBox.StandardButton.Yes | QDialogButtonBox.StandardButton.No

        # accept and reject connections close the dialog box
        buttonBox = QDialogButtonBox(warningButtons)
        buttonBox.accepted.connect(resetPiWarning.accept)
        buttonBox.rejected.connect(resetPiWarning.reject)

        # Delete the profile only when confirmation is accepted
        buttonBox.accepted.connect(self.resetRaspberryPi)

        resetPiWarning.layout = QVBoxLayout()
        resetPiWarning.layout.addWidget(QLabel("Only use this command if your device is having errors running.\nPlease confirm."))
        resetPiWarning.layout.addWidget(buttonBox)
        resetPiWarning.setLayout(resetPiWarning.layout)

        resetPiWarning.exec()

    def resetRaspberryPi(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
        try:
            ssh.connect(self.RASPBERRYPIPATH, username="pi", password="raspberry", timeout=10)
        except Exception as error:
            print(error)
            self.generateWarningDialog("Raspberry Pi not found", "Raspberry Pi not found")
            ssh.close()
            return
        sftp = ssh.open_sftp()
        zipTest = "zipTest"
        stdin, stdout, stderr = ssh.exec_command("ls")
        if (zipTest + "\n") in stdout.readlines():
            print("Deleting files")
            ssh.exec_command("rm -rf " + zipTest)
            time.sleep(3)
            
        print("Transferring new zipped files")
        zippedFilesPath = str(Path(__file__).parent) + "/" + zipTest + ".zip"
        sftp.put(zippedFilesPath, zipTest + ".zip")
        print("Unzipping files")
        stdin, stdout, stderr = ssh.exec_command("unzip " + zipTest)
        print("fin")
        

    # Exports profiles to the raspberry pi
    def exportProfilesToRaspberryPi(self):
        profilesPath = str(Path(__file__).parent) + "/.profiles.txt"
        ssh = paramiko.SSHClient()
        ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
        try:
            ssh.connect(self.RASPBERRYPIPATH, username="pi", password="raspberry", timeout=10)
        except:
            self.generateWarningDialog("Raspberry Pi not found", "Raspberry Pi not found")
            ssh.close()
            return
        sftp = ssh.open_sftp()
        if os.path.isfile(profilesPath):
            sftp.put(profilesPath, "profiles.txt")
        else:
            print("no profiles to export")
        sftp.close()
        ssh.close()

    # Imports profiles from the raspberry pi
    def importProfilesFromRaspberryPi(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(self.RASPBERRYPIPATH, username="pi", password="raspberry", timeout=10)
        except:
            self.generateWarningDialog("Raspberry Pi not found", "Raspberry Pi not found")
            ssh.close()
            return
        sftp = ssh.open_sftp()
        try:
            sftp.get("profiles.txt", "tempProfiles.txt")
        except:
            self.generateWarningDialog("Missing profiles", "No profiles file on hardware.\nPlease export to the hardware before importing.")
            sftp.close()
            ssh.close()
            return
        sftp.close()
        ssh.close()
        fname = "tempProfiles.txt"
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
        os.remove(fname)

    # Updates Raspberry Pi Settings
    def updateRaspberryPi(self):
        maxSlideLength = self.slideMaxLengthInput.text()
        maxSlideSpeed = self.slideMaxSpeedInput.text()
        valid = self.maxSpeedRange.validate("30", 0)[0]
        if self.maxSpeedRange.validate(maxSlideSpeed, 0)[0] != valid:
            self.generateWarningDialog("Invalid max slide speed", "Slide speed must be between 10-100")
            return
        settings = [maxSlideLength, "\n", maxSlideSpeed]
        ssh = paramiko.SSHClient()
        try:
            ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
            ssh.connect(self.RASPBERRYPIPATH, username="pi", password="raspberry", timeout=10)
        except:
            self.generateWarningDialog("Raspberry Pi not found", "Raspberry Pi not found")
            ssh.close()
            return
        configFile = open("config.txt", "x")
        configFile.writelines(settings)
        configFile.close()
        sftp = ssh.open_sftp()
        if os.path.isfile("config.txt"):
            print("listing dir")
            sftp.listdir(path="/..")
            sftp.put("config.txt", "./config.txt")
        else:
            print("wtf")
        sftp.close()
        ssh.close()
        os.remove("config.txt")

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
        defaultProfilesPath = str(Path(__file__).parent) + "/.profiles.txt"
        self.profiles = self.readProfilesFromFile(defaultProfilesPath)
        if len(self.profiles) == 0:
            self.profile = InstrumentProfile("Default")
            self.updateProfilesFiles()
        else:
            self.profile = self.profiles[list(self.profiles.keys())[0]]
        self.setTextBoxesToProfile()

    # Reads through the profile save file and constructs all profiles
    def readProfilesFromFile(self, file=str(Path(__file__).parent) + "/.profiles.txt") -> dict[str, InstrumentProfile]:
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
    def updateProfilesFiles(self, file=str(Path(__file__).parent) + "/.profiles.txt"):
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

        
# app = QApplication(sys.argv)

# window = ProfileInputWindow()
# window.show()

# app.exec()