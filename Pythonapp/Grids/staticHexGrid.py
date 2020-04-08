from PyQt5.QtCore import Qt, QSize
from random import choice, randint
from epidemicAgents import Agent
from AbstractGrid import AbstractGrid

class Grid(AbstractGrid):
    def __init__(self, cell_padding = .3,**kwargs):
        self.cell_padding = lambda: cell_padding
        self.cell_size = lambda: int((kwargs['size'][0]*kwargs['size'][1]/kwargs['number_agents'])**(1/2))
        self._agents = []
        super().__init__(**kwargs)
        self._calculateNeighbors()
    
    def _createAgents(self):
        offset = 0
        self._grid_size = (self.size()[0]//self.cell_size(), self.size()[1]//self.cell_size())
        for i in range(self._grid_size[0]):
            for j in range(self._grid_size[1]):
                self._agents.append(Agent(self._canvas, (self.cell_size()*(1+self.cell_padding())*j + offset + 0*randint(-int(self.cell_size()/2), int(self.cell_size()/2)), self.cell_size()*(1+self.cell_padding())*((3/4)**(1/2))*i + 0*randint(-int(self.cell_size()/2), int(self.cell_size()/2))), self.cell_size()))
            offset = 0 if offset else (offset+self.cell_size()*(1 + self.cell_padding())/2)
    
    def _calculateNeighbors(self):
        for index in range(len(self._agents)):
            offset = (index%(self._grid_size[1]*2))//self._grid_size[1]
            if not (index < self._grid_size[1] 
                or index%self._grid_size[1] == 0 
                or (index+1)%self._grid_size[1] == 0 
                or index >= (self._grid_size[0]-1)*self._grid_size[1]):
# If not on side, else it will be added by the reciprocity of addNeighbor
                self._agents[index].addNeighbor(self._agents[index + 1])
                self._agents[index].addNeighbor(self._agents[index - 1])
                self._agents[index].addNeighbor(self._agents[index - self._grid_size[1] + 2*offset - 1])
                self._agents[index].addNeighbor(self._agents[index - self._grid_size[1]])
                self._agents[index].addNeighbor(self._agents[index + self._grid_size[1] + 2*offset - 1])
                self._agents[index].addNeighbor(self._agents[index + self._grid_size[1]])

    def tell(self, num):
        n = self._agents[num].neighbors()
        self._agents[num].setColor((255,0,255))
        for nn in n:
             nn.setColor((0,0,255))
    
    def noTell(self, num):
        n = self._agents[num].neighbors()
        self._agents[num].setColor((0,0,0))
        for nn in n:
            nn.setColor((0,0,0))
