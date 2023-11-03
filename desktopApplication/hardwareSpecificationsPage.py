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

        self.raspberryPiDimensionsLabel = QLabel("Raspberry Pi Dimensions: 3.35″ x 2.2″ x 0.8″")
        self.totalWeightLabel = QLabel("Total weight: 946.251g")
        self.batteryChargingPortLabel = QLabel("Battery charging port: USB-C")
        self.batteryLifeLabel = QLabel("Battery Life: 3+ Hours")

        layout.addWidget(self.raspberryPiDimensionsLabel)
        layout.addWidget(self.totalWeightLabel)
        layout.addWidget(self.batteryChargingPortLabel)
        layout.addWidget(self.batteryLifeLabel)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)