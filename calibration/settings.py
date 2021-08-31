#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 10:27:37 2017

@author: ozi
"""

''' Global parameters '''
folder = '/home/ozi/Documents/cisnet/'

''' Biopsy related parameters '''
onset_ages = list() # To get onset_ages for each random seed
grid_width = 180
# Jumbo biopsy sizes
jumbo_x = 12
jumbo_y = 7
interval_x = (grid_width - 4*jumbo_x)//4 # Cell intervals between samples on the circumference (x-axis)
interval_y = 40 # Cell intervals between samples on the legth (y-axis)
# For optimization we only use three sensitivity levels, for visualization we use all
#sensitivity = [0.05,0.5,0.95]
sensitivity = [0.05,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,0.95]
n_reps = 100 # number of random samples for probabilistic runs
''' Simulation related parameters '''
biopsy_ages = [60]
random_seed_start_for_sim = 4000 # Starting random number seed for the simulation
replication = 1000 # How many times simulation will be run for each parameter set-up
''' Optimization related parameters '''
random_seed_for_opt = 4000 # Random seed for the optimization routine
n_population = 20 # Number of particles to generate in the optimization routines
n_generations = 500 # Number of generations to run optimization routines
# Initial population is the one that we start searching for optimum parameters.
# It is used in particle swarm (optimization.py).
initial_pop = [[2.1081578306624674e-08, 3.097614356717331e-08, 0.18186813788810668],
[2.5398016868475946e-06, 5.000943575620808e-08, 0.0377476356838063],
[6.055759261539668e-06, 1.5250784715703464e-06, 0.13602144309189758],
[1.0338703153564799e-07, 8.073225708812578e-09, 0.24457164448701161],
[1.512779671313914e-08, 1.661426241396711e-07, 0.16587140367010337],
[4.801509134975535e-06, 9.062144037960342e-07, 0.25803934383782849],
[3.1382996278230959e-08, 1.3408537840070214e-08, 0.17148491241001993],
[1.1382996278230959e-07, 4.3408537840070214e-09, 0.0148491241001993],
[4.096849235215503e-09, 3.272328574710641e-07, 0.16149473125255923],
[7.267606339193968e-08, 8.051581132156611e-09, 0.2245716444870116],
[5.842937630072671e-06, 5.4990700331510884e-07, 0.206570501009474265],
[5.687643805654544e-06, 2.514381113581014e-08, 0.02107310254708571],
[7.055759261539668e-06, 1.5250784715703464e-06, 0.13602144309189758],
[1.0338703153564799e-07, 2.073225708812578e-09, 0.24457164448701161],
[1.512779671313914e-06, 1.661426241396711e-09, 0.126587140367010337],
[4.801509134975535e-09, 9.062144037960342e-06, 0.23803934383782849],
[2.1382996278230959e-09, 4.3408537840070214e-09, 0.24148491241001993],
[1.1382996278230959e-06, 4.3408537840070214e-06, 0.11148491241001993],
[4.096849235215503e-09, 1.272328574710641e-06, 0.12149473125255923],
[1.8394478959861553e-08, 1.970854603160159e-08, 0.2049072031021171]]

