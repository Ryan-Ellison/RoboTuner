import sys
import os
from instrumentProfiles import InstrumentProfile
from datetime import datetime
from functools import cmp_to_key
from pathlib import Path
import paramiko
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
    QHBoxLayout,
    QFileDialog,
    QApplication,
    QButtonGroup,
    QRadioButton
)

class ImportExportWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.exportProfileButton = QPushButton("Export Profiles To Desktop")
        self.importProfileButton = QPushButton("Import Profiles From Desktop")
        self.exportProfilesToRPButton = QPushButton("Export Profiles To Device")
        self.importProfilesFromRPButton = QPushButton("Import Profiles From Device")

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
        self.importExportLabel = QLabel("Action")
        self.importRadio = QRadioButton("Import Profiles", self)
        self.exportRadio = QRadioButton("Export Profiles", self)

        actionColumn = QVBoxLayout()
        actionColumn.addWidget(self.importExportLabel)

        actions = [self.importRadio, self.exportRadio]
        for action in actions:
            self.importExportGroup.addButton(action)
            actionColumn.addWidget(action)

        layout = QHBoxLayout()
        layout.addLayout(connectionColumn)
        layout.addLayout(actionColumn)

        # Utilize the layout as a widget
        container = QWidget()
        container.setLayout(layout)

        # Place the layout in the app window
        self.setCentralWidget(container)

app = QApplication(sys.argv)

window = ImportExportWindow()
window.show()

app.exec()
