#!/usr/bin/env python3

import sys
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import Qt
from Desease import Desease
from movingGrid import Grid as GGrid
from staticHexGrid import Grid as HGrid
from staticNetwork import Network
from epidemicAgents import Agent
from Display import Display

app = QApplication(sys.argv)
# good medium values Desease(1/8, 0.05), 100 base infected
#grid = HGrid(QParent = None, size = (750,1500), number_agents = 5000, base_infected = 100 , base_immune = 0, desease = Desease(1/18, 0.20), sec_between_frame = .2)

#grid = GGrid(QParent = None, size = (800, 800), number_agents = 2000, base_infected = 100 , base_immune = 0, desease = Desease(1/6,0.15,15), startAnimate = True, sec_between_frame = .05)    

#grid = Network(QParent = None, size = (800, 800), number_agents = 500, base_connections = 2, rewiring = 0.1, base_infected = 10 , base_immune = 20, desease = Desease(1/6, 0), sec_between_frame = .1)

#grid.keyPressEvent = lambda e: grid.handleKeyPressed(e, Qt.Key_Space)
#grid.show()
d = Display("Epidemic Agents")
#    QMessageBox.information(grid.view(), 'Epidemic Agents', 'Press space to pause and resume')

sys.exit(app.exec_())   
