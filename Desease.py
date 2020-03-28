from random import random
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

class Desease(object):
    Sane, Infected, Immune = range(3)
    def __init__(self, infectivity, recoverability, immunity, infectionRadius = 1):
        self._transmission_rate = infectivity
        self._recovery_rate = recoverability
        self.infectionRadius = lambda: infectionRadius
        self.immunity = lambda: immunity
        self._infected = 0
        self._removed = 0
        
    def apply_to(self, agent, surrounding):
        inf_neigh = 0
        for neigh in surrounding:
            inf_neigh += neigh.isInfected()
        if agent.isInfected() and random() < self._recovery_rate:
            agent.setSane()
            self._infected -= 1
            if random()<self.immunity():
                self._removed += 1
                agent.setRecovered()
        elif not agent.isInfected() and binomial(self._transmission_rate*agent.vulnerability(), inf_neigh):
            agent.setInfected()
            self._infected += 1 
    
    def getTotals(self):
        return (self._infected, self._removed)

def binomial(p, n):
    """ Return True, False selon une binomiale (au moins un bon) de proba p pour n tirages.
    """
    return random() < 1-(1-p)**n
    
class DeseasePlot(FigureCanvasQTAgg):
    def __init__(self, size, max_value, dpi = 100):
        size = (size[0]/dpi, size[1]/dpi)
        self._max_value = max_value
        self._xlim = 50
        self._fig = Figure(figsize = size, dpi = dpi, linewidth = .1)
        super(DeseasePlot, self).__init__(self._fig)
        self._axes = self._fig.add_subplot()
        self._xdata, self._ydata1, self._ydata2 = [], [], []
        self.set_xlim(self._xlim)
        self.set_ylim(self._max_value)
        self._data1, = self._axes.plot(self._xdata, self._ydata1, 'r', fillstyle = "full")
        self._data2, = self._axes.plot(self._xdata, self._ydata2, 'k')
        self._x_index = 0
        
    def set_xlim(self, lim):
        self._axes.set_xlim(0, lim)
        
    def set_ylim(self, lim):
        self._axes.set_ylim(0, lim)
        
    def updatePlot(self, values):
        if self._x_index > self._xlim:
            self._xlim += 50
            self.set_xlim(self._xlim)
        if max(*values) > self._max_value:
            self._max_value = max(*values) + 20
            self.set_ylim(self._max_value + 20)
        self._xdata.append(self._x_index)
        self._ydata1.append(values[0])
        self._ydata2.append(values[1])
        self._data1.set_data(self._xdata, self._ydata1)
        self._data2.set_data(self._xdata, self._ydata2)
        self._fig.canvas.draw()
        self._x_index += 1
        
        
