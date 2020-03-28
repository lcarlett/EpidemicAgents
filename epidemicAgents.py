from Desease import Desease
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtCore import QTimer

NOT_MOVING_ERROR = '{} is not a moving agent'

class Agent(object):
    SaneColor = (0,0,0)
    InfectedColor = (255, 0, 0)
    ImmuneColor = (0, 255, 0)
    RecoveredColor = (150, 150, 150)
    
    def __init__(self, parent, pos, size=10, infected = False):
        self.size = lambda: size
        self.parent = lambda: parent
        self.__state = Desease.Infected if infected else Desease.Sane
        self.__color = QColor(*(Agent.InfectedColor if infected else Agent.SaneColor))
        self.__parent = parent
        self.__pos = pos
        self.__graphicItem = parent.addEllipse(pos[0]-self.size()//2, pos[1]-self.size()//2, self.size(), self.size())
        self.__neighbors = set()
        self.__vulnerability = 1
        self.__update()
        self.__moving = None
    
    def __update(self):
        self.__graphicItem.setBrush(QBrush(self.__color))
    
    def isInfected(self):
        return self.__state == Desease.Infected
    
    def isMoving(self):
        return self.__moving != None
    
    def setColor(self, color, ms=0):
        self.__color = QColor(*color)
        self.__update()
        if ms:
            QTimer.singleShot(ms, lambda: self.setColor((0,0,0)))
    
    def setDirection(self, direction):
        if not self.__moving:
            raise TypeError(NOT_MOVING_ERROR.format(self))
        else:
            self.__moving = direction
            
    def setInfected(self):
        self.__state = Desease.Infected
        self.setColor(Agent.InfectedColor)
    
    def setSane(self):
        self.__state = Desease.Sane
        self.setColor(Agent.SaneColor)
    
    def setImmune(self, immune = True):
        self.__vulnerability = 1-immune
        if immune:
            self.setSane()
            self.setColor(Agent.ImmuneColor)
        else:
            self.setColor(Agent.SaneColor)
    
    def setRecovered(self, recovery = True):
        self.setImmune(recovery)
        if recovery:
            self.setColor(Agent.RecoveredColor)
    
    def setPos(self, newPos):
        self.__pos = newPos
        self.__graphicItem.setRect(newPos[0]-self.size()//2, newPos[1]-self.size()//2, self.size(), self.size())
    
    def setMoving(self, moving_dir):
        self.__moving = moving_dir
    
    def addNeighbor(self, agent):
        if self is not agent:
            self.__neighbors.add(agent)
            if self not in agent.neighbors():
                agent.addNeighbor(self)
           
    def direction(self):
        if not self.__moving:
            raise TypeError(NOT_MOVING_ERROR.format(self))
        else:
            return self.__moving
     
    def illuminateNeighbors(self, sec):
        for n in self.__neighbors:
            n.setColor((255, 0, 0), sec*1000)
    
    def neighbors(self):
        return self.__neighbors
    
    def pos(self):
        return self.__pos
    
    def removeNeighbor(self, agent, removeSelf = True):   
        self.__neighbors.discard(agent)
        if removeSelf and self in agent.neighbors():
            agent.removeNeighbor(self)
    
    def resetNeighbors(self):
        for neighbor in self.__neighbors:
            neighbor.removeNeighbor(self, False)
        self.__neighbors = set()
        
    def vulnerability(self):
        return self.__vulnerability
