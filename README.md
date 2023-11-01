# RoboTuner
CS307 Group 14 RoboTuner

# Development Requirements
1. Python3
3. python3 -m pip install pyqt6
4. python3 -m pip install pyqtgraph
5. pip install pyinstaller
    For creating desktop application

# Desktop App Generating Command
1. pyinstaller -F -w \--onefile \
   --hidden-import='aubio' \
   --hidden-import='wave' \
   desktopApplication/tabManager.py
