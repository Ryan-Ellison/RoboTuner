import json
import os.path
import sys
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



# Subclass QMainWindow to customize application's profile setting menu
class TuningTendencyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Define the title of the application
        self.setWindowTitle("Tuning Information")
        file_name = str(sys.path[0]) + "/notes.json"
        file = open(file_name, "r")
        file_content = file.read()
        self.notesDict = json.loads(file_content)


        allLayout = QGridLayout()
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
        self.computeAverage.setLayout(self.computeAverage.layout)

        mainLayout.addWidget(self.tabs)
        self.setLayout(mainLayout)

        self.setCentralWidget(self.tabs)
    def computeAverageRange(self):
        print("Success")
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


"""
app = QApplication(sys.argv)
window = TuningTendencyWindow()
window.show()

app.exec()
"""