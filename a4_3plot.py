#modules----------------------------------------
import pickle
import scipy.stats.mstats as ssm
import numpy as np
import matplotlib as plt
from pylab import *

#first find actual data -------------------------
#execfile("a4_1timespread.py")

#second generate bootstrap data -----------------
#execfile("a4_2boot.py") #takes approx. 24 hours

#load 
#observed data
plot_timespread = pickle.load(open('save_plot_timespread.p', 'rb'))
#bootstrap data
bootdata = pickle.load(open('save_a4_2boot_bootdata.p','rb'))

#find CIs

#bootdata=np.random.rand( 100,20 )

#use ssm
ci_upper=np.zeros( (1,100))
ci_lower=np.zeros( (1,100))
m_boot=np.zeros( (1,100))
 
for i in range(100):
    ci_upper[0,i]=ssm.scoreatpercentile(bootdata[i,:],97.5)
    ci_lower[0,i]=ssm.scoreatpercentile(bootdata[i,:],02.5)
    m_boot[0,i]=np.mean(bootdata[i,:])


# plot -------------------------------------------
# thank you tomas http://www.staff.ncl.ac.uk/tom.holderness/software/pythonlinearfit
plt.clf()
    
# plot sample data
plot(plot_timespread,'ro',label='Sample observations')
 
# plot line of best fit
plot(m_boot[(0,)],'b-',label='bootstrap_mean')

# plot confidence limits
plot(ci_lower[(0,)],'b--',label='confidence limits (95%)')
plot(ci_upper[(0,)],'b--')

# configure legend
legend(loc=4) #lower left http://matplotlib.org/users/legend_guide.html
leg = gca().get_legend()
ltext = leg.get_texts()
setp(ltext, fontsize=10)

#plot_timespread = pickle.load(open('save_plot_timespread.p', 'rb'))

xlabel('maximum score percentile') 
ylabel('average gap between 1st and 10th plays/hours')

savefig('prcentile_vs_timespread.png', dpi=None, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=False, bbox_inches=None, pad_inches=0.1)

savefig('../cogsci13/figures/prcentile_vs_timespread.png', dpi=300, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=False, bbox_inches=None, pad_inches=0.1)       
        
        