import json
import pickle

# ------------------------------------------------
# import data from json
fh=open('data_by_cookie.json')
data=json.load(fh)

#-------------------------------------------------
#FIRST - some rude characterisation
#-------------------------------------------------
#
#
#1. Attempt number by average score
#
#collect scores for each attempt number
#
# make holding variable, a dictionary with keys 00001....00030
avg_score = {'%.5d'%(i+1):[] for i in range(100)}

## here is the verbose way of doing the above
#for i in range(10):
#	attempt=str(i+1)
#	avg_score[attempt] = []

#now look through dictionary, and extract score for each attempt number
#for which there is a position in the avg_score variable
for cookie in data:
	for attempt in avg_score:
		try:
			score = data[cookie][attempt][0]
		except KeyError:
			continue
           #if there is a score for that attempt, add it to the record
		avg_score[attempt].append(score)

    
#-------------------------------------------------
# now calculate some statistics by attempt number
#
# holding vars
avg={} #average
sterr={} #standard error
countp={} #count

#required libraries
import numpy as np  # NumPy (multidimensional arrays, linear algebra, ...)
from math import * #not needed if you're in spyder

for attempt in avg_score:
    avg[attempt]=sum(avg_score[attempt])/len(avg_score[attempt])
    sterr[attempt]=np.std(avg_score[attempt])/sqrt(len(avg_score[attempt]))
    countp[attempt]=len(avg_score[attempt])

#but the result is a dict, so we need to unpack to plot

# -------------method 1 -------------
#    
## this gets the keys of your dictionary
#attempt_number = avg.keys()
## this gets the score in the same order as the keys for plotting
#average_score = [avg[k] for k in attempt_number]
## this converts each key to an int
#attempt_number = [int(a) for a in attempt_number]
## then you can plot!
#plot(attempt_number, average_score,'.')

#------------ method 2 -------------
#There's a quicker way, and uses more python magic:

# get the data all at once, in order
attempt_number, average_score = zip(*avg.items())
attempt_numbers,std_err=zip(*sterr.items())
attempt_numbers,attempt_count=zip(*countp.items())

# convert the attempt numbers to integers
attempt_number = [int(a) for a in attempt_number]

pickle.dump(attempt_number, open('save_a1_attempt_number.p', 'wb'))
pickle.dump(average_score, open('save_a1_average_score.p', 'wb'))



#---------------------------------------------------
#now we plot
#---------------------------------------------------
import matplotlib as mpl         # Matplotlib (2D/3D plotting library)
import matplotlib.pyplot as plt  # Matplotlib's pyplot: MATLAB-like syntax
from pylab import *              # Matplotlib's pylab interface


# attempt number vs avg score 
errorbar(attempt_number, average_score, yerr=std_err, fmt='ro')
xlabel('attempt number')
ylabel('average score')
savefig('avs.png', dpi=None, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=False, bbox_inches=None, pad_inches=0.1)

savefig('../cogsci13/figures/avs.png', dpi=300, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=False, bbox_inches=None, pad_inches=0.1)
        
        
# attempt number vs record length
plt.clf()
plot(attempt_number,attempt_count,'.')
xlabel('attempt number')
ylabel('plays')
savefig('count.png', dpi=None, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=False, bbox_inches=None, pad_inches=0.1)
# .... this needs some explaining.....    
    
    