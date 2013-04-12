#-------------------------------------------------
#FORTH - look at patterns of practice timing
#        and how the affect scoring
#-------------------------------------------------

#import modules
import json
import pickle
import scipy.stats.mstats as ssm
import numpy as np
import random
import datetime


def timedelta_to_hours(td):
    x=td.seconds + td.days*24*60*60
    return x/60/60


print "loading data"
# ------------------------------------------------
# import data from json
fh=open('data_by_cookie.json')
data=json.load(fh)

print "organising data"
# --------------------------------------------
# look at subsample of people who played more than x times   
big = {k: data[k] for k in data if len(data[k]) > 9} #pythonic

pickle.dump(big, open('save_a4_1_big.p', 'wb'))

# --------------------------------------------
#collect all attempt scores and save
a=[]
for key in big:
    for attempt in big[key]:
        a.append(big[key][attempt][0])
        
pickle.dump(a, open('save_a4_1_a.p', 'wb'))

# --------------------------------------------
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
    last=max(datetime.datetime.combine(datetime.datetime.strptime(str(big[key][attempt][1]), '%Y%m%d'), datetime.time(big[key][attempt][2])) for attempt in big[key])
    first=min(datetime.datetime.combine(datetime.datetime.strptime(str(big[key][attempt][1]), '%Y%m%d'), datetime.time(big[key][attempt][2])) for attempt in big[key])
    timespread[key]=timedelta_to_hours(last-first)


pickle.dump(timespread, open('save_a4_1_timespread.p', 'wb'))


#now for each key weimport scipy.stats.mstats as ssm want to plot the value in decile against 
#the timespread value converted into hours

spreads=np.zeros( (100,1) ) #holding var for the time
counts=np.zeros( (100,1)) #holding var for the number of players' data

#sort timespread into holding variables according to decile value
for key in decile:
      spreads[decile[key]]+=timespread[key]
      counts[decile[key]]+=1
    
plot_timespread=spreads/counts    #now find average

pickle.dump(plot_timespread, open('save_plot_timespread.p', 'wb'))
