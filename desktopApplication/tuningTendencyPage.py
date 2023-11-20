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
    QApplication, QTabWidget, QLineEdit, QPushButton
)
from PyQt6.QtGui import QIntValidator


# Subclass QMainWindow to customize application's profile setting menu
class TuningTendencyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Define the title of the application
        self.setWindowTitle("Tuning Information")
        file_name = str(sys.path[0]) + "/notes.json"
        file = open(file_name, "r")
        file_content = file.read()
        notesDict = json.loads(file_content)


        allLayout = QGridLayout()
        # Create a button and a variable that tracks if the button is toggled
        note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        octaves = [1, 2, 3, 4, 5, 6, 7, 8]
        count_i = 0
        count_j = 0
        avgTendency = 0
        for note in notesDict:
            print(note)
            label = QLabel()
            label.setText(" " + note + " - " + str(round(notesDict[note], 3)))
            avgTendency += round(notesDict[note], 3)
            allLayout.addWidget(label, count_i // 8, count_j % 8)
            count_i += 1
            count_j += 1

        avgTendency /= len(notesDict)
        mainLayout = QGridLayout()
        self.all = QWidget()
        self.computeAverage = QWidget()
        self.tabs = QTabWidget()

        self.tabs.addTab(self.all, "Tuning Tendencies")
        self.tabs.addTab(self.computeAverage, "Compute Averages")
        self.setLayout(mainLayout)

        self.all.layout = allLayout
        self.all.setLayout(self.all.layout)

        avgTendencyLabel = QLabel()
        avgTendencyLabel.setText("Average Tendency = " + str(avgTendency))

        averageRangeTendency = QLabel()
        averageRangeTendency.setText("Average Tendency = ")

        computeTendencyBoxLow = QLineEdit()
        computeTendencyBoxLow.setText("From")
        computeTendencyBoxHigh = QLineEdit()
        computeTendencyBoxHigh.setText(("To"))
        computeTendencyButton = QPushButton()
        computeTendencyButton.setText("Compute")





        self.computeAverage.layout = QGridLayout()
        self.computeAverage.layout.addWidget(avgTendencyLabel)
        self.computeAverage.layout.addWidget(computeTendencyBoxLow)
        self.computeAverage.layout.addWidget(computeTendencyBoxHigh)
        self.computeAverage.layout.addWidget(computeTendencyButton)
        self.computeAverage.layout.addWidget(averageRangeTendency)
        self.computeAverage.setLayout(self.computeAverage.layout)

        mainLayout.addWidget(self.tabs)
        self.setLayout(mainLayout)

        self.setCentralWidget(self.tabs)

"""
app = QApplication(sys.argv)
window = TuningTendencyWindow()
window.show()

app.exec()
"""