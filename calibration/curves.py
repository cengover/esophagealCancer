#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 16:23:09 2017

@author: ozi
"""
import settings
import biopsies
import subprocess, os
import pandas as pd
from scoop import futures

''' Run method gets iteration/random number as the argument. Biopsy _ages is fixed.
In the future we can add multiple biopsy_ages with small changes.
'''
def run(randomseed, biopsy_ages):
    args = "-ranseed "+str(randomseed)
    for n in range(0,len(biopsy_ages)):
        args = args+" "+str(biopsy_ages[n])
    code = "./a.out " + args
    subprocess.call(code, shell=True)

''' Read method gets the random number seed as arguments
'''
def read(rand):
    os.chdir(settings.folder+"esophageal-cancer-abm")
    fi = str('tumor.csv.'+str(0)+"."+str(rand))
    df=pd.read_csv(fi, sep=',')
    return df

''' Function that samples jumbo-biopsies based on a protocol
'''
def pathology(n,df,y_interval):
        detection = biopsies.stomach(n,df,y_interval)  
        return detection
  
''' Main function that is used to calculate mean detection rates for various
scenarios. Futures.map creates workers on all available computational resources 
(cpus/processes) and runs in parallel.
'''      
def main():
    n = settings.replication
    # Run simulations 
    #list(futures.map(runSim, range(1,n+1)))
    intervals = range(10,40,2)
    # Read outputs
    reads = list(futures.map(read,range(1,n+1)))
    results = {}
    j = 0
    for values in intervals:
        y_interval = [int(round(values))]*n              
        # Run biopsy and pathology
        detection = list(futures.map(pathology, range(1,n+1), reads,y_interval))
        all = list()
        for i in range(1,n+1):
            samples = list(detection[i-1].values())
            sums = [sum(d) for d in zip(*samples)]
            averages = [d / float(len(samples)) for d in sums]
            all.append(averages)
        sums = [sum(d) for d in zip(*all)]
        averages = [d / float(settings.replication) for d in sums]
        results[str(j)] = averages
        j=j+1
    return results     
if __name__ == '__main__':
    x = main()
    print(x)
