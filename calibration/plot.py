#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 14:28:51 2017

@author: ozi
"""
''' Plotting results
'''
results =[0.02380952380952381, 0.027662668120683395, 0.03231552162849874, 0.03675027262813522, 0.04031261359505636, 0.044420210832424596, 0.04823700472555434, 0.052453653217011974, 0.0579425663395129, 0.06503089785532534, 0.07044711014176663, 0.2268266085059978, 0.018538713195201745, 1.6977099236641215, 917, [0.47254901960784323, 0.5392156862745099, 0.5921568627450979, 0.6333333333333334, 0.6666666666666667, 0.7000000000000002, 0.7274509803921569, 0.7411764705882353, 0.7588235294117648, 0.7803921568627452, 0.7941176470588236]]
#results=[0.008321167883211491, 0.011068964749866234, 0.015936331671710442, 0.02146842175538478, 0.0268057904575395, 0.033552163076375686, 0.04035995638241124, 0.04834030621328202, 0.05956538187644739, 0.0738867500445088, 0.08457895673847315, 0.3142580559017269, 0.010904397365141535, 2.0183420865230945, 89872, [0.18146938775510207, 0.226265306122449, 0.2969081632653061, 0.36759183673469426, 0.4254285714285714, 0.48597959183673567, 0.5385000000000002, 0.5885714285714299, 0.6487959183673474, 0.7039693877551041, 0.7355816326530633]]
import matplotlib.pyplot as plt
import settings
import numpy as np
labels=range(5,20,1)
x = [n * 100 for n in settings.sensitivity]
#for i in range(0,15):
 #   plt.plot(results[str(i)][0:11],label=str("Seattle Protocol-"+str(labels[i])+"mm"))
plt.plot(x, results[0:11],label="Seattle Protocol",linewidth=1.0,c="black")
#plt.plot(results[str(0)][0:11],label="Seattle Protocol-20mm")
plt.xticks(np.arange(5,100,5))
plt.ylabel("Probability of HGD detection")
plt.xlabel("Biopsy sensitivity (percent)")
plt.legend(loc=(0.2,0.6))
plt.axhline(y=0.008, xmin=0, xmax=1, linestyle='--' ,color="red")
plt.axhline(y=0.033, xmin=0, xmax=1, linestyle='--' ,color="red")
plt.axhline(y=0.075, xmin=0, xmax=1, linestyle='--' ,color="red")
plt.text(50, 0.01, 'O\'Conner et al., 1999')
plt.text(50, 0.035, 'Sharma et al., 2006')
plt.text(10, 0.07, 'Weston et al., 1999')
plt.grid(True)
#plt.gca().invert_xaxis() 
plt.savefig('sensitivity', format='png', dpi=300)
plt.close()

missed = [1-x for x in results[15]]
import matplotlib.pyplot as plt
import settings
import numpy as np
labels=range(5,20,1)
x = [n * 100 for n in settings.sensitivity]
#for i in range(0,15):
 #   plt.plot(results[str(i)][0:11],label=str("Seattle Protocol-"+str(labels[i])+"mm"))
plt.plot(x, missed,label="Seattle Protocol",linewidth=1.0,c="black")
#plt.plot(results[str(0)][0:11],label="Seattle Protocol-20mm")
plt.xticks(np.arange(5,100,5))
plt.ylabel("Probability of missed malignancy")
plt.xlabel("Biopsy sensitivity (percent)")
plt.legend(loc=(0.1,0.8))
plt.axhline(y=0.55, xmin=0, xmax=1, linestyle='--' ,color="red")
plt.axhline(y=0.44, xmin=0, xmax=1, linestyle='--' ,color="red")
plt.axhline(y=0.38, xmin=0, xmax=1, linestyle='--' ,color="red")
plt.axhline(y=0.33, xmin=0, xmax=1, linestyle='--' ,color="red")
plt.axhline(y=0.18, xmin=0, xmax=1, linestyle='--' ,color="red")
plt.axhline(y=0.11, xmin=0, xmax=1, linestyle='--' ,color="red")
plt.text(60, 0.555, 'Peters et al., 1994')
plt.text(60, 0.45, 'Heitmiller et al., 1996')
plt.text(60, 0.39, 'Falk et al., 1999, standard')
plt.text(60, 0.34, 'Falk et al., 1999, jumbo')
plt.text(60, 0.19, 'Konda et al., 2011')
plt.text(60, 0.12, 'Cameron et al., 1997')
plt.grid(True)
#plt.gca().invert_xaxis() 
plt.savefig('missed', format='png', dpi=300)
plt.close()
