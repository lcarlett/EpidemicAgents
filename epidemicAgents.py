import sys
from PyQt5.QtWidgets import QWidget, QApplication, QGraphicsScene, QGraphicsEllipseItem, QGraphicsView, QMessageBox
from PyQt5.QtGui import QPen, QColor, QBrush
from PyQt5.QtCore import Qt, pyqtSlot, QSize, QTimer
from random import choice, randint, random
from time import sleep

class Agent(object):
    Sane = 0
    Infected = 1
    SaneColor = (0,0,0)
    InfectedColor = (255, 0, 0)
    def __init__(self, parent, pos, size, infected = False):
        self.size = lambda: size
        self.__state = Agent.Infected if infected else Agent.Sane
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
        return self.__state == Agent.Infected
    
    def setInfected(self):
        self.__state = Agent.Infected
        self.__color = QColor(*Agent.InfectedColor)
        self.__update()
    
    def setSane(self):
        self.__state = Agent.Sane
        self.__color = QColor(*Agent.SaneColor)
        self.__update()
    
    def addNeighbor(self, agent):
        self.__neighbors.append(agent)
    
    def time_step(self, transmission_rate, recovery_rate):
        inf_neigh = 0
        for neigh in self.__neighbors:
            inf_neigh += neigh.isInfected()
        if self.isInfected() and random() > transmission_rate*inf_neigh - recovery_rate:
            self.setSane()
        elif random() < transmission_rate*inf_neigh*self.__vulnerability:
            self.setInfected()
    
class Grid(object):
    def __init__(self, size, cell_size, base_infected, infectivity = 0.2105, recoverability = 0.1, startAnimate = True, sec_between_frame = 1):
        if type(size) == int:
            size = (size, size)
        self.size = lambda: size
        self.cell_size = lambda: cell_size
        self.infectivity = lambda: infectivity
        self.recoverability = lambda: recoverability
        self.__canvas = QGraphicsScene()
        self.__agents = []
        offset = 0
        for i in range(size[0]):
            for j in range(size[1]):
                self.__agents.append(Agent(self.__canvas, (self.cell_size()*1.5*j + offset + randint(-int(self.cell_size()/2), int(self.cell_size()/2)), self.cell_size()*1.5*i + randint(-int(self.cell_size()/2), int(self.cell_size()/2))), self.cell_size())) #+ , 10*i + randint(-3, 3))))
            offset = (offset+self.cell_size()/2)%(self.cell_size())
        for _ in range(base_infected):
            choice(self.__agents).setInfected()
        self.__calculateNeighbors()
        self.__viewObject = QGraphicsView(self.__canvas)
        self.__timer = None
        if startAnimate:
            self.__timer_sec = sec_between_frame
            self.startAnimate(sec_between_frame)
            
    def handleKeyPressed(self, event, key_to_press, sec = None):
        if event.key() == key_to_press:
            if self.__timer:
                self.__stopAnimate()
            else:
                self.startAnimate(sec if sec else self.__timer_sec)
         
         
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
            if index == 0:
                self.__agents[index].addNeighbor(self.__agents[index + 1])
                self.__agents[index].addNeighbor(self.__agents[index + self.size()[1]])
            elif index == self.size()[1]-1:
                self.__agents[index].addNeighbor(self.__agents[index - 1])
                self.__agents[index].addNeighbor(self.__agents[index + self.size()[1] - 1])
                self.__agents[index].addNeighbor(self.__agents[index + self.size()[1]])
            elif index == (self.size()[0]-1)*self.size()[1]:
                self.__agents[index].addNeighbor(self.__agents[index - self.size()[1]])
                self.__agents[index].addNeighbor(self.__agents[index + 1])
            elif index == self.size()[0]*self.size()[1]-1:
                self.__agents[index].addNeighbor(self.__agents[index - 1])
                self.__agents[index].addNeighbor(self.__agents[index - self.size()[1] - 1])
                self.__agents[index].addNeighbor(self.__agents[index - self.size()[1]])
            elif index < self.size()[1]:
                self.__agents[index].addNeighbor(self.__agents[index - 1])
                self.__agents[index].addNeighbor(self.__agents[index + 1])
                self.__agents[index].addNeighbor(self.__agents[index + self.size()[1] - 1]) 
                self.__agents[index].addNeighbor(self.__agents[index + self.size()[1]]) 
            elif index%self.size()[1] == 0:
                self.__agents[index].addNeighbor(self.__agents[index - self.size()[1]])
                self.__agents[index].addNeighbor(self.__agents[index - self.size()[1] + 1])
                self.__agents[index].addNeighbor(self.__agents[index + 1])
                self.__agents[index].addNeighbor(self.__agents[index + self.size()[1] + 1])
                self.__agents[index].addNeighbor(self.__agents[index + self.size()[1]])
            elif (index+1)%self.size()[1] == 0:
                self.__agents[index].addNeighbor(self.__agents[index - self.size()[1]])
                self.__agents[index].addNeighbor(self.__agents[index - 1])
                self.__agents[index].addNeighbor(self.__agents[index + self.size()[1]])
            elif index >= (self.size()[0]-1)*self.size()[1]:
                self.__agents[index].addNeighbor(self.__agents[index - 1])
                self.__agents[index].addNeighbor(self.__agents[index + 1])
                self.__agents[index].addNeighbor(self.__agents[index - self.size()[1] - 1])
                self.__agents[index].addNeighbor(self.__agents[index - self.size()[1]])
            else:
                self.__agents[index].addNeighbor(self.__agents[index + 1])
                self.__agents[index].addNeighbor(self.__agents[index - 1])
                self.__agents[index].addNeighbor(self.__agents[index - self.size()[1] + 1])
                self.__agents[index].addNeighbor(self.__agents[index - self.size()[1]])
                self.__agents[index].addNeighbor(self.__agents[index + self.size()[1] + 1])
                self.__agents[index].addNeighbor(self.__agents[index + self.size()[1]])

    def time_step(self):
        for agent in self.__agents:
            agent.time_step(self.infectivity(), self.recoverability())
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    grid = Grid((100,250), 5, 25, sec_between_frame = .3)
    grid.view().keyPressEvent = lambda e: grid.handleKeyPressed(e, Qt.Key_Space)
    grid.view().show()
    QMessageBox.information(grid.view(), 'Epidemic Agents', 'Press space to pause and resume')
    sys.exit(app.exec_())   
