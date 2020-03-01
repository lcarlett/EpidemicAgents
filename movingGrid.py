from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtGui import QBrush, QColor
from random import randint, choice
from epidemicAgents import Agent
from math import cos, sin, pi


class Tile(object):
#    overcrowded = pyqtSignal(int)
    __maxContent = 6
    
    def __init__(self, grid, left, top, right, bottom, *content):
        super().__init__()
        self.parent = lambda: grid
        self.left = lambda: left
        self.top = lambda: top
        self.right = lambda: right
        self.bottom = lambda: bottom
        self.__content = [*content]
        self.rect = grid.canvas().addRect(left, bottom, right-left, top-bottom)
        
        
    def addContent(self, *content):
        for c in content:
            if c not in self.__content:
                self.__content.append(c)
#        if len(self.__content) >= self.__maxContent:
#            self.overcrowded.emit(len(self.__content))
                
    def remove(self, item):
        for c in self.__content:
            if c is item:
                self.__content.remove(c)
    
    def content(self):
        return self.__content
    
    
class Grid(object):
    def __init__(self, size, number_agents, base_infected, base_immune, desease, startAnimate = False, sec_between_frame = .1):
        if type(size) == int:
            size = (size, size)
        self.size = lambda: size
        self.cell_size = lambda: desease.infectionRadius()
        self.__canvas = QGraphicsScene()
        self.__desease = desease
        self.__viewObject = QGraphicsView(self.__canvas)
        self.__viewObject.setMouseTracking(True)
#        self.__viewObject.mouseMoveEvent = self.__handleMouseMove
        self.__cells = []
        for i in range(size[0]):
            for j in range(size[1]):
                self.__cells.append(Tile(self, i*self.cell_size(), j*self.cell_size(), (i+1)*self.cell_size(),(j+1)*self.cell_size())) 
        for _ in range(number_agents):
            x, y = randint(0, size[0]*self.cell_size()-1), randint(0, size[1]*self.cell_size()-1)
            index = x//self.cell_size() + (y//self.cell_size()) * size[0]
            agent = Agent(self.__canvas, (x, y))
            self.__cells[index].addContent(agent)
            agent.setMoving((randint(-5,5), randint(-5, 5)))
#        self.el = self.__cells[0].content()[0]
#        self.el.setColor((255,0,255))
#        self.el.size = lambda: 20
        for _ in range(base_infected):
            temp = choice(self.__cells).content()
            while temp == []:
                temp = choice(self.__cells).content()    
            choice(temp).setInfected()
        for _ in range(base_immune):
            temp = choice(self.__cells).content()
            while temp == []:
                temp = choice(self.__cells).content()    
            choice(temp).setImmune()
        self.__calculateNeighbors()
        self.__timer = None
        self.timer_sec = lambda: sec_between_frame
        if startAnimate:
            self.startAnimate(.1)
    
    def __handleMouseMove(self, e):
        I, J = e.x()//self.cell_size(), e.y()//self.cell_size()
        for agent in self.getCellsContent(I, J):
            agent.setColor((255,0,145))
    
    def __calculateNeighbors(self):
        for cell_base in self.__cells:
            for agent_base in cell_base.content():
                I, J = agent_base.pos()[0]//self.cell_size(), agent_base.pos()[1]//self.cell_size()
                for agent in self.getCellsContent((I-1, I+1), (J-1, J+1)):
                   agent_base.addNeighbor(agent)
    
    def __stopAnimate(self):
        self.__viewObject.killTimer(self.__timer)
        self.__timer = None
    
    def getCellsContent(self, indI, indJ):
        if type(indI) is int:
            indI = (indI, indI)
        if type(indJ) is int:
            indJ = (indJ, indJ)
        return {agent for cell in {self.__cells[i%self.size()[0] + (j%self.size()[1])*self.size()[0]] for i in range(indI[0], indI[1]+1) for j in range(indJ[0], indJ[1]+1)} for agent in cell.content()}
    
    def handleKeyPressed(self, event, key_to_press, sec = None):
        if event.key() == key_to_press:
            if self.__timer:
                self.__stopAnimate()
            else:
                self.startAnimate(sec if sec else self.timer_sec())
    
    def intersectWithCircle(self, center, radius):
        left   = (center[0] - radius)//self.cell_size()
        top    = (center[1] + radius)//self.cell_size()
        right  = (center[0] + radius)//self.cell_size() 
        bottom = (center[1] - radius)//self.cell_size()
        return self.getCellsContent((left, right), (bottom, top))
    
    def startAnimate(self, sec):
        self.__timer = self.__viewObject.startTimer(int(1000*sec))
        self.__viewObject.timerEvent = lambda e: self.time_step()    
    
    def time_step(self):
        toadd  = []
        for tile in self.__cells:
            for agent in tile.content():
                x, y = add(agent.pos(), agent.direction())
                teleport = False
                if x < 0:
                    x = self.size()[0]*self.cell_size()-1
                    teleport = True
                elif x >= self.size()[0]*self.cell_size():
                    x = 0
                    teleport = True
                if y < 0:
                    y = self.size()[1]*self.cell_size()-1
                    teleport = True
                elif y >= self.size()[1]*self.cell_size():
                    y = 0
                    teleport = True
                agent.setPos((x, y))
                if teleport:
                    tile.remove(agent)
                    toadd.append(agent)
                    agent.resetNeighbors()
                else:
                    if not(tile.left()<= x <= tile.right()) or not(tile.bottom()<= y <= tile.top()):
                        I, J = agent.pos()[0]//self.cell_size(), agent.pos()[1]//self.cell_size()
                        tile.remove(agent)
                        toadd.append(agent)
                        agent.resetNeighbors()
                        for a in self.getCellsContent((I-1, I+1), (J-1, J+1)):
                           agent.addNeighbor(a)
                self.__desease.apply_to(agent, agent.neighbors())
        for agent in toadd:
            x, y = agent.pos()
            index = x//self.cell_size() + (y//self.cell_size()) * self.size()[0]
            self.__cells[index].addContent(agent)
#        self.el.illuminateNeighbors(.8)
        
    def canvas(self):
        return self.__canvas
    
    def view(self):
        return self.__viewObject
    
def add(l1, l2):
    return (l1[0] + l2[0], l1[1] + l2[1])    
    
def Hue(t):
    t = t%1
    if t < 1/3:
        t = t*3*pi/2
        return (cos(t)*255, sin(t)*255, 0)
    elif t < 2/3:
        t = (t-1/3)*3*pi/2
        return (0, cos(t)*255, sin(t)*255)
    else:
        t = (t-2/3)*3*pi/2
        return (sin(t)*255, 0, cos(t)*255)
    
