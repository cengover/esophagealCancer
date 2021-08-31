#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 19 11:20:30 2018

@author: ozi
"""
import os
import settings
import pandas as pd
import pickle
import fnmatch
from scoop import futures

def get_list():
    path = settings.folder+"simulation/"
    os.chdir(path)
    return [name for name in os.listdir(path) if fnmatch.fnmatch(name, 'intervals.csv.0*')]

''' Read method gets the random number seed as an argument
'''
'''def read(rand):
    path = settings.folder+"simulation/"
    os.chdir(path)
    d=list()
    c=list()
    res = {}
    checkD = False
    checkC = False
    for j in range(0,60):
        fi = str('tumor.csv.'+str(j)+"."+str(rand))
        df=pd.read_csv(fi, sep=',')
        if len(df.loc[df['type'] == 2]) > 0 and checkD is not True:
            d.append(j+1)
            checkD = True
        if len(df.loc[df['type'] == 3]) > 0 and checkC is not True:
            c.append(j+1)
            checkC = True
        if checkD == True and checkC == True:
            break
    if checkD == False:
        d.append(0)
    if checkC == False:
        c.append(0)
    res["cancer"] = c
    res["dysplasia"] = d
    return res '''

def read(name):
    path = settings.folder+"simulation/"
    os.chdir(path)
    d=list()
    c=list()
    o=list()
    p=list()
    ld=list()
    lc=list()
    res = {}
    #fi = str('intervals.csv.0.'+str(rand))
    df=pd.read_csv(name, sep=',')
    o.append(df['onsetAge'])
    d.append(df['timeDysplasia'])
    c.append(df['timeCancer'])
    p.append(df['deathAge'])
    ld.append(df['timeDysList'])
    lc.append(df['timeCanList'])
    res["cancer"] = c
    res["dysplasia"] = d
    res["onset"] = o
    res["death"] = p
    res["ld"] = ld
    res["lc"] = lc
    return res

def main():
    # Read outputs
    filenames=list(get_list())
    reads = list(futures.map(read,filenames))
    cancer=list()
    dys=list()
    ons=list()
    death=list()
    ld=list()
    lc=list()
    for i in reads:
        cancer.append(i["cancer"][0])
        dys.append(i["dysplasia"][0])
        ons.append(i["onset"][0])
        death.append(i["death"][0])
        ld.append(i["ld"])
        lc.append(i["lc"])
    with open('cancer.txt', 'wb') as fp:
        pickle.dump(cancer, fp)
    fp.close()
    with open('dys.txt','wb') as fd:
        pickle.dump(dys,fd)
    fd.close()
    with open('ons.txt','wb') as fo:
        pickle.dump(ons,fo)
    fo.close()
    with open('death.txt', 'wb') as fde:
        pickle.dump(death,fde)
    fde.close()
    with open('ld.txt', 'wb') as d:
        pickle.dump(ld,d)
    d.close()
    with open('lc.txt', 'wb') as c:
        pickle.dump(lc,c)
    c.close()

if __name__ == '__main__':
    main()
    #with open ('cancer.txt', 'rb') as fp:
        #itemlist = pickle.load(fp)

'''# Plot density or histogram
import matplotlib.pyplot as plt
plt.hist([i for i in cancer if i > 0], bins=6)
plt.show()
import numpy as np
import seaborn as sns
sns.set_style('whitegrid')
sns.kdeplot(np.array([i for i in cancer if i > 0]), bw=0.5)
'''
