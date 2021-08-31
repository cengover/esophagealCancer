#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  4 21:53:05 2017
@author: ozi
"""
''' For further resources on how Deap works please go to:
    https://deap.readthedocs.io/en/master/examples/pso_basic.html
'''
import sys
import csv
import operator
import random
import numpy as np
import settings
import calibrationRoutine
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
    r = random.sample(range(0,3),1)
    #part[:] = list(map(operator.add, part, part.speed))
    part[r[0]] = part[r[0]]+part.speed[r[0]]

def eval(n):
    result = calibrationRoutine.detect(n)
    fitness_total = 0
    # These HGD detection rates are approximate values from the paper (for sensitivity 0.10, 0.50, 0.95, respectively). 
    # Kit Curtius, William D. Hazelton, Jihyoun Jeon, and E. Georg Luebeck (2015)
    #A Multiscale Model Evaluates Screening for Neoplasia in Barret's Esophagus
    #PLOS Computational Biology 11(5):e1004272. doi 10.1371/journal.pcbi.100472.
    data = [0.008,0.0330, 0.075]
    data1= [0.57,0.35,0.12]
    for i in range(0,len(data)):
        distance = data[i] - result[i]
        if i == 0 and distance > 0:
            fitness_total = fitness_total + 100000 #*(abs(distance)**2) # Penalty
        if i == 0 and distance < 0:
            fitness_total = fitness_total + abs(distance)**2
        if i == 2 and distance < 0:
            fitness_total = fitness_total + 100000 #*(abs(distance)**2) # Penalty
        if i == 2 and distance > 0:
            fitness_total = fitness_total + abs(distance)**2
        if i == 1:
            fitness_total = fitness_total + abs(distance)**2
    for j in range(0,len(data1)):
        #print(result)
        distance = data1[j] - (1-result[6][j])
        #print(distance)
        if j == 0 and distance < 0:
            fitness_total = fitness_total + 100000 #*(abs(distance/10)**2) # Penalty
        if j == 0 and distance > 0:
            fitness_total = fitness_total + abs(distance/10)**2 # Penalty
        if j == 2 and distance > 0:
            fitness_total = fitness_total + 100000 #*(abs(distance/10)**2) # Penalty
        if j == 2 and distance < 0:
            fitness_total = fitness_total + abs(distance/10)**2 # Penalty
        if j == 1:
            fitness_total = fitness_total + abs(distance/10)**2
    value = fitness_total/(len(data1)+len(data))
    fit = [value]
    return fit

toolbox = base.Toolbox()
toolbox.register("map", futures.map)
# Here pmin and pmax determines the ranges for each parameter when they are randomly initialized
# smin and smax determines the min and max velocity (how much each parameter can move between iterations)
toolbox.register("particle", generate, size=3,
                 pmin=[0.0000000001,0.0000000001,0.01], pmax=[0.0000001,0.0000001,0.1],
                 smin=[-0.000000000005,-0.000000000005,-0.001],
                 smax=[0.0000005,0.0000005,0.02])
toolbox.register("population", tools.initRepeat, list, toolbox.particle)
toolbox.register("update", updateParticle, phi1=0.5, phi2=0.5)
toolbox.register("evaluate", eval, n=settings.replication)

def main():
    # Open the outputfile
    fout = open("outputALL2.txt","w",1)
    # Set random seed
    random.seed(settings.random_seed_for_opt)
    pop = toolbox.population(n=settings.n_population)
    # Here we change randomly assigned particle locations with the ones entered
    # in settings.py for faster convergence.
    initial = settings.initial_pop
    for i, part in enumerate(pop):
        part[0] = initial[i][0]
        part[1] = initial[i][1]
        part[2] = initial[i][2]
        if i == len(initial)-1:
            break
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("std", np.std)
    stats.register("min", np.min)
    stats.register("max", np.max)
    logbook = tools.Logbook()
    logbook.header = ["gen", "evals","best_params","Fitness"] + stats.fields
    GEN = settings.n_generations
    best = None
    csvfile=open('popALL.csv','a')
    for g in range(GEN):
        if g % 50 == 0 and g != 0:
            pop = toolbox.population(n=settings.n_population)
            #initial = settings.initial_pop
            #for i, part in enumerate(pop):
            #    part[0] = initial[i][0]
            #    part[1] = initial[i][1]
            #    part[2] = initial[i][2]
            #    if i == len(initial)-1:
            #        break
            pop[0][0] = best[0]
            pop[0][1] = best[1]
            pop[0][2] = best[2]
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(pop)
        csvfile.flush()
        for part in pop:
            # Here change the input file of the model with new parameters
            input  = open(str(settings.folder+"simulation/input_copy.txt"), 'r')
            output = open(str(settings.folder+"simulation/input.txt"), 'w')
            clean  = input.read().replace("mutate_be 1E-4", str("mutate_be "+str(part[0]))).replace("mutate_dysplasia 1E-5"
                               , str("mutate_dysplasia "+str(part[1]))).replace("diffusion_rate 0.1", str("diffusion_rate "+str(part[2])))
            output.write(clean)
            input.close()
            output.close()
            # Evaluate each particle
            part.fitness.values = toolbox.evaluate()
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
        fout.write(logbook.stream)
        fout.write("\n")
        fout.flush()
        #print(logbook.stream)
    fout.close()
    csvfile.close()
    return pop, logbook, best
if __name__ == "__main__":
    main()
