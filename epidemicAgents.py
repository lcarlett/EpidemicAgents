import sys
from PyQt5.QtWidgets import QWidget, QApplication, QGraphicsScene, QGraphicsEllipseItem, QGraphicsView, QMessageBox
from PyQt5.QtGui import QPen, QColor, QBrush
from PyQt5.QtCore import Qt, pyqtSlot, QSize, QTimer
from random import choice, randint, random
from time import sleep

class Desease(object):
    Sane, Infected, Immune = range(3)
    def __init__(self, infectivity, recoverability):
        self.__transmission_rate = infectivity
        self.__recovery_rate = recoverability
        
    def apply_to(self, agent, surrounding):
        inf_neigh = 0
        for neigh in surrounding:
            inf_neigh += neigh.isInfected()
        if agent.isInfected() and random() > self.__transmission_rate*inf_neigh - self.__recovery_rate:
            agent.setSane()
            if random()<.5:
                agent.setImmune()
        elif random() < self.__transmission_rate*inf_neigh*agent.vulnerability():
            agent.setInfected()

class Agent(object):
    SaneColor = (0,0,0)
    InfectedColor = (255, 0, 0)
    ImmuneColor = (0, 255, 0)
    def __init__(self, parent, pos, size, infected = False):
        self.size = lambda: size
        self.__state = Desease.Infected if infected else Desease.Sane
        self.__color = QColor(*(Agent.InfectedColor if infected else Agent.SaneColor))
        self.__parent = parent
        self.pos = lambda: pos
        self.__graphicItem = parent.addEllipse(pos[0], pos[1], self.size(), self.size())
        self.__neighbors = []
        self.__vulnerability = 1
        self.__update()
    
    def __update(self):
        self.__graphicItem.setBrush(QBrush(self.__color))
    
    def isInfected(self):
        return self.__state == Desease.Infected
    
    def setColor(self, color):
        self.__color = QColor(*color)
        self.__update()
    
    def setInfected(self):
        self.__state = Desease.Infected
        self.setColor(Agent.InfectedColor)
    
    def setSane(self):
        self.__state = Desease.Sane
        self.setColor(Agent.SaneColor)
    
    def setImmune(self):
        self.__vulnerability = 0
        self.setColor(Agent.ImmuneColor)
    
    def addNeighbor(self, agent):
        self.__neighbors.append(agent)
        if self not in agent.neighbors():
            agent.addNeighbor(self)
            
    def neighbors(self):
        return self.__neighbors
        
    def vulnerability(self):
        return self.__vulnerability
    
    
class Grid(object):
    n = 1
    def __init__(self, size, cell_size, base_infected, desease, startAnimate = True, sec_between_frame = 1):
        if type(size) == int:
            size = (size, size)
        self.size = lambda: size
        self.cell_size = lambda: cell_size
        self.__canvas = QGraphicsScene()
        self.__agents = []
        self.__desease = desease
        offset = 0
        cell_padding = .3
        for i in range(size[0]):
            for j in range(size[1]):
                self.__agents.append(Agent(self.__canvas, (self.cell_size()*(1+cell_padding)*j + offset + 0*randint(-int(self.cell_size()/2), int(self.cell_size()/2)), self.cell_size()*(1+cell_padding)*((3/4)**(1/2))*i + 0*randint(-int(self.cell_size()/2), int(self.cell_size()/2))), self.cell_size()))
            offset = 0 if offset else (offset+self.cell_size()*(1 + cell_padding)/2)
        for _ in range(base_infected):
            choice(self.__agents).setInfected()
        self.__calculateNeighbors()
        self.__viewObject = QGraphicsView(self.__canvas)
        self.__timer = None
        self.timer_sec = lambda: sec_between_frame
        if startAnimate:
            self.startAnimate(sec_between_frame)
            
    def handleKeyPressed(self, event, key_to_press, sec = None):
        if event.key() == key_to_press:
            if self.__timer:
                self.__stopAnimate()
            else:
                self.startAnimate(sec if sec else self.timer_sec())
    
         
    def startAnimate(self, sec):
        self.__timer = self.__viewObject.startTimer(int(1000*sec))
        self.__viewObject.timerEvent = lambda e: self.time_step()
        self.__viewObject
    
    def __stopAnimate(self):
        self.__viewObject.killTimer(self.__timer)
        self.__timer = None
     
    def view(self):
        return self.__viewObject
    
    def __calculateNeighbors(self):
        for index in range(len(self.__agents)):
            offset = (index%(self.size()[1]*2))//self.size()[1]
            if not (index < self.size()[1] 
                or index%self.size()[1] == 0 
                or (index+1)%self.size()[1] == 0 
                or index >= (self.size()[0]-1)*self.size()[1]):
# If not on side, else it will be added by the reciprocity of addNeighbor
                self.__agents[index].addNeighbor(self.__agents[index + 1])
                self.__agents[index].addNeighbor(self.__agents[index - 1])
                self.__agents[index].addNeighbor(self.__agents[index - self.size()[1] + 2*offset - 1])
                self.__agents[index].addNeighbor(self.__agents[index - self.size()[1]])
                self.__agents[index].addNeighbor(self.__agents[index + self.size()[1] + 2*offset - 1])
                self.__agents[index].addNeighbor(self.__agents[index + self.size()[1]])

    def time_step(self):
        for agent in self.__agents:
            self.__desease.apply_to(agent, agent.neighbors())
        
    def tell(self, num):
        n = self.__agents[num].neighbors()
        self.__agents[num].setColor((255,0,255))
        for nn in n:
             nn.setColor((0,0,255))
    
    def noTell(self, num):
        n = self.__agents[num].neighbors()
        self.__agents[num].setColor((0,0,0))
        for nn in n:
            nn.setColor((0,0,0))
    
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    grid = Grid((50,100), 10, 7, Desease(1/6, 0.1), sec_between_frame = .3)
    grid.view().keyPressEvent = lambda e: grid.handleKeyPressed(e, Qt.Key_Space)
        
    grid.view().show()
    QMessageBox.information(grid.view(), 'Epidemic Agents', 'Press space to pause and resume')
    sys.exit(app.exec_())   
