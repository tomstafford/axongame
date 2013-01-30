#-------------------------------------------------
#FORTH - look at patterns of practice timing
#        and how the affect scoring
#-------------------------------------------------

#import modules
import json
import pickle
from datetime import datetime, date, time
#import datetime
import scipy.stats.mstats as ssm
import numpy as np
import random
from pylab import * #badness

#functions

def sample_wr(population, k):
    "Chooses k random elements (with replacement) from a population"
    "from http://code.activestate.com/recipes/273085-sample-with-replacement"
    n = len(population)
    _random, _int = random.random, int  # speed hack 
    result = [None] * k
    for i in xrange(k):
        j = _int(_random() * n)
        result[i] = population[j]
    return result


def timedelta_to_hours(td):
    x=td.seconds + td.days*24*60*60
    return x/60/60


# ------------------------------------------------
# import data from json
fh=open('data_by_cookie.json')
data=json.load(fh)


# --------------------------------------------
# look at subsample of people who played more than x times

##old way of doing this
#big={}
#
#for key in data:
#	if len(data[key])>10:
#		big[key]=data[key]
   
big = {k: data[k] for k in data if len(data[k]) > 9} #pythonic

#calc dict of maximum score for each player(=each key)
maxscore={}
    
for key in big:
    maxscore[key]= max([big[key][attempt][0] for attempt in big[key]])

# sort maximum scores, smallest to biggest
ranked_maxscore=sorted(maxscore[key] for key in maxscore)
        
#calc percentile ranking for each player (=each key)
prcentiles=[]
for p in range(100):
    prcentiles.append(ssm.scoreatpercentile(ranked_maxscore,p))

decile={}
    
for key in big:
    for i in prcentiles:
        if maxscore[key]>i:
            decile[key]=prcentiles.index(float(i))
    
#------------------------------------------------
# now calculate some index of spread
# - the simplest one is range

timespread={}

for key in big:
    last=max(datetime.datetime.combine(datetime.datetime.strptime(str(big[key][attempt][1]), '%Y%m%d'), time(big[key][attempt][2])) for attempt in big[key])
    first=min(datetime.datetime.combine(datetime.datetime.strptime(str(big[key][attempt][1]), '%Y%m%d'), time(big[key][attempt][2])) for attempt in big[key])
    timespread[key]=last-first

#now for each key weimport scipy.stats.mstats as ssm want to plot the value in decile against 
#the timespread value converted into hours

spreads=np.zeros( (100,1) ) #holding var for the time
counts=np.zeros( (100,1)) #holding var for the number of players' data

#sort timespread into holding variables according to decile value
for key in decile:
      spreads[decile[key]]+=timedelta_to_hours(timespread[key])
      counts[decile[key]]+=1
    
plot_timespread=spreads/counts    #now find average

pickle.dump(plot_timespread, open('save_plot_timespread.p', 'wb'))

plt.plot(timespread)
plt.xlabel('percentile') 
plt.ylabel('average score')

#now I have to normalise for amount of time spent playing

#1. bootstrap control, shuffling

#collect all scores
a=[]
for key in big:
    for attempt in big[key]:
        a.append(big[key][attempt][0])

#find maxscores, when actual scores are a sample [attempts] long of a
maxscore_boot={}
for key in big:
    maxscore_boot[key]=max(sample_wr(a,len(big[key])))
    
# sort maximum scores, smallest to biggest
ranked_maxscore_boot=sorted(maxscore_boot[key] for key in maxscore_boot)

#calculate percentiles on these bootstrapped maximum scores
prcentiles_boot=[]
for p in range(100):
    prcentiles_boot.append(ssm.scoreatpercentile(ranked_maxscore_boot,p))

#assign prcentile to key in decile_boot
decile_boot={}
  
for key in big:
    for i in prcentiles_boot:
        if maxscore_boot[key]>i:
            decile_boot[key]=prcentiles_boot.index(float(i))

#now calculate timespread to score percentile, using these
#bootstrapped maximum scores
spreads_b=np.zeros( (100,1) ) #holding var for the time
counts_b=np.zeros( (100,1)) #holding var for the number of players' data

#sort timespread into holding variables according to decile value
for key in decile_boot:
      spreads_b[decile_boot[key]]+=timedelta_to_hours(timespread[key])
      counts_b[decile_boot[key]]+=1
    
timespread_b=spreads_b/counts_b

plt.plot(timespread_b)
plt.savefig('prcentile_vs_timespread.png', dpi=None, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=False, bbox_inches=None, pad_inches=0.1)