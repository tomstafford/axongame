#modules----------------------------------------
import pickle
import scipy.stats.mstats as ssm
import numpy as np
import matplotlib as plt
from pylab import *
import scipy.stats

loading=1

if not loading:
    #first find actual data -------------------------
    print "OBSERVED DATA (fig4_observed.py)"
    execfile("ps_fig3obs.py")

    #second generate bootstrap data -----------------
    print "BOOTSTRAP CONFIDENCE LIMITS"
    execfile("ps_fig3boot.py") #this can take a long time (e.g. 24 hours) if you use many (e.g. 2000) resamples
else:
    print "LOADING DATA"
    #load 
    #observed data
    plot_timespread = pickle.load(open('save_plot_timespread.p', 'rb'))
    #bootstrap data
    bootdata = pickle.load(open('save_a4_2boot_bootdata.p','rb'))


print "finding CIs"

#find CIs, using ssm

ci_upper=np.zeros( (1,100))
ci_lower=np.zeros( (1,100))
m_boot=np.zeros( (1,100))
 
for i in range(100):
    ci_upper[0,i]=ssm.scoreatpercentile(bootdata[i,:],97.5)
    ci_lower[0,i]=ssm.scoreatpercentile(bootdata[i,:],02.5)
    m_boot[0,i]=np.mean(bootdata[i,:])

print "running t-test"

#make the same shape
expt=a=np.reshape(m_boot[(0,)],100) #expected values (from bootstrap, ie under H0)
obsv=a=np.reshape(plot_timespread,100) #observed values

#recode so that a positive difference supports the theory (ie that spacing helps)
#for the bottom 50% this means their observed is lower than expected
#for the top 50% this means their obseved is higher than expected
diffs=np.concatenate([expt[0:50]-obsv[0:50],obsv[50:100]-expt[50:100]])

print "mean difference in difference from zero (+ve means more spacing among higher scorers, less among low)= %6.2f" % mean(diffs)
print 't-statistic = %6.3f pvalue = %6.4f' %  scipy.stats.ttest_1samp(diffs,0)

print "PLOTTING"

# plot -------------------------------------------
# thank you tomas http://www.staff.ncl.ac.uk/tom.holderness/software/pythonlinearfit
plt.clf()
    
# plot sample data
plot(plot_timespread,'ro',label='sample means')
 
# plot line of best fit
plot(m_boot[(0,)],'b-',label='bootstrap mean')

# plot confidence limits
plot(ci_lower[(0,)],'b--',label='confidence limits (95%)')
plot(ci_upper[(0,)],'b--')

# configure legend
legend(loc=4) #lower left http://matplotlib.org/users/legend_guide.html
leg = gca().get_legend()
ltext = leg.get_texts()
setp(ltext, fontsize=10)

xlabel('percentile according to maximum score') 
ylabel('average gap between first and last plays/hours')

savefig('StaffordFig3.png', dpi=None, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=False, bbox_inches=None, pad_inches=0.1)

generatepaperfigs=1
if generatepaperfigs:
    savefig('../psychscience/StaffordFig3.png', dpi=300, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=False, bbox_inches=None, pad_inches=0.1)       

print "done!"        
        