#modules----------------------------------------
import random
import pickle
import json
import scipy as sp
import scipy.stats.mstats as ssm
from scipy.stats.stats import pearsonr
import bisect
import numpy as np

#functions-------------------------------------
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

# ------------------------------------------------
# import data from json
print "loading data"
fh=open('data_by_cookie.json')
data=json.load(fh)


# --------------------------------------------
# look at subsample of people who played more than x times   
print "organising data"
big = {k: data[k] for k in data if len(data[k]) > 9} #pythonic


#---------------------------------------------
# build records for bootstrap
print "organising bootstrap data"
attempts = ['%.5d'%(i+1) for i in range(10)]
bootdata={a:[] for a in attempts}

#collate
loading=0
if not loading:
    for key in big:
        for attempt in attempts:
            try:
                bootdata[attempt].append(big[key][attempt][0])
            except KeyError:
                continue
    
    pickle.dump(bootdata, open('save_a5_boot_bootdata.p', 'wb'))
else:
    bootdata = pickle.load(open('save_a5_boot_bootdata.p', 'rb'))

#now build boot sample, this will be iterated

boot_n=1000
bootrec=np.zeros( (1,boot_n) )

print "Starting bootstrap calculations"
for booti in range(boot_n):
    print "iteration " +str(booti) + " of " + str(boot_n)
    av1={}
    var1={}
    av2={}
    var2={}
    
    first_plays = ['%.5d'%(i+1) for i in range(5)]
    second_plays = ['%.5d'%(i+6) for i in range(5)]
    
    for key in big:
        first=[]
        for attempt in first_plays:
            first.append(sample_wr(bootdata[attempt],1))
        av1[key]=sp.mean(first)
        var1[key]=sp.var(first)
        second=[]
        for attempt in second_plays:
            second.append(sample_wr(bootdata[attempt],1))      
        av2[key]=sp.mean(second) 
        var2[key]=sp.var(second)
    
    
    #make list of summary stats
    x=[]
    y=[]
    for key in big:
        x.append(var1[key])
        y.append(av2[key])
    
    #find percentile values
    prcentiles_x=[]
    for p in range(100):
        prcentiles_x.append(ssm.scoreatpercentile(x,p))
    
    prcentiles_y=[]
    for p in range(100):
        prcentiles_y.append(ssm.scoreatpercentile(y,p))
    
    
    #make dict of prcentile values for each statistic for each player
    prcentile_xindex={key: bisect.bisect(prcentiles_x,var1[key]) for key in big}
    prcentile_yindex={key: bisect.bisect(prcentiles_y,av2[key]) for key in big}
           
#    #plot subset       
#    i=1001
#    for key in big:
#        i+=1
#        plot(prcentile_xindex[key],prcentile_yindex[key],'b.')
#        if i==2000:
#           break
    
    #pearson r correlation
    xlist=[]
    ylist=[]
    for key in prcentile_xindex:
        xlist.append(prcentile_xindex[key])
        ylist.append(prcentile_yindex[key])
        
    print "Boot %i" % booti 
    print "r = %.2f, p = %.2f" % pearsonr(xlist,ylist)

    a,b=pearsonr(xlist,ylist)
    bootrec[0,booti]=a


pickle.dump(bootrec, open('save_a5_boot_bootrec.p', 'wb'))