#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 19 10:59:33 2018

@author: ozi
"""
import pickle
import os
import settings
import pandas as pd
import fnmatch
from scoop import futures

# Read the names of the files
def get_list():
    path = settings.folder+"simulation/"
    #os.chdir(path)
    return [name for name in os.listdir(path) if fnmatch.fnmatch(name, 'tumor.csv.0*')]

files = get_list()
# Read method
def read(name):
    # Change the directory pointing to the simulation results
    path = settings.folder+"simulation/"
    os.chdir(path)
    #fi = str('tumor.csv.'+str(0)+"."+str(i))
    df=pd.read_csv(name, sep=',')
    m = 0
    if len(df) > 0:
        m = df["zcoord"].max()
    else:
        m = 0
    return m

def main():
    # Read outputs
    filenames=list(get_list())
    reads = list(futures.map(read,filenames))
    return reads

if __name__ == '__main__':
    #path = settings.folder+"calibration/"
    #os.chdir(path)
    x = main()
    with open('maxz.txt', 'wb') as fp:
        pickle.dump(x, fp)
    fp.close()



# Plot density or histogram
'''import matplotlib.pyplot as plt
plt.hist(maxz, bins=6)
plt.show()

import numpy as np
import seaborn as sns
sns.set_style('whitegrid')
sns.kdeplot(np.array(maxz), bw=0.5)'''
