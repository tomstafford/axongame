import pickle
from scipy.stats.stats import pearsonr
import scipy.stats.mstats as ssm
import matplotlib.pyplot as plt
from pylab import * #i know I shouldn't do this
from matplotlib import cm


#import x and y data for each key (as two dicts)
prcentile_xindex = pickle.load(open('save_a5_prcentile_xindex.p', 'rb'))
prcentile_yindex = pickle.load(open('save_a5_prcentile_yindex.p', 'rb'))

#put data in two lists, so I can plot and correlate it
# (there must be a better way, but I don't know it)
xlist=[]
ylist=[]
for key in prcentile_xindex:
    xlist.append(prcentile_xindex[key])
    ylist.append(prcentile_yindex[key])

##simple scatter plot is pretty uninformative
#plt.scatter(xlist,ylist)
#
#xlabel('variation in first five plays')
#ylabel('average in second five plays')
#title("r = %.2f, p = %.2f" % pearsonr(xlist,ylist))
#
#savefig('visprob_plot.png', dpi=None, facecolor='w', edgecolor='w',
#        orientation='portrait', papertype=None, format=None,
#        transparent=False, bbox_inches=None, pad_inches=0.1) 
        
        
#solution attempt 2
plt.clf()
gridsize=20
plt.hexbin(xlist, ylist,gridsize=gridsize, cmap=cm.jet, bins=None)
cb = plt.colorbar()
cb.set_label('frequency')

xlabel('percentile by variation in first five plays')
ylabel('percentile by average in second five plays')
print "r = %.3f, p = %.5f" % pearsonr(xlist,ylist)

savefig('../cogsci13/figures/a5_e-e_heatscatter.png', dpi=300, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=False, bbox_inches='tight', pad_inches=0.1) 
        
#now do CI for r value

bootrec=pickle.load(open('save_a5_boot_bootrec.p', 'rb'))
bootrec=bootrec[0]
ci_upper=ssm.scoreatpercentile(bootrec,97.5)
ci_lower=ssm.scoreatpercentile(bootrec,02.5)
ci_mean=np.mean(bootrec)
print "Bootstrapped confidence intervals were Upper = %0.3f, Lower = %0.3f" % (ci_upper,ci_lower)