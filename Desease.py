from random import random

class Desease(object):
    Sane, Infected, Immune = range(3)
    def __init__(self, infectivity, recoverability, infectionRadius = 1):
        self.__transmission_rate = infectivity
        self.__recovery_rate = recoverability
        self.infectionRadius = lambda: infectionRadius
        self.__infected = 0
        
    def apply_to(self, agent, surrounding):
        inf_neigh = 0
        for neigh in surrounding:
            inf_neigh += neigh.isInfected()
        if agent.isInfected() and random() < self.__recovery_rate:
            agent.setSane()
            self.__infected -= 1
#            if random()<.5:
#                agent.setImmune()
        elif binomial(self.__transmission_rate*agent.vulnerability(), inf_neigh):
            agent.setInfected()
            self.__infected += 1 
    
    def getTotalInfected(self):
        return self.__infected

def binomial(p, n):
    """ Return True, False selon une binomiale (au moins un bon) de proba p pour n tirages.
    """
    return random() < 1-(1-p)**n
