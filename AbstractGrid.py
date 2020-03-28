from abc import abstractmethod
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView
from PyQt5.QtCore import pyqtSignal
from random import choice

class AbstractGrid(QGraphicsView):
    timeStep = pyqtSignal(tuple)
    
    def __init__(self, QParent, size, number_agents, base_infected, base_immune, desease, sec_between_frame = .1):
        super().__init__(QParent)
        if type(size) == int:
            size = (size, size)
        self.size = lambda: (size[0] + desease.infectionRadius() - (size[0]%desease.infectionRadius()),
                        size[1] + desease.infectionRadius() - (size[1]%desease.infectionRadius()))
        self.number_agents = lambda: number_agents
        self._canvas = QGraphicsScene()
        self.setScene(self._canvas)
        self._desease = desease
        self.base_infected = lambda: base_infected
        self.base_immune = lambda: base_immune
        self._timer = None
        self.timer_sec = lambda: sec_between_frame
        
        self._createAgents()
        self._infect_immune()
        
    @abstractmethod
    def _createAgents(self):
        pass
                
    def _infect_immune(self):
        for _ in range(self.base_infected()):
            choice(self._agents).setInfected()
        for _ in range(self.base_immune()):
            choice(self._agents).setImmune()
            
    def handleKeyPressed(self, event, key_to_press, sec = None):
        if event.key() == key_to_press:
            if self._timer:
                self.stopAnimate()
            else:
                self.startAnimate(sec if sec else self.timer_sec())
    
    def startAnimate(self, sec = None):
        if not sec:
            sec = self.timer_sec()
        else:
            self.timer_sec = lambda: sec
        self._timer = self.startTimer(int(1000*sec))
        self.timerEvent = lambda e: self.time_step()   

    def stopAnimate(self):
        self.killTimer(self._timer)
        self._timer = None
        
    def time_step(self, container = None):
        if not container:
            container = self._agents
        for agent in container:
            self._desease.apply_to(agent, agent.neighbors())
        self.timeStep.emit(self._desease.getTotals())
