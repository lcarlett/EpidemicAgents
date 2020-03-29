from AbstractGrid import AbstractGrid
from PyQt5.QtGui import QBrush, QColor
from random import randint, choice
from epidemicAgents import Agent
from math import cos, sin, pi, ceil


class Tile(object):
    _maxContent = 6
    
    def __init__(self, grid, left, top, right, bottom, *content, debug = False):
        super().__init__()
        self.parent = lambda: grid
        self.left = lambda: left
        self.top = lambda: top
        self.right = lambda: right
        self.bottom = lambda: bottom
        self._content = [*content]
        if debug:
            self.rect = grid.canvas().addRect(left, bottom, right-left, top-bottom)
        
        
    def addContent(self, *content):
        for c in content:
            if c not in self._content:
                self._content.append(c)
#        if len(self._content) >= self._maxContent:
#            self.overcrowded.emit(len(self._content))
            
    def remove(self, item):
        for c in self._content:
            if c is item:
                self._content.remove(c)
    
    def content(self):
        return self._content
    
    
class Grid(AbstractGrid):
    def __init__(self, debug = False, **kwargs):
        self._cells = []
        self.debug = lambda: debug
        self.cell_size = lambda: kwargs['desease'].infectionRadius()
        super().__init__(**kwargs)
#        self.setMouseTracking(True)
#        self.mouseMoveEvent = self._handleMouseMove
        self._calculateNeighbors()
    
    def _createAgents(self):
        self._grid_size = (self.size()[0]//self.cell_size(), self.size()[1]//self.cell_size())
        for i in range(self._grid_size[0]):
            for j in range(self._grid_size[1]):
                self._cells.append(Tile(self, i*self.cell_size(), j*self.cell_size(), (i+1)*self.cell_size(),(j+1)*self.cell_size(), debug = self.debug())) 
        for _ in range(self.number_agents()):
            x, y = randint(0, self._grid_size[0]*self.cell_size()-1), randint(0, self._grid_size[1]*self.cell_size()-1)
            index = x//self.cell_size() + (y//self.cell_size()) * self._grid_size[0]
            agent = Agent(self._canvas, (x, y), size = 20*min(self.size()[0], self.size()[1])/self.number_agents())
            self._cells[index].addContent(agent)
            direction = (randint(-5,5), randint(-5, 5))
#            self._canvas.addLine(x, y, x+direction[0]*5, y+direction[1]*5)
            agent.setMoving(direction)
#        self.el = self._cells[0].content()[0]
#        self.el.setColor((255,0,255))
#        self.el.size = lambda: 20
    
    def _infect_immune(self):
        for _ in range(self.base_infected()):
            temp = choice(self._cells).content()
            while temp == []:
                temp = choice(self._cells).content()    
            choice(temp).setInfected()
        for _ in range(self.base_immune()):
            temp = choice(self._cells).content()
            while temp == []:
                temp = choice(self._cells).content()    
            choice(temp).setImmune()
    
    def _handleMouseMove(self, e):
        I, J = e.x()//self.cell_size(), e.y()//self.cell_size()
        for agent in self.getCellsContent(I, J):
            agent.setColor((255,0,145))
    
    def _calculateNeighbors(self):
        for cell_base in self._cells:
            for agent_base in cell_base.content():
                I, J = agent_base.pos()[0]//self.cell_size(), agent_base.pos()[1]//self.cell_size()
                for agent in self.getCellsContent((I-1, I+1), (J-1, J+1)):
                   agent_base.addNeighbor(agent)
    
    def getCellsContent(self, indI, indJ):
        if type(indI) is int:
            indI = (indI, indI)
        if type(indJ) is int:
            indJ = (indJ, indJ)
        return {agent for cell in {self._cells[i%self._grid_size[0] + (j%self._grid_size[1])*self._grid_size[0]] for i in range(indI[0], indI[1]+1) for j in range(indJ[0], indJ[1]+1)} for agent in cell.content()}

    def intersectWithCircle(self, center, radius):
        left   = (center[0] - radius)//self.cell_size()
        top    = (center[1] + radius)//self.cell_size()
        right  = (center[0] + radius)//self.cell_size() 
        bottom = (center[1] - radius)//self.cell_size()
        return self.getCellsContent((left, right), (bottom, top))
    
    def time_step(self):
        toadd  = []
        for tile in self._cells:
            for agent in tile.content():
                x, y = add(agent.pos(), agent.direction())
                teleport = False
                if x < 0:
                    x = self.size()[0]-1
                    teleport = True
                elif x >= self.size()[0]:
                    x = 0
                    teleport = True
                if y < 0:
                    y = self.size()[1]-1
                    teleport = True
                elif y >= self.size()[1]:
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
        for agent in toadd:
            x, y = agent.pos()
            index = x//self.cell_size() + (y//self.cell_size()) * self._grid_size[0]
            self._cells[index].addContent(agent)
        super().time_step([a for cell in self._cells for a in cell.content()])
#        self.el.illuminateNeighbors(.8)
    
    def canvas(self):
        return self._canvas
    
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
    
