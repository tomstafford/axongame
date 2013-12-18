import json
from datetime import datetime, time, timedelta
from scipy import stats
from numpy import mean, std, sqrt
#import pylab as p
import matplotlib.pyplot as plt  # Matplotlib's pyplot: MATLAB-like syntax

# ------------------------------------------------
# import data from json
fh=open('data_by_cookie.json')
data=json.load(fh)

#-------------------------------------------------
#FORTH - look at patterns of practice timing

#-------------------------------------------------

# --------------------------------------------
# look at subsample of people who played more than x times

big = {k: data[k] for k in data if len(data[k]) > 14} #pythonic



#calv seperation in time between firstand last plays
spread={}
#assign players to two groups, accmean()mean()ording to spreadS
sleepers={}
wakers={}


for key in big:
    #find time between first plays and plays 9 or 10
    first=[]
    last=[]
    try:
        attempt='00001'
        first=datetime.combine(datetime.strptime(str(big[key][attempt][1]), '%Y%m%d'), time(big[key][attempt][2]))
    except KeyError:
        try:
            attempt='00002'
            first=datetime.combine(datetime.strptime(str(big[key][attempt][1]), '%Y%m%d'), time(big[key][attempt][2]))
        except KeyError:
            continue
        continue
    #            
    try:
        attempt='00010'
        last=datetime.combine(datetime.strptime(str(big[key][attempt][1]), '%Y%m%d'), time(big[key][attempt][2]))
    except KeyError:
        try:
            attempt='00009'
            last=datetime.combine(datetime.strptime(str(big[key][attempt][1]), '%Y%m%d'), time(big[key][attempt][2]))
        except KeyError:
            continue
        continue    
    #
    if first and last:
        spread[key]=last-first
        if first.day == last.day:
            wakers[key]=big[key] 
        else:
            sleepers[key]=big[key]
#    if spread[key]>plt.timedelta(hours=8):
#       if first.hour>20:
#           sleepers[key]=big[key]

#        
            
#find maximum score from attempts 11-15 for each key

attempts={'%.5d'%(i+1):[] for i in range(10,15)}

endmax={}

for key in big:
    try:
        endmax[key]= max([big[key][attempt][0] for attempt in attempts])            
    except KeyError:
        continue
    

rec=[]
for key in spread:
    try:
        rec.append([spread[key],endmax[key]])
    except KeyError:
        continue



p=[]
diff=[]  
mean_rester=[]
mean_goer=[]             

for h in range(24,25): #change this to get different cut off between resters and goers
    goers=[]
    resters=[]
    
    for key in big:
        try:
            if spread[key]>timedelta(hours=h):
                resters.append(endmax[key])
            else:
                goers.append(endmax[key])
        except KeyError:
            continue
    print 'H = %2.0f' % h
    print 't-statistic = %6.3f pvalue = %6.4f' % stats.ttest_ind(resters, goers)
    print "degrees of freedom = %i" % (len(resters)+len(goers)-2)    
    t,prob=stats.ttest_ind(resters, goers)
    
    poolstd=sqrt(0.5*(std(resters)**2 + std(goers)**2)) #pooled standard deviation
    effect_size=(mean(resters)-mean(goers))/poolstd #difference in means / std
    print "Cohen's d effect size = %2.2f" %effect_size
    
#    p.append(prob)
#    diff.append(mean(resters)-mean(goers))
#    print "Mean resters = %i, mean goers = %i" (int(mean(resters)), int(mean(goers)))
    #print "Std Err resters = %0.2f, std err goers = %0.2f" % (std(resters)/sqrt(len(resters)),std(goers)/sqrt(len(goers)))
    


fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.errorbar([1,2],[mean(goers), mean(resters)], yerr=[std(goers)/sqrt(len(goers)),std(resters)/sqrt(len(resters))], marker='o')
ax.set_xticks([1,2])
plt.xlim(0.7,2.3)
plt.ylim(40000,50000)
group_labels = ['\'goers\'','\'resters\'']
ax.set_xticklabels(group_labels)

plt.ylabel('average maximum score on plays 11-15')
plt.xlabel('players grouped according to delay between first and tenth play')
#size of benefit with extent of rest??


plt.savefig('figure5.png', dpi=None, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=False, bbox_inches=None, pad_inches=0.1)

generatepaperfigs=1
if generatepaperfigs:
    plt.savefig('../cogsci13/figures/resters_vs_goers.png', dpi=300, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=False, bbox_inches='tight', pad_inches=0.1) 

import pickle
pickle.dump(p, open('save_4b_p.p', 'wb'))
pickle.dump(diff, open('save_4b_diff.p', 'wb'))

#loading
#p= pickle.load(open('save_4b_p.p',     t=spreads_b/counts_b # find average'rb'))
#diff= pickle.load(open('save_4b_diff.p', 'rb'))


## run this if looking at a range of cut off points
#plt.figure(1)
#plt.plot(diff)
#plt.xlabel('divider between resters and goers')
#plt.ylabel('benefit of resting')
#               
#plt.savefig('spacing_benefit_of_resting.png', dpi=None, facecolor='w', edgecolor='w',
#        orientation='portrait', papertype=None, format=None,
#        transparent=False, bbox_inches=None, pad_inches=0.1)
        
