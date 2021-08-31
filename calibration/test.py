import settings
import biopsies
import subprocess
import os,time
import pandas as pd
import fnmatch
from scoop import futures

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

def main():
    #df = read('tumor.csv.0.11')
    #detection = pathology(1,df)
    #print(detection)
    # Run simulations ## Parallelization
    #list(futures.map(runSim, range(1,n+1)))
    # Read outputs/csvs ## Parallelization
    file_names = ['tumor.csv.0.55','tumor.csv.0.44','tumor.csv.0.33','tumor.csv.0.26','tumor.csv.0.122']#list(get_list())
    reads = list(futures.map(read,file_names))
    # Run biopsy and pathology ## Parallelization
    #reads = []
    #reads.append(df)
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
        if all[i][12] == 1:
            a = a+1
        for j in range(0,11):
            cancer.append(all[i][12]*all[i][j])
        missedc.append(cancer)
        print(missedc)
    sums = [sum(i) for i in zip(*missedc)]
    if  a > 0:
        avg = [d / a for d in sums]
    else:
        avg = [0 for d in sums]
    averages.append(avg)
    print(averages)


if __name__ == "__main__":
    main()
