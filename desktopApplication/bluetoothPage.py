import sys

from PyQt6 import QtBluetooth
from PyQt6.QtBluetooth import (
    QBluetoothDeviceDiscoveryAgent,
    QBluetoothDeviceInfo
)
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTabWidget,
    QVBoxLayout,
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
    QFileDialog,
)

class bluetoothPage(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("RoboTuner")
        
        self.discoveryAgent = QBluetoothDeviceDiscoveryAgent(self)
        self.discoveryAgent.deviceDiscovered.connect(self.addItem)
        self.discoveryAgent.finished.connect(self.scanFinished)
        self.discoveryAgent.canceled.connect(self.scanFinished)

        self.discoverBluetoothButton = QPushButton("Discover Bluetooth")
        self.discoverBluetoothButton.clicked.connect(self.startDiscoveryService)
        self.stopSearchingBluetooth = QPushButton("Stop Bluetooth search")
        self.stopSearchingBluetooth.clicked.connect(self.endDiscoveryService)

        self.btDevices = []
        
        layout = QVBoxLayout()
        layout.addWidget(self.discoverBluetoothButton)
        layout.addWidget(self.stopSearchingBluetooth)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

    def startDiscoveryService(self):
        self.btDevices.clear()
        self.discoveryAgent.start(QBluetoothDeviceDiscoveryAgent.DiscoveryMethod(1))
        print("starting search")


    def addItem(self, device):
        self.btDevices.append(QBluetoothDeviceInfo(device))
        print("item found")

    def scanFinished(self):
        for device in self.btDevices:
            #QtBluetooth.QBluetoothDeviceInfo.
            print('UUID: {UUID}, Name: {name}, rssi: {rssi}'.format(UUID=device.deviceUuid().toString(),
                                                                    name=device.name(),
                                                                    rssi=device.rssi()))
            if device.name() == "raspberrypi":
                print("yurrrr")

    def endDiscoveryService(self):
        self.discoveryAgent.stop()
        print("search fin")


app = QApplication(sys.argv)

window = bluetoothPage()
window.show()

app.exec()