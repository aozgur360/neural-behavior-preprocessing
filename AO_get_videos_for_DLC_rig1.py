#check entire directory for non dlc'd sessions

import os
def getsubfolders(folder):
    ''' returns list of subfolders '''
    return [os.path.join(folder,p) for p in os.listdir(folder) if os.path.isdir(os.path.join(folder,p))]
shuffle=1


temp = []
basepath='Z:\Ali O\yarm_miniscope_recording'
basefolders = []
subfolders=getsubfolders(basepath)
for subfolder in subfolders:
    subfolders=getsubfolders(subfolder)
    for subfolder in subfolders:
         subfolders=getsubfolders(subfolder)
         for subfolder in subfolders:
             if "dlc" not in subfolder:
                 if "hbug" not in subfolder:
                     if "ignore" not in subfolder:
                         if "checkerror" not in subfolder:
                             if "r1" in subfolder:
                                 basefolders.append(subfolder)
                                 subfolders = getsubfolders(subfolder)
                                 for subfolder in subfolders:
                                     subfolders = getsubfolders(subfolder)
                                     for subfolder in subfolders:
                                         if "My_WebCam" in subfolder:
                                             temp.append(subfolder)
             
mystring = '/0.avi' 
temp_orig = temp
temp = [s + mystring for s in temp]

videos = []
for i in temp:
    videos.append(i.replace(os.sep, '/'))
print(videos)

#change 'r1' for 'r2' and 'r3' for other rigs


# conda activate deeplabcut
# ipython
# import deeplabcut
# ...enter
# for rig1....deeplabcut.analyze_videos("Z:\Ali O\DLC_projects\Mix_rig1-Ali-2022-05-12\config.yaml",,save_as_csv=True)

# paste in list
# ; for multiple commands
#%%
# rename entire directory of finished dlc'd sessions

test_exist = []
true_index = []
webcam_folders = []
for i in temp_orig:
    webcam_folders.append(i.replace(os.sep, '/'))
    
for i in webcam_folders:
    file_exists = os.path.exists(i+'/0DLC_mobnet_100_Mix_rig1May12shuffle1_1030000.csv')
    #file_exists = os.path.exists(i+'/0DLC_mobnet_100_nose_trainNov5shuffle1_500000.csv')
    test_exist.append(file_exists)
    true_index= [i for i, x in enumerate(test_exist) if x]
    

for i in true_index:
    #print(basefolders[i]) 
    try:
        name = basefolders[i]
        os.rename(name,name+'_dlc')
    except:
        name = basefolders[i]
        print(name)
        continue






#%%






























#%%
# for only specific sections
import os
def getsubfolders(folder):
    ''' returns list of subfolders '''
    return [os.path.join(folder,p) for p in os.listdir(folder) if os.path.isdir(os.path.join(folder,p))]
shuffle=1
#config='D:/DLC_projects/nose_followpattern_211213-Ali-2021-12-13/config.yaml'

temp = []
basepath='Z:\Ali O\yarm_miniscope_recording\snr\snr_3'
basefolders = []
subfolders=getsubfolders(basepath)
for subfolder in subfolders:
    if "dlc" not in subfolder: 
        basefolders.append(subfolder)
        subfolders=getsubfolders(subfolder)
        for subfolder in subfolders:
            subfolders=getsubfolders(subfolder)
            for subfolder in subfolders:
                if "My_WebCam" in subfolder:
                    temp.append(subfolder)
                 
mystring = '/0.avi' 
temp_orig = temp
temp = [s + mystring for s in temp]

videos = []
for i in temp:
    videos.append(i.replace(os.sep, '/'))
print(videos)

# deeplabcut.analyze_videos('D:/DLC_projects/nose_followpattern_211213-Ali-2021-12-13/config.yaml',,save_as_csv=True)

#%%
test_exist = []
true_index = []
webcam_folders = []
for i in temp_orig:
    webcam_folders.append(i.replace(os.sep, '/'))
    
for i in webcam_folders:
    file_exists = os.path.exists(i+'/0DLC_mobnet_100_nose_followpattern_211213Dec13shuffle1_100000.csv')
    #file_exists = os.path.exists(i+'/0DLC_mobnet_100_nose_trainNov5shuffle1_500000.csv')
    test_exist.append(file_exists)
    true_index= [i for i, x in enumerate(test_exist) if x]

for i in true_index:
    #print(basefolders[i]) 
    name = basefolders[i]
    os.rename(name,name+'_dlc')
    
       
        #for x in basefolders:
                #print(file_exists)
            #os.rename(x,x+'_dlc')
        #print(i+'/0DLC_mobnet_100_nose_followpattern_211213Dec13shuffle1_100000.csv')