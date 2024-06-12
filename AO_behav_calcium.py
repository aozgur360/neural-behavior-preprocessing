import numpy as np
import pickle
import pandas as pd
import scipy.stats as sp
from matplotlib import pyplot as plt
import scipy.io as spio
import re
from pathlib import Path
import time
import glob
import os

##### CONFIGURATION #####

main_base = r'Z:\Ali O\yarm_miniscope_recording\m25lr\m25lr_6\2023_01_12_r2_good_dlc\10_15_08'
os.chdir(main_base)
main_text = glob.glob('*.txt')[0]

#calcium_csv_path = r'Z:\Ali O\yarm_miniscope_recording\m12lr\m12lr_3\2022_05_20_r2_dlc_ez_good_epa\15_00_33\YrA.csv'
calcium_csv_path = main_base + '\\YrA.csv'

split_frame_numbers = []


data_paths_config = {
    'location_sequence_path': '\\loc_seq.csv',
    'location_path': '\\0fixed_LocationOutput.csv',
    'webcam_timestamps_path': '\\My_WebCam\\timeStamps.csv',
    'miniscope_timestamps_path': '\\My_V4_Miniscope\\timeStamps.csv',
    'session_configs': [
                {
            #'base_path': r"Z:\Ali O\yarm_miniscope_recording\m12lr\m12lr_3\2022_05_20_r2_dlc_ez_good_epa\15_00_33",
            'base_path': main_base,
            #'date': '05_20_2022___15_00_32',
            'date': Path(main_text).stem,
            #'text_file_path': '\\05_20_2022___15_00_32.txt'
            'text_file_path': "\\" + main_text
            }]}




def get_saved_data(file_name):
    try:
        with open(file_name, 'rb') as handle:
            response = pickle.load(handle)
            return response
    except FileNotFoundError:
        print(f'Could not find saved data for file {file_name}')
        return None



def save_data(data, file_name):
    with open(file_name, 'wb') as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)



def get_or_save_data_frame_from_csv(csv_path, use_pickle = True):
    if not use_pickle:
        data_frame = pd.read_csv(csv_path, usecols=["unit_id","frame","YrA"])
    else:
        csv_pickle_path = csv_path + '.pickle'
        data_frame = get_saved_data(csv_pickle_path)
        if (data_frame is None):
            data_frame = pd.read_csv(csv_path, usecols=["unit_id","frame","YrA"])
            save_data(data_frame, csv_pickle_path)
        
    return data_frame


def get_yras_for_unique_cells(data_frame):
    data = pd.DataFrame()

    unique_cell_ids = np.unique(data_frame["unit_id"])

    for cell_id in unique_cell_ids:
        if cell_id == -1:
            continue

        cell_data_series = data_frame[data_frame['unit_id'] == cell_id]
        data[str(cell_id)] = cell_data_series['YrA'].to_numpy()

    #drop nans
    data = data.dropna(axis=1, how='all')

    #rename columns because may need reordering after dropped nans
    rename_col = list(range(len(data.columns)))
    data.columns = rename_col

    return data

def normalize_yras_for_each_cell(data_frame):
    max_scaled = data_frame / data_frame.max()
    return max_scaled




def split_daily_data_frames(data_frame, split_frame_numbers):
    split_data_frames = []
    remaining_data_frame = data_frame

    for split_frame_number in split_frame_numbers:
        split_data_frame = remaining_data_frame.head(split_frame_number)
        split_data_frames.append(split_data_frame)

        remaining_data_frame = remaining_data_frame[split_frame_number:]

        # re index frames to start from 0 again
        remaining_data_frame = remaining_data_frame.reset_index()

        # drop first column of all index
        remaining_data_frame = remaining_data_frame.drop(['index'], axis = 1)

    split_data_frames.append(remaining_data_frame)

    return split_data_frames

###TEST
def split_daily_data_frames_then_normalize(data_frame, split_frame_numbers):
    split_data_frames = []
    remaining_data_frame = data_frame

    for split_frame_number in split_frame_numbers:
        split_data_frame = remaining_data_frame.head(split_frame_number)
        split_data_frames.append(split_data_frame)

        remaining_data_frame = remaining_data_frame[split_frame_number:]

        # re index frames to start from 0 again
        remaining_data_frame = remaining_data_frame.reset_index()

        # drop first column of all index
        remaining_data_frame = remaining_data_frame.drop(['index'], axis = 1)
        
        remaining_data_frame = remaining_data_frame / remaining_data_frame.max()

    split_data_frames.append(remaining_data_frame)
    split_data_frames_temp = []
    for i in split_data_frames:
        split_data_frames_temp.append(i / i.max())
        
    split_data_frames = split_data_frames_temp
    return split_data_frames



def load_base_data(session_config):
    base_path = session_config['base_path']
    behavior_file_path = base_path + session_config['text_file_path']
    
    #load edited location seq data
    location_sequence_data_frame = pd.read_csv(base_path + data_paths_config['location_sequence_path'])
    
    #load location data
    location_data_frame = pd.read_csv(base_path + data_paths_config['location_path'])
    
    #load webcam timestamps data
    webcam_timestamps_data_frame = pd.read_csv(base_path + data_paths_config['webcam_timestamps_path'])
    
    #load miniscope frames/timestamps data
    miniscope_timestamps_data_frame = pd.read_csv(base_path + data_paths_config['miniscope_timestamps_path'])
    
    base_data = {
        'location_sequence_data_frame': location_sequence_data_frame, 
        'location_data_frame': location_data_frame,
        'webcam_timestamps_data_frame': webcam_timestamps_data_frame,
        'miniscope_timestamps_data_frame': miniscope_timestamps_data_frame,
        'behavior_file_path': behavior_file_path,
    }
    
    return base_data


def get_split_trials(behavior_file_path):
    with open(behavior_file_path, 'r') as f:    
        txt = f.read()
    
    #separate trials
    split_trials_init = (re.split(r'begin_trial', txt, flags=re.MULTILINE))
    split_trials = []
    for i in split_trials_init:
                sep = 'timeout'
                stripped = i.split(sep, 1)[0]
                split_trials.append(stripped)
    
    # remove non-trial info in the beginning of the session
    split_trials.pop(0)
        
    return split_trials

##############################
# now on to actual trial processing

def get_trial_parameters(split_trials):
    ####key:
    # vh = 0 , fm = 1
    # stage2 = 0, stage100 = 1
    # left trial = 0, right trial = 1
    # correct = 0, incorrect = 1
    
    # determine stimuli: if vertical/horizontal or fan/marbles
    # determine mode: if stage2 or stage100
    # determine direction: if trial was supposed to be a left or right trial
    # determine correctness: if correct or incorrect

    df_trials_params = pd.DataFrame(columns = ['stimuli', 'mode', 'direction', 'correctness'])
    for i in split_trials:
        
        # params_list = []
        # if "verticalhorizontal_trial" in i:
        #     if "novis_trial" not in i:
        #         params_list.append('VH')
        # elif "icecream_pizza_trial" in i:
        #     if "novis_trial" not in i:
        #         params_list.append('IP')
        # elif "fanmarbles_trial" in i:
        #     if "novis_trial" not in i:
        #         params_list.append('FM')
        # elif "novis_trial" in i:
        #     params_list.append("NS")
        
        params_list = []
        if "verticalhorizontal_trial" in i:
            if "nostim_trial" in i:
                params_list.append('NS')
            else:
                params_list.append('VH')
        elif "icecream_pizza_trial" in i:
            if "nostim_trial" in i:
                params_list.append('NS')
            else:
                params_list.append('IP')
        elif "fanmarbles_trial" in i:
            if "nostim_trial" in i:
                params_list.append('NS')
            else:
                params_list.append('FM')
                
        
        if "start_stage2" in i:
            params_list.append('FTP')
        elif "start_stage100" in i:
            params_list.append('INIT')
        else:
            params_list.append('BLANK')
            
        if "stimL" in i:
            params_list.append('L')
        elif "stimR" in i:
            params_list.append('R')
        else:
            params_list.append('BLANK')
            
        if "reward" in i:
            params_list.append("correct")
        else:
            params_list.append("wrong")
                
        df_trials_params = df_trials_params.append({'stimuli' : params_list[0], 'mode' : params_list[1], 'direction' : params_list[2], 
                                                    'correctness' : params_list[3]}, ignore_index=True)

        #df_trials_params = df_trials_params.append({'stimuli' : params_list[0], 'mode' : params_list[1], 'direction' : params_list[2]}, ignore_index=True)
        
    trial_parameters = {
    'trials':split_trials,
    'params':df_trials_params,
    }
    
    return trial_parameters
                
def get_arduino_timestamps_for_trials(split_trials):
    arduino_timestamps_for_trials = []
    for i in split_trials:
        trial_ts = []
        for line in (i.split('\n')):  
            if 'ts' in line: 
               trial_ts.append(float(line[0:6])*1000)
        arduino_timestamps_for_trials.append(trial_ts)
    
    return arduino_timestamps_for_trials

def get_start_and_end_arduino_timestamps_for_trials(arduino_timestamps):
    start_and_end_arduino_timestamps_for_trials = []
    for i in arduino_timestamps:
        trial_se = []
        trial_se.append(i[0])
        trial_se.append(i[-1])
        start_and_end_arduino_timestamps_for_trials.append(trial_se)
    
    return start_and_end_arduino_timestamps_for_trials
        
def get_closest_start_and_end_webcam_frames_for_trials(start_and_end_arduino_timestamps_for_trials, base_data):
    df = base_data['webcam_timestamps_data_frame']
    
    frame_start = []
    frame_end = []
    
    #get closest start and end webcam frames
    for i in start_and_end_arduino_timestamps_for_trials: 
        frame_start.append(df.iloc[(df['Time Stamp (ms)']-i[0]).abs().argsort()[:1]])
        frame_end.append(df.iloc[(df['Time Stamp (ms)']-i[-1]).abs().argsort()[:1]])
    
    frame_start_final = []
    for i in frame_start:
        frame_start_final.append(i.iloc[0]['Frame Number'])
    frame_end_final = []
    for i in frame_end:
        frame_end_final.append(i.iloc[0]['Frame Number'])       
        
    
    closest_start_and_end_webcam_frames_for_trials = {
    'start':frame_start_final,
    'end':frame_end_final,
    }
    
    return closest_start_and_end_webcam_frames_for_trials
    
def get_webcam_frames_for_each_trial(closest_start_and_end_webcam_frames_for_trials, base_data):
    
    frame_start = closest_start_and_end_webcam_frames_for_trials['start']
    frame_end = closest_start_and_end_webcam_frames_for_trials['end']
    
    loc_seq = base_data['location_sequence_data_frame']
    df_location = base_data['location_data_frame']
    seq_ideal = ['main','inter','main','spout']
    
    dec_frames_1 = []
    dec_frames_2 = []
    all_seq = []
    all_seq_frames = []
    seq_ideal_frames = []
    seq_ideal_frames_start = []
    seq_ideal_frames_end = []
    seq_ideal_dec_frames_start = []
    first = []
    second = []
    
    clean_trials = []
    all_seq_frames_start = []
    all_seq_frames_end = []
    

    #for x in range(0,2):
    for x in range(len(frame_start)):
        start = frame_start[x]
        end = frame_end[x]
        all_seq.append([])
        all_seq_frames.append([])
        
        #for y in range(0,2):
        for y in range(len(loc_seq)):
              #max number of frames in excel 
            if start <= len(df_location['Frame']):
                frame = loc_seq.iloc[y]['Frame']
                if frame >= start and frame <= end:
                    all_seq[x].append(loc_seq.iloc[y]['ROI_location'])
                    all_seq_frames[x].append(loc_seq.iloc[y]['Frame'])
                    
        all_seq_frames_start.append(start)
        all_seq_frames_end.append(end)
                   
        if all_seq[x] == seq_ideal:
            clean_trials.append(x)
            #use this next variable to check webcam frames
            #seq_ideal_frames.append([start,end])
            seq_ideal_frames.append([start,end])
            seq_ideal_frames_start.append(start)
            seq_ideal_frames_end.append(end)

    inters_index = []
    for i in all_seq:
        if 'inter' in i:
            inters_index.append(i.index('inter'))
        else:
            inters_index.append('NaN')
             
    inters = []        
    for index, val in enumerate(inters_index):
        if type(val) == int:
            inters.append(all_seq_frames[index][val])
        # else:
        #     inters.append(35491)
        #     #continue
    
    for item in all_seq_frames:
      if len(item) > 1:  
          #first = [item[0] for item in all_seq_frames]
          #second = [item[1] for item in all_seq_frames]
          #print(item[0])
          first.append(item[0])
          second.append(item[1])
         
    dec_frames_1 = first
    dec_frames_2 = second
            
    start_dec_ideal =[]
    end_dec_ideal = []
    for x in range(len(seq_ideal_frames_start)):
        start = seq_ideal_frames_start[x]
        end = seq_ideal_frames_end[x]
        
        for y in range(len(first)):
    
            if first[y] >= start and first[y] <= end:
                start_dec_ideal.append(first[y])
    
            if second[y] >= start and second[y] <= end:
                end_dec_ideal.append(second[y])       
                
    #can grab non-ideal frames later if needed       
                
    # ideal_webcam_frames_for_each_trial = {
    #     'trial_start':seq_ideal_frames_start,
    #     'stim_start':start_dec_ideal,
    #     'turn_frame':end_dec_ideal,
    #     'trial_end':seq_ideal_frames_end
    #     }       

    #note stim start and turn frames are only for clean trials
    #will take care to match these properly in the update parameters function
    webcam_frames_for_each_trial = {
    'trial_start':all_seq_frames_start,
    'stim_start':start_dec_ideal,
    'turn_frame':end_dec_ideal,
    'trial_end':all_seq_frames_end,
    'clean_trials':clean_trials
    }          

    # ideal_webcam_frames_for_each_trial = {
    #     'full_trial':{
    #     'start':seq_ideal_frames_start,
    #     'end':seq_ideal_frames_end,
    #     },
    #     'decision_making':{
    #     'start':start_dec_ideal,
    #     'end':end_dec_ideal,   
    #     },
    #     # 1 = dec_making, 2 = inter, so 1_2 is same as decision_making
    #     #no longer 1_2, now 1_inter...
    #     'non_ideal_filtered_1_2':{
    #     '1':dec_frames_1,
    #     '2':inters,   
    #     }
    # }
    
    return webcam_frames_for_each_trial
    
    
# def get_webcam_frames_for_each_trial(closest_start_and_end_webcam_frames_for_trials, base_data):
    
#     frame_start = closest_start_and_end_webcam_frames_for_trials['start']
#     frame_end = closest_start_and_end_webcam_frames_for_trials['end']
    
#     loc_seq = base_data['location_sequence_data_frame']
#     df_location = base_data['location_data_frame']
#     seq_ideal = ['main','inter','main','spout']
    
#     dec_frames_1 = []
#     dec_frames_2 = []
#     all_seq = []
#     all_seq_frames = []
#     seq_ideal_frames = []
#     seq_ideal_frames_start = []
#     seq_ideal_frames_end = []
#     seq_ideal_dec_frames_start = []
#     first = []
#     second = []
    
#     clean_trials = []
#     all_seq_frames_start = []
#     all_seq_frames_end = []

#     #for x in range(0,2):
#     for x in range(len(frame_start)):
#         start = frame_start[x]
#         end = frame_end[x]
#         all_seq.append([])
#         all_seq_frames.append([])
        
#         #for y in range(0,2):
#         for y in range(len(loc_seq)):
#              #max number of frames in excel 
#            if start <= len(df_location['Frame']):
#                frame = loc_seq.iloc[y]['Frame']
#                if frame >= start and frame <= end:
#                    all_seq[x].append(loc_seq.iloc[y]['ROI_location'])
#                    all_seq_frames[x].append(loc_seq.iloc[y]['Frame'])
        
#         #trial start
#         #trial end
#         all_seq_frames_start.append(start)
#         all_seq_frames_end.append(end)
           
#         #determine if clean trial or unclean trial
#         if all_seq[x] == seq_ideal:
#             clean_trials.append(x)

#     inters_index = []
#     for i in all_seq:
#         if 'inter' in i:
#             inters_index.append(i.index('inter'))
#         else:
#             inters_index.append('NaN')
    
#     #determine turn frame
#     inters = []        
#     for index, val in enumerate(inters_index):
#         if type(val) == int:
#             inters.append(all_seq_frames[index][val])
#         # else:
#         #     inters.append(35491)
#         #     #continue
    
#     for item in all_seq_frames:
#       if len(item) > 1:  
#           #first = [item[0] for item in all_seq_frames]
#           #second = [item[1] for item in all_seq_frames]
#           #print(item[0])
#           first.append(item[0])
#           second.append(item[1])
         
#     dec_frames_1 = first
#     dec_frames_2 = second
            
#     start_dec_ideal =[]
#     end_dec_ideal = []
#     for x in range(len(seq_ideal_frames_start)):
#         start = seq_ideal_frames_start[x]
#         end = seq_ideal_frames_end[x]
        
#         for y in range(len(first)):
    
#             if first[y] >= start and first[y] <= end:
#                 start_dec_ideal.append(first[y])
    
#             if second[y] >= start and second[y] <= end:
#                 end_dec_ideal.append(second[y])       
                
#     #can grab non-ideal frames later if needed       
                
#     webcam_frames_for_each_trial = {
#         'trial_start': all_seq_frames_start,
#         'stim_start':dec_frames_1,
#         'turn_frame':inters,
#         'trial_end':all_seq_frames_end,
#         'clean_trials':clean_trials
#         }           
#     return webcam_frames_for_each_trial
    
def get_closest_start_and_end_webcam_timestamps_for_webcam_frames(webcam_frames_for_each_trial, base_data):
    df = base_data['webcam_timestamps_data_frame']
    trial_start_frame = webcam_frames_for_each_trial['trial_start']
    stim_start_frame = webcam_frames_for_each_trial['stim_start']
    turn_frame = webcam_frames_for_each_trial['turn_frame']
    trial_end_frame = webcam_frames_for_each_trial['trial_end']
    
    #get closest start and end webcam timestamps for trial_start webcam frames
    trial_start_frame_wf = []
    for i in trial_start_frame:
        trial_start_frame_wf.append(df.iloc[(df['Frame Number']-i).abs().argsort()[:1]])
    trial_start_frame_wts = []
    for i in trial_start_frame_wf:
        trial_start_frame_wts.append(i.iloc[0]['Time Stamp (ms)'])
      
    #get closest start and end webcam timestamps for stim_start webcam frames
    stim_start_frame_wf = []
    for i in stim_start_frame:
        stim_start_frame_wf.append(df.iloc[(df['Frame Number']-i).abs().argsort()[:1]])
    stim_start_frame_wts = []
    for i in stim_start_frame_wf:
        stim_start_frame_wts.append(i.iloc[0]['Time Stamp (ms)'])

    #get closest start and end webcam timestamps for turn_frame webcam frames
    turn_frame_wf = []
    for i in turn_frame:
        turn_frame_wf.append(df.iloc[(df['Frame Number']-i).abs().argsort()[:1]])
    turn_frame_wts = []
    for i in turn_frame_wf:
        turn_frame_wts.append(i.iloc[0]['Time Stamp (ms)'])

    #get closest start and end webcam timestamps for trial_end webcam frames
    trial_end_frame_wf = []
    for i in  trial_end_frame:
         trial_end_frame_wf.append(df.iloc[(df['Frame Number']-i).abs().argsort()[:1]])
    trial_end_frame_wts = []
    for i in  trial_end_frame_wf:
         trial_end_frame_wts.append(i.iloc[0]['Time Stamp (ms)'])
    
    
    closest_start_and_end_webcam_timestamps_for_webcam_frames = {
    'trial_start':trial_start_frame_wts,
    'stim_start':stim_start_frame_wts,
    'turn_frame':turn_frame_wts,
    'trial_end':trial_end_frame_wts,
        }
    return closest_start_and_end_webcam_timestamps_for_webcam_frames

def get_miniscope_frames_from_webcam_timestamps(closest_start_and_end_webcam_timestamps_for_webcam_frames,base_data):        
    
    df_mini = base_data['miniscope_timestamps_data_frame']
    
    trial_start = closest_start_and_end_webcam_timestamps_for_webcam_frames['trial_start']
    stim_start = closest_start_and_end_webcam_timestamps_for_webcam_frames['stim_start']
    turn_frame = closest_start_and_end_webcam_timestamps_for_webcam_frames['turn_frame']
    trial_end = closest_start_and_end_webcam_timestamps_for_webcam_frames['trial_end']
    
    #use timestamp webcam to get timestamp miniscope and then use that to get miniscope frames
    #for trial_start
    trial_start_mts = []
    for i in trial_start:
        trial_start_mts.append(df_mini.iloc[(df_mini['Time Stamp (ms)']-i).abs().argsort()[:1]])
    trial_start_mf = []
    for i in trial_start_mts:
        trial_start_mf.append(i.iloc[0]['Frame Number'])
    
    #for stim_start
    stim_start_mts = []
    for i in stim_start:
        stim_start_mts.append(df_mini.iloc[(df_mini['Time Stamp (ms)']-i).abs().argsort()[:1]])
    stim_start_mf = []
    for i in stim_start_mts:
        stim_start_mf.append(i.iloc[0]['Frame Number'])
        
    #for turn_frame
    turn_frame_mts = []
    for i in turn_frame:
        turn_frame_mts.append(df_mini.iloc[(df_mini['Time Stamp (ms)']-i).abs().argsort()[:1]])
    turn_frame_mf = []
    for i in turn_frame_mts:
        turn_frame_mf.append(i.iloc[0]['Frame Number']) 
        
    #for trial_end
    trial_end_mts = []
    for i in trial_end:
        trial_end_mts.append(df_mini.iloc[(df_mini['Time Stamp (ms)']-i).abs().argsort()[:1]])
    trial_end_mf = []
    for i in trial_end_mts:
        trial_end_mf.append(i.iloc[0]['Frame Number'])    
        
    miniscope_frames_from_webcam_timestamps = {
        'trial_start':trial_start_mf,
        'stim_start':stim_start_mf,
        'turn_frame':turn_frame_mf,
        'trial_end':trial_end_mf
        }
    
    return miniscope_frames_from_webcam_timestamps

# def get_labeled_clean_trials(ideal_webcam_frames_for_each_trial,closest_start_and_end_webcam_frames_for_trials):
    
#     ideal_start = ideal_webcam_frames_for_each_trial['trial_start'] 
#     any_start = closest_start_and_end_webcam_frames_for_trials['start']
    
#     labeled_clean_trials = []
#     for i in ideal_start:
#         if i in any_start:
#             labeled_clean_trials.append(any_start.index(i))
            
#     return labeled_clean_trials

def get_updated_trial_params(trial_parameters,webcam_frames_for_each_trial,miniscope_frames_from_webcam_timestamps):
    df = trial_parameters['params']
    clean_trials = webcam_frames_for_each_trial['clean_trials']
    
    df['trial_start'] = miniscope_frames_from_webcam_timestamps['trial_start']
    df['trial_end'] = miniscope_frames_from_webcam_timestamps['trial_end']

    df['clarity'] = "messy"
    
    for i in clean_trials:       
        df['clarity'].iloc[i] = 'clean'
    
    df['stim_start'] = 'NaN'
    df['turn_frame'] = 'NaN' 

    clean_counter = -1
    for num,val in enumerate(df['clarity']):
        if val == 'clean':
            clean_counter = clean_counter + 1
            df['stim_start'].iloc[num] = miniscope_frames_from_webcam_timestamps['stim_start'][clean_counter]
            df['turn_frame'].iloc[num] = miniscope_frames_from_webcam_timestamps['turn_frame'][clean_counter]
    
    df = df[['stimuli','mode','direction','correctness','clarity','trial_start','stim_start','turn_frame','trial_end']]
    
    return df


########################################################

def get_session_data(data_frame, session_config):
    #print(len(data_frame))
    #print(session_config['base_path'])

    base_data = load_base_data(session_config)
    split_trials = get_split_trials(base_data['behavior_file_path'])
    
    trial_parameters = get_trial_parameters(split_trials)
    arduino_timestamps_for_trials = get_arduino_timestamps_for_trials(split_trials)
    start_and_end_arduino_timestamps_for_trials = get_start_and_end_arduino_timestamps_for_trials(arduino_timestamps_for_trials)
    closest_start_and_end_webcam_frames_for_trials = get_closest_start_and_end_webcam_frames_for_trials(start_and_end_arduino_timestamps_for_trials, base_data)
    webcam_frames_for_each_trial = get_webcam_frames_for_each_trial(closest_start_and_end_webcam_frames_for_trials, base_data)
    closest_start_and_end_webcam_timestamps_for_webcam_frames = get_closest_start_and_end_webcam_timestamps_for_webcam_frames(webcam_frames_for_each_trial, base_data)
    miniscope_frames_from_webcam_timestamps = get_miniscope_frames_from_webcam_timestamps(closest_start_and_end_webcam_timestamps_for_webcam_frames,base_data)
    #labeled_clean_trials = get_labeled_clean_trials(ideal_webcam_frames_for_each_trial,closest_start_and_end_webcam_frames_for_trials)
    updated_trial_params = get_updated_trial_params(trial_parameters,webcam_frames_for_each_trial,miniscope_frames_from_webcam_timestamps)
    final_data = {
    'trial_parameters':trial_parameters,
    'arduino_timestamps_for_trials': arduino_timestamps_for_trials,
    'arduino_start_end_ts': start_and_end_arduino_timestamps_for_trials,
    'closest_start_end_webcam_frames_for_trials': closest_start_and_end_webcam_frames_for_trials,
    'webcam_frames_for_each_trial':webcam_frames_for_each_trial,
    'closest_start_and_end_webcam_timestamps_for_webcam_frames': closest_start_and_end_webcam_timestamps_for_webcam_frames,
    'miniscope_frames': miniscope_frames_from_webcam_timestamps,
    #'clean_trial_numbers':labeled_clean_trials,
    'updated_trial_params':updated_trial_params
    }

    return final_data

def get_sessions_data(data_frames):
    sessions_data = []

    for i in range(len(data_frames)):
        data_frame = data_frames[i]
        session_config = data_paths_config['session_configs'][i]
        session_data = get_session_data(data_frame, session_config)
        sessions_data.append(session_data)
    
    return sessions_data





#%%

tic = time.perf_counter()
calcium_data_frame = get_or_save_data_frame_from_csv(calcium_csv_path)

unique_cells_yras_data_frame = get_yras_for_unique_cells(calcium_data_frame)

daily_data_frames_raw = split_daily_data_frames(unique_cells_yras_data_frame, split_frame_numbers)
normalized_cells_yras_data_frame = normalize_yras_for_each_cell(unique_cells_yras_data_frame)

daily_data_frames = split_daily_data_frames(normalized_cells_yras_data_frame, split_frame_numbers)

sessions_data = get_sessions_data(daily_data_frames)
toc = time.perf_counter()
print(f"Function took {toc - tic:0.4f} seconds")

#%%
tic = time.perf_counter()
import os

basefolder = data_paths_config['session_configs'][0]['base_path'] + '\exported_python_analysis'

# Check whether the specified path exists or not
isExist = os.path.exists(basefolder)

if not isExist:
  # Create a new directory because it does not exist 
  os.makedirs(basefolder)

date = data_paths_config['session_configs'][0]['date']

for i in range(len(daily_data_frames_raw)):
    file = (basefolder + '\\calcium_raw_' + date + ".csv")
    #daily_data_frames_raw[i].to_csv(base_folder + '\\ca_raw_s' + str[i] + '.csv')
    daily_data_frames_raw[i].to_csv(file)
    
for i in range(len(sessions_data)):
    file = (basefolder + '\\trial_parameters_' + date + ".csv")
    sessions_data[i]['updated_trial_params'].to_csv(file,index=False)
##############    

webcam_csv = pd.read_csv(data_paths_config['session_configs'][0]['base_path'] + "\\My_WebCam\\timeStamps.csv")
ms_csv = pd.read_csv(data_paths_config['session_configs'][0]['base_path'] + '\\My_V4_Miniscope\\timeStamps.csv')

for i in range(len(sessions_data)):
    file = (basefolder + '\\webcam_timestamps_' + date + ".csv")
    webcam_csv.to_csv(file,index=False)

for i in range(len(sessions_data)):
    file = (basefolder + '\\miniscope_timestamps_' + date + ".csv")
    ms_csv.to_csv(file,index=False)

coords = pd.read_csv(data_paths_config['session_configs'][0]['base_path'] + data_paths_config['location_path'])
coords_x = coords['X']
coords_y = coords['Y']

df_coords = pd.DataFrame()
df_coords['X'] = coords_x
df_coords['Y'] = coords_y
df_coords['Center'] = None

for i in range(len(sessions_data)):
    file = (basefolder + '\\xy_' + date + ".csv")
    df_coords.to_csv(file,index=False)

#make empty new folder
newpath = basefolder + "\\" + date
if not os.path.exists(newpath):
    os.makedirs(newpath)


toc = time.perf_counter()
print(f"Function took {toc - tic:0.4f} seconds")












#%%
# # to get miniscope frames for xy coordinates    
# import pandas as pd
# #webcam_csv = pd.read_csv(r"Z:\Ali O\yarm_miniscope_recording\m13l\m13l_3\2022_05_18_r2_dlc_ez_good\11_00_50\My_WebCam\timeStamps.csv")
# #ms_csv = pd.read_csv(r"Z:\Ali O\yarm_miniscope_recording\m13l\m13l_3\2022_05_18_r2_dlc_ez_good\11_00_50\My_V4_Miniscope\timeStamps.csv")
# webcam_csv = pd.read_csv(data_paths_config['session_configs'][0]['base_path'] + "\\My_WebCam\\timeStamps.csv")
# ms_csv = pd.read_csv(data_paths_config['session_configs'][0]['base_path'] + '\\My_V4_Miniscope\\timeStamps.csv')

# coords = pd.read_csv(data_paths_config['session_configs'][0]['base_path'] + data_paths_config['location_path'])
# coords_x = coords['X']
# coords_y = coords['Y']

# #use webcam timestamp to get timestamp miniscope
# ms_ts = []
# for i in webcam_csv.iloc[:,1]:
#     ms_ts.append(ms_csv.iloc[(ms_csv['Time Stamp (ms)']-i).abs().argsort()[:1]])
    
# #use miniscope timestamp to get miniscope frame
# ms_frame = []
# for i in ms_ts:
#     ms_frame.append(i.iloc[0]['Frame Number'])
    
# df_msframes = pd.DataFrame({'MS Frame':ms_frame})    
# df_msframes['X'] = coords_x
# df_msframes['Y'] = coords_y
# df_msframes['Center'] = None

# # save coordinates data
# #basefolder_xy = r'Z:\Ali O\yarm_miniscope_recording\m13l\m13l_3\2022_05_18_r2_dlc_ez_good\11_00_50\exported_python_analysis'
# xy_file = (basefolder + '\\xy_' + date + ".csv")
# df_msframes.to_csv(xy_file, index=False)

# toc = time.perf_counter()
# print(f"Function took {toc - tic:0.4f} seconds")



#%%

# #get clean, correct, left, init triails (start-end)
# df = sessions_data[0]['updated_trial_params']
# # clean
# df_clean = df[df['clarity'] =='clean']
# # clean, correct
# df_clean_correct = df_clean[df_clean['correctness'] =='correct']
# # clean, correct, init
# df_clean_correct_init = df_clean_correct[df_clean_correct['mode'] =='INIT']
# # clean, correct, init, left
# df_clean_correct_init_left = df_clean_correct_init[df_clean_correct_init['direction'] =='L']
#%%

# raw_calcium = daily_data_frames_raw[0]
# for i in range(len(raw_calcium.columns)):
#     plt.figure()
#     plt.plot(raw_calcium[i].iloc[507:1006])
#     plt.axvline(x=507,color="red")
#     plt.axvline(x=625,color="orange")
#     plt.axvline(x=643,color="green")
#     plt.axvline(x=677,color="purple")
#     plt.axvline(x=682,color="red")
#     plt.axvline(x=788,color="orange")
#     plt.axvline(x=805,color="green")
#     plt.axvline(x=837,color="purple")
#     plt.axvline(x=843,color="red")
#     plt.axvline(x=952,color="orange")
#     plt.axvline(x=973,color="green")
#     plt.axvline(x=1005,color="purple")
#     plt.show()
    
# # for i in range(len(input1)):
# #     plt.figure()
# #     plt.plot(input1[i])
# #     plt.plot(input2[i])
# #     plt.axvline(x=turnline)
# #     plt.show()
#%%
# raw_calcium = daily_data_frames_raw[0]
# for i in range(len(raw_calcium.columns)):
#     plt.figure()
#     plt.plot(raw_calcium[i].iloc[36309:36902])
#     plt.show()
#%%

