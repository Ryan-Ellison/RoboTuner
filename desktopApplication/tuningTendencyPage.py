import json
import os.path
import sys
from tkinter import *
from datetime import date, datetime
from pathlib import Path

pyaudioPath = str(Path(__file__).parent.parent) + "/raspi"
print("path = " + pyaudioPath)
sys.path.insert(0, pyaudioPath)
print("path = " + str(sys.path))
#import Tuner

from PyQt6.QtWidgets import (
    QMainWindow,
    QLabel,
    QGridLayout,
    QWidget,
    QApplication, QTabWidget, QLineEdit, QPushButton, QFrame,
)
from PyQt6.QtGui import QFont

file = str(sys.path[0]) + "/notes.json"
# Subclass QMainWindow to customize application's profile setting menu
class TuningTendencyWindow(QMainWindow):
    def __init__(self):
        global file
        print(str(file))
        super().__init__()
        # Define the title of the application
        self.numSaved = 0
        self.setWindowTitle("Tuning Information")
        #self.file_name = str(sys.path[0]) + "/notes.json"
        file_json = open(file, "r")
        file_content = file_json.read()
        self.notesDict = json.loads(file_content)


        allLayout = QGridLayout()
        allLayout.setHorizontalSpacing(0)
        allLayout.setVerticalSpacing(0)
        # Create a button and a variable that tracks if the button is toggled
        note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        octaves = [1, 2, 3, 4, 5, 6, 7, 8]
        count_i = 0
        count_j = 0
        avgTendency = 0
        for note in self.notesDict:
            print(note)
            label = QLabel()
            label.setText(" " + note + " - " + str(round(self.notesDict[note], 3)))
            font = QFont("Times", 12)


            label.setFixedSize(125, 30)
            label.setFont(font)
            frame = QFrame()
            frame.setFixedSize(100,12)
            label.setFrameStyle(QFrame.Shape.Panel)
            avgTendency += round(self.notesDict[note], 3)
            allLayout.addWidget(label, count_i % 12, count_j // 12)
            count_i += 1
            count_j += 1

        avgTendency /= len(self.notesDict)
        mainLayout = QGridLayout()
        self.all = QWidget()
        self.computeAverage = QWidget()
        self.tabs = QTabWidget()

        self.tabs.addTab(self.all, "Tuning Tendencies")
        self.tabs.addTab(self.computeAverage, "Compute Averages")
        self.setLayout(mainLayout)

        self.all.layout = allLayout
        self.all.setLayout(self.all.layout)

        self.avgTendencyLabel = QLabel()
        self.avgTendencyLabel.setFixedHeight(16)
        self.avgTendencyLabel.setText("Average Tendency = " + str(avgTendency))

        self.lowBoxLabel = QLabel()
        self.lowBoxLabel.setFixedHeight(16)
        self.highBoxLabel = QLabel()
        self.highBoxLabel.setFixedHeight(16)

        self.lowBoxLabel.setText("From:")
        self.highBoxLabel.setText("To:")

        self.computeTendencyBoxLow = QLineEdit()
        self.computeTendencyBoxLow.setFixedHeight(16)
        self.computeTendencyBoxLow.setText("C1")
        self.computeTendencyBoxHigh = QLineEdit()
        self.computeTendencyBoxHigh.setFixedHeight(16)
        self.computeTendencyBoxHigh.setText(("B8"))
        self.computeTendencyButton = QPushButton()
        self.computeTendencyButton.setFixedHeight(25)
        self.computeTendencyButton.setText("Compute")
        self.computeTendencyButton.clicked.connect(self.computeAverageRange)

        self.saveButton = QPushButton()
        self.saveButton.setFixedHeight(25)
        self.saveButton.setText("Save")
        self.saveButton.clicked.connect(self.saveTuningInfo)

        self.averageRangeTendency = QLabel()
        self.averageRangeTendency.setFixedHeight(16)
        self.averageRangeTendency.setText("Average Tendency for Range "
                                          + self.computeTendencyBoxLow.text()
                                          + " -> "
                                          + self.computeTendencyBoxHigh.text()
                                          + " is: ")

        self.computeAverage.layout = QGridLayout()
        self.computeAverage.layout.addWidget(self.avgTendencyLabel, 0, 0)
        self.computeAverage.layout.addWidget(self.averageRangeTendency, 1, 0)
        self.computeAverage.layout.addWidget(self.lowBoxLabel, 2, 0)
        self.computeAverage.layout.addWidget(self.computeTendencyBoxLow, 3, 0)
        self.computeAverage.layout.addWidget(self.highBoxLabel, 4, 0)
        self.computeAverage.layout.addWidget(self.computeTendencyBoxHigh, 5, 0)
        self.computeAverage.layout.addWidget(self.computeTendencyButton, 6, 0)
        self.computeAverage.layout.addWidget(self.saveButton, 7, 0)
        i = 0
        directory = os.fsencode("savedTuningInformation")

        for file_json in os.listdir(directory):
            filename = os.fsdecode(file_json)
            self.button = QPushButton()
            self.button.setFixedHeight(25)
            self.button.setText(filename)
            self.button.clicked.connect(lambda: self.loadTuning(self.button.text()))
            self.computeAverage.layout.addWidget(self.button, 8 + i, 0)
            i += 1
        self.computeAverage.setLayout(self.computeAverage.layout)

        mainLayout.addWidget(self.tabs)
        self.setLayout(mainLayout)

        self.setCentralWidget(self.tabs)
    def computeAverageRange(self):
        low = self.computeTendencyBoxLow.text()
        high = self.computeTendencyBoxHigh.text()

        reachedLow = False
        sum = 0.0
        totalNotes = 0.0
        print(self.notesDict)
        for key in self.notesDict:
            if key == high:
                break
            if key == low:
                reachedLow = True

            if reachedLow:
                if (not self.notesDict[key] == 0):
                    sum += self.notesDict[key]
                    totalNotes += 1

        self.averageRangeTendency.setText("Average Tendency for Range: "
                                          + self.computeTendencyBoxLow.text()
                                          + " -> "
                                          + self.computeTendencyBoxHigh.text()
                                          + " is: "
                                          + str((sum / totalNotes)))

    def saveTuningInfo(self):
        if (self.numSaved > 4):
            return

        file = open("savedTuningInformation/tuning-" + str(date.today()) + "-" + str(datetime.now()) + ".json",  "w")

        json_format = json.dumps(self.notesDict, indent=4)

        for line in json_format:
            file.write(line)

        file.close()
        self.numSaved = 0

    def loadTuning(self, toLoad):
        print("Pressed" + toLoad)
        file_json = open("savedTuningInformation/" + toLoad, "r")
        file_content = file_json.read()
        self.notesDict = json.loads(file_content)
        file_json.close()


        json_format = json.dumps(self.notesDict, indent=4)
        global file
        print("da path = " + str(file))
        newFile = open(file, "w")
        for line in json_format:
            newFile.write(line)

        newFile.close()
        os.execl(sys.executable, sys.executable, *sys.argv)





"""
app = QApplication(sys.argv)
window = TuningTendencyWindow()
window.show()

app.exec()
"""