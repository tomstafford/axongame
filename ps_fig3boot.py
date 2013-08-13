#bootstrap h0 for timespread against percentiles

#modules----------------------------------------
import random
import pickle
import scipy.stats.mstats as ssm
import numpy as np
import bisect

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


#first find actual data -------------------------
#execfile("fig4_observed.py")

print "Loading"
#load scores for bootstrap
big = pickle.load(open('save_a4_1_big.p', 'rb'))
a = pickle.load(open('save_a4_1_a.p', 'rb'))
timespread = pickle.load(open('save_a4_1_timespread.p', 'rb'))

#-------------------------------------------
#build loop out of everything after this


boot_n=2000 #define how many resamples the bootstrap uses 
bootdata=np.zeros( (100,boot_n) )

print "Starting bootstrap calculations"
for n in range(boot_n):
    
    print "iteration " +str(n) + " of " + str(boot_n)
    #find maxscores, when actual scores are a sample [attempts] long of a
    #maxscore_boot={key: max(random.sample(a,len(big[key]))) for key in big}
    maxscore_boot={key: max(sample_wr(a,len(big[key]))) for key in big}
    
    # sort maximum scores, smallest to biggest, put in list
    ranked_maxscore_boot=sorted(maxscore_boot[key] for key in maxscore_boot)
    
    #calculate percentiles on these bootstrapped maximum scores
    prcentiles_boot=[ssm.scoreatpercentile(ranked_maxscore_boot,p) for p in range(100)]
        
    #assign prcentile to key in decile_boot
    decile_boot={key: bisect.bisect(prcentiles_boot,maxscore_boot[key]) for key in big}
    
    #now calculate timespread to score percentile, using these
    #bootstrapped maximum scores
    spreads_b=np.zeros( (100,1) ) #holding var for the time
    counts_b=np.zeros( (100,1)) #holding var for the number of players' data
    
    #sort timespread into holding variables according to decile value
    for key in decile_boot:
          spreads_b[decile_boot[key]-1]+=timespread[key]
          counts_b[decile_boot[key]-1]+=1
        
    t=spreads_b/counts_b # find average
    bootdata[:,n]=t.reshape(1,100)
    
    #pickle.dump(timespread_b, open('save_timespread_b.p', 'wb'))
    

print "Saving bootstrap data"
pickle.dump(bootdata, open('save_a4_2boot_bootdata.p', 'wb'))


