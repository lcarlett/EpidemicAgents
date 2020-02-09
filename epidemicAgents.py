import sys
from PyQt5.QtWidgets import QWidget, QApplication, QGraphicsScene, QGraphicsEllipseItem, QGraphicsView, QPushButton, QVBoxLayout
from PyQt5.QtGui import QPen, QColor, QBrush
from PyQt5.QtCore import QSize
from random import choice, randint, random


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
        self.__update()
        self.__neighbors = []
    
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
        elif random() < transmission_rate*inf_neigh:
            self.setInfected()
    
class Grid(object):
    def __init__(self, size, cell_size, base_infected, infectivity = 0.1, recoverability = 0.1):
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
                self.__agents.append(Agent(self.__canvas, (2*self.cell_size()*j + offset, 2*self.cell_size()*i), self.cell_size())) #+ randint(-3, 3), 10*i + randint(-3, 3))))
            offset = (offset+self.cell_size())%(2*self.cell_size())
        for _ in range(base_infected):
            choice(self.__agents).setInfected()
        self.__calculateNeighbors()
        self.__viewObject = QGraphicsView(self.__canvas)
#        self.__viewObject.show()
        
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
                self.__agents[index].addNeighbor(self.__agents[index - 1])
                self.__agents[index].addNeighbor(self.__agents[index + 1])
                self.__agents[index].addNeighbor(self.__agents[index - self.size()[1]])
                self.__agents[index].addNeighbor(self.__agents[index - self.size()[1] + 1])
                self.__agents[index].addNeighbor(self.__agents[index + self.size()[1]])
                self.__agents[index].addNeighbor(self.__agents[index + self.size()[1] + 1])

    def time_step(self):
        for agent in self.__agents:
            agent.time_step(self.infectivity(), self.recoverability())
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    grid = Grid(25, 10, 25)
    b = QPushButton(grid.view())
    b.setGeometry(0, 550, 50 ,50)
    b.clicked.connect(grid.time_step)
    grid.view().setFixedSize(QSize(600,650))
    grid.view().show()
    sys.exit(app.exec_())    