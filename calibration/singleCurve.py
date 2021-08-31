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
import fnmatch
from scoop import futures

def get_list():
    path = settings.folder+"simulation/"
    os.chdir(path)
    return [name for name in os.listdir(path) if fnmatch.fnmatch(name, 'tumor.csv.0*')]

''' Run method gets iteration/random number as an argument
'''
def run(randomseed):
    biopsy_ages = settings.biopsy_ages
    path = settings.folder+"simulation/"
    os.chdir(path)
    args = "-ranseed "+str(randomseed)
    for n in range(0,len(biopsy_ages)):
        args = args+" "+str(biopsy_ages[n])
    code = "./a.out " + args
    subprocess.call(code, shell=True)

''' Read method gets the random number seed as an argument
'''
def read(name):
    os.chdir(settings.folder+"simulation")
    #fi = str('tumor.csv.'+str(0)+"."+str(rand))
    df=pd.read_csv(name, sep=',')
    return df

''' Function that samples jumbo-biopsies based on a protocol
'''
def pathology(n,df):
        detection = biopsies.seattlePerturbation(n,df) # Change the protocol function and variables here  
        return detection

''' Main function that is used to calculate mean detection rates. Futures.map 
creates workers on all available computational resources (cpus/processes) and runs in parallel.
'''
def main():
    n = settings.replication
    # Run simulations
    list(futures.map(run, range(1,n+1)))
    # Read outputs
    filenames=list(get_list())
    reads = list(futures.map(read,filenames))
    # Run biopsy and pathology
    detection = list(futures.map(pathology, range(1,len(filenames)+1), reads))
    # Calculate mean detection rates
    all = list()
    for i in range(1,len(filenames)+1):
        samples = list(detection[i-1].values())
        sums = [sum(d) for d in zip(*samples)]
        averages = [d / float(len(samples)) for d in sums]
        all.append(averages)
    sums = [sum(d) for d in zip(*all)]
    averages = [d / float(len(filenames)) for d in sums]
    averages.append(len(filenames))
    missedc = list()
    a = 0
    for i in range(0,len(all)):
        cancer = list()
        if all[i][12] == 1:
            a = a+1
        for j in range(0,11):
            cancer.append(all[i][12]*all[i][j])
        missedc.append(cancer)
    sums = [sum(i) for i in zip(*missedc)]
    if  a > 0:
        avg = [d / a for d in sums]
    else:
        avg = [0 for d in sums]
    averages.append(avg)
    return averages
if __name__ == '__main__':
    x = main()
    print(x)
    #main()
