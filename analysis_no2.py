#-------------------------------------------------
#SECOND - rank people according to their highest ever score
#           and look at the number of attempts they make
#-------------------------------------------------



import pickle
import json

# ------------------------------------------------
# import data from json
print "loading data"
fh=open('data_by_cookie.json')
data=json.load(fh)


# --------------------------------------------
# look at subsample of people who played more than ten times
print "taking subset"
big={}

for key in data:
	if len(data[key])>9:
		big[key]=data[key]


# -------------------------------------------
# for each individual, find maximum score over all attempts
#
# key attempt number [list]. In list:
# [0] is score
# [1] is day
# [2] is the hour

loading = 0

print "finding maxscores"

if not loading:
    maxscore={}
    maxattempt={}
    
    for key in big:
        maxscore[key]= max([big[key][attempt][0] for attempt in big[key]])
        maxattempt[key]=len([big[key][attempt] for attempt in big[key]])
    
    #save
    pickle.dump(maxscore, open('maxscore_save.p', 'wb'))
else:
    #load
     maxscore = pickle.load(open('maxscore_save.p', 'rb'))



# -----------------------------------------------
# sort maximum scores, smallest to biggest
ranked_maxscore=sorted(maxscore[key] for key in maxscore)

import scipy.stats.mstats as ssm

#----------------------------------------------
#now get percentiles for 0 - 99

print "finding percentiles for scores"

if not loading:
    prcentiles=[]
    for p in range(100):
        prcentiles.append(ssm.scoreatpercentile(ranked_maxscore,p))
    #and save
    pickle.dump(prcentiles, open('prcentiles_save.p', 'wb'))
else:
    prcentiles = pickle.load(open('prcentiles_save.p', 'rb'))


#graph this
print "graphing percentiles against max score values"

import matplotlib.pyplot as plt
from pylab import *
plt.clf()
plot(prcentiles,'.')
xlabel('percentile')
ylabel('maximum score required')
savefig('percentile_vs_score.png', dpi=None, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=False, bbox_inches=None, pad_inches=0.1)


#--------------------------------------------
# now collect number of attempts for people 
# according to their maxscore percentile
#
print "finding percentiles for number of attempts"

if not loading:
    #this is the dictionary where we'll collect the scores
    attempt_centiles={'%.5d'%(i+1):[] for i in range(100)}

    #this is the collection
    for key in big:
        for i in attempt_centiles:
            if int(i)<100:
                if maxscore[key]>=prcentiles[int(i)-1] and maxscore[key]<prcentiles[int(i)]:             
                    attempt_centiles[i].append(len(big[key]))
            else:
                if maxscore[key]>=prcentiles[int(i)-1]:             
                    attempt_centiles[i].append(len(big[key]))

    #save the bit that takes the longest time
    with open('att_data.json', 'wb') as fp:
        json.dump(attempt_centiles, fp)
else:
    ## to open   
    fh=open('att_data.json')
    attempt_centiles=json.load(fh)

#-----------------------------------------------
#now some statistics on those scores
centile_av={}
centile_length={}
centile_sterr={}        
for attempt in attempt_centiles:
    centile_av[attempt]=sum(attempt_centiles[attempt])/len(attempt_centiles[attempt])
    centile_sterr[attempt]=np.std(attempt_centiles[attempt])/sqrt(len(attempt_centiles[attempt]))
    centile_length[attempt]=len(attempt_centiles[attempt])

# get the data all at once, in order
pcentile, average_attempts = zip(*centile_av.items())
attempt_numbers,std_err=zip(*centile_sterr.items())
attempt_numbers,indiv_count=zip(*centile_length.items())

# convert the attempt numbers to integers
pcentile = [int(a) for a in pcentile]


print "graphing score percentiles against number of attempts average"

# now a graph
plt.clf()
errorbar(pcentile, average_attempts, yerr=std_err, fmt='ro')
xlabel('percentile')
ylabel('average number of attempts (with standard error)')
savefig('prcentile_vs_attempts.png', dpi=None, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=False, bbox_inches=None, pad_inches=0.1)

#n for each point ~ mean(indiv_count)

#------------------------------------------------
