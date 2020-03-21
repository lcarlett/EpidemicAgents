from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView
from PyQt5.QtGui import QPen, QColor
from epidemicAgents import Agent
from math import cos, sin, pi, ceil
from random import choice, randint
import numpy as np

class Links:
    def __init__(self, size):
        self.size = size
        self.__matrix = np.zeros((size, size), dtype = bool)
            
    def __iter__(self):
        return iter(self.toList())        
            
    def addLink(self, link):
        self.__matrix[link[0], link[1]] = self.__matrix[link[1], link[0]] = 1
    
    def getRandom(self):
        return choice(self.toList())
        
    def print(self):
        print(self.__matrix)
    
    def remove(self, link):
        if self.__matrix[link[0], link[1]]:
            self.__matrix[link[0], link[1]] = self.__matrix[link[1], link[0]] = 0
    
    def toList(self):
        return [(i, j) for i in range(self.size) for j in range(i, self.size) if self.__matrix[i, j]]

class PhysicsAgent(Agent):
    def __init__(self, parent, pos):
        super().__init__(parent, pos)
        self.__force = (0, 0)
        self.__speed = (0, 0)
    
    def addForce(self, force):
        self.__force = add(self.__force, force)
        
    def applyForce(self):
        self.__speed = add(self.__speed, self.__force)   
    
    def speed(self):
        return self.__speed
    
    def move(self):
        self.applyForce()
        self.setPos(add(self.pos, self.__speed))
        self.__force = (0, 0)

class Network(object):
    def __init__(self, size, number_agents, base_connections, rewiring, base_infected, base_immune, desease, startAnimate = False, sec_between_frame = .05):
        if type(size) == int:
            size = (size, size)
        self.__canvas = QGraphicsScene()
        self.__viewObject = QGraphicsView(self.__canvas)
        radius = min(size[0], size[1])/2
        center = (size[0]/2, size[1]/2)
        self.__moving = False
        self.__agents = []
        self.__links = Links(number_agents)
        self.__lines = []
        self.__desease = desease
        for i in range(number_agents):
            pos = add(center, (radius*cos(2*pi*i/number_agents), radius*sin(2*pi*i/number_agents)))
            self.__agents.append(PhysicsAgent(self.__canvas, pos))
        for index in range(number_agents):
            base_agent = self.__agents[index]
            for i in range(1, base_connections+1):
                self.__links.addLink((index, (index+i)%number_agents))
                neighbor = self.__agents[(index+i)%number_agents]
                base_agent.addNeighbor(neighbor)
        for _ in range(ceil(number_agents*base_connections*rewiring)):
            temp = self.__links.getRandom()
            self.__links.remove(temp)
            self.__agents[temp[0]].removeNeighbor(self.__agents[temp[1]])
            neighbor_index = randint(0, number_agents-1)
            self.__links.addLink((temp[0], neighbor_index))
            self.__agents[temp[0]].addNeighbor(self.__agents[neighbor_index])
        for link in self.__links:
            base = self.__agents[link[0]].pos
            next = self.__agents[link[1]].pos
            self.__lines.append((link[0], link[1], self.__canvas.addLine(base[0], base[1], next[0], next[1], QPen(QColor(0,0,0,50))))) 
        for _ in range(base_infected):
            choice(self.__agents).setInfected()
        for _ in range(base_immune):
            choice(self.__agents).setImmune()
        self.__timer = None
        self.timer_sec = lambda: sec_between_frame
    
    def __animate_move(self):
        if self.__timer:
            self.__viewObject.killTimer(self.__timer)
        self.__timer = self.__viewObject.startTimer(int(1000*self.timer_sec()))
        self.__viewObject.timerEvent = lambda e: self.__moveTime_step()
    
    def __animate_epidemic(self):
        if self.__timer:
            self.__viewObject.killTimer(self.__timer)
        self.__timer = self.__viewObject.startTimer(int(1000*self.timer_sec()))
        self.__viewObject.timerEvent = lambda e: self.time_step()
    
    def handleKeyPressed(self, event, key_to_press):
        if event.key() == key_to_press:
            if not self.__moving:
                self.__animate_move()
                self.__moving = True
            else:
                self.__animate_epidemic()
                self.__moving = False
        
    def __moveTime_step(self):
        import time
        tic = time.time()
        for agent in self.__agents:
            for other in agent.neighbors():
                agent.addForce(makeElastic(other.pos, agent.pos))
                other.addForce(makeElastic(agent.pos, agent.pos))
            for other in self.__agents:
                agent.addForce(makeRepulsion(agent.pos, other.pos))
                other.addForce(makeRepulsion(other.pos, agent.pos))
            agent.addForce(makeFriction(agent))    
        for agent in self.__agents:
            agent.move()
        self.__replaceAgents()    
        if not self.__moving:
            self.time_step()
        print(time.time()-tic)
        
    def __replaceAgents(self):
        for line in self.__lines:
            base = self.__agents[line[0]].pos
            next = self.__agents[line[1]].pos     
            line[2].setLine(base[0], base[1], next[0], next[1])
    
    def time_step(self):
        for agent in self.__agents:
            self.__desease.apply_to(agent, agent.neighbors())
        
    def view(self):
        return self.__viewObject
    
def add(*vecs, weights = None):
    if not weights:
        weights = [1]*len(vecs)
    return (sum([vecs[i][0]*weights[i] for i in range(len(vecs))]), sum([vecs[i][1]*weights[i] for i in range(len(vecs))]))     
    
def cap(vec, magn):
    return (min(vec[0], magn) if vec[0] > 0 else max(vec[0], -magn), min(vec[0], magn) if vec[0] > 0 else max(vec[0], -magn))
    
def dist(l):
    return (l[0]**2 + l[1]**2)**(1/2)

R = 20

def makeRepulsion(base, other):
    vect = (base[0]-other[0], base[1]-other[1])
    d = dist(vect)
    if d == 0:
        return (randint(-R//2,R//2), randint(-R//2,R//2))
    elif d > R:
        return (0, 0)
    else:
        d_cube = d*d*d
        return cap((vect[0]*R/(2*d_cube), vect[1]*R/(2*d_cube)), 5)

def makeFriction(agent):
    friction = .04
    sped = agent.speed()
    d = dist(sped)
    return (-d*sped[0]*friction, -d*sped[1]*friction)
    
def makeElastic(next, base):
    vect = (next[0]-base[0], next[1]-base[1])
    d = dist(vect)
    if d == 0 or d <= R:
        return (0, 0)
    else:
        n_vect = (vect[0]/d, vect[1]/d)
        magn = ((d-R)/R)**2
        magn = min(magn, 5) if magn > 0 else max(magn, -5)
        return (n_vect[0]*magn, n_vect[1]*magn)
