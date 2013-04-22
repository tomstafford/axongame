import pickle
from scipy.stats.stats import pearsonr
import scipy.stats.mstats as ssm
import matplotlib.pyplot as plt
from pylab import * #i know I shouldn't do this
from matplotlib import cm


print "OBSERVED DATA"
execfile("fig6_observed.py")

print "BOOTSTRAP"
execfile("fig6_boot.py")

print "PLOTTING"

xlist= pickle.load(open('save_a5_xlist.p', 'rb'))
ylist= pickle.load(open('save_a5_ylist.p', 'rb'))


##simple scatter plot is pretty uninformative
#plt.scatter(xlist,ylist)

##So you can plot subsection of data
#print "plotting subset of data in scatterplot"
#i=1001
#for key in big:
#    i+=1
#    plot(prcentile_xindex[key],prcentile_yindex[key],'b.')
#    if i==2000:
#       break
#
#xlabel('variation in first five plays')
#ylabel('average in second five plays')
#title("Subset of total data set, for visualisation r = %.2f, p = %.2f" % pearsonr(xlist,ylist))
#
#savefig('a5_var1av2.png', dpi=None, facecolor='w', edgecolor='w',
#        orientation='portrait', papertype=None, format=None,
#        transparent=False, bbox_inches=None, pad_inches=0.1) 

        
#solution attempt 2 - heatmap
plt.clf()
gridsize=20
plt.hexbin(xlist, ylist,gridsize=gridsize, cmap=cm.jet, bins=None)
cb = plt.colorbar()
cb.set_label('frequency')

xlabel('percentile by variation in first five plays')
ylabel('percentile by average in second five plays')
print "r = %.3f, p = %.5f" % pearsonr(xlist,ylist)

savefig('Figure6.png', dpi=300, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=False, bbox_inches='tight', pad_inches=0.1) 

generatepaperfigs=0
if generatepaperfigs:
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