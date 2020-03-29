#!/usr/bin/env python3

import sys
from PyQt5.QtWidgets import QApplication
sys.path.append("Pythonapp/")
from Display import Display

app = QApplication(sys.argv)
d = Display("Epidemic Agents")

sys.exit(app.exec_())   
