from random import random

class Desease(object):
    Sane, Infected, Immune = range(3)
    def __init__(self, infectivity, recoverability, infectionRadius):
        self.__transmission_rate = infectivity
        self.__recovery_rate = recoverability
        self.infectionRadius = lambda: infectionRadius
        
    def apply_to(self, agent, surrounding):
        inf_neigh = 0
        for neigh in surrounding:
            inf_neigh += neigh.isInfected()
        if agent.isInfected() and random() < self.__recovery_rate:
            agent.setSane()
#            if random()<.5:
#                agent.setImmune()
        elif binomial(self.__transmission_rate*agent.vulnerability(), inf_neigh):
            agent.setInfected()

def binomial(p, n):
    """ Return True, False selon une binomiale (au moins un bon) de proba p pour n tirages.
    """
    return random() < 1-(1-p)**n
