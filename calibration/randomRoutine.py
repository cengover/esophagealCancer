#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 12:57:10 2017

@author: ozi
"""

#!/usr/bin/env python
import subprocess
import os
import pandas as pd
import settings
import biopsies
from scoop import futures

''' Run method gets iteration/random number as the argument. Biopsy _ages is fixed.
In the future we can add multiple biopsy_ages with small changes.
'''
def runSim (rand):
    path = settings.folder+"esophageal-cancer-abm/"
    os.chdir(path)
    cmd = path+"a.out -ranseed "+str(rand)+" "+str(settings.biopsy_ages[0])
    subprocess.call(cmd,shell=True)
    fname = str("tumor.csv.0."+str(rand)) 
    if os.path.isfile(fname):
        return 1
    else: 
        return 0
    
''' Read method gets the random number seed as an argument.
'''
def read(randomseed):
    path = settings.folder+"esophageal-cancer-abm/"
    os.chdir(path)
    fi = str('tumor.csv.'+str(0)+"."+str(randomseed))
    df=pd.read_csv(fi, sep=',')
    return df

''' Function that samples jumbo-biopsies based on a protocol
'''
def pathology(n,df,jumbo_x,jumbo_y,number_of_samples):	
    biopsy = biopsies.random_overlap(n,df,jumbo_x,jumbo_y,number_of_samples)         
    settings.onset_ages.append(df['onset_age'][0])
    return biopsy

''' Main function that is used to calculate mean detection rates. Futures.map 
creates workers on all available computational resources (cpus/processes) and runs in parallel.
'''
def detect(lst):
    n = settings.replication       
    '''Here we assume that model was run for N replications and csv files are in the model folder.'''      
    # Create lists of free parameters to be used in the map function
    jumbo_x = [int(round(lst[0]))]*n
    jumbo_y = [int(round(lst[1]))]*n
    number_of_samples = [int(round(lst[2]))]*n
    # Read outputs
    reads = list(futures.map(read,range(1,n+1)))
    # Run biopsy and pathology
    detection = list(futures.map(pathology, range(1,n+1),reads,jumbo_x,jumbo_y,number_of_samples))
    # Calculate mean detection rates
    all = list()
    for i in range(1,n+1):
        x = list(detection[i-1].values())
        sums = [sum(d) for d in zip(*x)]
        averages = [d / float(settings.n_reps) for d in sums]
        all.append(averages)
    sums = [sum(d) for d in zip(*all)]
    averages = [d / float(settings.replication) for d in sums]
    return averages
