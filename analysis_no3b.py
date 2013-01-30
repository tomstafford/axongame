#-------------------------------------------------
#THIRD - analyse attempts vs scores according to pentile groups of maxscore

#-------------------------------------------------

import json
import scipy.stats.mstats as ssm
import bisect
import numpy as np
from math import *
import matplotlib.pyplot as plt
from pylab import *       

# ------------------------------------------------
# import data from json
fh=open('data_by_cookie.json')
data=json.load(fh)

# --------------------------------------------
# look at subsample of people who played more than x times   
big = {k: data[k] for k in data if len(data[k]) > 19} #pythonic

# ....maxscore
#maxscore={}
#for key in big:
#    maxscore[key]=max([big[key][attempt][0] for attempt in big[key]])


maxscore={}
for key in big:
	scores=[]
	for attempts in big[key]:
		if int(attempts)<21:
			scores.append(big[key][attempts][0])
	try:
		maxscore[key]=max(scores)
	except:
		continue

# -----------------------------------------------
# sort maximum scores, smallest to biggest
ranked_maxscore=sorted(maxscore[key] for key in maxscore)

#.....prcentiles
prcentiles=[]
for p in range(100):
    print p
    prcentiles.append(ssm.scoreatpercentile(ranked_maxscore,p))

#now make dictionary of percentile rank of each player
decile={key: bisect.bisect(prcentiles,maxscore[key]) for key in big}



#-------------------------------------------------------- 

#find average score vs attempt no for pentiles
scores_total=np.zeros( (20,5) )
scores_count=np.zeros( (20,5) )
tallyA=0

for key in big:
    for attempt in big[key]:
            if int(attempt)<21: #we only look at first x scores       
                try:
                    scores_total[int(attempt)-1,int(ceil(decile[key]/20)-1)]+=big[key][attempt][0]
                    scores_count[int(attempt)-1,int(ceil(decile[key]/20)-1)]+=1
                except KeyError:
                    tallyA+=1
                    continue
               
#pickle.dump(scores_total, open('save_scores_total.p', 'wb'))             
#pickle.dump(scores_count, open('save_scores_count.p', 'wb'))             
           
scores_average=scores_total/scores_count                
#stanard error = sum of squared differences from mean / sqrt(n)

#now calc standard error, in a really lazy way by going round again, 
#totalling the squared diffences from the mean               
scores_var=np.zeros( (20,5) )     
tallyB=0       
for key in big:
    for attempt in big[key]:
            if int(attempt)<21: #we only look at first x scores       
                try:
                    diff=float()
                    scores_var[int(attempt)-1,int(ceil(decile[key]/20)-1)]+=(big[key][attempt][0]-scores_average[int(attempt)-1,ceil(decile[key]/20)-1])**2
                except KeyError:
                    tallyB+=1
                    continue            

#pickle.dump(scores_var, open('save_scores_var.p', 'wb'))     

#scores_count=pickle.load(open('save_scores_count.p', 'rb'))
#scores_var=pickle.load(open('save_scores_var.p', 'rb'))



#ie the sum of the squared differences from the mean, divided by n, all sqrt'd
scores_var=np.sqrt(scores_var/scores_count) #calc the standard deviation
scores_var=scores_var/np.sqrt(scores_count) #standard erro
        
plt.clf()

with_errorbars=1

vals=[(1,20),(21,40),(41,60),(61,80),(81,100)]
markervals=['o','s','v','^','D']

if not with_errorbars:
    plot(scores_average)
else:   
    for i in range(4,-1,-1):
        labelname='Percentiles %i to %i' %(vals[i])
        errorbar(range(1,21), scores_average[:,i],yerr=scores_var[:,i],marker=markervals[i],color='k',label=labelname)
       
legend(loc=4)
xlabel('Attempt number')
ylabel('Average score')
ylim([-2000,45000])
savefig('pentiles_attempts_vs_scores.png', dpi=None, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=False, bbox_inches=None, pad_inches=0.1)
        
savefig('../cogsci13/figures/pentiles_attempts_vs_scores.png', dpi=300, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=False, bbox_inches=None, pad_inches=0.1)
        
        
##this checks that the mean of deciles is 2.something 
#from math
#
#a=[]
#for key in decile:
#    a.append(math.ceil(decile[key]/20))
#
#print mean(a) #4.23 something is wrong with deciles

    

