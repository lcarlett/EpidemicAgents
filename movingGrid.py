from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QBrush, QColor
from random import randint
from epidemicAgents import Agent
from math import cos, sin, pi

class Tile(object):
    overcrowded = pyqtSignal(int)
    __maxContent = 6
    
    def __init__(self, grid, left, top, right, bottom, *content):
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
                
    def content(self):
        return self.__content
    
    
class Grid(object):
    def __init__(self, size, cell_size, number_agents):#, base_infected, base_immune, desease):
        if type(size) == int:
            size = (size, size)
        self.size = lambda: size
        self.cell_size = lambda: cell_size
        self.__canvas = QGraphicsScene()
        
        self.__viewObject = QGraphicsView(self.__canvas)
        self.__viewObject.setMouseTracking(True)
        self.__viewObject.mouseMoveEvent = self.__handleMouseMove
        
        self.__cells = []
        self.__agents = []
        for i in range(size[0]):
            for j in range(size[1]):
                self.__cells.append(Tile(self, i*cell_size, j*cell_size, (i+1)*cell_size,(j+1)*cell_size)) 
        for _ in range(number_agents):
            x, y = randint(0, size[0]*cell_size-1), randint(0, size[1]*cell_size-1)
            index = x//cell_size + (y//cell_size) * size[0]
            agent = Agent(self.__canvas, (x, y))
            self.__cells[index].addContent(agent)
        self.el = None
        self.temp = []
#        for _ in range(base_infected):
#            choice(self.__agents).setInfected()
#        for _ in range(base_immune):
#            choice(self.__agents).setImmune()
#        self.__calculateNeighbors()
    
    def intersectWithCircle(self, center, radius):
        left   = max(center[0]-radius, 0)//self.cell_size()
        top    = min((center[1]+radius)//self.cell_size(), self.size()[1]-1)
        right  = min((center[0]+radius)//self.cell_size(), self.size()[0]-1) 
        bottom = max(center[1]-radius, 0)//self.cell_size()
        return [self.__cells[i + j*self.size()[0]] for i in range(left, right+1) for j in range(bottom, top+1)]
    
    def __handleMouseMove(self, event):
        x, y = event.pos().x(), event.pos().y()
        r = 20
        if self.el:
            self.__canvas.removeItem(self.el)
            for re in self.temp:
                for ee in re.content(): 
                    ee.setColor((0,0,0))
            self.temp = []
        self.el = self.__canvas.addEllipse(x-r, y-r, 2*r, 2*r)
        for t in self.intersectWithCircle((x, y), r):
            for e in t.content():
                e.setColor((255,0,0))
            self.temp.append(t)
           
    
    def canvas(self):
        return self.__canvas
    
    def view(self):
        return self.__viewObject
    
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
    
