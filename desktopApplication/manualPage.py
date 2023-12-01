
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

        self.setFixedWidth(1000)
        self.setFixedHeight(1000)

        self.tabs = QTabWidget()
        self.index = QWidget()
        self.assembly = QWidget()
        self.configuration = QWidget()
        self.usage = QWidget()
        self.tabs.resize(1000,1000)

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
        self.assemblyLabel.setText("<b>Hardware Testing:</b>")
        self.assembly.layout.addWidget(self.assemblyLabel, 0, 1)
        self.assembly.layout.setRowStretch(0, 0)
        self.assembly.setLayout(self.assembly.layout)

        self.assemblyText = QTextEdit()
        self.assemblyText.append("<b>Hardware Testing Protocol</b>\n")
        self.assemblyText.append("1. Orient the trombone so the movement of the stepper motor and tuning slide is unobstructed.\n")
        self.assemblyText.append("2. Press the button on the raspberry pi three times. The OLED screen should indicate the protocol has started.\n")
        self.assemblyText.append("3. Monitor the OLED screen and the movement of the stepper motor.\n")
        self.assemblyText.append("4. The protocol will then finish and the OLED will read that the protocol has completed.\n")
        self.assemblyText.append("5. The results of the test can then be discerned from the criteria below.\n")
        self.assemblyText.append("\n<b>Success Criteria:</b>\n")
        self.assemblyText.append("• The tuning slide should be pulled in completely and the gold disc should be close to the base of the stepper motor.\n")
        self.assemblyText.append("• The stepper motor should then push the tuning slide out to its maximum extension without the tuning slide disconnecting from the instrument.\n")
        self.assemblyText.append("• The tuning slide should then be pulled in completely and the OLED should read that the protocol has completed.\n")
        self.assemblyText.append("\n<b>Failure Remedies:</b>\n")
        self.assemblyText.append("• Tuning slide is not completely pushed in when the gold disc reaches the stepper motor.")
        self.assemblyText.append("\to The distance between the stepper motor and the tuning slide needs to be increased.\n")
        self.assemblyText.append("• Tuning slide detaches when the stepper motor extends the tuning slide")
        self.assemblyText.append("\to The length of the tuning slide needs to be reduced in user settings\n")
        self.assemblyText.append("• OLED displays resistance error")
        self.assemblyText.append("\to Slide needs to be lubricated")
        self.assemblyText.append("\to The stepper motor needs to be recentered\n")
        self.assemblyText.append("• The stepper motor significantly moves during the maneuvers")
        self.assemblyText.append("\to The Velcro straps supporting the stepper motor need to be tightened.")
        self.assembly.layout.addWidget(self.assemblyText, 1, 1)

        #Component List
        #self.assemblyItemList = QListWidget()
        #self.assemblyItemList.insertItem(0, "List")
        #self.assembly.layout.addWidget(self.assemblyItemList, 1, 0)
        #self.assembly.layout.setRowStretch(1, 25)

        #Assembly Instructions Header
        self.assemblyLabel = QLabel()
        self.assemblyLabel.setText("<b>Hardware Assembly Instructions:</b>")
        self.assembly.layout.addWidget(self.assemblyLabel, 0, 0)
        self.assembly.layout.setRowStretch(0, 0)

        #Hardware Assembly Instructions
        self.assemblyText = QTextEdit()
        self.assemblyText.append("1. Attach the top of the upper connection component to an attachment piece. These pieces use a friction fit to stay together so it should require some effort to combine them.\n")
        self.assemblyText.append("2. Remove the tuning slide.\n")
        self.assemblyText.append("3. Use the Velcro straps on the attachment piece to secure the combined attachment piece and connection component to the straight bar on the tuning slide. Tighten the Velcro as much as possible and check it cannot move freely.\n")
        self.assemblyText.append("4. Take the stepper motor and insert it into the stepper motor casing and insert four M3 screws into the holes on top of the casing.\n")
        self.assemblyText.append("5. Attach the motor casing top to the open end of the motor casing and screw four M3 screws into the holes on the motor casing top.\n")
        self.assemblyText.append("6. Attach two attachment pieces to opposing sides of the motor casing. These pieces are a friction fit so should require some effort to fit together.\n")
        self.assemblyText.append("7. Align the golden servo dial with the bottom of the lower connection so two of the opposing holes on the dial line up with the holes on the lower connection. Insert two M3 screws in the holes on the lower connection to secure it to the dial.\n")
        self.assemblyText.append("8. Attach the golden servo dial and lower connection to the motor by twisting the servo dial down the motor’s lead screw until the servo dial is touching the bottom of the lead screw.\n")
        self.assemblyText.append("9. Manually twist the lead screw so that the lower connection is aligned with the trombone.\n")
        self.assemblyText.append("10. Attach the servo motor assembly to the trombone using the Velcro straps. Align the lower connection so that it straddles the bar. The end of the lead screw on the stepper motor should be roughly half an inch away from the bar. Wrap the four Velcro straps (two on each connection) around the bars on either side such that the servo is tautly suspended in the center of the two bars and the lead screw is parallel to the bars.\n")
        self.assemblyText.append("11. Insert the tuning slide all the way and such that the upper connection fits within the lower connection. The notches on the side of the upper and lower connections should line up, if they do not pull the tuning slide out until this is the case.\n")
        self.assemblyText.append("12. Push a key through a notch on the lower connection that is aligned with a notch on the upper connection. The keys flanges should touch the outer wall of the lower connection. Insert one key on each side.\n")
        self.assemblyText.append("13. Open the raspberry pi box by removing the screws from the four corners\n")
        self.assemblyText.append("14. Take the cable exiting from the bottom of the stepper motor and plug that into the raspberry pi. Fit the wire into the wide and thin gap in the lip of the box.\n")
        self.assemblyText.append("15. Reattach the same four screws to the raspberry pi box and secure as tightly as possible.\n")
        self.assemblyText.append("16. Attach the electronics attachments to the raspberry pi box and battery box.\n")
        self.assemblyText.append("17. Attach the raspberry pi box and battery box using the attachments to any point on the trombone that the length of the wires allows using the two Velcro straps on each attachment.\n")
        self.assemblyText.append("18. Follow the steps below to test that the hardware is successfully attached.\n")
                                
        self.assembly.layout.addWidget(self.assemblyText, 1, 0)
        self.assembly.layout.setRowStretch(1, 2)
        self.assembly.layout.setRowStretch(2, 1)





'''app = QApplication(sys.argv)
window = ManualWindow()
window.show()

app.exec()'''