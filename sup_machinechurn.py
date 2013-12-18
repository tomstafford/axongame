#make Figure 3

import json
import bisect
import pylab as pb
import scipy.stats as stats
import numpy as np
import pickle
import matplotlib.pyplot as plt  # Matplotlib's pyplot: MATLAB-like syntax

print "loading data"
data = json.load(open('data_by_cookie.json'))

# basics
print "organising data"
players = data.keys()
num_attempts = [len(data[player]) for player in players]
attempt_numbers = [sorted(data[player].keys()) for player in players]
scores = [[data[player][attempt][0] for attempt in attempt_number] for attempt_number, player in zip(attempt_numbers, players)]

maxscore_method=1

if maxscore_method:
    #this defines max score as max on any play
    maxscores = pb.array([max(score) for score in scores]) 
else:
    #this defines max score as max on 20th play
    maxscores_notarray=[]
    for score in scores:
    	if len(score)>19:
    		maxscores_notarray.append(score[19])
    	else:
    		maxscores_notarray.append(0)
    maxscores = pb.array(maxscores_notarray)

#rows: players
# columns: attempts
sum_longplays=pb.zeros((max(num_attempts),1))
n_longplays=pb.zeros((max(num_attempts),1))
for i,attempts in enumerate(scores):
    for j,score in enumerate(attempts):
        sum_longplays[j]+=score
        n_longplays[j]+=1
        
        
print "making graph"
plt.plot(sum_longplays/n_longplays,label='all players') #shows that for very long players, they are not necessarily learning (and so should be excluded)
plt.plot(sum_longplays[:200]/n_longplays[:200],label='first 200 attempts') #shows that smooth learning continues up to attempt 200
plt.xlabel('Attempt number')
plt.ylabel('Average score')
plt.title('beyond 200 plays, relation between attempt and score breaks down', fontsize=14)
plt.savefig('longplays.png', dpi=300, facecolor='w', edgecolor='w',
            orientation='portrait', papertype=None, format=None,
            transparent=False, bbox_inches=None, pad_inches=0.1)

print "done!"            