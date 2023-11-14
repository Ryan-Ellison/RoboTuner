import sys
import os

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QVBoxLayout
)

class HardwareSpecificationsPage(QMainWindow):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.raspberryPiVersionLabel = QLabel("Raspberry Pi 3b is used")
        self.raspberryPiDimensionsLabel = QLabel("Raspberry Pi Dimensions: 3.35″ x 2.2″ x 0.8″")
        self.motorVersionLabel = QLabel("Motor: Iverntech NEMA 17 Stepper Motor")
        self.batteryLabel = QLabel("Battery: Rechargeable NiMH Battery Pack")
        self.portableChargerLabel = QLabel("Portable Charger: EAFU Portable Charger, Compact 10000mAh USB C Power Bank")
        self.soundAdapterLabel = QLabel("Sound Adapter: SABRENT USB External Stereo Sound Adapter")
        self.totalWeightLabel = QLabel("Total weight: 946.251g")
        self.batteryChargingPortLabel = QLabel("Battery charging port: USB-C")
        self.batteryLifeLabel = QLabel("Battery Life: 3+ Hours")

        layout.addWidget(self.raspberryPiVersionLabel)
        layout.addWidget(self.raspberryPiDimensionsLabel)
        layout.addWidget(self.motorVersionLabel)
        layout.addWidget(self.batteryLabel)
        layout.addWidget(self.portableChargerLabel)
        layout.addWidget(self.soundAdapterLabel)
        layout.addWidget(self.totalWeightLabel)
        layout.addWidget(self.batteryChargingPortLabel)
        layout.addWidget(self.batteryLifeLabel)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)