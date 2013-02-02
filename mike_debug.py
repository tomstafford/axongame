import json
import bisect
import pylab as pb
import scipy.stats as stats
import numpy as np
import pickle

print "loading data"
data = json.load(open('data_by_cookie.json'))

# basics
print "organising data"
players = data.keys()
num_attempts = [len(data[player]) for player in players]
attempt_numbers = [sorted(data[player].keys()) for player in players]
scores = [[data[player][attempt][0] for attempt in attempt_number] for attempt_number, player in zip(attempt_numbers, players)]
maxscores = pb.array([max(score) for score in scores])

# rows: players
# columns: attempts
first_20_scores = pb.zeros((len(scores),20))
for i,attempts in enumerate(scores):
    for j,score in enumerate(attempts[:20]):
        first_20_scores[i,j] = score

def mean_score_per_attempt(num_attempts, num_attempt_limit, maxscores, first_20_scores):
    played_more_than = pb.array(num_attempts) > num_attempt_limit
    percentiles = [stats.scoreatpercentile(maxscores[played_more_than], per) for per in range(20,120,20)]
    player_percentiles = [bisect.bisect(percentiles, maxscore) for maxscore in maxscores]
    mean_score_at_attempt_i_for_percentile_j = pb.zeros((20,5))
    count_at_attempt_i_for_percentile_j = pb.zeros((20,5))
    std_at_attempt_i_for_percentile_j = pb.zeros((20,5))
    for j in range(5):
        print "looking at percentile %s"%j
        # this second mask chooses only those players whose max score is in the jth percentile
        scores_in_this_percentile = pb.array(player_percentiles) == j
        # we AND these together to get the mask
        mask = played_more_than & scores_in_this_percentile
        # Then add up all the scores that satisfy the mask (everyone in this percentile who played more than 19 times)
        # and we divide them by the number of people maskwho satisfy the mask
        ## NOTE THAT WE ASSUME THAT NOONE SCORES ZERO!
        mean_score_at_attempt_i_for_percentile_j[:,j] = pb.sum(first_20_scores[mask,:],0) / sum(first_20_scores[mask,:] > 0, 0)
        #
        #tom added this
        count_at_attempt_i_for_percentile_j[:,j] = sum(first_20_scores[mask,:] > 0, 0)
        # the square route of the average squared difference from the mean
        std_at_attempt_i_for_percentile_j[:,j] = np.sqrt(sum(((first_20_scores[mask,:]-mean_score_at_attempt_i_for_percentile_j[:,j])**2)*(first_20_scores[mask,:] > 0),0)/count_at_attempt_i_for_percentile_j[:,j]) 
    pickle.dump(count_at_attempt_i_for_percentile_j, open('save_count_at_attempt_i_for_percentile_j.p', 'wb'))
    pickle.dump(std_at_attempt_i_for_percentile_j, open('save_std_at_attempt_i_for_percentile_j.p', 'wb'))  
    return mean_score_at_attempt_i_for_percentile_j

pb.plot(mean_score_per_attempt(num_attempts, 19, maxscores, first_20_scores), 'b')
pb.plot(mean_score_per_attempt(num_attempts, 3, maxscores, first_20_scores), 'r')
pb.plot(mean_score_per_attempt(num_attempts, 8, maxscores, first_20_scores), 'g')
pb.plot(mean_score_per_attempt(num_attempts, 15, maxscores, first_20_scores), 'k')
pb.xlabel('Attempt number')
pb.ylabel('Average score')
#pb.show()
pb.savefig('mike_debug.png')

makefig=0
if makefig:
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
           
    legend(loc=4)
    xlabel('Attempt number')
    ylabel('Average score')
    xlim([0.5, 20.5])
    ylim([-7000,49000])
    savefig('../cogsci13/figures/pentiles_attempts_vs_scores.png', dpi=300, facecolor='w', edgecolor='w',
            orientation='portrait', papertype=None, format=None,
            transparent=False, bbox_inches=None, pad_inches=0.1)