import sys
from profile import Profile
from datetime import datetime
from functools import cmp_to_key
from noteReader import NoteReader

from PyQt6.QtCore import QTimer
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
    QVBoxLayout
)

class NoteDisplayPage(QMainWindow):
    def __init__(self):
        super().__init__()

        self.label = QLabel("test")
        self.noteReader = NoteReader()

        self.setCentralWidget(self.label)

    def callPitch(self):
        print("called")
        note = self.noteReader.getNote()
        if note is not None:
            self.label.setText(note)
       
       



