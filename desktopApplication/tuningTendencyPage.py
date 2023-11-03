import json
import os.path
import sys
from pathlib import Path
pyaudioPath = str(Path(__file__).parent.parent) + "/raspi"
print("path = " + pyaudioPath)
sys.path.insert(0, pyaudioPath)
print("path = " + str(sys.path))
import Tuner



from PyQt6.QtWidgets import (
    QMainWindow,
    QLabel,
    QGridLayout,
    QWidget,
    QApplication
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

        layout = QGridLayout()
        # Create a button and a variable that tracks if the button is toggled
        note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        octaves = [1, 2, 3, 4, 5, 6, 7, 8]
        count_i = 0
        count_j = 0
        for note in notesDict:
            print(note)
            label = QLabel()
            label.setText(" " + note + " - " + str(round(notesDict[note], 3)))
            layout.addWidget(label, count_i // 8, count_j % 8)
            count_i += 1
            count_j += 1
        """
        for i in octaves:
            for j in note_names:
                label = QLabel()
                label.setText(j + str(i) + "-")
                layout.addWidget(label, count_i, count_j)
                count_j += 1
            count_i += 1
            count_j = 0
        """

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

"""
app = QApplication(sys.argv)
window = TuningTendencyWindow()
window.show()

app.exec()
"""