from PyQt5.QtGui import QPen, QColor
from epidemicAgents import Agent
from math import cos, sin, pi, ceil
from random import choice, randint
import numpy as np
import networkx as nx
from AbstractGrid import AbstractGrid

class Links:
    def __init__(self, size):
        self.size = lambda: size
        self._matrix = np.zeros((size, size), dtype = bool)
        self._graph = nx.Graph()
        self._graph.add_nodes_from([i for i in range(size)])
            
    def __iter__(self):
        return iter(self.toList())        
            
    def addLink(self, link):
        self._matrix[link[0], link[1]] = self._matrix[link[1], link[0]] = 1
        self._graph.add_edge(link[0], link[1])
    
    def clustering(self):
        m_2 = self._matrix @ self._matrix
        m_3 = m_2 @ self._matrix
        return np.trace(m_3)/(m_2.sum() - np.trace(m_2))
    
    def meanDist(self):
        return nx.average_shortest_path_length(self._graph)
    
    def getRandom(self):
        return choice(self.toList())
        
    def makeGraphPos(self, canvas_size):
        center = (canvas_size[0]/2, canvas_size[1]/2)
        scale = min(canvas_size[0]/3, canvas_size[1]/3)
        return nx.spring_layout(self._graph, center = center, scale = scale)    
    
    def print(self):
        print(self._matrix)
    
    def remove(self, link):
        if self._matrix[link[0], link[1]]:
            self._matrix[link[0], link[1]] = self._matrix[link[1], link[0]] = 0
            self._graph.remove_edge(link[0], link[1])
            
    def toList(self):
        return [(i, j) for i in range(self.size()) for j in range(i, self.size()) if self._matrix[i, j]]


class Network(AbstractGrid):
    def __init__(self, base_connections, rewiring, **kwargs):
        self._agents = []
        self._links = Links(kwargs['number_agents'])
        self.base_connections = lambda: base_connections
        self.rewiring = lambda: rewiring
        super().__init__(**kwargs)
        
        
    def _createAgents(self):
        # Create small world watts-strogatz graph
        for index in range(self.number_agents()):
            for i in range(1, self.base_connections()+1):
                self._links.addLink((index, (index+i)%self.number_agents()))
        for _ in range(ceil(self.number_agents()*self.base_connections()*self.rewiring())):
            temp = self._links.getRandom()
            self._links.remove(temp)
            neighbor_index = randint(0, self.number_agents()-1)
            while neighbor_index == temp[0]:
                neighbor_index = randint(0, self.number_agents()-1)
            self._links.addLink((temp[0], neighbor_index))
        # Create epidemicAgents and paint them on canvas with links
        pos = self._links.makeGraphPos((self.size()[0], self.size()[1]))
        for i in range(self._links.size()):
            self._agents.append(Agent(self._canvas, pos[i], size = 5*min(self.size()[0], self.size()[1])/self._links.size()))
        for link in self._links:
            base = self._agents[link[0]].pos()
            next = self._agents[link[1]].pos()
            self._canvas.addLine(base[0], base[1], next[0], next[1], QPen(QColor(0,0,0,50)))
            self._agents[link[0]].addNeighbor(self._agents[link[1]])
            
if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    import sys
    from PyQt5.QtCore import Qt
    from Desease import Desease
    from movingGrid import Grid

    app = QApplication(sys.argv)

    grid = Network(QParent = None, size = (800, 800), number_agents = 400, base_connections = 2, rewiring = 0.4, base_infected = 100 , base_immune = 20, desease = Desease(1/3, 0.2, None))
    grid.keyPressEvent = lambda e: grid.handleKeyPressed(e, Qt.Key_Space)
    grid.show()
    print(grid._links.clustering(), grid._links.meanDist())
    sys.exit(app.exec_())
