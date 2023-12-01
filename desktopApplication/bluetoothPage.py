import sys

from PyQt6 import QtBluetooth as PyQtBt
from PyQt6.QtBluetooth import (
    QBluetoothDeviceDiscoveryAgent,
    QBluetoothDeviceInfo,
    QBluetoothSocket,
    QBluetoothServiceInfo,
    QBluetoothAddress
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
        self.discoveryAgent.setLowEnergyDiscoveryTimeout(5000)
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
        print("search fin")
        for device in self.btDevices:
            print('UUID: {UUID}, Name: {name}, rssi: {rssi}'.format(UUID=device.deviceUuid().toString(),
                                                                    name=device.name(),
                                                                    rssi=device.rssi()))
            if device.name() == "raspberrypi":
                print("\n\n!!rp found!!!\n\n")
                self.connectToPi(device)
                break

    def connectToPi(self, device):
        self.sock = QBluetoothSocket(QBluetoothServiceInfo.Protocol(2))

        self.sock.connected.connect(self.connectedToBluetooth)
        #self.sock.readyRead.connect(self.receivedBluetoothMessage)
        self.sock.disconnected.connect(self.disconnectedFromBluetooth)
        self.sock.errorOccurred.connect(self.socketError)
        for address in PyQtBt.QBluetoothLocalDevice(self).connectedDevices():
            if address.toString().strip() == "B8:27:EB:6C:CE:50":
                print("Already connected")

        port = 1025
        print(device.address().toString())
        rpGeneralAccessUuid = "{00001801-0000-1000-8000-00805f9b34fb}"
        idx = 0
        for i in range(len(device.serviceUuids())):
            if rpGeneralAccessUuid == device.serviceUuids()[i].toString():
                idx = i
                print("idx: ", idx)
                break
        self.sock.connectToService(device.address(), device.serviceUuids()[idx])

    def connectedToBluetooth(self):
        print("connected")
        try:
            self.sock.write("test".encode())
            print("success")
        except Exception as error:
            print("\n\n", error, "\n\n")
            print("error sending")
        print("disconnecting post message")
        self.sock.disconnect()
    
    def socketError(self, error):
        print(error)
        print("socket error :(")

    def disconnectedFromBluetooth(self):
        print("disconnected :/")

    def endDiscoveryService(self):
        self.discoveryAgent.stop()


# app = QApplication(sys.argv)

# window = bluetoothPage()
# window.show()

# app.exec()