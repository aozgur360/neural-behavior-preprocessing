import os
#os.chdir('C:\\Users\\LurLab\Desktop\\Ali_general_behav_code\\code\\Python3\\behavior')
os.chdir('z:\\Ali O\\code\\Python3')
" config "
stage = 3
#mouse = 'm15n_ignore_beforerulechange'
#mouse = 'm15n'
mouse = 'iL'

dataDir = 'z:/Ali O/yarm_rig/yarm/Mice Data/'

mouse2 = 'iN'
mouse3 = 'iR'
mouse4 = 'gL'
mouse5 = 'gR'
#%%
import os
import AO_yarm as behav

os.chdir('z:\\Ali O\\code\\Python3')
folder_path = r'Z:\Ali O\yarm_miniscope_recording' #if want data from only mice with miniscope recordings, default (except for when looking at the rulechange data)

#folder_path = 'z:/Ali O/yarm_rig/yarm/Mice Data/stage 333' #if want to look at the traditional rule change dataset (see guide txt file in mice data > stage 3)

# Get all folder names in the specified location, excluding "examples" and "ignore"
folder_names = [
    folder
    for folder in os.listdir(folder_path)
    #comment out the line of code below if looking at stage 333 for rule change
    #if os.path.isdir(os.path.join(folder_path, folder)) and "examples" not in folder.lower() and "ignore" not in folder.lower() and "rulechange" not in folder.lower() and "rule23change" not in folder.lower() and "ruledelaychange" not in folder.lower()
]


os.chdir('z:\\Ali O\\code\\Python3')
" config "
stage = 3
dataDir = 'z:/Ali O/yarm_rig/yarm/Mice Data/'

#mouse_count = 0
# Accessing individual mice
#mice_used = []
for mouse in folder_names:
    try:
        behav.stage_mix_yarm_graph_paper(dataDir, stage, mouse)
        #mice_used.append(mouse)
        #mouse_count +=1
        #behav.stage_all_yarm_graph_paper(dataDir, stage, mouse)
    except:
        pass

#print(mice_used)
#print(mouse_count)
#%%
###### TESTING ADDING AVERAGE TRACE

import os
import AO_yarm as behav
import numpy as np
import matplotlib.pyplot as plt

os.chdir('z:\\Ali O\\code\\Python3\\behavior')
folder_path = r'Z:\Ali O\yarm_miniscope_recording'

# Get all folder names in the specified location, excluding "examples" and "ignore"
folder_names = [
    folder
    for folder in os.listdir(folder_path)
    if os.path.isdir(os.path.join(folder_path, folder)) and "examples" not in folder.lower() and "ignore" not in folder.lower()
]

os.chdir('z:\\Ali O\\code\\Python3\\behavior')

# config
stage = 2
dataDir = 'z:/Ali O/yarm_rig/yarm/Mice Data/'

# Lists to store data for average calculation
all_x = []
all_y = []

# Accessing individual mice
for mouse in folder_names:
    try:
        x,y = behav.stage_all_yarm_graph_paper2(dataDir, stage, mouse)
        #x,y = behav.stage_mix_yarm_graph_paper(dataDir, stage, mouse)
        all_x.append(x)
        all_y.append(y)
    except Exception as e:
        print(f"Error processing {mouse}: {e}")
        

# Find the maximum length of arrays in the list
max_length = max(len(arr) for arr in all_y)

# Initialize arrays to store the sums and counts for each index
sums = np.zeros(max_length)
counts = np.zeros(max_length)

# Loop through each array and accumulate sums and counts for each index
for arr in all_y:
    for i in range(len(arr)):
        sums[i] += arr[i]
        counts[i] += 1

# Calculate the averages for each index
averages = np.divide(sums, counts, out=np.zeros_like(sums), where=counts != 0)

# Plot the average trace
#plt.plot(range(1, max_length + 1), averages, marker='o')
plt.plot(range(1, max_length + 1), averages, color='black')  # Set color to black
plt.xlabel('Index')
plt.ylabel('Average Value')
plt.title('Average Trace Across All Indices')
plt.grid(False)
plt.show()


# # Plot individual traces
for x, y in zip(all_x, all_y):
     #plt.plot(x, y, alpha=0.5)  # Alpha controls transparency
     plt.plot(x, y, color='lightgray', alpha=0.7)  # Set color to light gray and adjust transparency
#%%



    
#%%
#TEST

import os
import AO_yarm as behav

folder_path = r'Z:\Ali O\yarm_miniscope_recording'

# Get all folder names in the specified location, excluding "examples" and "ignore"
folder_names = [
    folder
    for folder in os.listdir(folder_path)
    if os.path.isdir(os.path.join(folder_path, folder)) and "examples" not in folder.lower() and "ignore" not in folder.lower()
]

os.chdir('z:\\Ali O\\code\\Python3\\behavior')
" config "
stage = 3
dataDir = 'z:/Ali O/yarm_rig/yarm/Mice Data/'

# Define variables to count points above and below 65
above_65_count = 0
below_65_count = 0

# Accessing individual mice
for mouse in folder_names:
    try:
        # Get the plot data
        x, y = behav.stage_mix_yarm_graph_paper(dataDir, stage, mouse)
        # Calculate the counts
        if y[0] > 65:
            above_65_count += 1
        else:
            below_65_count += 1
    except Exception as e:
        print(f"Error processing {mouse}: {e}")

# Output the counts
print(f"Number of first points above 65: {above_65_count}")
print(f"Number of first points 65 or below: {below_65_count}")

    
#%%
import os

folder_path = r'Z:\Ali O\yarm_miniscope_recording'

# Get all folder names in the specified location, excluding "examples" and "ignore"
folder_names = [
    folder
    for folder in os.listdir(folder_path)
    if os.path.isdir(os.path.join(folder_path, folder)) and "examples" not in folder.lower() and "ignore" not in folder.lower()
]

# Print the list of folder names
print(folder_names)



#%%
# only print percent correct. if stage < 3, FTP trials. if stage >=3, init trials
import AO_yarm as behav
behav.stage_print_behav(dataDir, stage, mouse)

#%%5
" for all stages " #ftp main
import AO_yarm as behav
behav.stage_all_yarm(dataDir, stage, mouse)

behav.stage_all_yarm(dataDir, stage, mouse2)
behav.stage_all_yarm(dataDir, stage, mouse3)
behav.stage_all_yarm(dataDir, stage, mouse4)
behav.stage_all_yarm(dataDir, stage, mouse5)

#%%
" for stage101 "
import AO_yarm as behav
behav.stage_101_yarm(dataDir, stage, mouse)
#%%
" for stage 3 mix " #init main
import AO_yarm as behav
behav.stage_mix_yarm(dataDir, stage, mouse)

#behav.stage_mix_yarm(dataDir, stage, mouse2)
#behav.stage_mix_yarm(dataDir, stage, mouse3)
#behav.stage_mix_yarm(dataDir, stage, mouse4)
#behav.stage_mix_yarm(dataDir, stage, mouse5)


#%%
" for stage 5 (rule change mixing) " 
import AO_yarm as behav
behav.stage_5_yarm(dataDir, stage, mouse)
#%%
" for stage 5TF (rule change mixing, true false trial) " 
import AO_yarm as behav
behav.stage_5TF_yarm(dataDir, stage, mouse)
#%%
" for troubleshooting "
import AO_yarm as behav
behav.stage_troubleshoot(dataDir, stage, mouse)
#%%
" for all stages "
import AO_yarm as behav
#behav.stage_all_yarm(dataDir, stage, mouse)
#behav.stage_all_yarm(dataDir, stage, mouse2)
#behav.stage_all_yarm(dataDir, stage, mouse3)
#behav.stage_all_yarm(dataDir, stage, mouse4)
#behav.stage_all_yarm(dataDir, stage, mouse5)

#behav.stage_all_yarm(dataDir, stage, mouse6)
#behav.stage_all_yarm(dataDir, stage, mouse7)
#behav.stage_all_yarm(dataDir, stage, mouse8)
#behav.stage_all_yarm(dataDir, stage, mouse9)
#behav.stage_all_yarm(dataDir, stage, mouse10)