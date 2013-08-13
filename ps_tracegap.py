import json
from datetime import datetime, time, timedelta
from scipy import stats
import pylab as pb
import pickle
import numpy as np
import matplotlib.pyplot as plt  # Matplotlib's pyplot: MATLAB-like syntax


# ------------------------------------------------
# import data from json
print "loading data"
fh=open('data_by_cookie.json')
data=json.load(fh)

print "organising data"

minplays=19
# look at subsample of people who played more than x times   
big = {k: data[k] for k in data if len(data[k]) > minplays} #pythonic

players = big.keys()
num_attempts = [len(data[player]) for player in players]
attempt_numbers = [sorted(data[player].keys()) for player in players]
scores = [[data[player][attempt][0] for attempt in attempt_number] for attempt_number, player in zip(attempt_numbers, players)]
days =  [[data[player][attempt][1] for attempt in attempt_number] for attempt_number, player in zip(attempt_numbers, players)]
hours =  [[data[player][attempt][2] for attempt in attempt_number] for attempt_number, player in zip(attempt_numbers, players)]


# rows: players
# columns: attempts
first_x_scores = pb.zeros((len(scores),minplays+1))
for i,attempts in enumerate(scores):
    for j,score in enumerate(attempts[:minplays+1]):
        first_x_scores[i,j] = score

print "looking at time differences"
#function for converting time differences to total hours (the highest resolution we have)
def timedelta_to_hours(td):
    x=td.seconds + td.days*24*60*60
    return x/60/60

#calculate difference in time, in hours, between 5th and 6th play
a_hours_diff=pb.zeros((len(big),1))
b_hours_diff=pb.zeros((len(big),1))
c_hours_diff=pb.zeros((len(big),1))
for player in range(len(big)):
    play1=datetime.combine(datetime.strptime(str(days[player][0]), '%Y%m%d'), time(hours[player][0]))    
    play5=datetime.combine(datetime.strptime(str(days[player][4]), '%Y%m%d'), time(hours[player][4]))    
    play6=datetime.combine(datetime.strptime(str(days[player][5]), '%Y%m%d'), time(hours[player][5]))    
    play10=datetime.combine(datetime.strptime(str(days[player][9]), '%Y%m%d'), time(hours[player][9]))    
    play11=datetime.combine(datetime.strptime(str(days[player][10]), '%Y%m%d'), time(hours[player][10]))    
    play15=datetime.combine(datetime.strptime(str(days[player][14]), '%Y%m%d'), time(hours[player][14]))    
    play20=datetime.combine(datetime.strptime(str(days[player][19]), '%Y%m%d'), time(hours[player][19]))    
    a_hours_diff[player]=timedelta_to_hours(play6-play1)
    b_hours_diff[player]=timedelta_to_hours(play15-play6)
    c_hours_diff[player]=timedelta_to_hours(play20-play15)
    
#test1=((a_hours_diff<6) & (b_hours_diff>12) & (c_hours_diff<6))
#test2=((a_hours_diff<6) & (b_hours_diff<=12) & (c_hours_diff<6))

hours_criterion=(2,6)

testA=((a_hours_diff<hours_criterion[0]) & (b_hours_diff>hours_criterion[1]))
testB=((a_hours_diff<hours_criterion[0]) & (b_hours_diff<=hours_criterion[1]))
test1=testA.flatten() #make 1d array
test2=testB.flatten() #make 1d array

num_attempt_limit=19
#def mean_score_per_attempt(num_attempts, num_attempt_limit, first_x_scores, test1, test2): 
    #create mask, so we only include people who play more than some number of games
played_more_than = pb.array(num_attempts) > num_attempt_limit
eligible_mask = played_more_than     
print str(sum(eligible_mask))+' players in analysis'

#this sets up some holding variables for the means
n_factors=3
mean_score_at_attempt_i_for_factor_j = pb.zeros((minplays+1,n_factors))
count_at_attempt_i_for_factor_j = pb.zeros((minplays+1,n_factors))
std_at_attempt_i_for_factor_j = pb.zeros((minplays+1,n_factors))

for j in range(n_factors):
    if j==0:
        mask=eligible_mask & test1#add in other terms here if you want to split the data up by some other factor indexed by j
    elif j==1:
        mask=eligible_mask & test2
    else:
        mask=eligible_mask & (~ (test2 | test1)) #ie isn't one of the other two
    # Then add up all the scores that satisfy the mask (everyone in this percentile who played more than 19 times)
    # and we divide them by the number of people maskwho satisfy the mask
    ## NOTE THAT WE ASSUME THAT NOONE SCORES ZERO!
    mean_score_at_attempt_i_for_factor_j[:,j] = pb.sum(first_x_scores[mask,:],0) / sum(first_x_scores[mask,:] > 0, 0)
    count_at_attempt_i_for_factor_j[:,j] = sum(first_x_scores[mask,:] > 0, 0)
    # the square route of the average squared difference from the mean
    std_at_attempt_i_for_factor_j[:,j] = np.sqrt(sum(((first_x_scores[mask,:]-mean_score_at_attempt_i_for_factor_j[:,j])**2)*(first_x_scores[mask,:] > 0),0)/count_at_attempt_i_for_factor_j[:,j]) 

print "making plot"
#1 gap
#2 no gap
#3 other
m=mean_score_at_attempt_i_for_factor_j
stderr=std_at_attempt_i_for_factor_j/np.sqrt(count_at_attempt_i_for_factor_j)
vals=range(1,minplays+2)
markervals=['o','s','v']
labelname=['gap between plays 6 and 15','no gap between plays 6 and 15','other']
colors=['r','b']

plt.clf()
for i in range(2):
    pb.errorbar(vals,m[:,i],yerr=stderr[:,i],marker=markervals[i],color=colors[i],label=labelname[i])


     
plt.legend(loc=4)          #centre right 
plt.xlabel('Attempt number')
plt.ylabel('Average score')
#    plt.xlim([0.5, 20.5])
#plt.ylim([-7000,49000])

print "saving plot"
plt.savefig('ps_gaptrace.png', dpi=None, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=False, bbox_inches=None, pad_inches=0.1)
        
print count_at_attempt_i_for_factor_j[1,:]

print "done!"