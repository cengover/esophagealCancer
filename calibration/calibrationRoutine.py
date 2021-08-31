#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 12:57:10 2017

@author: ozi
"""
import settings
import biopsies
import subprocess
import os,time
import pandas as pd
import fnmatch
from scoop import futures

''' Run method gets iteration/random number as the argument. Biopsy _ages is fixed.
In the future we can add multiple biopsy_ages with small changes.
'''
def get_list():
    path = settings.folder+"simulation/"
    os.chdir(path)
    return [name for name in os.listdir(path) if fnmatch.fnmatch(name, 'tumor.csv.0*')]

def runSim (rand):
    path = settings.folder+"simulation/"
    os.chdir(path)
    cmd = path+"a.out -ranseed "+str(rand)+" "+str(settings.biopsy_ages[0])
    subprocess.run(cmd,shell=True)
    ## Here subprocess finishes but sometimes writing results may take time.
    ## We make sure that csv file is created by waiting additional 2 seconds.
    fname = str("tumor.csv.0."+str(rand))
    #while os.path.isfile(fname) == False:
        #time.sleep(2)
    return 0

''' Read method gets the random number seed as an argument.
'''
def read(name):
    path = settings.folder+"simulation/"
    os.chdir(path)
    #fi = str('tumor.csv.'+str(0)+"."+str(randomseed))
    df=pd.read_csv(name, sep=',')
    return df

''' Function that samples jumbo-biopsies based on a protocol
'''
def pathology(n,df):
    # Here we determine what biopsy protocol we use - seattle
    detection = biopsies.seattlePerturbation(n,df)
    #settings.onset_ages.append(df['onset_age'][0])
    return detection

''' Main function that is used to calculate mean detection rates. Futures.map 
creates workers on all available computational resources (cpus/processes) and runs in parallel.
'''
def detect(n):
    # Run simulations ## Parallelization
    path = settings.folder+"simulation/"
    os.chdir(path)
    cmd = path+"remove.sh"
    subprocess.run("./remove.sh", shell=True)
    list(futures.map(runSim, range(1,n+1)))
    # Read outputs/csvs ## Parallelization
    file_names = list(get_list())
    reads = list(futures.map(read,file_names))
    # Run biopsy and pathology ## Parallelization
    detection = list(futures.map(pathology, range(1,len(file_names)+1), reads))
    # Calculate mean detection rates
    all = list()
    for i in range(1,len(file_names)+1):
        samples = list(detection[i-1].values())
        sums = [sum(d) for d in zip(*samples)]
        averages = [d / float(len(samples)) for d in sums]
        all.append(averages)
    sums = [sum(i) for i in zip(*all)]
    averages = [d / float(len(file_names)) for d in sums]
    #path = settings.folder+"simulation/"
    #os.chdir(path)
    #cmd = "./remove.sh"
    #subprocess.run(cmd,shell=True)
    missedc = list()
    a = 0
    for i in range(0,len(all)):
        cancer = list()
        if all[i][4] == 1:
            a = a+1
        for j in range(0,3):
            cancer.append(all[i][4]*all[i][j])
        missedc.append(cancer)
    sums = [sum(i) for i in zip(*missedc)]
    if  a > 0:
        avg = [d / a for d in sums]
    else:
        avg = [0 for d in sums]
    averages.append(avg)
    return averages
