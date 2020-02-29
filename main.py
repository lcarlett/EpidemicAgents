import sys
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import Qt
from Desease import Desease
from movingGrid import Grid
#from staticHexGrid import Grid

app = QApplication(sys.argv)
# good medium values Desease(1/8, 0.05), 100 base infected
#grid = Grid(size = (50,100), cell_size = 10, base_infected = 100 , base_immune = 0, Desease(1/8, 0.05), sec_between_frame = .2)

grid = Grid(size = (30, 30), number_agents = 2000, base_infected = 100 , base_immune = 1600, desease = Desease(1/8,0), startAnimate = True)    

grid.view().keyPressEvent = lambda e: grid.handleKeyPressed(e, Qt.Key_Space)
grid.view().show()
#    QMessageBox.information(grid.view(), 'Epidemic Agents', 'Press space to pause and resume')
sys.exit(app.exec_())   
