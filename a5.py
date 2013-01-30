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
fh=open('data_by_cookie.json')
data=json.load(fh)


# --------------------------------------------
# look at subsample of people who played more than x times   
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
       
#plot subset       
i=1001
for key in big:
    i+=1
    plot(prcentile_xindex[key],prcentile_yindex[key],'b.')
    if i==2000:
       break

#pearson r correlation
xlist=[]
ylist=[]
for key in prcentile_xindex:
    xlist.append(prcentile_xindex[key])
    ylist.append(prcentile_yindex[key])



xlabel('variation in first five plays')
ylabel('average in second five plays')
title("r = %.2f, p = %.2f" % pearsonr(xlist,ylist))

savefig('a5_var1av2.png', dpi=None, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=False, bbox_inches=None, pad_inches=0.1) 
        
        
pickle.dump(xlist, open('save_a5_xlist.p', 'wb'))
pickle.dump(ylist, open('save_a5_ylist.p', 'wb'))

#recreate nontriviality result - using bootstrap, as with a4 (?) 
#replicate with number of wipe outs

#not this
newylist=ylist
random.shuffle(newylist)
print("r = %.2f, p = %.2f" % pearsonr(xlist,newylist))
