# ------------------------------------------------
# import data from json
import json
fh=open('data_by_cookie.json')
data=json.load(fh)

#-------------------------------------------------
#THIRD - analyse the top scorers compared to the rest

#-------------------------------------------------

#from previous analysis load...
import pickle
# ....maxscore
maxscore = pickle.load(open('maxscore_save.p', 'rb'))
#.....prcentiles
prcentiles = pickle.load(open('prcentiles_save.p', 'rb'))


# --------------------------------------------
# look at subsample of people who played more than ten times

big={}

for key in data:
	if len(data[key])>10:
		big[key]=data[key]


best={}
rest={}
for key in big:
    if maxscore[key]>prcentiles[99]:
       best[key]=big[key]
    else:
        rest[key]=big[key]

#this is the dictionary where we'll collect the scores
best_scores={'%.5d'%(i+1):[] for i in range(20)}
rest_scores={'%.5d'%(i+1):[] for i in range(20)}


for key in best:
    for attempts in best[key]:
        if int(attempts)<21:
            #print int(attempts)
            best_scores[attempts].append(best[key][attempts][0])

for key in rest:
    for attempts in rest[key]:
        if int(attempts)<21:
            #print int(attempts)
            rest_scores[attempts].append(rest[key][attempts][0])

        
best_av={}
best_length={}
best_sterr={}        
rest_av={}
rest_length={}
rest_sterr={}        

for attempt in best_scores:
    best_av[attempt]=sum(best_scores[attempt])/len(best_scores[attempt])
    best_sterr[attempt]=np.std(best_scores[attempt])/sqrt(len(best_scores[attempt]))
    best_length[attempt]=len(best_scores[attempt])


for attempt in rest_scores:
    rest_av[attempt]=sum(rest_scores[attempt])/len(rest_scores[attempt])
    rest_sterr[attempt]=np.std(rest_scores[attempt])/sqrt(len(rest_scores[attempt]))
    rest_length[attempt]=len(rest_scores[attempt])

# get the data all at once, in order
attempt_countb,best_average= zip(*best_av.items())
attempt_numbers,best_std_err=zip(*best_sterr.items())
attempt_numbers,best_count=zip(*best_length.items())

# get the data all at once, in order
attempt_countr,rest_average= zip(*rest_av.items())
attempt_numbers,rest_std_err=zip(*rest_sterr.items())
attempt_numbers,rest_count=zip(*rest_length.items())


# convert the attempt numbers to integers
attempt_countb= [int(a) for a in attempt_countb]
attempt_countr= [int(a) for a in attempt_countr]

# now a graph
plt.clf()
errorbar(attempt_count, best_average, yerr=best_std_err, fmt='ro')
errorbar(attempt_count, rest_average, yerr=rest_std_err, fmt='bo')

xlabel('attempt number')
ylabel('average score (with standard error)')
savefig('best_v_rest.png', dpi=None, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=False, bbox_inches=None, pad_inches=0.1)