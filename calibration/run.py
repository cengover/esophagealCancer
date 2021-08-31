#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 16:23:09 2017

@author: ozi
"""
import settings
import subprocess, os
import pandas as pd
from scoop import futures

''' Run method gets iteration/random number as an argument
'''
def run(randomseed):
    path = settings.folder+"simulation/"
    os.chdir(path)
    args = "-ranseed "+str(randomseed)
    biopsy_ages = [100]
    for n in biopsy_ages:
        args = args+" "+str(n)
    code = "./a.out " + args
    subprocess.call(code, shell=True)

def main():
    n = settings.replication
    # Run simulations
    list(futures.map(run, range(1,n+1)))
if __name__ == '__main__':
    main()
