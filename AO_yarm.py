def stage_1_easymode(dataDir, stage, mouse):  
    import os
    import glob
    import re

#    import matplotlib.pyplot as plt
#    import numpy as np 
    
    timestamps = []
    trials_sep = []
    
    filepath = dataDir + 'stage ' + str(stage) + '/' + mouse
    
    for filename in glob.glob(os.path.join(filepath, '*.txt')):
        with open(filename, 'r') as f:
            txt = f.read()
                
        count_trials = (sum(1 for match in re.finditer("stim", txt)))
        count_rewards = sum(1 for match in re.finditer("reward", txt))
        more_accurate_trials_count = count_trials - 1
        
        # get largest number in text file aka last timestamp
        trials_sep = (re.split(r'stim', txt, flags=re.MULTILINE))
        for i in trials_sep:
            for line in (i.split('\n')):  
                if "lck" in line:
                    timestamps.append(float(line[0:6]))
        
        
        rpm = (count_rewards / (max(timestamps))) * 60

        print("number of trials:", more_accurate_trials_count)
        print("total rewards:", count_rewards)
        print("rewards per min:", rpm)
        print(" ")
#    plt.plot(x,y, "-o")
#%% 
def stage_allold_yarm(dataDir, stage, mouse):  
    import os
    import glob
    import re  
    
    import matplotlib.pyplot as plt
    import numpy as np 
    import statistics 
    
    from pathlib import Path
    
    timestamps = []
    trials_sep = []
    
    x_count = 0
    x_results = []
    y_results = []
    
    filepath = dataDir + 'stage ' + str(stage) + '/' + mouse
    paths = sorted(Path(filepath).iterdir(), key=os.path.getmtime)
    for filename in paths:
        with open(filename, 'r') as f:
            txt = f.read()

                
        count_trials = (sum(1 for match in re.finditer("begin_trial", txt)))
        count_rewards = sum(1 for match in re.finditer("reward", txt))
        
        more_accurate_trials_count = count_trials - 1
        
        count_spout1 = (sum(1 for match in re.finditer("lck_spout1", txt)))
        count_spout2 = (sum(1 for match in re.finditer("lck_spout2", txt)))
        count_spout3 = (sum(1 for match in re.finditer("lck_spout3", txt)))
        
        
#        count_punishments = sum(1 for match in re.finditer("punishment", txt))
        
        # get largest number in text file aka last timestamp
        trials_sep = (re.split(r'begin_trial', txt, flags=re.MULTILINE))
        for i in trials_sep:
            for line in (i.split('\n')):  
                if "lck" in line:
                    timestamps.append(float(line[0:6]))
#        
#        
        if count_rewards > 8:            
            rpm = (count_rewards / (max(timestamps))) * 60
            pcorrect = ((count_rewards)/(count_trials-1)) * 100
            
            
            x_count = x_count + 1               
            x_results.append(x_count)
            y_results.append(pcorrect)
            

            
            
            print(os.path.basename(filename))
            
            if "Mixstage     1" in txt:
                for line in txt.split('\n'):    
                    if "percent_stage2" in line:
                        print(line)
            
            print("number of trials:", more_accurate_trials_count)
            print("total rewards:", count_rewards)
            print("count_spout1", count_spout1)
            print("count_spout2", count_spout2)
            print("count_spout3", count_spout3)
            print("rewards per min:", rpm)
            print("percent correct:", pcorrect)
            
            
            for line in txt.splitlines():
                if "timeout_punishment" in line:
                    print(line)
            
#            print("rewardcount:", count_rewards)
#            print("punishmentcount:", count_punishments)
            print(" ")
            
    x = (np.hstack(x_results))
    y = (np.hstack(y_results))
    plt.xlabel('Session Number')
    plt.ylabel('Percent Correct')
 #   plt.axhline(50, color="gray")
#    plt.figure(0)
    plt.title('Learning')
    plt.plot(x,y, "-o")
    
#%%#%% 
def stage_all_yarm(dataDir, stage, mouse):  
    import os
    import glob
    import re  
    
    import matplotlib.pyplot as plt
    import numpy as np 
    import statistics 
    
    
    from pathlib import Path
    
    
    
    timestamps = []
    trials_sep = []
    
    x_count = 0
    x_results = []
    y_results = []
    
    water = []
#    stimr_count = []
#    stiml_count = []
    
    stimr_reward = []
    stimr_punishment = []
    stiml_reward = []
    stiml_punishment = []
    
    
    filepath = dataDir + 'stage ' + str(stage) + '/' + mouse
    paths = sorted(Path(filepath).iterdir(), key=os.path.getmtime)
    for filename in paths:
        with open(filename, 'r') as f:
            txt = f.read()

        count_rewards = sum(1 for match in re.finditer("reward", txt))
        count_punishments = sum(1 for match in re.finditer("timeout punishment", txt))
        count_trials = count_rewards + count_punishments
        

 #       count_trials = sum(1 for match in re.finditer("begin_trial", txt))
        
        count_spout1 = (sum(1 for match in re.finditer("lck_spout1", txt)))
        count_spout2 = (sum(1 for match in re.finditer("lck_spout2", txt)))
        count_spout3 = (sum(1 for match in re.finditer("lck_spout3", txt)))
        
        
        # get largest number in text file aka last timestamp
        trials_sep = (re.split(r'begin_trial', txt, flags=re.MULTILINE))
        

        for i in trials_sep:
            if "stimR" in i:
                if "reward" in i:
                    stimr_reward.append(1)
                if "punishment" in i:
                    stimr_punishment.append(1)
            if "stimL" in i:
                if "reward" in i:
                    stiml_reward.append(1)
                if "punishment" in i:
                    stiml_punishment.append(1)
#        
#        
        if count_rewards > 8:            
#            rpm = (count_rewards / (max(timestamps))) * 60
            pcorrect = ((count_rewards)/(count_trials)) * 100
            
            
            x_count = x_count + 1               
            x_results.append(x_count)
            y_results.append(pcorrect)
            water.append(count_rewards *4)
            
            ####
            
            stimr_reward_count = len(stimr_reward)
            stiml_reward_count = len(stiml_reward)
            stimr_punishment_count = len(stimr_punishment)
            stiml_punishment_count = len(stiml_punishment)
            
            stimr_count = stimr_reward_count + stimr_punishment_count
            stiml_count = stiml_reward_count + stiml_punishment_count
            
            pcor_r = (stimr_reward_count/stimr_count)*100
            pcor_l = (stiml_reward_count/stiml_count)*100
            
  #############          
#             print(os.path.basename(filename))
            
#             if "Mixstage     1" in txt:
#                 for line in txt.split('\n'):    
#                     if "percent_stage2" in line:
#                         print(line)
            
#             print("number of trials:", count_trials)
#             print("total rewards:", count_rewards)
#             print("water collected:", count_rewards *4)
#             print("count_spout1", count_spout1)
#             print("count_spout2", count_spout2)
#             print("count_spout3", count_spout3)
#             print("percent correct:", pcorrect)
#             print("number of right trials:", stimr_count)
#             print("numbmer of left trials:", stiml_count)
#             print("percent correct right trials:", pcor_r)
#             print("percent correct left trials:", pcor_l)
            
            
            
#             for line in txt.splitlines():
#                 if "timeout_punishment" in line:
#                     print(line)
            
# #            print("rewardcount:", count_rewards)
# #            print("punishmentcount:", count_punishments)
#             print(" ")
#############
            stimr_reward.clear()
            stimr_punishment.clear()
            stiml_reward.clear()
            stiml_punishment.clear()
            
    x = (np.hstack(x_results))
    y2 = (np.hstack(water))
    y = (np.hstack(y_results))
    #plt.xlabel('Session Number')
    #plt.ylabel('Percent Correct')
 #   plt.axhline(50, color="gray")
#    plt.figure(0)
    #plt.title('FTP sham')
    
    #x = np.array(x_results)
    #y = np.array(y_results)
    
    #print(f"x values for mouse {mouse}: {x.tolist()}")
    y_values_str = ' '.join(map(str, y))
    print(f"y values for mouse {mouse}: {y_values_str}")
    print("")
    
    
    plt.plot(x,y)
    #plt.figure()
    
    #### water graphs
    #plt.plot(x,y2,"-o")
    #plt.figure()
    #m, b = np.polyfit(y2, y, 1)
    #plt.scatter(y,y2)
    #correlation_matrix = np.corrcoef(y, y2)
    #correlation_xy = correlation_matrix[0,1]
    #r_squared = correlation_xy**2
    #print(r_squared)
   # plt.plot(y2,m*y2+b)
#%%
def stage_all_yarm_graph_paper(dataDir, stage, mouse):  
    import os
    import glob
    import re  
    
    import matplotlib.pyplot as plt
    import numpy as np 
    import statistics 

    from scipy.interpolate import interp1d
    
    
    from pathlib import Path
    
    
    
    timestamps = []
    trials_sep = []
    
    x_count = 0
    x_results = []
    y_results = []
    
    water = []
#    stimr_count = []
#    stiml_count = []
    
    stimr_reward = []
    stimr_punishment = []
    stiml_reward = []
    stiml_punishment = []
    
    
    filepath = dataDir + 'stage ' + str(stage) + '/' + mouse
    paths = sorted(Path(filepath).iterdir(), key=os.path.getmtime)
    for filename in paths:
        with open(filename, 'r') as f:
            txt = f.read()

        count_rewards = sum(1 for match in re.finditer("reward", txt))
        count_punishments = sum(1 for match in re.finditer("timeout punishment", txt))
        count_trials = count_rewards + count_punishments
        

 #       count_trials = sum(1 for match in re.finditer("begin_trial", txt))
        
        count_spout1 = (sum(1 for match in re.finditer("lck_spout1", txt)))
        count_spout2 = (sum(1 for match in re.finditer("lck_spout2", txt)))
        count_spout3 = (sum(1 for match in re.finditer("lck_spout3", txt)))
        
        
        # get largest number in text file aka last timestamp
        trials_sep = (re.split(r'begin_trial', txt, flags=re.MULTILINE))
        

        for i in trials_sep:
            if "stimR" in i:
                if "reward" in i:
                    stimr_reward.append(1)
                if "punishment" in i:
                    stimr_punishment.append(1)
            if "stimL" in i:
                if "reward" in i:
                    stiml_reward.append(1)
                if "punishment" in i:
                    stiml_punishment.append(1)
#        
#        
        if count_rewards > 8:            
#            rpm = (count_rewards / (max(timestamps))) * 60
            pcorrect = ((count_rewards)/(count_trials)) * 100
            
            
            x_count = x_count + 1               
            x_results.append(x_count)
            y_results.append(pcorrect)
            water.append(count_rewards *4)
            
            ####
            
            stimr_reward_count = len(stimr_reward)
            stiml_reward_count = len(stiml_reward)
            stimr_punishment_count = len(stimr_punishment)
            stiml_punishment_count = len(stiml_punishment)
            
            stimr_count = stimr_reward_count + stimr_punishment_count
            stiml_count = stiml_reward_count + stiml_punishment_count
            
            pcor_r = (stimr_reward_count/stimr_count)*100
            pcor_l = (stiml_reward_count/stiml_count)*100
            
            
#             print(os.path.basename(filename))
            
#             if "Mixstage     1" in txt:
#                 for line in txt.split('\n'):    
#                     if "percent_stage2" in line:
#                         print(line)
            
#             print("number of trials:", count_trials)
#             print("total rewards:", count_rewards)
#             print("water collected:", count_rewards *4)
#             print("count_spout1", count_spout1)
#             print("count_spout2", count_spout2)
#             print("count_spout3", count_spout3)
#             print("percent correct:", pcorrect)
#             print("number of right trials:", stimr_count)
#             print("numbmer of left trials:", stiml_count)
#             print("percent correct right trials:", pcor_r)
#             print("percent correct left trials:", pcor_l)
            
            
            
#             for line in txt.splitlines():
#                 if "timeout_punishment" in line:
#                     print(line)
            
# #            print("rewardcount:", count_rewards)
# #            print("punishmentcount:", count_punishments)
#             print(" ")

            stimr_reward.clear()
            stimr_punishment.clear()
            stiml_reward.clear()
            stiml_punishment.clear()
            
    x = (np.hstack(x_results))
    y = (np.hstack(y_results))
    #print(x)
    #print(y)
    
    y_values_str = ' '.join(map(str, y))
    print(f"y values for mouse {mouse}: {y_values_str}")
    print("")
    
    #plt.xlabel('Session Number')
    #plt.ylabel('Percent Correct')
 #   plt.axhline(50, color="gray")
#    plt.figure(0)
  #  plt.title('Learning')
  # Set the limits of the x-axis
    plt.xlim(1, 24)
    plt.ylim(30,100)
    
    figure_path = r"C:\Users\LurLab\Downloads\ftp_learning_rates" + ".eps"
    plt.savefig(figure_path, format='eps', bbox_inches='tight')
    
    plt.plot(x,y)
    #%%
def stage_mix_yarm_graph_paper(dataDir, stage, mouse):  
    import os
    import glob
    import re  
    import matplotlib.pyplot as plt
    import numpy as np 
    import statistics 
    
    from pathlib import Path
    
    timestamps = []
    trials_sep = []
    
    x_count = 0
    x_results = []
    y_results = []
    y_results2 = []
    
    trial100_count = []
    r100_count = []
    p100_count = []
    trial2_count = []
    r2_count = []
    p2_count = []
    
    filepath = dataDir + 'stage ' + str(stage) + '/' + mouse
    paths = sorted(Path(filepath).iterdir(), key=os.path.getmtime)

    for filename in paths:
        with open(filename, 'r') as f:
            txt = f.read()

        count_rewards = sum(1 for match in re.finditer("reward", txt))
        count_punishments = sum(1 for match in re.finditer("timeout punishment", txt))
        count_trials = count_rewards + count_punishments
        
        count_spout1 = (sum(1 for match in re.finditer("lck_spout1", txt)))
        count_spout2 = (sum(1 for match in re.finditer("lck_spout2", txt)))
        count_spout3 = (sum(1 for match in re.finditer("lck_spout3", txt)))

        trials_sep = (re.split(r'begin_trial', txt, flags=re.MULTILINE))

        for i in trials_sep:
            if "start_stage100" in i:
                trial100_count.append(1)
                if "reward" in i:
                    r100_count.append(1)
                if "punishment" in i:
                    p100_count.append(1)
            if "start_stage2" in i:
                trial2_count.append(1)
                if "reward" in i:
                    r2_count.append(1)
                if "punishment" in i:
                    p2_count.append(1)
        
        if count_rewards > 8:
            pcorrect = ((count_rewards) / (count_trials - 1)) * 100
            
            if len(trial2_count) > 0:
                x_count = x_count + 1
                x_results.append(x_count)
                y_results.append((len(r100_count) / len(trial100_count)) * 100)
                y_results2.append((len(r2_count) / len(trial2_count)) * 100)
 ##############               
            # print(os.path.basename(filename))
            # print("number of trials:", count_trials)
            # print("water collected:", count_rewards * 4)
            # print("total rewards:", count_rewards)
            # print("count_spout1", count_spout1)
            # print("count_spout2", count_spout2)
            # print("count_spout3", count_spout3)
            # print("percent correct:", pcorrect)

            # if len(trial100_count) and len(trial2_count) > 0:
            #     print("number of INIT ONLY trials:", len(trial100_count))
            #     print("number of FTP trials:", len(trial2_count))
                
            # if len(trial100_count) > 0 and len(r100_count) > 0:
            #     print("percent correct INIT ONLY trials:", len(r100_count) / len(trial100_count) * 100)
            
            # if len(trial2_count) > 0 and len(r2_count) > 0:
            #     print("percent correct FTP trials:", len(r2_count) / len(trial2_count) * 100)
                
            # for line in txt.splitlines():
            #     if "timeout_punishment" in line:
            #         print(line)
                    
            # print(" ")
            
 ############           
            trial100_count.clear()
            r100_count.clear()
            p100_count.clear()
            trial2_count.clear()
            r2_count.clear()
            p2_count.clear()
            
########### old    
    # # Plotting and saving graphs
    # x = np.hstack(x_results)
    # y = np.hstack(y_results)
    # print(x)
    # print(y)
    # plt.xlabel('Session Number')
    # plt.ylabel('Percent Correct')
    # #plt.xlim(1, 24)
    # plt.xlim(1,6)
    # #plt.ylim(30, 100)
    # plt.ylim(50, 90)
    # figure_path = r"C:\Users\LurLab\Downloads\init_learning_rates" + ".eps"
    # plt.savefig(figure_path, format='eps', bbox_inches='tight')
    # plt.plot(x, y)
###################

    x = (np.hstack(x_results))
    y = (np.hstack(y_results))
    
    y_values_str = ' '.join(map(str, y))
    print(f"y values for mouse {mouse}: {y_values_str}")
    print("")
    
    return x, y  # Return x and y values
#%%
def stage_all_yarm_graph_paper2(dataDir, stage, mouse):  
    import os
    import glob
    import re  
    
    import matplotlib.pyplot as plt
    import numpy as np 
    import statistics 

    from scipy.interpolate import interp1d
    
    
    from pathlib import Path
    
    
    
    timestamps = []
    trials_sep = []
    
    x_count = 0
    x_results = []
    y_results = []
    
    water = []
    
    stimr_reward = []
    stimr_punishment = []
    stiml_reward = []
    stiml_punishment = []
    
    
    filepath = dataDir + 'stage ' + str(stage) + '/' + mouse
    paths = sorted(Path(filepath).iterdir(), key=os.path.getmtime)
    for filename in paths:
        with open(filename, 'r') as f:
            txt = f.read()

        count_rewards = sum(1 for match in re.finditer("reward", txt))
        count_punishments = sum(1 for match in re.finditer("timeout punishment", txt))
        count_trials = count_rewards + count_punishments
        
        count_spout1 = (sum(1 for match in re.finditer("lck_spout1", txt)))
        count_spout2 = (sum(1 for match in re.finditer("lck_spout2", txt)))
        count_spout3 = (sum(1 for match in re.finditer("lck_spout3", txt)))
        
        trials_sep = (re.split(r'begin_trial', txt, flags=re.MULTILINE))
        
        for i in trials_sep:
            if "stimR" in i:
                if "reward" in i:
                    stimr_reward.append(1)
                if "punishment" in i:
                    stimr_punishment.append(1)
            if "stimL" in i:
                if "reward" in i:
                    stiml_reward.append(1)
                if "punishment" in i:
                    stiml_punishment.append(1)
            
        if count_rewards > 8:            
            pcorrect = ((count_rewards)/(count_trials)) * 100
            
            x_count = x_count + 1               
            x_results.append(x_count)
            y_results.append(pcorrect)
            water.append(count_rewards *4)
            
            stimr_reward_count = len(stimr_reward)
            stiml_reward_count = len(stiml_reward)
            stimr_punishment_count = len(stimr_punishment)
            stiml_punishment_count = len(stiml_punishment)
            
            stimr_count = stimr_reward_count + stimr_punishment_count
            stiml_count = stiml_reward_count + stiml_punishment_count
            
            pcor_r = (stimr_reward_count/stimr_count)*100
            pcor_l = (stiml_reward_count/stiml_count)*100

            stimr_reward.clear()
            stimr_punishment.clear()
            stiml_reward.clear()
            stiml_punishment.clear()
            
    x = (np.hstack(x_results))
    y = (np.hstack(y_results))
    return x, y  # Return x and y values
    #return y

# Rest of your code remains unchanged



#%%    
def stage_mix_yarm(dataDir, stage, mouse):  
    import os
    import glob
    import re  
    import matplotlib.pyplot as plt
    import numpy as np 
    import statistics 
    
    from pathlib import Path
    
    timestamps = []
    trials_sep = []
    
    x_count = 0
    x_results = []
    y_results = []
    y_results2 = []
    
    trial100_count = []
    r100_count = []
    p100_count = []
    trial2_count = []
    r2_count = []
    p2_count = []
    
    filepath = dataDir + 'stage ' + str(stage) + '/' + mouse
    paths = sorted(Path(filepath).iterdir(), key=os.path.getmtime)
    for filename in paths:
        with open(filename, 'r') as f:
            txt = f.read()

                
        count_rewards = sum(1 for match in re.finditer("reward", txt))
        count_punishments = sum(1 for match in re.finditer("timeout punishment", txt))
        count_trials = count_rewards + count_punishments
        
        
        count_spout1 = (sum(1 for match in re.finditer("lck_spout1", txt)))
        count_spout2 = (sum(1 for match in re.finditer("lck_spout2", txt)))
        count_spout3 = (sum(1 for match in re.finditer("lck_spout3", txt)))
        
#        count_punishments = sum(1 for match in re.finditer("punishment", txt))
        
        # get largest number in text file aka last timestamp
        trials_sep = (re.split(r'begin_trial', txt, flags=re.MULTILINE))
        

        for i in trials_sep:
            if "start_stage100" in i:
                trial100_count.append(1)
                if "reward" in i:
                    r100_count.append(1)
                if "punishment" in i:
                    p100_count.append(1)
            if "start_stage2" in i:
                trial2_count.append(1)
                if "reward" in i:
                    r2_count.append(1)
                if "punishment" in i:
                    p2_count.append(1)
        
        
#        for i in trials_sep:
#            for line in (i.split('\n')):  
#                if "lck" in line:
#                    timestamps.append(float(line[0:6]))
                    

#        
#        
        if count_rewards > 8:            
#            rpm = (count_rewards / (max(timestamps))) * 60
            pcorrect = ((count_rewards)/(count_trials-1)) * 100
            
            if len(trial2_count) > 0:
                x_count = x_count + 1               
                x_results.append(x_count)
                #y_results.append(pcorrect)
                y_results.append((len(r100_count)/len(trial100_count))*100)
                y_results2.append((len(r2_count)/len(trial2_count))*100)
                
  ######################
            
#             print(os.path.basename(filename))
            
#             if "Mixstage     1" in txt:
#                 for line in txt.split('\n'):    
#                     if "percent_stage2" in line:
#                         print(line)
#    #         print(trials_sep)
#             print("number of trials:", count_trials)
#             print("water collected:", count_rewards *4)
#             print("total rewards:", count_rewards)
#             print("count_spout1", count_spout1)
#             print("count_spout2", count_spout2)
#             print("count_spout3", count_spout3)
# #            print("rewards per min:", rpm)
#             print ("percent correct:", pcorrect)
            
            
#             if len(trial100_count) and len(trial2_count) > 0:
    
#                 # print("number of stage100 trials:", len(trial100_count))
#                 # print("number of stage2 trials:", len(trial2_count))
                
#                 print("number of INIT ONLY trials:", len(trial100_count))
#                 print("number of FTP trials:", len(trial2_count))
                
#  #           print("number of correct stage100 trials:", len(r100_count))
#  #           print("number of incorrect stage100 trials:", len(p100_count))
            
#             if len(trial100_count) > 0 and len(r100_count) > 0:
#                 print("percent correct INIT ONLY trials:", len(r100_count)/len(trial100_count)*100)
            
#             if len(trial2_count) > 0 and len(r2_count) > 0:
#                 print("percent correct FTP trials:", len(r2_count)/len(trial2_count)*100)
                
                
#             for line in txt.splitlines():
#                 if "timeout_punishment" in line:
#                     print(line)
      
 #           print("percent correct stage100 trials:", num_r100_count/num_trial100_count)
            
            
#            print("rewardcount:", count_rewards)
#            print("punishmentcount:", count_punishments)
#            print(" ")
########################      
            trial100_count.clear()
            r100_count.clear()
            p100_count.clear()
            trial2_count.clear()
            r2_count.clear()
            p2_count.clear()
            
       #default graphs     
    x = (np.hstack(x_results))
    y = (np.hstack(y_results))
    #y2 = (np.hstack(y_results2))
    #plt.xlabel('Session Number')
    #plt.ylabel('Percent Correct')
    #plt.title('INIT lesion')
    
    #plt.xlim(1, 24)
    #plt.ylim(30, 100)
    
    #figure_path = r"C:\Users\LurLab\Downloads\init_learning_rates" + ".eps"
    #plt.savefig(figure_path, format='eps', bbox_inches='tight')
    
        #print(f"x values for mouse {mouse}: {x.tolist()}")
    y_values_str = ' '.join(map(str, y))
    print(f"y values for mouse {mouse}: {y_values_str}")
    print("")
    
    plt.plot(x,y) #init
    #plt.plot(x,y2,"-o") #ftp
    
    
    #for checking the 15 custom
    # x = (np.hstack(x_results))
    # y = (np.hstack(y_results))

    # plt.plot(x,y, "k")
#%%    
def stage_print_behav(dataDir, stage, mouse):  
    import os
    import glob
    import re  
    import matplotlib.pyplot as plt
    import numpy as np 
    import statistics 
    
    from pathlib import Path
    
    timestamps = []
    trials_sep = []
    
    x_count = 0
    x_results = []
    y_results = []
    y_results2 = []
    
    trial100_count = []
    r100_count = []
    p100_count = []
    trial2_count = []
    r2_count = []
    p2_count = []
    
    filepath = dataDir + 'stage ' + str(stage) + '/' + mouse
    paths = sorted(Path(filepath).iterdir(), key=os.path.getmtime)
    for filename in paths:
        with open(filename, 'r') as f:
            txt = f.read()

                
        count_rewards = sum(1 for match in re.finditer("reward", txt))
        count_punishments = sum(1 for match in re.finditer("timeout punishment", txt))
        count_trials = count_rewards + count_punishments
        
        
        count_spout1 = (sum(1 for match in re.finditer("lck_spout1", txt)))
        count_spout2 = (sum(1 for match in re.finditer("lck_spout2", txt)))
        count_spout3 = (sum(1 for match in re.finditer("lck_spout3", txt)))
        
#        count_punishments = sum(1 for match in re.finditer("punishment", txt))
        
        # get largest number in text file aka last timestamp
        trials_sep = (re.split(r'begin_trial', txt, flags=re.MULTILINE))
        

        for i in trials_sep:
            if "start_stage100" in i:
                trial100_count.append(1)
                if "reward" in i:
                    r100_count.append(1)
                if "punishment" in i:
                    p100_count.append(1)
            if "start_stage2" in i:
                trial2_count.append(1)
                if "reward" in i:
                    r2_count.append(1)
                if "punishment" in i:
                    p2_count.append(1)
        

        ####################            ######
        if count_rewards > 8:            

            print(os.path.basename(filename))
            
            if stage < 3:
                ftp_behav_perc = ((len(r2_count))/(len(trial2_count))) * 100
                print(ftp_behav_perc)
            else:
                init_behav_perc = ((len(r100_count))/(len(trial100_count))) * 100
                print(init_behav_perc)
            
            print(" ")
            trial100_count.clear()
            r100_count.clear()
            p100_count.clear()
            trial2_count.clear()
            r2_count.clear()
            p2_count.clear()
            
    
    #%%    
def stage_5_yarm(dataDir, stage, mouse):  
    import os
    import glob
    import re  
    import matplotlib.pyplot as plt
    import numpy as np 
    import statistics 
    
    from pathlib import Path
    
    timestamps = []
    trials_sep = []
    
    x_count = 0
    x_results = []
    y_fm_results = []
    y_vh_results = []
    
    fm_count = []
    fmr_count = []
    fmp_count = []
    vh_count = []
    vhr_count = []
    vhp_count = []
    
    filepath = dataDir + 'stage ' + str(stage) + '/' + mouse
    paths = sorted(Path(filepath).iterdir(), key=os.path.getmtime)
    for filename in paths:
        with open(filename, 'r') as f:
            txt = f.read()

                
        count_rewards = sum(1 for match in re.finditer("reward", txt))
        count_punishments = sum(1 for match in re.finditer("timeout punishment", txt))
        count_trials = count_rewards + count_punishments
        
        
        count_spout1 = (sum(1 for match in re.finditer("lck_spout1", txt)))
        count_spout2 = (sum(1 for match in re.finditer("lck_spout2", txt)))
        count_spout3 = (sum(1 for match in re.finditer("lck_spout3", txt)))
        
#        count_punishments = sum(1 for match in re.finditer("punishment", txt))
        
        # get largest number in text file aka last timestamp
        trials_sep = (re.split(r'begin_trial', txt, flags=re.MULTILINE))
        
        del trials_sep[0]
        for i in trials_sep:
            if "fanmarbles_trial" in i:
                fm_count.append(1)
                if "reward" in i:
                    fmr_count.append(1)
                if "punishment" in i:
                    fmp_count.append(1)
            if not "fanmarbles_trial" in i:
                vh_count.append(1)
                if "reward" in i:
                    vhr_count.append(1)
                if "punishment" in i:
                    vhp_count.append(1)
                
            
        
        
#        for i in trials_sep:
#            for line in (i.split('\n')):  
#                if "lck" in line:
#                    timestamps.append(float(line[0:6]))
                    

#        
#        
        if count_rewards > 8:            
#            rpm = (count_rewards / (max(timestamps))) * 60
            pcorrect = ((count_rewards)/(count_trials-1)) * 100
            
            
            x_count = x_count + 1               
            x_results.append(x_count)
            #y_results.append(pcorrect)
            y_fm_results.append(len(fmr_count)/len(fm_count)*100)
            y_vh_results.append(len(vhr_count)/len(vh_count)*100)
            
  
            
            print(os.path.basename(filename))
            
            if "Mixstage     1" in txt:
                for line in txt.split('\n'):    
                    if "percent_stage2" in line:
                        print(line)
   #         print(trials_sep)
            print("number of trials:", count_trials)
            print("water collected:", count_rewards *4)
            print("total rewards:", count_rewards)
            print("count_spout1", count_spout1)
            print("count_spout2", count_spout2)
            print("count_spout3", count_spout3)
#            print("rewards per min:", rpm)
            print ("percent correct:", pcorrect)
            
            
            if len(fm_count) and len(vh_count) > 0:
    
                print("number of fanmarble trials:", len(fm_count))
                print("number of vertical/horizontal trials:", len(vh_count))
 #           print("number of correct stage100 trials:", len(r100_count))
 #           print("number of incorrect stage100 trials:", len(p100_count))
            
            if len(fm_count) > 0 and len(fmr_count) > 0:
                print("percent correct fanmarble trials:", len(fmr_count)/len(fm_count)*100)
            
            if len(vh_count) > 0 and len(vhr_count) > 0:
                print("percent correct vertical/horizontal trials:", len(vhr_count)/len(vh_count)*100)
                
                
            for line in txt.splitlines():
                if "timeout_punishment" in line:
                    print(line)
            
 #           print("percent correct stage100 trials:", num_r100_count/num_trial100_count)
            
            
#            print("rewardcount:", count_rewards)
#            print("punishmentcount:", count_punishments)
            print(" ")
            fm_count.clear()
            fmr_count.clear()
            fmp_count.clear()
            vh_count.clear()
            vhr_count.clear()
            vhp_count.clear()
            
    x = (np.hstack(x_results))
    y = (np.hstack(y_fm_results))
    y2 = (np.hstack(y_vh_results))
    plt.xlabel('Session Number')
    plt.ylabel('Percent Correct')
   # plt.title('Learning')
    plt.plot(x,y, "-o")
    plt.plot(x,y2, "-o")
    #%%    
def stage_5TF_yarm(dataDir, stage, mouse):  
    import os
    import glob
    import re  
    import matplotlib.pyplot as plt
    import numpy as np 
    import statistics 
    
    from pathlib import Path
    
    
    timestamps = []
    trials_sep = []
    
    x_count = 0
    x_results = []
    y_fm_results = []
    y_vh_results = []
    
    fm_count = []
    fmr_count = []
    fmp_count = []
    vh_count = []
    vhr_count = []
    vhp_count = []
    
    tf_list = []
    switch_reward = []
    switch_punishment = []
    other_reward = []
    other_punishment = []
    
    filepath = dataDir + 'stage ' + str(stage) + '/' + mouse
    paths = sorted(Path(filepath).iterdir(), key=os.path.getmtime)
    for filename in paths:
        with open(filename, 'r') as f:
            txt = f.read()

                
        count_rewards = sum(1 for match in re.finditer("reward", txt))
        count_punishments = sum(1 for match in re.finditer("timeout punishment", txt))
        count_trials = count_rewards + count_punishments
        
        
        count_spout1 = (sum(1 for match in re.finditer("lck_spout1", txt)))
        count_spout2 = (sum(1 for match in re.finditer("lck_spout2", txt)))
        count_spout3 = (sum(1 for match in re.finditer("lck_spout3", txt)))
        
#        count_punishments = sum(1 for match in re.finditer("punishment", txt))
        
        # get largest number in text file aka last timestamp
        trials_sep = (re.split(r'begin_trial', txt, flags=re.MULTILINE))
        
        del trials_sep[0]
        
        for i in range(len(trials_sep)):
            if "switch" in trials_sep[i-1]:
                if "reward" in trials_sep[i]:
                    switch_reward.append(1)
                if "punishment" in trials_sep[i]:
                    switch_punishment.append(1)
            else:
                if "reward" in trials_sep[i]:
                    other_reward.append(1)
                if "punishment" in trials_sep[i]:
                    other_punishment.append(1)
        
        
        for i in trials_sep:
            
            #if "fanmarbles_trial" in i:
            #    tf_list.append(True)
            #else:
            #    tf_list.append(False)
            
            
            if "fanmarbles_trial" in i:
                fm_count.append(1)
                if "reward" in i:
                    fmr_count.append(1)
                if "punishment" in i:
                    fmp_count.append(1)
            if not "fanmarbles_trial" in i:
                vh_count.append(1)
                if "reward" in i:
                    vhr_count.append(1)
                if "punishment" in i:
                    vhp_count.append(1)
                
            
        
        
#        for i in trials_sep:
#            for line in (i.split('\n')):  
#                if "lck" in line:
#                    timestamps.append(float(line[0:6]))
                    

#        
#        
        if count_rewards > 8:            
#            rpm = (count_rewards / (max(timestamps))) * 60
            pcorrect = ((count_rewards)/(count_trials-1)) * 100
            
            
            x_count = x_count + 1               
            x_results.append(x_count)
            #y_results.append(pcorrect)
            y_fm_results.append(len(fmr_count)/len(fm_count)*100)
            y_vh_results.append(len(vhr_count)/len(vh_count)*100)
            
  
            
            print(os.path.basename(filename))
            
            if "Mixstage     1" in txt:
                for line in txt.split('\n'):    
                    if "percent_stage2" in line:
                        print(line)
   #         print(trials_sep)
            print("number of trials:", count_trials)
            print("water collected:", count_rewards *4)
            print("total rewards:", count_rewards)
            print("count_spout1", count_spout1)
            print("count_spout2", count_spout2)
            print("count_spout3", count_spout3)
#            print("rewards per min:", rpm)
            print ("percent correct:", pcorrect)
            
            
            if len(fm_count) and len(vh_count) > 0:
    
                print("number of fanmarble trials:", len(fm_count))
                print("number of vertical/horizontal trials:", len(vh_count))
 #           print("number of correct stage100 trials:", len(r100_count))
 #           print("number of incorrect stage100 trials:", len(p100_count))
            
            if len(fm_count) > 0 and len(fmr_count) > 0:
                print("percent correct fanmarble trials:", len(fmr_count)/len(fm_count)*100)
            
            if len(vh_count) > 0 and len(vhr_count) > 0:
                print("percent correct vertical/horizontal trials:", len(vhr_count)/len(vh_count)*100)
                
                
            for line in txt.splitlines():
                if "timeout_punishment" in line:
                    print(line)
            
 #           print("percent correct stage100 trials:", num_r100_count/num_trial100_count)
            
            percor_switch = (len(switch_reward) / (len(switch_reward) + len(switch_punishment)))*100
            percor_other = (len(other_reward) / (len(other_reward) + len(other_punishment)))*100
    
            print("percent correct on switch:",percor_switch)
            print("percent correct other:",percor_other)
    
#            print("rewardcount:", count_rewards)
#            print("punishmentcount:", count_punishments)
            print(" ")
            switch_reward.clear()
            switch_punishment.clear()
            other_reward.clear()
            other_punishment.clear()
            
            fm_count.clear()
            fmr_count.clear()
            fmp_count.clear()
            vh_count.clear()
            vhr_count.clear()
            vhp_count.clear()
            tf_list.clear()

    x = (np.hstack(x_results))
    y = (np.hstack(y_fm_results))
    y2 = (np.hstack(y_vh_results))
    plt.xlabel('Session Number')
    plt.ylabel('Percent Correct')
   # plt.title('Learning')
    plt.plot(x,y, "-o")
    plt.plot(x,y2, "-o")            
            
    
#%%
def stage_101_yarm(dataDir, stage, mouse):  
    import os
    import glob
    import re  
    import matplotlib.pyplot as plt
    import numpy as np 
    import statistics 
    
    from pathlib import Path
    
    timestamps = []
    trials_sep = []
    
    x_count = 0
    x_results = []
    y_results = []
    
    y_res = []
    
    ez_trial_count = []
    real_trial_count = []
    ez_reward_count = []
    real_reward_count = []
    ez_punishment_count = []
    real_punishment_count = []
    
    filepath = dataDir + 'stage ' + str(stage) + '/' + mouse
    paths = sorted(Path(filepath).iterdir(), key=os.path.getmtime)
    for filename in paths:
        with open(filename, 'r') as f:
            txt = f.read()

                
        count_rewards = sum(1 for match in re.finditer("reward", txt))
        count_punishments = sum(1 for match in re.finditer("timeout punishment", txt))
        count_trials = count_rewards + count_punishments

        
        count_spout1 = (sum(1 for match in re.finditer("lck_spout1", txt)))
        count_spout2 = (sum(1 for match in re.finditer("lck_spout2", txt)))
        count_spout3 = (sum(1 for match in re.finditer("lck_spout3", txt)))
        
#        count_punishments = sum(1 for match in re.finditer("punishment", txt))
        
        # get largest number in text file aka last timestamp
        trials_sep = (re.split(r'begin_trial', txt, flags=re.MULTILINE))
        

        for i in trials_sep:
            if "Eztest" in i:
                ez_trial_count.append(1)
                if "reward" in i:
                    ez_reward_count.append(1)
                if "punishment" in i:
                    ez_punishment_count.append(1)
            elif "Eztest" not in i:
                real_trial_count.append(1)
                if "reward" in i:
                    real_reward_count.append(1)
                if "punishment" in i:
                        real_punishment_count.append(1)
        
        
#        for i in trials_sep:
#            for line in (i.split('\n')):  
#                if "lck" in line:
#                    timestamps.append(float(line[0:6]))
#        
#        
        if count_rewards > 8:            
#            rpm = (count_rewards / (max(timestamps))) * 60
            pcorrect = ((count_rewards)/(count_trials)) * 100
            
            
            x_count = x_count + 1               
            x_results.append(x_count)
            y_results.append(pcorrect)
            
  
            
            print(os.path.basename(filename))
            
            if "Mixstage     1" in txt:
                for line in txt.split('\n'):    
                    if "percent_stage2" in line:
                        print(line)
   #         print(trials_sep)
            print("number of trials:", count_trials)
            print("total rewards:", count_rewards)
            print("count_spout1", count_spout1)
            print("count_spout2", count_spout2)
            print("count_spout3", count_spout3)
#            print("rewards per min:", rpm)
            print ("percent correct:", pcorrect)
            
            
  #          if len(ez_trial_count) and len(real_trial_count) > 0:
    
   #             print("number of ez trials:", len(ez_trial_count)-1)
    #            print("number of real trials:", len(real_reward_count)+len(real_punishment_count))
 #           print("number of correct stage100 trials:", len(r100_count))
 #           print("number of incorrect stage100 trials:", len(p100_count))
 #               print(len(ez_reward_count))
 #               print(len(ez_punishment_count))
            
            if len(ez_trial_count) > 0 and len(real_trial_count) > 0:
   #             print("percent correct ez trials:", len(ez_reward_count)/(len(ez_trial_count)-1)*100)
                print("percent correct ez trials:", len(ez_reward_count)/(len(ez_reward_count)+len(ez_punishment_count))*100)
            
            if len(ez_trial_count) > 0 and len(real_trial_count) > 0:
                y_real = len(real_reward_count)/(len(real_reward_count)+len(real_punishment_count))*100
                y_res.append(y_real)
                print("percent correct real trials:", y_real)
                
                
            for line in txt.splitlines():
                if "timeout_punishment" in line:
                    print(line)
            
 #           print("percent correct stage100 trials:", num_r100_count/num_trial100_count)
            
            
#            print("rewardcount:", count_rewards)
#            print("punishmentcount:", count_punishments)
            print(" ")
            ez_trial_count.clear()
            real_trial_count.clear()
            ez_reward_count.clear()
            real_reward_count.clear()
            ez_punishment_count.clear()
            real_punishment_count.clear()
    
            
    x = (np.hstack(x_results))
    y = (np.hstack(y_res))
    plt.xlabel('Session Number')
    plt.ylabel('Percent Correct')
 #   plt.axhline(50, color="gray")
#    plt.figure(0)
    plt.title('Learning')
    plt.plot(x,y, "-o")
    
   # return a,b
    
    
   

            #%% troubleshoot
def stage_troubleshoot(dataDir, stage, mouse):  
    import os
    import glob
    import re  
    
    import matplotlib.pyplot as plt
    import numpy as np 
    import statistics 
    
    timestamps = []
    trials_sep = []
    
    x_count = 0
    x_results = []
    y_results = []
    
    count_stage2_rewards = 0
    
    filepath = dataDir + 'stage ' + str(stage) + '/' + mouse
    
    for filename in glob.glob(os.path.join(filepath, '*.txt')):
        with open(filename, 'r') as f:
            txt = f.read()
                
        count_trials = (sum(1 for match in re.finditer("stim", txt)))
        count_rewards = sum(1 for match in re.finditer("reward", txt))
        more_accurate_trials_count = count_trials - 1
        
        count_stage2_trials = sum(1 for match in re.finditer("stage 2 mode", txt))
        count_stage100_trials = sum(1 for match in re.finditer("stage 100 mode", txt))
        
#        count_punishments = sum(1 for match in re.finditer("punishment", txt))
        
        # get largest number in text file aka last timestamp
        trials_sep = (re.split(r'stim', txt, flags=re.MULTILINE))
        for i in trials_sep:
            for line in (i.split('\n')):  
                if "lck" in line:
                    timestamps.append(float(line[0:6]))
            if "stage 2 mode" in i:
                if "reward" in i:
                    count_stage2_rewards =+ 1
#        
#        
        if count_rewards > 5:            
            rpm = (count_rewards / (max(timestamps))) * 60
            pcorrect = ((count_rewards)/(count_trials-1)) * 100
            
            
            x_count = x_count + 1               
            x_results.append(x_count)
            y_results.append(pcorrect)
            
            
            print(os.path.basename(filename))
            print("number of trials:", more_accurate_trials_count)
            print("total rewards:", count_rewards)
            print("rewards per min:", rpm)
            print("percent correct:", pcorrect)
            
            print('stage2rewards', count_stage2_rewards)
            
#            print("rewardcount:", count_rewards)
#            print("punishmentcount:", count_punishments)
            print(" ")
            
#    x = (np.hstack(x_results))
#    y = (np.hstack(y_results))
##    plt.xlabel('Session Number')
# #   plt.ylabel('Percent Correct')
#  #  plt.axhline(50, color="gray")
#    plt.figure(0)
#    plt.title('Learning')
#    plt.plot(x,y, "-o")