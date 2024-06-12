import os
os.chdir('Z:\\Ali O\\code\\Python3\\behavior')
" config "
stage = 4
mouse = 'muscAll'
#mouse = 'c1/fig'
#mouse = 'b/fig'
#mouse = 'm/fig'
#mouse = 'pg/fig'
#mouse = 'w/fig'

dataDir = 'Z:/Ali O/Behavioral Training/Learning Mice Data/'
#%% 
" stage 3 learning curve and bias "
import AO_behavior as behav
behav.stage_3(dataDir, stage, mouse)
#plt.savefig(r'Z:\Ali O\Behavioral Training\behavioral figures\c5learn' + '.pdf', bbox_inches='tight')
#plt.savefig(r'Z:\Ali O\Behavioral Training\behavioral figures\c5learn' + '.eps', format='eps', dpi=1200)

#%%
" stage 2 Trial Counter "
import AO_behavior as behav
behav.stage_2_trial_counter(dataDir, stage, mouse)
#%%
" stage 4 single curves NO TEST PUNISHMENT "
import AO_behavior as behav
behav.stage_4_singlecurve_notestpunish(dataDir, stage, mouse)
#%%
" stage 4 psycho curve 6P"
import AO_curve_fitting as behav
behav.stage_4_psycho_6p(dataDir, stage, mouse)
#%%
" previous trial bias average "
import AO_behavior as behav
behav.previous_trial_bias_avg(dataDir, stage, mouse)
#%%
" test trials previous trial bias average "
import AO_behavior as behav
behav.testtrials_previous_trial_bias_avg(dataDir, stage, mouse)
#%%
" stage 4 avg curve 6P fitted psychometric (OLD 8P TO 6P) "
import AO_curve_fitting as behav
behav.stage_4_6pall_psycho(dataDir, stage, mouse)
#%%








#%%
" stage 4 single curves WITH TEST PUNISHMENT "
import AO_behavior as behav
behav.stage_4_singlecurve(dataDir, stage, mouse)










#%%
" stage 4 multiple curves "
import AO_behavior as behav
behav.stage_4_multicurve(dataDir, stage, mouse)
#%%
" stage 4 last file "
import AO_behavior as behav
behav.stage_4_lastfile(dataDir, stage, mouse)
#%% #not updated
" previous trial bias "
import AO_behavior as behav
behav.previous_trial_bias(dataDir, stage, mouse)

#%% IGNORE (OLD 8P)
" stage 4 average curve "
import AO_behavior as behav
behav.stage_4_avgcurve(dataDir, stage, mouse)
#%% IGNORE (OLD 8P)
" stage 4 average curve fitted psychometric "
import AO_behavior as behav
behav.stage_4_fitavgcurve(dataDir, stage, mouse)