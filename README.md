"# neural-behavior-preprocessing" 

This code can be used to get the behavioral data for mice running in a freely-moving y-maze 2AFC task.

AO_yarm (functions) and AO_yarm_main (execution) can be used to view behavioral metrics.

AO_behav_calcium can be used to sync behavioral events with neural activity (calcium imaging).
The final output is a folder containing the following .csv files:
1) Perameters pertaining to all events alongside neural activity time frames.
  ![parameters_ex](https://github.com/aozgur360/neural-behavior-preprocessing/assets/77759136/f302fba5-630d-44d7-beeb-a99aa553b5c5)
2) Raw calcium activity (fluorescence intensities) for each cell (x-axis) and each frame (y-axis).
   ![raw_calcium_ex](https://github.com/aozgur360/neural-behavior-preprocessing/assets/77759136/57c1e3ee-38d9-4a33-8ba7-056b6f1a76e2)
3) Spike rate activity (deconvolved calcium activity) for each cell (x-axis) and each frame (y-axis).
   ![spike_rate_ex](https://github.com/aozgur360/neural-behavior-preprocessing/assets/77759136/8f1bbf06-45ff-425f-9f6a-d973a939094d)
4) Rejected cells (cells that were determined not be neurons, via size and shape parameters ran through an algorithm post-cell extraction pipeline).
   
   ![rejected_cells_ex](https://github.com/aozgur360/neural-behavior-preprocessing/assets/77759136/5574cfff-7308-4f9f-8269-d2bec3e8356c)
5) Mouse location tracking (coordinates of the animal's nose throughout the entire experiment).
   
   ![mouse_location_ex](https://github.com/aozgur360/neural-behavior-preprocessing/assets/77759136/2173c357-bd8f-4e00-8840-7ef120c2cb13)
6) Webcam timestamps (frame numbers with corresponding timestamps, used to sync with miniscope frames).

    ![webcam_ex](https://github.com/aozgur360/neural-behavior-preprocessing/assets/77759136/9837c5e7-ec63-4fea-a32f-77037bad5b7e)
7) Miniscope timestamps (frame numbers with corresponding timestamps, used to sync with webcam frames).
    
    ![miniscope_ex](https://github.com/aozgur360/neural-behavior-preprocessing/assets/77759136/d3a9700e-1682-413e-9dbf-ba90f022f680)

get_all_behav_params can be used to output a .csv file containing the following information on a given behavioral session:
mouseID, training stage, sessionID, percent correct left trials, percent correct right trials, overall behavioral performance accuracy, and number of clean trials
![get_all_behav_params_ex](https://github.com/aozgur360/neural-behavior-preprocessing/assets/77759136/2204f684-4f46-4cfe-bdb3-7c4c14673fde)

For mouse location tracking, all credit goes to DeepLabCut: https://github.com/DeepLabCut/DeepLabCut
LocationTracking_Functions and LocationTracking_Individual were written by DeepLabCut, with the only main changes being the specific parameters I used when processing and batching my behavioral data.
AO_get_videos_for_DLC_rig1 was used to generate a list of sessionIDs ready for processing with DeepLabCut. The parameters can be changed to be used on other behavioral rigs for which the algorithm was
separately trained on. For batch processing I used the following steps:
...conda activate deeplabcut
...ipython
...import deeplabcut
...for rig1....deeplabcut.analyze_videos("[insert directory of config file for trained rig]",,save_as_csv=True)
...paste in list
...; for multiple commands






