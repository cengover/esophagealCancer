#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 12:57:10 2017

@author: ozi
"""
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
def pathology(n, df, slice_x, slice_y,jumbo_x, jumbo_y):
    biopsy = biopsies.random_slice(n,df,slice_x, slice_y,jumbo_x, jumbo_y)
    #settings.onset_ages.append(df['onset_age'][0])
    return biopsy

''' Main function that is used to calculate mean detection rates. Futures.map 
creates workers on all available computational resources (cpus/processes) and runs in parallel.
'''
def detect(lst):
    n = settings.replication       
    '''Here we assume that model was run for N replications and csv files are in the model folder.'''      
    # Create lists of free parameters to be used in the map function
    slice_x = [int(round(lst[0]))]*n
    slice_y = [int(round(lst[1]))]*n
    jumbo_x = [int(round(lst[2]))]*n
    jumbo_y = [int(round(lst[3]))]*n
    # Read outputs
    reads = list(futures.map(read,range(1,n+1)))
    # Run biopsy and pathology
    detection = list(futures.map(pathology, range(1,n+1), reads, slice_x, slice_y,jumbo_x, jumbo_y))
    # Calculate mean detection rates
    all = list()
    for i in range(1,n+1):
        samples = list(detection[i-1].values())
        sums = [sum(d) for d in zip(*samples)]
        averages = [d / float(len(samples)) for d in sums]
        all.append(averages)
    sums = [sum(d) for d in zip(*all)]
    averages = [d / float(settings.replication) for d in sums]
    return averages