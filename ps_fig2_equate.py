#make Figure 3

import json
import bisect
import pylab as pb
import scipy.stats as stats
import numpy as np
import pickle
import matplotlib.pyplot as plt  # Matplotlib's pyplot: MATLAB-like syntax

print "loading data"
data = json.load(open('data_by_cookie.json'))

# basics
print "organising data"
players = data.keys()
num_attempts = [len(data[player]) for player in players]
attempt_numbers = [sorted(data[player].keys()) for player in players]
scores = [[data[player][attempt][0] for attempt in attempt_number] for attempt_number, player in zip(attempt_numbers, players)]

maxscore_method=1

if maxscore_method:
    #this defines max score as max on any play
    maxscores = pb.array([max(score) for score in scores]) 
else:
    #this defines max score as max on 20th play
    maxscores_notarray=[]
    for score in scores:
    	if len(score)>19:
    		maxscores_notarray.append(score[19])
    	else:
    		maxscores_notarray.append(0)
    maxscores = pb.array(maxscores_notarray)


# rows: players
# columns: attempts
first_20_scores = pb.zeros((len(scores),20))
for i,attempts in enumerate(scores):
    for j,score in enumerate(attempts[:20]):
        first_20_scores[i,j] = score

def mean_score_per_attempt(num_attempts, num_attempt_limit, maxscores, first_20_scores):
    #create mask, so we only include people who play more than some number of games
    played_more_than = pb.array(num_attempts) > num_attempt_limit
    # this mask means we only look at people who got roughly equivalent scores on plays 1 and 2
    equate_mask1bot=pb.array(first_20_scores[:,0]>7500)   
    equate_mask1top=pb.array(first_20_scores[:,0]<12500)
    equate_mask2bot=pb.array(first_20_scores[:,1]>7500)
    equate_mask2top=pb.array(first_20_scores[:,1]<12500)
    equate_mask3bot=pb.array(first_20_scores[:,2]>7500)
    equate_mask3top=pb.array(first_20_scores[:,2]<12500)
    #can't figure out the all function to do this elegantly    
    
    #equate_mask=equate_mask1bot & equate_mask1top & equate_mask2bot & equate_mask2top & equate_mask3bot & equate_mask3top
    equate_mask=equate_mask1bot & equate_mask1top     
    #eligible_mask = equate_mask & played_more_than     
    eligible_mask = played_more_than     
    print str(sum(eligible_mask))+' players in analysis'
    #now rank everyone according to their top score
    #this calculates the boundaries
    percentiles = [stats.scoreatpercentile(maxscores[eligible_mask], per) for per in range(20,120,20)]
    #this assigns to percentiles (actually quintile) groups    
    #NB assignment is to ALL players, but based on boundaries of only those who are eligible
    #non-eligible players get excluded later (because we reuse the eligible mask)
    player_percentiles = [bisect.bisect(percentiles, maxscore) for maxscore in maxscores]
    #this sets up some holding variables for the means
    mean_score_at_attempt_i_for_percentile_j = pb.zeros((20,5))
    count_at_attempt_i_for_percentile_j = pb.zeros((20,5))
    std_at_attempt_i_for_percentile_j = pb.zeros((20,5))
    
    # -------------
    for j in range(5):
        print "looking at percentile group %s"%j
        # this second mask chooses only those players whose max score is in the jth percentile
        scores_in_this_percentile = pb.array(player_percentiles) == j
        # we AND these together to get the mask
        #mask = played_more_than & scores_in_this_percentile & equate_mask
        percentile_mask = scores_in_this_percentile & eligible_mask
        # Then add up all the scores that satisfy the mask (everyone in this percentile who played more than 19 times)
        # and we divide them by the number of people maskwho satisfy the mask
        ## NOTE THAT WE ASSUME THAT NOONE SCORES ZERO!
        mean_score_at_attempt_i_for_percentile_j[:,j] = pb.sum(first_20_scores[percentile_mask ,:],0) / sum(first_20_scores[percentile_mask ,:] > 0, 0)
        #
        #tom added this
        count_at_attempt_i_for_percentile_j[:,j] = sum(first_20_scores[percentile_mask ,:] > 0, 0)
        # the square route of the average squared difference from the mean
        std_at_attempt_i_for_percentile_j[:,j] = np.sqrt(sum(((first_20_scores[percentile_mask ,:]-mean_score_at_attempt_i_for_percentile_j[:,j])**2)*(first_20_scores[percentile_mask,:] > 0),0)/count_at_attempt_i_for_percentile_j[:,j]) 
    pickle.dump(count_at_attempt_i_for_percentile_j, open('save_count_at_attempt_i_for_percentile_j.p', 'wb'))
    pickle.dump(std_at_attempt_i_for_percentile_j, open('save_std_at_attempt_i_for_percentile_j.p', 'wb'))  
    return mean_score_at_attempt_i_for_percentile_j

## we still don't know why these don't look like they should
#pb.plot(mean_score_per_attempt(num_attempts, 19, maxscores, first_20_scores), 'b')
#pb.plot(mean_score_per_attempt(num_attempts, 3, maxscores, first_20_scores), 'r')
#pb.plot(mean_score_per_attempt(num_attempts, 8, maxscores, first_20_scores), 'g')
#pb.plot(mean_score_per_attempt(num_attempts, 15, maxscores, first_20_scores), 'k')
#pb.xlabel('Attempt number')
#pb.ylabel('Average score')
##pb.show()
#pb.savefig('mike_debug.png')


makefig=1
if makefig:
    print "making figure"
    s=mean_score_per_attempt(num_attempts, 19, maxscores, first_20_scores)
    count_at_attempt_i_for_percentile_j=pickle.load(open('save_count_at_attempt_i_for_percentile_j.p', 'rb'))    
    std_at_attempt_i_for_percentile_j=pickle.load(open('save_std_at_attempt_i_for_percentile_j.p', 'rb'))    
    stderr=std_at_attempt_i_for_percentile_j/np.sqrt(count_at_attempt_i_for_percentile_j)
    vals=[(1,20),(21,40),(41,60),(61,80),(81,100)]
    markervals=['o','s','v','^','D']
    for i in range(4,-1,-1):
        labelname='Percentiles %i to %i' %(vals[i])
        pb.errorbar(range(1,21),s[:,i],yerr=stderr[:,i],marker=markervals[i],color='k',label=labelname)
        #errorbar(range(1,21), s[:,i],yerr=scores_var[:,i],marker=markervals[i],color='k',label=labelname)
           
    plt.legend(loc=4)
    plt.xlabel('Attempt number')
    plt.ylabel('Average score')
    plt.xlim([0.5, 20.5])
    plt.ylim([-7000,49000])
    plt.savefig('StaffordFig2equate.png', dpi=300, facecolor='w', edgecolor='w',
            orientation='portrait', papertype=None, format=None,
            transparent=False, bbox_inches=None, pad_inches=0.1)
    
    generatepaperfigs=0
    if generatepaperfigs:    
        plt.savefig('../psycscience/StaffordFig2equate.png', dpi=300, facecolor='w', edgecolor='w',
            orientation='portrait', papertype=None, format=None,
            transparent=False, bbox_inches=None, pad_inches=0.1)

#tell me the n
countdata=pickle.load(open('save_count_at_attempt_i_for_percentile_j.p','rb'))
print sum(countdata,0)/20
plt.clf()
plt.plot(countdata)
plt.savefig('counts.png', dpi=300, facecolor='w', edgecolor='w',
            orientation='portrait', papertype=None, format=None,
            transparent=False, bbox_inches=None, pad_inches=0.1)
            