#make Figure 2
#and some others

#required libraries
import numpy as np  # NumPy (multidimensional arrays, linear algebra, ...)
#from math import * #not needed if you're in spyder
from math import sqrt
import json
import pickle
#import matplotlib as mpl         # Matplotlib (2D/3D plotting library)
import matplotlib.pyplot as plt  # Matplotlib's pyplot: MATLAB-like syntax
#from pylab import *              # Matplotlib's pylab interface

generatepaperfigs=1 # toggle this to 1 to save figures in manuscript dir

# ------------------------------------------------
# import data from json
print "loading data"
fh=open('data_by_cookie.json')
data=json.load(fh)

#-------------------------------------------------
#FIRST - some rude characterisation
#-------------------------------------------------
#
#
print "organising data"
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

# save the data 
pickle.dump(attempt_number, open('save_a1_attempt_number.p', 'wb'))
pickle.dump(average_score, open('save_a1_average_score.p', 'wb'))



#---------------------------------------------------
#now we plot
#---------------------------------------------------
print "saving graphs"

# attempt number vs avg score 
plt.errorbar(attempt_number, average_score, yerr=std_err, fmt='ro')
plt.xlabel('attempt number')
plt.ylabel('average score')
plt.savefig('figure2.png', dpi=None, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=False, bbox_inches=None, pad_inches=0.1)


if generatepaperfigs:
    plt.savefig('../cogsci13/figures/avs.png', dpi=300, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=False, bbox_inches=None,savefig('../cogsci13/figures/a5_e-e_heatscatter.png', dpi=300, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=False, bbox_inches='tight', pad_inches=0.1)  pad_inches=0.1)
        
        
# attempt number vs record length
plt.clf()
plt.plot(attempt_number,attempt_count,'.')
plt.xlabel('attempt number')
plt.ylabel('plays')
plt.savefig('count.png', dpi=None, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=False, bbox_inches=None, pad_inches=0.1)
 
    
    