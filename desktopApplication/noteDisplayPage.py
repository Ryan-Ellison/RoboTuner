import sys
from profile import Profile
from datetime import datetime
from functools import cmp_to_key
from noteReader import NoteReader
import time

from PyQt6.QtCore import (
    QTimer,
    QObject,
    QThread,
    pyqtSignal
)
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

class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(str)
    noteReader = NoteReader()
    note = "~"

    def run(self):
        while True:
            note = self.noteReader.getNote()
            print(note)
            if note is not None:
                self.note = note
                self.progress.emit(note)
                time.sleep(0.1)


class NoteDisplayPage(QMainWindow):
    def __init__(self):
        super().__init__()

        self.label = QLabel("Play a note")

        self.thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.finished.connect(self.thread.deleteLater)
        self.worker.progress.connect(self.reportNote)

        self.thread.finished.connect(
            lambda: self.label.setText("Play a note")
        )

        self.setCentralWidget(self.label)

        self.thread.start()

    def reportNote(self, note):
        print("called", note)
        self.label.setText(note)
"""
    def callPitch(self):
        note = self.noteReader.getNote()
        if note is not None:
            self.label.setText(note)
"""
       



