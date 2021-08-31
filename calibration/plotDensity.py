#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 19 22:39:44 2018

@author: ozi
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 19 10:59:33 2018

@author: ozi
"""
import os
import settings
import pandas as pd
import pickle
# Change the directory pointing to the simulation results
path = "/home/ozi/Documents/cisnet/simulation"
os.chdir(path)
# Read the biopsy output at age 60 for all runs
with open ('cancer.txt', 'rb') as fp:
    cancer = pickle.load(fp)
with open ('dys.txt', 'rb') as fp:
    dys = pickle.load(fp)
with open ('ons.txt', 'rb') as fp:
    ons = pickle.load(fp)
with open ('maxz.txt', 'rb') as fp:
    maxz = pickle.load(fp)
with open ('death.txt', 'rb') as fp:
    death = pickle.load(fp)
with open ('ld.txt', 'rb') as fp:
    ld = pickle.load(fp)
with open ('lc.txt', 'rb') as fp:
    lc = pickle.load(fp)
# Plot density or histogram

#plt.hist([i for i in death if i > 0], bins=20)
#plt.show()

ldys=list()
lcan=list()
for i,n in enumerate(ld):
    if len(ld[i][0]) >= 1: # Here we pick the first xth occurrence.
        ldys.append(sorted(ld[i][0])[0])
    else:
        ldys.append(10000)
for i,n in enumerate(lc):
    if len(lc[i][0]) >=1:
        lcan.append(sorted(lc[i][0])[0])
    else:
        lcan.append(10000)
    ons[i]=ons[i][0]
    death[i]=death[i][0]
    cancer[i]=cancer[i][0]
    dys[i]=dys[i][0]

# save here
path = "/home/ozi/Documents/cisnet/calibration/plots"
os.chdir(path)

#plot cancer after dys
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
sns.set_style('whitegrid')
#print([j for j,z in zip(ldys,lcan) if j < 10000 and z < 10000 and z > j])
#sns.distplot(np.array([j for j,z in zip(ldys,lcan) if j < 10000 and z < 10000 and z > j]),rug=True,hist=False,kde_kws={'clip': (0, 100)})
sns.kdeplot(np.array([z for j,z in zip(ldys,lcan) if j < 10000 and z < 10000 and z > j]),shade=True,cut=0)
#sns.rugplot(np.array([z for j,z in zip(ldys,lcan) if j < 10000 and z < 10000 and z > j]))
#plt.ylabel("Density")
plt.xlabel("Years to cancer onset (from Dysplasia)")
plt.ylabel("Probability")
plt.savefig('cancerdistafterdys', format='png', dpi=300)
plt.close()

# Plot for BE onset age
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
sns.set_style('whitegrid')
sns.kdeplot(np.array([i for i in ons if i < 10000]),shade=True,cut=0)
#sns.rugplot(np.array([i for i in ons if i < 10000]))
#sns.distplot(np.array([i for i in ons if i < 10000]),rug=True,hist=False,kde_kws={'clip': (0, 100)})
#plt.ylabel("Density")
plt.xlabel("Age")
plt.ylabel("Probability")
plt.savefig('beonset', format='png', dpi=300)
plt.close()

# Plot for Death age
sns.set_style('whitegrid')
sns.kdeplot(np.array([i for i in death if i < 10000]),shade=True,cut=0)
#sns.rugplot(np.array([i for i in death if i < 10000]))
#sns.distplot(np.array([i for i in death if i < 10000]),rug=True,hist=False,kde_kws={'clip': (0, 100)})
plt.xticks([0,10,20,30,40,50,60,70,80,90,100])
#plt.ylabel("Density")
plt.xlabel("Age")
plt.ylabel("Probability")
plt.savefig('death', format='png', dpi=1200)
plt.close()

# Plot for Max z
import numpy as np
sns.set_style('whitegrid')
sns.kdeplot(np.array([i for i in maxz if i > 0]),shade=True,cut=0)
#sns.rugplot(np.array([i for i in maxz if i > 0]))
#sns.distplot(np.array([i for i in maxz if i > 0]),rug=True,hist=False,kde_kws={'clip': (0, 10)})
#plt.ylabel("Density")
plt.xlabel("Tissue Depth (grid cells)")
plt.ylabel("Probability")
plt.savefig('maxz', format='png', dpi=300)
plt.close()

# Plot for cancer age and onset
import matplotlib.pyplot as plt
sns.set_style('whitegrid')
sns.kdeplot(np.array([j+i for i,j in zip(ons,cancer) if i < 10000 and j < 10000]),shade=True,cut=0)
#sns.rugplot(np.array([j+i for i,j in zip(ons,cancer) if i < 10000 and j < 10000]))
#sns.distplot(np.array([j+i for i,j in zip(ons,cancer) if i < 10000 and j < 10000]),rug=True,hist=False,kde_kws={'clip': (0, 100)})
#plt.ylabel("Density")
plt.xticks([0,10,20,30,40,50,60,70,80,90,100])
plt.xlabel("Age")
plt.ylabel("Probability")
plt.savefig('cancerdistage', format='png', dpi=300)
plt.close()

sns.set_style('whitegrid')
#sns.kdeplot(np.array([i+j for i,j,n in zip(ons,dys,cancer) if i <10000 and j < 10000 and n < 10000]), linewidth=1.0,c="black")
#sns.kdeplot(np.array([i for i in cancer if i < 10000]), linewidth=1.0,c="black")
#sns.distplot(np.array([i for i in cancer if i < 10000]))
#sns.distplot(np.array([j for i,j in zip(ons,cancer) if i < 10000 and j < 10000]),rug=True,hist=False,kde_kws={'clip': (0, 100)})
sns.kdeplot(np.array([j for i,j in zip(ons,cancer) if i < 10000 and j < 10000]),shade=True,cut=0)
#plt.ylabel("Density")
plt.xlabel("Years to Cancer onset (from BE)")
plt.ylabel("Probability")
plt.savefig('cancerdistonset', format='png', dpi=300)
plt.close()

sns.set_style('whitegrid')
#sns.kdeplot(np.array([i+j for i,j,n in zip(ons,dys,cancer) if i <10000 and j < 10000 and n < 10000]), linewidth=1.0,c="black")
sns.kdeplot(np.array([j-z for i,j,z in zip(ons,cancer,dys) if i < 10000 and j < 10000 and z < 10000 and j > z]),shade=True,cut=0)
#sns.rugplot(np.array([j-z for i,j,z in zip(ons,cancer,dys) if i < 10000 and j < 10000 and z < 10000 and j > z]))
#sns.distplot(np.array([i for i in cancer if i < 10000]))
#sns.distplot(np.array([j-z for i,j,z in zip(ons,cancer,dys) if i < 10000 and j < 10000 and z < 10000 and j > z]),rug=True,hist=False,kde_kws={'clip': (0, 100)})
#sns.kdeplot(np.array([j-z for i,j,z in zip(ons,cancer,dys) if i < 10000 and j < 10000 and z < 10000 and j > z]), linewidth=1.0,c="black")
#plt.ylabel("Density")
plt.xlabel("Years to Cancer onset (from Dysplasia)")
plt.ylabel("Probability")
plt.savefig('cancerdistafterdys', format='png', dpi=300)
plt.close()

# Plot for dysplasia age and onset   
sns.set_style('whitegrid')
sns.kdeplot(np.array([j+i for i,j in zip(ons,dys) if i < 10000 and j < 10000]),shade=True,cut=0)
#sns.rugplot(np.array([j+i for i,j in zip(ons,dys) if i < 10000 and j < 10000]))
#sns.distplot(np.array([j+i for i,j in zip(ons,dys) if i < 10000 and j < 10000]),rug=True,hist=False,kde_kws={'clip': (0, 100)})
#plt.ylabel("Density")
plt.xticks([0,10,20,30,40,50,60,70,80,90,100])
plt.xlabel("Age")
plt.ylabel("Probability")
plt.savefig('dysdistage', format='png', dpi=300)
plt.close()

sns.set_style('whitegrid')
#sns.kdeplot(np.array([i+j for i,j,n in zip(ons,dys,cancer) if i <10000 and j < 10000 and n < 10000]), linewidth=1.0,c="black")
sns.kdeplot(np.array([i for i in cancer if i < 10000]),shade=True,cut=0)
#sns.rugplot(np.array([i for i in cancer if i < 10000]))
#sns.distplot(np.array([i for i in cancer if i < 10000]))
#sns.distplot(np.array([j for i,j in zip(ons,dys) if i < 10000 and j < 10000]),rug=True,hist=False,kde_kws={'clip': (0, 100)})
#sns.kdeplot(np.array([j for i,j in zip(ons,dys) if i < 10000 and j < 10000]), linewidth=1.0,c="black")
#plt.ylabel("Density")
plt.xlabel("Years to Dysplasia onset (from BE)")
plt.ylabel("Probability")
plt.savefig('dysdistonset', format='png', dpi=300)
plt.close()
