#-------------------------------------------------
# Try and predict score on play n 
#-------------------------------------------------

#import modules
import json
import scipy.stats.mstats as ssm
import scipy
import numpy as np
from pylab import * 
from scipy.stats.stats import pearsonr

import ols #download ols.0.2.py from http://www.scipy.org/Cookbook/OLS and rename ols.py


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


#now let's calc variance

av1={}
var1={}
av2={}
var2={}

score1={}
score2={}
score3={}
score4={}
score5={}
score10={}

first_plays = ['%.5d'%(i+1) for i in range(5)]
second_plays = ['%.5d'%(i+6) for i in range(5)]

#construct vaiables dicts

print "calculating summary stats"
#for each player make two lists, of plays 1-5 (first) and 6-10 (second)
#and calculate summary stats av1,var1 and av2, var2
for key in big:
    attempt=first_plays[0]
    try:
        score1[key]=big[key][attempt][0]
    except KeyError:
        score1[key]=NaN    
    attempt=first_plays[1]
    try:
        score2[key]=big[key][attempt][0]
    except KeyError:
        score2[key]=NaN       
    attempt=first_plays[2]
    try:
        score3[key]=big[key][attempt][0]
    except KeyError:
        score3[key]=NaN    
    attempt=first_plays[3]
    try:
        score4[key]=big[key][attempt][0]
    except KeyError:
        score4[key]=NaN       
    attempt=first_plays[4]
    try:
        score5[key]=big[key][attempt][0]
    except KeyError:
        score5[key]=NaN       
    attempt=second_plays[4]
    try:
        score10[key]=big[key][attempt][0]
    except KeyError:
        score10[key]=NaN    
    
    first=[]
    for attempt in first_plays:
        try:
            first.append(big[key][attempt][0])
        except KeyError:
            continue
    av1[key]=scipy.stats.nanmean(first)
    var1[key]=var(first)
    second=[]
    for attempt in second_plays:
        try:
            second.append(big[key][attempt][0])
        except KeyError:
            continue       
    av2[key]=scipy.stats.nanmean(second) 
    var2[key]=var(second)


#make list of summary stats
avs1=[]
vars1=[]
avs2=[]
vars2=[]
scores1=[]
scores2=[]
scores3=[]
scores4=[]
scores5=[]
scores10=[]

for key in big:
    avs1.append(av1[key])
    vars1.append(var1[key])
    avs2.append(av2[key])
    vars2.append(var2[key])
    scores1.append(score1[key])
    scores2.append(score2[key])
    scores3.append(score3[key])
    scores4.append(score4[key])
    scores5.append(score5[key])
    scores10.append(score10[key])
    
    
#make array
arravs1=np.array(avs1)
arravs2=np.array(avs2)
arrvars1=np.array(vars1)
arrvars2=np.array(vars2)
arrscores1=np.array(scores1)
arrscores2=np.array(scores2)
arrscores3=np.array(scores3)
arrscores4=np.array(scores4)
arrscores5=np.array(scores5)
arrscores10=np.array(scores10)

#mask according to nans in eitherof the paired variable arrays
#print "score 1 predicts average of 5-10"
#pearsonr((arrscores1[~isnan(arrscores1)&~isnan(arravs2)]),(arravs2[~isnan(arrscores1)&~isnan(arravs2)]))
#print "average of 1-5 predicts average of 5-10"
#pearsonr((arravs1[~isnan(arravs1)&~isnan(arravs2)]),(arravs2[~isnan(arravs1)&~isnan(arravs2)]))
#print "variance of 1-5 predicts average of 5-10"
#pearsonr((arrvars1[~isnan(arrvars1)&~isnan(arravs2)]),(arravs2[~isnan(arrvars1)&~isnan(arravs2)]))
#
#print "score 1 predicts score 10"
#pearsonr((arrscores1[~isnan(arrscores1)&~isnan(arrscores10)]),(arrscores10[~isnan(arrscores1)&~isnan(arrscores10)]))
#print "av 1-5 predicts score 10"
#pearsonr((arravs1[~isnan(arravs1)&~isnan(arrscores10)]),(arrscores10[~isnan(arravs1)&~isnan(arrscores10)]))
#print "var 1-5 predicts score 10"
#pearsonr((arrvars1[~isnan(arrvars1)&~isnan(arrscores10)]),(arrscores10[~isnan(arrvars1)&~isnan(arrscores10)]))

####### testing


#define mask to remove NaNs
#mask=~isnan(arravs2)&~isnan(arrscores1)&~isnan(arrscores2)&~isnan(arrscores3)&~isnan(arrscores4)&~isnan(arrscores5)&~isnan(arrvars1)
#mask=~isnan(arrscores10)&~isnan(arrscores1)&~isnan(arrscores2)&~isnan(arrscores3)&~isnan(arrscores4)&~isnan(arrscores5)&~isnan(arrvars1)
mask=~isnan(arrscores10)&~isnan(arravs1)&~isnan(arrvars1)

#convert variables for regression to z scores, so coefficients are beta weights

#predict average on scores 6-10....
#y=arravs2[mask] #better predictions for av6-10 than score 10
y=arrscores10[mask]
yz=(y-mean(y))/std(y)

#...using score 1
x1z=(arrscores2[mask]-mean(arrscores2[mask]))/std(arrscores2[mask])

#...using av1-5
x1z=(arravs1[mask]-mean(arravs1[mask]))/std(arravs1[mask])

#...and variance of scores 1-5
x2z=(arrvars1[mask]-mean(arrvars1[mask]))/std(arrvars1[mask])
xz=column_stack((x1z,x2z))

mymodel = ols.ols(yz,xz,'scores10',['avs1-5','var1to5'])
mymodel.summary()



