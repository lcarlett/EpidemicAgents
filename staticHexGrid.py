from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView
from PyQt5.QtCore import Qt, QSize
from random import choice, randint
from epidemicAgents import Agent

class Grid(object):
    def __init__(self, size, cell_size, base_infected, base_immune, desease, startAnimate = False, sec_between_frame = 1):
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
        for _ in range(base_immune):
            choice(self.__agents).setImmune()
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
