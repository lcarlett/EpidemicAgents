from Desease import Desease
from PyQt5.QtGui import QColor, QBrush

class Agent(object):
    SaneColor = (0,0,0)
    InfectedColor = (255, 0, 0)
    ImmuneColor = (0, 255, 0)
    def __init__(self, parent, pos, size=10, infected = False):
        self.size = lambda: size
        self.__state = Desease.Infected if infected else Desease.Sane
        self.__color = QColor(*(Agent.InfectedColor if infected else Agent.SaneColor))
        self.__parent = parent
        self.__pos = pos
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
    
    def setPos(self, newPos):
        self.__pos = newPos
        self.__graphicItem.setRect(newPos[0], newPos[1], self.size(), self.size())
    
    def addNeighbor(self, agent):
        self.__neighbors.append(agent)
        if self not in agent.neighbors():
            agent.addNeighbor(self)
            
    def neighbors(self):
        return self.__neighbors
    
    def pos(self):
        return self.__pos
        
    def vulnerability(self):
        return self.__vulnerability
