#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 23:36:36 2018

@author: ozi
"""

import matplotlib.pyplot as plt
import numpy as np

x = np.array([1,2,3,4,5,6,7])
y = np.array([1106102.66,551587.33,277874.66,170560.33,116454.33,91596.33,76646.66])
y = y/1000
e = np.array([4993.19,1296.16,890.14,372.65,206.65,1006.92,1971.55])
e = e/1000
#e = np.log(e)

plt.errorbar(x, y, e, marker='.',linewidth=1,elinewidth=10,ecolor='r',capsize=10)
plt.xticks(x,[2,4,8,16,32,64,128])
plt.yticks(np.arange(y.min(), y.max(), 100))
plt.ylabel("Runtime (seconds)")
plt.xlabel("The number of processes")
#plt.show()
plt.savefig('runtime', format='png', dpi=600)