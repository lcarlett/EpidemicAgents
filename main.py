import sys
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import Qt
from Desease import Desease
#from movingGrid import Grid
from staticHexGrid import Grid
from staticNetwork import Network

app = QApplication(sys.argv)
# good medium values Desease(1/8, 0.05), 100 base infected
#grid = Grid(size = (50,100), cell_size = 10, base_infected = 100 , base_immune = 0, desease = Desease(1/18, 0.20, None), sec_between_frame = .2)

#grid = Grid(size = (90, 90), number_agents = 2000, base_infected = 100 , base_immune = 0, desease = Desease(1/6,0.15,15), startAnimate = True)    

grid = Network(size = (800, 800), number_agents = 100, base_connections = 2, rewiring = 0.2, base_infected = 100 , base_immune = 20, desease = Desease(1/3, 0.2, None))

grid.view().keyPressEvent = lambda e: grid.handleKeyPressed(e, Qt.Key_Space)
grid.view().show()

#    QMessageBox.information(grid.view(), 'Epidemic Agents', 'Press space to pause and resume')

sys.exit(app.exec_())   
