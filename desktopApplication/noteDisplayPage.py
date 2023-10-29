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
    QVBoxLayout,
    QHBoxLayout
)
from pyqtgraph import (
    PlotWidget,
    PlotItem,
    mkPen
)

class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(str, int)
    noteReader = NoteReader()
    note = "~"

    def run(self):
        while True:
            note, tendency = self.noteReader.getNote()
            if note is not None:
                self.note = note
                self.progress.emit(note, tendency)
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

        self.graphWidget = PlotWidget()
        self.graphWidget.setYRange(-50, 50, padding=0.15)
        self.times = [0]
        self.tendencies = [0]
        self.graphWidget.setBackground('w')

        pen = mkPen(color = (255, 255, 255), width = 100000)

        self.dataLine = self.graphWidget.plot(self.times, self.tendencies, pen)

        layout = QHBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.graphWidget)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.thread.start()

    def reportNote(self, note, tendency):
        print("called", note, tendency)
        self.label.setText(note)

        self.times.append(self.times[-1] + 0.1)
        self.tendencies.append(tendency)

        self.dataLine.setData(self.times, self.tendencies)
"""
    def callPitch(self):
        note = self.noteReader.getNote()
        if note is not None:
            self.label.setText(note)
"""
       



