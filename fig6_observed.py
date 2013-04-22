#-------------------------------------------------
#FIFTH - look for evidence of exploration-exploitation
#        trade off 
#-------------------------------------------------

#import modules
import json
import pickle
import scipy.stats.mstats as ssm
import numpy as np
import random
import datetime
import bisect
from pylab import *
from scipy.stats.stats import pearsonr

# ------------------------------------------------
# import data from json
print "loading data"
fh=open('data_by_cookie.json')
data=json.load(fh)


# --------------------------------------------
# look at subsample of people who played more than x times   
print "organising data"
big = {k: data[k] for k in data if len(data[k]) > 9} #pythonic


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


#decile={}
#    
#for key in big:
#    for i in prcentiles:
#        if maxscore[key]>i:
#            decile[key]=prcentiles.index(float(i))

#so now we know how good each player is

#now let's calc variance

av1={}
var1={}
av2={}
var2={}

first_plays = ['%.5d'%(i+1) for i in range(5)]
second_plays = ['%.5d'%(i+6) for i in range(5)]

#construct vaiables dicts

print "calculating summary stats"
#for each player make two lists, of plays 1-5 (first) and 6-10 (second)
#and calculate summary stats av1,var1 and av2, var2
for key in big:
    first=[]
    for attempt in first_plays:
        try:
            first.append(big[key][attempt][0])
        except KeyError:
            continue
    av1[key]=mean(first)
    var1[key]=var(first)
    second=[]
    for attempt in second_plays:
        try:
            second.append(big[key][attempt][0])
        except KeyError:
            continue       
    av2[key]=mean(second) 
    var2[key]=var(second)


#make list of summary stats
x=[]
y=[]
for key in big:
    x.append(var2[key])
    y.append(av1[key])

#find percentile values
prcentiles_x=[]
for p in range(100):
    prcentiles_x.append(ssm.scoreatpercentile(x,p))

prcentiles_y=[]
for p in range(100):
    prcentiles_y.append(ssm.scoreatpercentile(y,p))


#make dict of prcentile values for each statistic for each player
prcentile_xindex={key: bisect.bisect(prcentiles_x,var2[key]) for key in big}
prcentile_yindex={key: bisect.bisect(prcentiles_y,av1[key]) for key in big}
       
print "saving data"        

#convert to list
xlist=[]
ylist=[]
for key in prcentile_xindex:
    xlist.append(prcentile_xindex[key])
    ylist.append(prcentile_yindex[key])

pickle.dump(xlist, open('save_a5_xlist.p', 'wb'))
pickle.dump(ylist, open('save_a5_ylist.p', 'wb'))
       
       
