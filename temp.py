# -*- coding: utf-8 -*-
"""
Created on Sun Aug  4 08:40:06 2013

@author: tom
"""

count=0


for p in player_percentiles:
    if player_percentiles[p]==3:
        count+=1

print count


agg_scores = pb.zeros((len(scores),20))

agg_scores[:,1]=first_20_scores[:,1]

for i in range(1,20):
    agg_scores[:,i]=first_20_scores[:,i]+agg_scores[:,i-1]
    

pb.errorbar(range(1,21),s[:,i],yerr=stderr[:,i],marker=markervals[i],color='k',label=labelname)


pb.errorbar(mean_agg_score_at_attempt_i_for_percentile_j[:,i],s[:,i],yerr=stderr[:,i],marker=markervals[i],color='k',label=labelname)

mean_agg_score_at_attempt_i_for_percentile_j[:,i]

