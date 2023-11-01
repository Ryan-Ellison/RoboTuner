
import Note
import sys
from profile import Profile
from datetime import datetime
from functools import cmp_to_key

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
    QVBoxLayout, QApplication
)
from PyQt6.QtGui import QIntValidator


# Subclass QMainWindow to customize application's profile setting menu
class TuningTendencyWindow(QMainWindow):

    def __init__(self) -> None:
        super().__init__()
        # Define the title of the application
        self.setWindowTitle("Tuning Information")

        layout = QGridLayout()
        # Create a button and a variable that tracks if the button is toggled
        note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        octaves = [1, 2, 3, 4, 5, 6, 7, 8]
        count_i = 0
        count_j = 0
        for i in octaves:
            for j in note_names:
                label = QLabel()
                label.setText(j + str(i) + "-")
                layout.addWidget(label, count_i, count_j)
                count_j += 1
            count_i += 1
            count_j = 0

        label = QL

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)


app = QApplication(sys.argv)
window = TuningTendencyWindow()
window.show()

app.exec()