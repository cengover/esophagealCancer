#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 10:26:18 2017

@author: ozi
"""
import settings
import numpy as np
import pandas as pd
import random
# Division function
def divided(x,y):
    try:
        return int(round(x/float(y)))
    except ZeroDivisionError:
        return None

''' Seattle Protocol - Determines HGD only when n_f fraction of cells are
detected with dysplasia or cancer
'''
def seattle(n,df):
    biopsy = {} # Keys are biopsy samplings
    sampled_x = {}
    sampled_y = {}
    if len(df) > 0: # determine the length of the BE - y axis       
        max_y = int(df['ycoord'].max())
    else:
        max_y = 0
    '''Sample points on the length '''
    start_y = 0 # assign here so that no need to re-calculate in the loop
    j = 0
    end = 0
    while start_y < max_y: # Find all y-axis sampled points.
         j = j + 1
         end = start_y + settings.jumbo_y
         if (end > max_y):
             end = max_y 
         sampled_y[str(j)] = range(start_y,end,1)
         start_y = start_y + settings.jumbo_y + settings.interval_y
    # Check if there is no dysplasia or cancer- do nothing
    if (len(df.query("type == 3 or type == 2")) == 0 or len(df) == 0):
        detected = list()
        for m in range(0,len(settings.sensitivity)+2):
            detected.append(0)
        detected.append(len(sampled_y)*4)
        for biopsy_start in range(0,settings.jumbo_x+settings.interval_x,1):
            biopsy[str(biopsy_start)] = detected
    # Otherwise, biopsy sampling
    else:
        ''' Collect different biopsy samples'''    
        for biopsy_start in range(0,settings.jumbo_x+settings.interval_x,1):
            detected = list()
            '''Sample points on the width - circumference'''
            start_x = biopsy_start
            for i in range(1,5): # Getting 4 samples on the x-axis
                end = start_x + settings.jumbo_x
                if (end < settings.grid_width):
                    sampled_x[str(i)] = range(start_x,end,1)
                    start_x = start_x + settings.jumbo_x + settings.interval_x
                else:
                    sampled_x[str(i)] = [m for z in (range(start_x,settings.grid_width,1) , range(0, end-settings.grid_width,1)) for m in z]   
            '''Check sampled points against sensitivity'''
            for m in range(0,len(settings.sensitivity)):
                detected.append(0)
                for i in range(1,len(sampled_x)+1):
                    for j in range(1,len(sampled_y)+1):
                        sample = df.loc[df['xcoord'].isin(sampled_x[str(i)]) & df['ycoord'].isin(sampled_y[str(j)])]
                        if (len(sample)!=0):
                            condition = float(len(sample[sample['type'].isin([2,3])]))/float(len(sample))
                            if (condition >= (1 - settings.sensitivity[m])):
                                detected[m] = 1
                                break
                    if detected[m] == 1:
                        break
            detected.append(1) #There is at least one dysplasia or cancer cell
            if len(df.query("type == 3")) > 0: # check if there is any cancer cell
                detected.append(1)
            else:
                detected.append(0)
            detected.append(len(sampled_y)*4)
            biopsy[str(biopsy_start)] = detected
    return biopsy

''' Seattle Protocol with variable y-axis (length) distance - Determines HGD only when n_f fraction of cells are
detected with dysplasia or cancer
'''
def varSeattle(n,df,y_interval):
    biopsy = {} # Keys are biopsy samplings
    sampled_x = {}
    sampled_y = {}
    np.random.seed(n)
    if len(df) > 0: # determine the length of the BE - y axis       
        max_y = int(df['ycoord'].max())
    else:
        max_y = 0
    '''Sample points on the length '''
    start_y = 0 # assign here so that no need to re-calculate in the loop
    j = 0
    end = 0
    while start_y < max_y:
         j = j + 1
         end = start_y + settings.jumbo_y
         if (end > max_y):
             end = max_y 
         sampled_y[str(j)] = range(start_y,end,1)
         start_y = start_y + settings.jumbo_y + y_interval
    # Check if there is no dysplasia or cancer- do nothing
    if (len(df.query("type == 3 or type == 2")) == 0 or len(df) == 0):
        detected = list()
        for m in range(0,len(settings.sensitivity)+2): #+2 is for real_rates and the cancer rates
            detected.append(0)
        # Add total number of samples. 4 is the number of samples on x-axis
        detected.append(len(sampled_y)*4) 
        for biopsy_start in range(0,settings.jumbo_x+settings.interval_x):
            biopsy[str(biopsy_start)] = detected
    # Otherwise, biopsy sampling
    else:
        ''' Collect different biopsy samples'''    
        for biopsy_start in range(0,settings.jumbo_x+settings.interval_x):
            detected = list()
            '''Sample points on the width - circumference'''
            start_x = biopsy_start
            for i in range(1,5): # Getting 4 samples on the x-axis
                end = start_x + settings.jumbo_x
                if (end < settings.grid_width):
                    sampled_x[str(i)] = range(start_x,end,1)
                    start_x = start_x + settings.jumbo_x + settings.interval_x
                else:
                    sampled_x[str(i)] = [m for z in (range(start_x,settings.grid_width,1) , range(0, end-settings.grid_width,1)) for m in z]   
            '''Check sampled points against sensitivity'''
            for m in range(0,len(settings.sensitivity)):
                detected.append(0)
                for i in range(1,len(sampled_x)+1):
                    for j in range(1,len(sampled_y)+1):
                        sample = df.loc[df['xcoord'].isin(sampled_x[str(i)]) & df['ycoord'].isin(sampled_y[str(j)])]
                        if (len(sample)!=0):
                            condition = float(len(sample[sample['type'].isin([2,3])]))/float(len(sample))
                            if (condition >= (1 - settings.sensitivity[m])):
                                detected[m] = 1
                                break
                    if detected[m] == 1:
                        break
            detected.append(1) #There is at least one dysplasia or cancer cell
            if len(df.query("type == 3")) > 0: # check if there is any cancer cell
                detected.append(1)
            else:
                detected.append(0)
            # Add total number of samples. 4 is the number of samples on x-axis
            detected.append(len(sampled_y)*4)
            biopsy[str(biopsy_start)] = detected
    return biopsy

''' Seattle Protocol with variable y-axis (length) distance - Determines HGD only when n_f fraction of cells are
detected with dysplasia or cancer
'''
def seattleVary(n,df):
    biopsy = {} # Keys are biopsy samplings
    sampled_x = {}
    sampled_y = {}
    random.seed(n)
    if len(df) > 0: # determine the length of the BE - y axis       
        max_y = int(df['ycoord'].max())
    else:
        max_y = 0
    # Check if there is no dysplasia or cancer- do nothing
    if (len(df.query("type == 3 or type == 2")) == 0 or len(df) == 0):
        detected = list()
        for m in range(0,len(settings.sensitivity)+2): #+2 is for real_rates and the cancer rates
            detected.append(0)
        # Add total number of samples
        detected.append(0) 
        for biopsy_start in range(0,settings.jumbo_x+settings.interval_x):
            biopsy[str(biopsy_start)] = detected
    # Otherwise, biopsy sampling
    else:
        ''' Collect different biopsy samples'''
        for biopsy_start in range(0,settings.jumbo_x+settings.interval_x,1):
            '''Sample points on the length '''
            start_y = round(random.uniform(24,48)) # assign here so that no need to re-calculate in the loop
            j = 0
            end = 0
            while start_y < max_y:
                j = j + 1
                end = start_y + settings.jumbo_y
                if (end > max_y):
                    break
                sampled_y[str(j)] = range(start_y,end,1)
                start_y = end + round(random.uniform(24,48))
            detected = list()
            '''Sample points on the width - circumference'''
            start_x = biopsy_start
            for i in range(1,5): # Getting 4 samples on the x-axis
                end = start_x + settings.jumbo_x
                if (end < settings.grid_width):
                    sampled_x[str(i)] = range(start_x,end,1)
                    start_x = start_x + settings.jumbo_x + settings.interval_x
                else:
                    sampled_x[str(i)] = [m for z in (range(start_x,settings.grid_width,1) , range(0, end-settings.grid_width,1)) for m in z]   
                '''Check sampled points against sensitivity'''
            for m in range(0,len(settings.sensitivity)):
                detected.append(0)
                for i in range(1,len(sampled_x)+1):
                    for j in range(1,len(sampled_y)+1):
                        sample = df.loc[df['xcoord'].isin(sampled_x[str(i)]) & df['ycoord'].isin(sampled_y[str(j)])]
                        if (len(sample)!=0):
                            condition = float(len(sample[sample['type'].isin([2,3])]))/float(len(sample))
                            if (condition >= (1 - settings.sensitivity[m])):
                                detected[m] = 1
                                break
                    if detected[m] == 1:
                        break
            detected.append(1) #There is at least one dysplasia or cancer cell
            if len(df.query("type == 3")) > 0: # check if there is any cancer cell
                detected.append(1)
            else:
                detected.append(0)
            # Add total number of samples. 4 is the number of samples on x-axis
            detected.append(len(sampled_y)*4)
            biopsy[str(biopsy_start)] = detected
    return biopsy

''' Seattle Protocol with variable y-axis (length) distance - Determines HGD only when n_f fraction of cells are
detected with dysplasia or cancer
'''
def seattlePerturbation(n,df):
    biopsy = {} # Keys are biopsy samplings
    sampled_x = {}
    sampled_y = {}
    random.seed(n)
    if len(df) > 0: # determine the length of the BE - y axis       
        max_y = int(df['ycoord'].max())
    else:
        max_y = 0
    # Check if there is no dysplasia or cancer- do nothing
    if (len(df.query("type == 3 or type == 2")) == 0 or len(df) == 0):
        detected = list()
        for m in range(0,len(settings.sensitivity)+2): #+2 is for real_rates and the cancer rates
            detected.append(0)
        # Add total number of samples
        detected.append(0) 
        for biopsy_start in range(0,settings.jumbo_x+settings.interval_x):
            biopsy[str(biopsy_start)] = detected
    # Otherwise, biopsy sampling
    else:
        ''' Collect different biopsy samples'''
        for biopsy_start in range(0,settings.n_reps,1):
            '''Sample points on the length '''
            start_y = round(random.uniform(24,48)) # assign here so that no need to re-calculate in the loop
            j = 0
            end = 0
            while start_y < max_y:
                j = j + 1
                end = start_y + settings.jumbo_y
                if (end > max_y):
                    break
                sampled_y[str(j)] = range(start_y,end,1)
                start_y = end + round(random.uniform(24,48))
            detected = list()
            '''Sample points on the width - circumference'''
            start_x = 16
            for i in range(1,5): # Getting 4 samples on the x-axis
                end = start_x + settings.jumbo_x
                if (end < settings.grid_width):
                    sampled_x[str(i)] = range(start_x,end,1)
                    start_x = start_x + settings.jumbo_x + settings.interval_x
                else:
                    sampled_x[str(i)] = [m for z in (range(start_x,settings.grid_width,1) , range(0, end-settings.grid_width,1)) for m in z]      
            '''Perturbations'''
            for m in range(0,len(settings.sensitivity)):
                detected.append(0)
            for i in range(1,len(sampled_x)+1):
                for j in range(1,len(sampled_y)+1):
                    dx = list(sampled_x[str(i)])
                    perturbation = round(random.uniform(-16,16))
                    for ind,x in enumerate(dx):
                        dx[ind] = dx[ind]+perturbation
                    dy = list(sampled_y[str(j)])
                    perturbation = round(random.uniform(-6,6))
                    for ind,y in enumerate(dy):
                        if(dy[ind]+perturbation<max_y):
                            dy[ind] = dy[ind]+perturbation
                        else:
                            dy = sampled_y[str(j)]
                    sample = df.loc[df['xcoord'].isin(dx) & df['ycoord'].isin(dy)]
                    if (len(sample)!=0):
                        condition = float(len(sample[sample['type'].isin([2,3])]))/float(len(sample))
                        '''Check sampled points against sensitivity'''
                        for m in range(0,len(settings.sensitivity)):
                            if (condition >= (1 - settings.sensitivity[m])):
                                detected[m] = 1
                    if sum(detected) == len(settings.sensitivity):
                        break        
            detected.append(1) #There is at least one dysplasia or cancer cell
            if len(df.query("type == 3")) > 0: # check if there is any cancer cell
                detected.append(1)
            else:
                detected.append(0)
            # Add total number of samples. 4 is the number of samples on x-axis
            detected.append(len(sampled_y)*4)
            biopsy[str(biopsy_start)] = detected
    return biopsy

''' Probabilistic biopsy protocol - Samples n_f fraction of biopsy samples multiple
times and if algorithm detects 1 dysplasia or cancer determines HGD.
'''       
def probabilistic(n,df):
    biopsy = {} # Keys are biopsy samplings
    sampled_x = {}
    sampled_y = {}
    start_y = 0 # assign here so that no need to re-calculate in the loop
    np.random.seed(n)
    if len(df) > 0: # determine the length of the BE - y axis       
        max_y = int(df['ycoord'].max())
    else:
        max_y = 0
    '''Sample points on the length '''
    start_y = 0
    j = 0
    end = 0
    while start_y < max_y:
        j = j + 1
        end = start_y + settings.jumbo_y
        if (end > max_y):
            end = max_y 
        sampled_y[str(j)] = range(start_y,end,1)
        start_y = start_y + settings.jumbo_y + settings.interval_y
     # Check if there is no dysplasia or cancer- do nothing
    if (len(df.query("type == 3 or type == 2")) == 0 or len(df) == 0):
        detected = list()
        for m in range(0,len(settings.sensitivity)+2):
            detected.append(0)
        # Add total number of samples. 4 is the number of samples on x-axis
        detected.append(len(sampled_y)*4)
        for biopsy_start in range(0,settings.jumbo_x+settings.interval_x,1):
            biopsy[str(biopsy_start)] = detected
    # Otherwise, biopsy sampling
    else:
        ''' Collect different biopsy samples'''    
        for biopsy_start in range(0,settings.jumbo_x+settings.interval_x,1):
            detected = list()
            '''Sample points on the width - circumference'''
            start_x = biopsy_start
            for i in range(1,5):
                end = start_x + settings.jumbo_x
                if (end < settings.grid_width):
                    sampled_x[str(i)] = range(start_x,end,1)
                    start_x = start_x + settings.jumbo_x + settings.interval_x
                else:
                    sampled_x[str(i)] = [m for z in (range(start_x,settings.grid_width,1), range(0, end-settings.grid_width,1)) for m in z]  
            '''Check sampled points against sensitivity'''
            for m in range(0,len(settings.sensitivity)):
                detected.append(0)
                sample = pd.DataFrame() 
                for i in range(1,len(sampled_x)+1):
                    for j in range(1,len(sampled_y)+1):
                        d = df.loc[df['xcoord'].isin(sampled_x[str(i)]) & df['ycoord'].isin(sampled_y[str(j)])]
                        sample = sample.append(d)
                count = 0
                for v in range(0,settings.number_of_samples):
                    rsample = sample.sample(frac=settings.sensitivity[m])
                    if (len(rsample) > 0 and len(rsample[rsample['type'].isin([2,3])]) >= 1):
                        count = count + 1
                detected[m] = float(count)/settings.number_of_samples
            detected.append(1) #There is at least one dysplasia or cancer cell
            if len(df.query("type == 3")) > 0: # check if there is any cancer cell
                detected.append(1)
            else:
                detected.append(0)
            # Add total number of samples. 4 is the number of samples on x-axis
            detected.append(len(sampled_y)*4)
            biopsy[str(biopsy_start)] = detected
    return biopsy
''' Stomach Protocol - Determines HGD only when n_f fraction of cells are
detected with dysplasia or cancer but does the sampling closer to the stomach.
We simply shrink the gap/distance on the y-axis between samples.
So, the number of samples stays the same as Seattle protocol.
'''
def stomach(n,df,shrink_by):
    biopsy = {} # Keys are biopsy samplings
    sampled_x = {}
    sampled_y = {}
    start_y = 0 # assign here so that no need to re-calculate in the loop
    if len(df) > 0: # determine the length of the BE - y axis       
        max_y = int(df['ycoord'].max())
    else:
        max_y = 0
    '''Sample points on the length '''
    start_y = 0
    j = 0
    end = 0
    while start_y < max_y:
        j = j + 1
        end = start_y + settings.jumbo_y
        if (end > max_y):
            end = max_y 
        sampled_y[str(j)] = list(range(start_y,end))
        start_y = start_y + settings.jumbo_y + settings.interval_y
    for r in range(2,len(sampled_y)+1):    
        sampled_y[str(r)][:] = [y - shrink_by for y in sampled_y[str(r)]]
    # Check if there is no dysplasia or cancer- do nothing
    if (len(df.query("type == 3 or type == 2")) == 0 or len(df) == 0):
        detected = list()
        for m in range(0,len(settings.sensitivity)+2):
            detected.append(0)
        # Add total number of samples. 4 is the number of samples on x-axis
        detected.append(len(sampled_y)*4)
        for biopsy_start in range(0,settings.jumbo_x+settings.interval_x,1):
            biopsy[str(biopsy_start)] = detected
    # Otherwise, biopsy sampling
    else:
        ''' Collect different biopsy samples'''
        for biopsy_start in range(0,settings.jumbo_x+settings.interval_x):
            '''Sample points on the width - circumference'''
            start_x = biopsy_start
            for i in range(1,5): # Four samples on the x-axis
                end = start_x + settings.jumbo_x
                if (end < settings.grid_width):
                    sampled_x[str(i)] = range(start_x,end,1)
                    start_x = start_x + settings.jumbo_x + settings.interval_x
                else:
                    sampled_x[str(i)] = [m for z in (range(start_x,settings.grid_width,1) , range(0, end-settings.grid_width,1)) for m in z]  
            '''Check sampled points against sensitivity'''
            detected = list()
            for m in range(0,len(settings.sensitivity)):
                detected.append(0)
                for i in range(1,len(sampled_x)+1):
                    for j in range(1,len(sampled_y)+1):
                        sample = df.loc[df['xcoord'].isin(sampled_x[str(i)]) & df['ycoord'].isin(sampled_y[str(j)])]
                        if (len(sample)!=0):
                            condition = float(len(sample[sample['type'].isin([2,3])]))/float(len(sample))
                            if (condition >= (1 - settings.sensitivity[m])):
                                detected[m] = 1
                                break
                    if detected[m] == 1:
                        break
            detected.append(1) #There is at least one dysplasia or cancer cell
            if len(df.query("type == 3")) > 0: # check if there is any cancer cell
                detected.append(1)
            else:
                detected.append(0)
            # Add total number of samples. 4 is the number of samples on x-axis
            detected.append(len(sampled_y)*4)
            biopsy[str(biopsy_start)] = detected
    return biopsy

''' Random Protocol - Determines HGD only when n_f fraction of cells are
detected with dysplasia or cancer. We slice the grid into quadrants and get a sample
from each slice. This way samples do not overlap. 
'''
def random_slice(n,df,slice_x, slice_y, jumbo_x, jumbo_y):
    biopsy = {} # Keys are biopsy samplings
    sampled_x = {}
    sampled_y = {}
    slices_x = {}
    slices_y = {}
    np.random.seed(n)
    # Check if there is no dysplasia or cancer- do nothing
    if (len(df.query("type == 3 or type == 2")) == 0 or len(df) == 0):
        detected = list()
        for m in range(0,len(settings.sensitivity)+2):
            detected.append(0)
        # Find the number of samples collected
        detected.append(slice_x*slice_y)
        for biopsy_start in range(0,settings.jumbo_x+settings.interval_x):
            biopsy[str(biopsy_start)] = detected
    # Otherwise, biopsy sampling
    else:
        if len(df) > 0: # determine the length of the BE - y axis       
            max_y = int(df['ycoord'].max())
        else:
            max_y = 0
        ''' Divide the grid into small slices '''
        x_width = divided(settings.grid_width,slice_x)
        for i in range(0,slice_x):
            if i == (slice_x-1):
                slices_x[str(i)] = range(i*x_width, settings.grid_width)
            else:
                slices_x[str(i)] = range(i*x_width, i*x_width+x_width)
        y_width = int(round(max_y/float(slice_y)))
        if (slice_y>max_y):
            slices_y[str(0)] = range(0,max_y)
        else:    
            for j in range(0,slice_y):
                if j == (slice_y-1):
                    slices_y[str(j)] = range(j*y_width, max_y)
                else:
                    slices_y[str(j)] = range(j*y_width, j*y_width+y_width)    
        ''' Collect random biopsy samples in each slice for R times. If the distance
        to both directions exceeds the limits of a slice, then sample from the beginning. 
        If a slice is smaller than the jumbo size, get whole slice as sample.  
        '''
        for r in range(0,settings.n_reps):
            for i in range(0,slice_x):
                quad = slices_x[str(i)]
                if (len(quad) > 0):
                    select = random.choice(quad)
                    if (quad[-1]-select) > jumbo_x:
                        sampled_x[str(i)] = range(select,select+jumbo_x)
                    elif (select-quad[0]) > jumbo_x:
                        sampled_x[str(i)] = range(select-jumbo_x,select)
                    else:
                        if quad[-1]-quad[0] > jumbo_x:
                            sampled_x[str(i)] = range(quad[0],quad[0]+jumbo_x)
                        else:
                            sampled_x[str(i)] = range(quad[0],quad[-1]) 
            for j in range(0,len(slices_y)):
                quad = slices_y[str(j)]
                if (len(quad) > 0):
                    select = random.choice(quad)
                    if (quad[-1]-select) > jumbo_y:
                        sampled_y[str(j)] = range(select,select+jumbo_y)
                    elif (select-quad[0]) > jumbo_y:
                        sampled_y[str(j)] = range(select-jumbo_y,select) 
                    else:
                        if quad[-1]-quad[0] > jumbo_y:
                            sampled_y[str(j)] = range(quad[0],quad[0]+jumbo_x)
                        else:
                            sampled_y[str(j)] = range(quad[0],quad[-1])
            '''Check sampled points against sensitivity'''
            detected = list()
            for m in range(0,len(settings.sensitivity)):
                detected.append(0)
                sample = pd.DataFrame() 
                for i in range(0,len(sampled_x)):
                    for j in range(0,len(sampled_y)):
                        sample = df.loc[df['xcoord'].isin(sampled_x[str(i)]) & df['ycoord'].isin(sampled_y[str(j)])]
                        if (len(sample)!=0):
                            condition = float(len(sample[sample['type'].isin([2,3])]))/float(len(sample))
                            if (condition >= (1 - settings.sensitivity[m])):
                                detected[m] = 1
                                break
            detected.append(1) #There is at least one dysplasia or cancer cell
            if len(df.query("type == 3")) > 0: # check if there is any cancer cell
                detected.append(1)
            else:
                detected.append(0)
            # Find the number of samples collected
            detected.append(slice_x*slice_y)
            biopsy[str(r)] = detected
    return biopsy

''' Random Protocol with overlap - Determines HGD only when n_f fraction of cells are
detected with dysplasia or cancer. We arbitrarily sample n_biopsies at specified sizes.
Samples can overlap.  
'''
def random_overlap(n,df,jumbo_x,jumbo_y,n_biopsies):
    biopsy = {} # Keys are biopsy samplings
    sampled_x = {}
    sampled_y = {}
    np.random.seed(n)
    if len(df) > 0:       
        max_y = int(df['ycoord'].max())
    else:
        max_y = 0
    ''' Collect random biopsy samples in each slice for ~45 times randomly'''
    # Check if there is no dysplasia or cancer- do nothing
    if (len(df.query("type == 3 or type == 2")) == 0 or len(df) == 0):
        detected = list()
        for m in range(0,len(settings.sensitivity)+2):
            detected.append(0)
        detected.append(n_biopsies)
        for biopsy_start in range(0,settings.jumbo_x+settings.interval_x,1):
            biopsy[str(biopsy_start)] = detected
    # Otherwise, biopsy sampling
    else:
        for r in range(0,settings.n_reps):
            for i in range(0,n_biopsies):
                select = random.choice(range(0,settings.grid_width))
                end = select + jumbo_x
                if (end < settings.grid_width):
                    sampled_x[str(i)] = range(select,end,1)
                else:
                    sampled_x[str(i)] = [m for z in (range(select,settings.grid_width), range(0, end-settings.grid_width)) for m in z]
                '''Sample points on the length '''
                j = 0
                end = 0
                select = random.choice(range(0,max_y))
                end = select + jumbo_y
                if (end > max_y):
                    end = max_y
                sampled_y[str(i)] = range(select,end,1)
            '''Check sampled points against sensitivity'''
            detected = list()
            for m in range(0,len(settings.sensitivity)):
                detected.append(0)
                sample = pd.DataFrame() 
                for i in range(0,len(sampled_x)):
                    for j in range(0,len(sampled_y)):
                        sample = df.loc[df['xcoord'].isin(sampled_x[str(i)]) & df['ycoord'].isin(sampled_y[str(j)])]
                        if (len(sample)!=0):
                            condition = float(len(sample[sample['type'].isin([2,3])]))/float(len(sample))
                            if (condition >= (1 - settings.sensitivity[m])):
                                detected[m] = 1
                                break
            detected.append(1) #There is at least one dysplasia or cancer cell
            if len(df.query("type == 3")) > 0: # check if there is any cancer cell
                detected.append(1)
            else:
                detected.append(0)
            detected.append(n_biopsies)
            biopsy[str(r)] = detected
    return biopsy