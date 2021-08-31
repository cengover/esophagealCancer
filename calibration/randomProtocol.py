#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  4 21:53:05 2017
@author: ozi
"""
import operator
import random
import numpy as np
import settings
import randomRoutine
from scoop import futures
from deap import base
from deap import creator
from deap import tools

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Particle", list, fitness=creator.FitnessMin, speed=list, 
    smin=list, smax=list, best=None)

def generate(size, pmin, pmax, smin, smax):
    part = creator.Particle(random.uniform(pmin[i], pmax[i]) for i in range(size))
    part.speed = [random.uniform(smin[i], smax[i]) for i in range(size)]
    part.smin = smin
    part.smax = smax
    return part

def updateParticle(part, best, phi1, phi2):
    u1 = (random.uniform(0, phi1) for _ in range(len(part)))
    u2 = (random.uniform(0, phi2) for _ in range(len(part)))
    v_u1 = map(operator.mul, u1, map(operator.sub, part.best, part))
    v_u2 = map(operator.mul, u2, map(operator.sub, best, part))
    part.speed = list(map(operator.add, part.speed, map(operator.add, v_u1, v_u2)))
    for i, speed in enumerate(part.speed):
        if speed < -part[i]:
            part.speed[i] = part.smin[i]
        elif speed > part.smax[i]:
            part.speed[i] = part.smax[i]
    part[:] = list(map(operator.add, part, part.speed))    
 
def eval(lst):
    result = randomRoutine.detect(lst)
    fitness_total = 0
    data = [10] # Num of biopsies on average with Seattle Protocol
    for i in range(0,3):
        fitness_total = fitness_total + (abs(result[3]-result[i]))**2
    value = fitness_total/11
    value = value + ((result[5]-data[0])/float(10))**2
    fit = [value]
    return fit

toolbox = base.Toolbox()
toolbox.register("map", futures.map)
# Here pmin and pmax determines the ranges for each parameter when they are randomly initialized
# smin and smax determines the min and max velocity (how much each parameter can move between iterations)
toolbox.register("particle", generate, size=3, 
                 pmin=[2,2,4], pmax=[15,10,20], 
                 smin=[-0.5,-0.5,-1], 
                 smax=[0.5,0.5,2])
toolbox.register("population", tools.initRepeat, list, toolbox.particle)
toolbox.register("update", updateParticle, phi1=0.5, phi2=0.5)
toolbox.register("evaluate", eval)

def main():   
    random.seed(settings.random_seed_for_opt)
    pop = toolbox.population(n=settings.n_population)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("std", np.std)
    stats.register("min", np.min)
    stats.register("max", np.max)
    logbook = tools.Logbook()
    logbook.header = ["gen", "evals","best_params","Fitness"] + stats.fields
    GEN = settings.n_generations
    best = None
    for g in range(GEN):
        print(pop)
        for part in pop:
            # Prepare the list that is passed to pathology as an argument
            lst = list()
            for i in range(0,3): # 3 is the number of free parameters
                lst.append(part[i])
            # Evaluate each particle
            part.fitness.values = toolbox.evaluate(lst)
            if not part.best or part.best.fitness < part.fitness:
                part.best = creator.Particle(part)
                part.best.fitness.values = part.fitness.values
            if not best or best.fitness < part.fitness:
                best = creator.Particle(part)
                best.fitness.values = part.fitness.values
        for part in pop:
            toolbox.update(part, best)
        # Gather all the fitnesses in one list and print the stats
        logbook.record(gen=g, evals=len(pop), best_params = best, Fitness = best.fitness, **stats.compile(pop))
        print(logbook.stream)
    return pop, logbook, best
if __name__ == "__main__":
    main()
