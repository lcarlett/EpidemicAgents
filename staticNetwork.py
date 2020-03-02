from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView
from PyQt5.QtGui import QPen, QColor
from epidemicAgents import Agent
from math import cos, sin, pi, ceil
from random import choice, randint


class PhysicsAgent(object):
    def __init__(self, pos):
        self.__pos = pos
        self.__force = (0, 0)
        self.__speed = (0, 0)
    
    def addForce(self, force):
        self.__force = add(self.__force, force)
        
    def applyForce(self):
        self.__speed = add(self.__speed, self.__force)   
           
    def pos(self):
        return self.__pos
        
    def time_step(self):
        self.applyForce()
        self.__pos = add(self.__pos, self.__speed)
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
        self.__links = []
        self.__physics = []
        self.__lines = []
        self.__desease = desease
        for i in range(number_agents):
            pos = add(center, (radius*cos(2*pi*i/number_agents), radius*sin(2*pi*i/number_agents)))
            self.__agents.append(Agent(self.__canvas, pos, size=10))
            self.__physics.append(PhysicsAgent(pos))
        for index in range(number_agents):
            base_agent = self.__agents[index]
            for i in range(1, base_connections+1):
                self.__links.append((index, (index+i)%number_agents))
                neighbor = self.__agents[(index+i)%number_agents]
                base_agent.addNeighbor(neighbor)
        for _ in range(ceil(number_agents*base_connections*rewiring)):
            temp = choice(self.__links)
            self.__links.remove(temp)
            self.__agents[temp[0]].removeNeighbor(self.__agents[temp[1]])
            neighbor_index = randint(0, number_agents-1)
            self.__links.append((temp[0], neighbor_index))
            self.__agents[temp[0]].addNeighbor(self.__agents[neighbor_index])
        for link in self.__links:
            base = self.__agents[link[0]].pos()
            next = self.__agents[link[1]].pos()
            self.__lines.append(self.__canvas.addLine(base[0], base[1], next[0], next[1], QPen(QColor(0,0,0,50)))) 
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
        for link in self.__links:
            base = self.__agents[link[0]].pos()
            next = self.__agents[link[1]].pos()
            self.__physics[link[0]].addForce(makeforce(next, base))
            self.__physics[link[1]].addForce(makeforce(base, next))
        for agent in self.__physics:
            agent.time_step()
        self.__replaceAgents()    
        self.time_step()
        
    def __replaceAgents(self):
        for index in range(len(self.__agents)):
            self.__agents[index].setPos(self.__physics[index].pos())
        for index in range(len(self.__links)):
            link = self.__links[index]
            base = self.__agents[link[0]].pos()
            next = self.__agents[link[1]].pos()     
            self.__lines[index].setLine(base[0], base[1], next[0], next[1])
    
    def time_step(self):
        for agent in self.__agents:
            self.__desease.apply_to(agent, agent.neighbors())
        
    def view(self):
        return self.__viewObject
    
def add(l1, l2):
    return (l1[0] + l2[0], l1[1] + l2[1])    
    
def dist_sq(l):
    return l[0]**2 + l[1]**2
    
def makeforce(next, base):
    R = 4
    vect = (next[0]-base[0], next[1]-base[1])
    d = dist_sq(vect)**(1/2)
    if d == 0:
        return (0, 0)
    else:
        n_vect = (vect[0]/d, vect[1]/d)
        if d < R:
            magn = (R/d - 1)*0.001
        else:
            magn = (d-R)**2 *0.001
        magn = min(magn, 10)*.3
        return (n_vect[0]*magn, n_vect[1]*magn)
