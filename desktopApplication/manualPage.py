
import sys

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
    QVBoxLayout, QApplication, QTabWidget,
    QDockWidget,
    QListWidget,
    QTextEdit,
    QScrollArea 
)
from PyQt6.QtGui import QIntValidator
from PyQt6.QtCore import Qt


# Subclass QMainWindow to customize application's profile setting menu
class ManualWindow(QMainWindow):

    def __init__(self) -> None:
        super().__init__()
        # Define the title of the application
        self.setWindowTitle("Manual")

        layout = QGridLayout()

        #self.setFixedWidth(1000)
        #self.setFixedHeight(1000)

        self.tabs = QTabWidget()
        self.index = QWidget()
        self.assembly = QWidget()
        self.configuration = QWidget()
        self.usage = QWidget()
        #self.tabs.resize(1000,1000)

        self.indexLabel = QLabel()
        self.indexLabel.setText("Hello There!")

        self.tabs.addTab(self.index, "Index")
        self.tabs.addTab(self.assembly, "Assembly")
        self.tabs.addTab(self.configuration, "Configuration")
        self.tabs.addTab(self.usage, "Usage")

        #add content to index tab
        self.index.layout = QGridLayout()
        self.indexLabel = QLabel()
        self.indexLabel.setText("Hello There!")
        self.index.layout.addWidget(self.indexLabel)
        self.index.setLayout(self.index.layout)

        #add content to usage tab
        self.usage.layout = QGridLayout()
        self.usageContent = QLabel()
        self.usageContent.setText("""
            1. Turning on the RoboTuner
                - When turning on the device, it will first auto home by moving the tuning slide into the instrument
                - The display will show when it is homing and show once it is ready for you to start playing
                - Make sure to attach the the contact mic to the horn of your instrument
                                  
            2. Modes
                - Switch between modes by press and holding the button for 2 seconds
                                  
                a. Auto Tuning Mode
                    - The device will always start in this mode on startup
                    - This mode will automatically move the tuning slide according to how many cents off the current tuning is
                    - While in this mode, the device will shine red and stop moving if it detects too much resistance in the tuning slide
                        - If this happens, please grease your tuning slide and restart the device
                b. Reference Pitch Mode
                    - This mode will play a reference pitch shortly after a note is played so the user can adjust the tuning slide manually
                                  
            3. Hardware Check
                - Triple click the button within 5 seconds and the device will perform a hardware check by pulling the tuning slide all
                    the way in, then pushing it out all the way, and pulling it back in again. If this works properly the tuning slide
                    won't pop out and the device will be ready to use!
                                  
        """)
        self.usageContent.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.usage.layout.addWidget(self.usageContent)
        self.usage.setLayout(self.usage.layout)

        layout.addWidget(self.tabs)
        self.setLayout(layout)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        #add content to assembly tab
        self.assembly.layout = QGridLayout()

        #Component List Header
        self.assemblyLabel = QLabel()
        self.assemblyLabel.setText("<b>List of Components:</b>")
        self.assembly.layout.addWidget(self.assemblyLabel, 0, 0)
        self.assembly.layout.setRowStretch(0, 0)
        self.assembly.setLayout(self.assembly.layout)

        self.assemblyText = QTextEdit()
        self.assemblyText.append("Hello")
        self.assembly.layout.addWidget(self.assemblyText, 1, 1)

        #Component List
        self.assemblyItemList = QListWidget()
        self.assemblyItemList.insertItem(0, "List")
        self.assembly.layout.addWidget(self.assemblyItemList, 1, 0)
        self.assembly.layout.setRowStretch(1, 25)

        #Assembly Instructions Header
        self.assemblyLabel = QLabel()
        self.assemblyLabel.setText("<b>Hardware Assembly Instructions:</b>")
        self.assembly.layout.addWidget(self.assemblyLabel, 2, 0)
        self.assembly.layout.setRowStretch(0, 0)

        #Hardware Assembly Instructions
        self.assemblyText = QTextEdit()
        self.assemblyText.append("1. Scream incredibly loung\n2. Probably start crying\n3. Finish crying and get a move on")
        self.assembly.layout.addWidget(self.assemblyText, 3, 0)
        self.assembly.layout.setRowStretch(3, 50)





'''app = QApplication(sys.argv)
window = ManualWindow()
window.show()

app.exec()'''