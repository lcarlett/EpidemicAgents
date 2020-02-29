from random import random

class Desease(object):
    Sane, Infected, Immune = range(3)
    def __init__(self, infectivity, recoverability):
        self.__transmission_rate = infectivity
        self.__recovery_rate = recoverability
        
    def infectionRadius(self):
        return 15
        
    def apply_to(self, agent, surrounding):
        inf_neigh = 0
        for neigh in surrounding:
            inf_neigh += neigh.isInfected()
        if agent.isInfected() and random() > self.__transmission_rate*inf_neigh - self.__recovery_rate:
            agent.setSane()
#            if random()<.5:
#                agent.setImmune()
        elif random() < self.__transmission_rate*inf_neigh*agent.vulnerability():
            agent.setInfected()

