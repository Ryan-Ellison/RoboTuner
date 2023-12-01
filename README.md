# RoboTuner
CS307 Group 14 RoboTuner

# Development Requirements
1. Python3
3. python3 -m pip install pyqt6
4. python3 -m pip install pyqtgraph
5. python3 -m pip install pyinstaller
       For creating desktop application
7. python3 -m pip install paramiko

# Desktop App Generating Command
1. pyinstaller -F -w --onefile --noconfirm \\
--hidden-import='aubio' \\
--hidden-import='wave' \\
--hidden-import='raspi/Tuner.py' \\
desktopApplication/tabManager.py