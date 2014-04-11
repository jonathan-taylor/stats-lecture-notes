from matplotlib import pyplot as plt
import numpy as np, scipy.stats
ndist = scipy.stats.norm
import scipy.interpolate
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.path as path
from pylab import poly_between

try:
   import rpy2.robjects as rpy
   import rpy2.robjects.numpy2ri
except (ImportError, LookupError):
   rpy = None

# histogram our data with numpy

patchopt = {'facecolor':'blue',
           'alpha':0.8,
           'edgecolor':'gray'}

def PL_density(mass, binpoints, facecolor='red',
               alpha=0.8, edgecolor='black', 
               ax=None,
               **opts):
   """
   Form a density from observing masss in
   specific bins. This is different from 
   hist in that the bins are specified and not assumed
   equally spaced.

   The height of the bars is the mass within the bin
   divided by the length of bin.

   Parameters
   ----------

   mass : [float]
       Mass in each bin.

   binpoints : [float]
       End points of each bin. The first bin is `w=binpoints[1]-binpoints[0]`
       resulting in a bar of heighth `mass[0]/w`.

   facecolor : 
       Color for each bar.

   alpha : float
       Opacity for each bar.

   edgecolor : str
       Color for each bar.

   ax : `Axes`
       Optional axes to add the density estimate to.

   opts : {}
       Additional arguments passed to `patches.PathPatch`

   """

   if ax is None:
      fig = plt.gcf()
      ax = fig.add_subplot(111)

   opts['facecolor'] = facecolor
   opts['alpha'] = alpha
   opts['edgecolor'] = edgecolor

   mass = np.array(mass, np.float)
   n = mass.sum() / 100.

   # get the corners of the rectangles for the histogram
   diff = np.diff(binpoints)
   left = np.array(binpoints[:-1])
   right = np.array(binpoints[1:])
   bottom = np.zeros(len(left))
   top = bottom + mass / (n * diff)

   # we need a (numrects x numsides x 2) numpy array for the path helper
   # function to build a compound path

   XY = np.array([[left,left,right,right], [bottom,top,top,bottom]]).T

   # get the Path object
   barpath = path.Path.make_compound_path_from_polys(XY)

   # make a patch out of it
   patch = patches.PathPatch(barpath, **opts)
   ax.add_patch(patch)

   # update the view limits
   ax.set_xlim(left[0], right[-1])
   ax.set_ylim(bottom.min(), top.max())

   return ax

def sample_density(data_sample, bins=10, facecolor='#820000',
            alpha=0.8, edgecolor='black', 
            ax=None,
            regions=(),
            **opts):
   """
   Form a density from observing masss in
   specific bins. This is different from 
   hist in that the bins are specified and not assumed
   equally spaced.

   The height of the bars is the mass within the bin
   divided by the length of bin.

   Parameters
   ----------

   data_sample : [float]

   bins : [float] (optional)
       Bins passed to `matplotlib.hist`

   facecolor : 
       Color for each bar.

   alpha : float
       Opacity for each bar.

   edgecolor : str
       Color for each bar.

   ax : `Axes`
       Optional axes to add the density estimate to.

   opts : {}
       Additional arguments passed to `patches.PathPatch`

   regions : ()
       A sequence of (args,opts) pairs
       where `args` is a tuple of arguments for `np.linspace`
       and `opts` is a dict of keyword arguments to
       `pyplot.fill_between`. The space is filled between
       0 and the density estimate.

   Returns
   -------

   ax : `matplotlib.axes.Axes`

   density : callable
      A function to evaluate the piecewise constant density.
      Takes a single float argument

   area : callable
      A function to evaluate the area under piecewise constant density
      over an interval [a, b]. Takes two float arguments.

   """

   if ax is None:
      fig = plt.gcf()
      ax = fig.add_subplot(111)

   opts['facecolor'] = facecolor
   opts['alpha'] = alpha
   opts['edgecolor'] = edgecolor

   # try using R's binpoints
   if type(bins) == type(3) and rpy is not None: # is an integer
      rpy.r.assign('DS', data_sample)
      bins = np.array(rpy.r('pretty(range(DS), n=%d)' % bins))

   heights, binpts = ax.hist(data_sample, bins=bins, 
                             normed=True, **opts)[:2]
   ax.set_yticklabels(100*ax.get_yticks())
   heights = [0] + list(heights) + [0]

   binpts = [-np.inf] + list(binpts)
   density = scipy.interpolate.interp1d(binpts, 
                                        heights, kind='zero',
                                        bounds_error=False,
                                        fill_value=0)

   diff = density.x[1:] - density.x[:-1]
   diff = diff[1:]
   P = diff * density.y[1:-1]
   X = [-10**6] + list(density.x[1:]) + [10**6]
   Y = [0,0] + list(np.cumsum(P)) + [1.]
   CDF = scipy.interpolate.interp1d(X, Y, kind='linear',
                                     bounds_error=False)

   for args, opts in regions:
      interval = np.linspace(*args)
      ax.fill_between(interval, 0*interval, density(interval), **opts)
   return ax, density, CDF

def stylized_density(sample, ax=None, regions=[],
                     alpha=0.7, mult=None):
   regions = list(regions)
   SD = np.std(sample)
   sample = np.asarray(sample)

   if mult is not None:
      regions = list(regions)
      regions += [((np.mean(sample) - mult * np.std(sample), 
                    np.mean(sample) + mult * np.std(sample),
                    501), {'facecolor':'yellow', 'hatch':'/'})]

   dens = scipy.stats.gaussian_kde(sample)
   _min, _max = np.min(sample), np.max(sample)
   _range = _max - _min
   DX = np.linspace(_min - 0.1 * _range, _max + 0.1 * _range, 151)
   DY = dens(DX)

   if ax is None:
      fig = plt.gcf()
      ax = fig.add_subplot(111)

   ax.fill_between(DX,DY,0*DX, facecolor='gray', alpha=alpha)
   ax.plot(DX, DY, linewidth=4, c='k')
   ax.set_ylabel('Density (% per unit change)', fontsize=20)
   ax.set_xlabel('Units', fontsize=20)
   ax.set_xticks([])
   ax.set_yticks([])

   for args, opts in regions:
      interval = np.linspace(*args)
      ax.fill_between(interval, 0*interval, dens(interval), **opts)

   if mult is not None:
      standY = (sample - np.mean(sample)) / SD
      within = (np.fabs(standY) <= mult).sum() * 1. / sample.shape[0] * 100
      ax.set_title('Percentage within %0.1f SD: %d %%' % (mult, int(within)), fontsize=20, color='red')

   return ax

def SD_rule_of_thumb_normal(mult, ax=None, bins=30, regions=(), **opts):

   sample = (np.random.standard_normal(size=(5000,)) - 1) * 0.3 + 1 + np.random.uniform(size=(5000,)) * 2.
   if ax is None:
      fig = plt.gcf()
      ax = fig.add_subplot(111)
      
   ax, density, CDF = sample_density(sample, bins=bins, **opts)
   SD = np.std(sample)
   ax.annotate('Average', xy=(np.mean(sample), 0),
              arrowprops=dict(facecolor='black'), xytext=(np.mean(sample),-0.2),
              fontsize=20,
              horizontalalignment='center')

   interval = np.linspace(np.mean(sample) - mult * SD,
                          np.mean(sample) + mult * SD,
                          500)
   ax.fill_between(interval, 0*interval, density(interval), 
                   hatch='/',
                   facecolor='yellow')

   standY = (sample - np.mean(sample)) / SD
   within = (np.fabs(standY) <= mult).sum() * 1. / sample.shape[0] * 100
   ax.set_title('Percentage within %0.1f SD: %d %%' % (mult, int(within)), fontsize=20, color='red')
   ax.set_yticks([])
   ax.set_ylim([0,ax.get_ylim()[1]])
   return ax

def SD_rule_of_thumb_skewed(mult, ax=None, bins=30, regions=(), **opts):

   sample = np.random.exponential(size=15000) * 1.1 + np.random.uniform(size=15000) * 2.

   if ax is None:
      fig = plt.gcf()
      ax = fig.add_subplot(111)
      
   ax, density, CDF = sample_density(sample, bins=bins, **opts)
   SD = np.std(sample)
   ax.annotate('Average', xy=(np.mean(sample), 0),
              arrowprops=dict(facecolor='black'), xytext=(np.mean(sample),-0.1),
              fontsize=20,
              horizontalalignment='center')

   interval = np.linspace(np.mean(sample) - mult * SD,
                          np.mean(sample) + mult * SD,
                          500)
   ax.fill_between(interval, 0*interval, density(interval), 
                   hatch='/',
                   facecolor='yellow')

   standY = (sample - np.mean(sample)) / SD
   within = (np.fabs(standY) <= mult).sum() * 1. / sample.shape[0] * 100
   ax.set_title('Percentage within %0.1f SD: %d %%' % (mult, int(within)), fontsize=20, color='red')
   ax.set_yticks([])
   ax.set_xlim([-2,12])
   ax.set_ylim([0,ax.get_ylim()[1]])
   return ax

def normal_curve(ax=None, linewidth=4, color='k', **plot_opts):

   if ax is None:
      fig = plt.gcf()
      ax = fig.add_subplot(111)
   
   plot_opts['linewidth'] = linewidth
   plot_opts['color'] = color

   X = np.linspace(-4,4,101)
   Y = ndist.pdf(X)
   ax.plot(X, Y, **plot_opts)
   ax.fill_between(X, 0*X, Y, alpha=0.5, facecolor='gray')
   ax.set_xlabel('standardized units', fontsize=20)
   ax.set_ylabel('% per standardized unit', fontsize=20)
   ax.set_ylim([0,0.45])
   ax.set_xlim([-4,4])
   return ax

def standardize_interval(lower, upper, mean, SD, ax=None,
                         units='Units', 
                         standardized=False,
                         include_mean=False,
                         fontsize=15,
                         **fill_opts):
   if ax is None:
      fig = plt.gcf()
      ax = fig.add_subplot(111)

   xf, yf = poly_between([lower,mean,upper],[-0.05,-0.05,-0.05],[0.05,0.05,0.05])
   ax.fill(xf, yf, hatch='/', alpha=0.5, **fill_opts)
   ax.set_ylim([-0.4,0.3])
   ax.set_xlim([lower-0.55*SD,upper+0.3*SD])
   ax.set_xticks([lower,upper])
   ax.set_yticks([])
   ax.set_xticklabels(['',''])

   ax.text(lower - 0.4*SD, -0.2, units + ':', fontsize=fontsize)
   ax.text(lower, -0.3, lower, fontsize=fontsize, horizontalalignment='left')
   ax.text(upper, -0.3, upper, fontsize=fontsize, horizontalalignment='right')

   include_mean = include_mean or standardized
   if include_mean:
      ax.plot([mean, mean], [-0.1,0.1], 'k--', linewidth=4)

   if standardized:
      ax.set_ylim([-0.6,0.3])
      ax.text(lower-0.5*SD, -0.4, 'Standardized:', color='red', fontsize=fontsize)
      ax.text(lower, -0.5, '(%0.1f-%0.1f)/%0.1f=%0.2f' % (lower, mean, SD,
                                                          (lower-mean)/SD), fontsize=fontsize, horizontalalignment='left', color='red')
      ax.text(upper, -0.5, '(%0.1f-%0.1f)/%0.1f=%0.2f' % (upper, mean, SD,
                                                          (upper-mean)/SD), fontsize=fontsize, horizontalalignment='right', color='red')
   ax.set_title('Mean=%s, SD=%s' % (mean, SD), fontsize=20)
   return ax

def standardize_right(point, mean, SD, ax=None,
                      units='Units', 
                      standardized=False,
                      include_mean=False,
                      fontsize=15,
                      **fill_opts):
   '''
   Half-open interval to the right...
   '''
   if ax is None:
      fig = plt.gcf()
      ax = fig.add_subplot(111)

   lower = min(point, mean - 2*SD)
   upper = max(point, mean + 2*SD)

   xf, yf = poly_between([point,mean+1000*SD],[-0.05,-0.05],[0.05,0.05])
   ax.fill(xf, yf, hatch='/', alpha=0.5, **fill_opts)
   ax.set_ylim([-0.4,0.3])
   ax.set_xlim([lower-0.55*SD,upper+1.5*SD])
   ax.set_xticks([lower,upper])
   ax.set_yticks([])
   ax.set_xticklabels(['',''])

   ax.text(lower - 0.4*SD, -0.2, units + ':', fontsize=fontsize)
   ax.text(point, -0.3, point, fontsize=fontsize, horizontalalignment='left')

   if include_mean:
      ax.plot([mean, mean], [-0.1,0.1], 'k--', linewidth=4)

   if standardized:
      ax.set_ylim([-0.6,0.3])
      ax.text(lower-0.5*SD, -0.4, 'Standardized:', color='red', fontsize=fontsize)
      ax.text(point, -0.5, '(%0.1f-%0.1f)/%0.1f=%0.2f' % (point, mean, SD,
                                                          (point*1.-mean)/SD), fontsize=fontsize, horizontalalignment='right', color='red')
   ax.set_title('Mean=%s, SD=%s' % (mean, SD), fontsize=20)
   return ax

def standardize_left(point, mean, SD, ax=None,
                     units='Units', 
                     standardized=False,
                     include_mean=False,
                     fontsize=15,
                     **fill_opts):
   '''
   Half-open interval to the right...
   '''
   if ax is None:
      fig = plt.gcf()
      ax = fig.add_subplot(111)

   lower = min(point, mean - 2*SD)
   upper = max(point, mean + 2*SD)

   xf, yf = poly_between([mean-1000*SD,point],[-0.05,-0.05],[0.05,0.05])
   ax.fill(xf, yf, hatch='/', alpha=0.5, **fill_opts)
   ax.set_ylim([-0.4,0.3])
   ax.set_xlim([lower-0.55*SD,upper+1.5*SD])
   ax.set_xticks([lower,upper])
   ax.set_yticks([])
   ax.set_xticklabels(['',''])

   ax.text(lower - 0.4*SD, -0.2, units + ':', fontsize=fontsize)
   ax.text(point, -0.3, point, fontsize=fontsize, horizontalalignment='left')

   if include_mean:
      ax.plot([mean, mean], [-0.1,0.1], 'k--', linewidth=4)

   if standardized:
      ax.set_ylim([-0.6,0.3])
      ax.text(lower-0.5*SD, -0.4, 'Standardized:', color='red', fontsize=fontsize)
      ax.text(point, -0.5, '(%0.1f-%0.1f)/%0.1f=%0.2f' % (point, mean, SD,
                                                          (point*1.-mean)/SD), fontsize=fontsize, horizontalalignment='left', color='red')
   ax.set_title('Mean=%s, SD=%s' % (mean, SD), fontsize=20)
   return ax


def find_percentile(density, q):
    diff = density.x[1:] - density.x[:-1]
    diff = diff[1:]
    P = diff * density.y[1:-1]
    X = [-10**6] + list(density.x[1:]) + [10**6]
    Y = [0,0] + list(np.cumsum(P)) + [1.]
    CDF = scipy.interpolate.interp1d(X, Y, kind='linear',
                                     bounds_error=False)
    lower, upper = 0, 300
    niter = 0
    while True:
        mid = (lower + upper) / 2.
        if CDF(mid) > q:
            upper = mid
        else:
            lower = mid
        if niter >= 40:
            break
        niter += 1
    return mid

def percentile_figure(q, mean, SD, ax=None, 
                      standardized=False,
                      units='Units',
                      **fill_opts):

   ax = normal_curve(ax=ax)
   ax.set_yticks([])
   ax.set_ylabel('')
   ax.set_ylim([0,0.5])
   interval = np.linspace(-4, ndist.ppf(q), 101)
   ax.fill_between(interval, 0*interval, ndist.pdf(interval),
                   **fill_opts)
   if not standardized:
      ann_text = 'Percentile=%0.2f' % ndist.ppf(q)
   else:
      ann_text = 'Percentile=%0.2f' % (ndist.ppf(q) * SD + mean)

   if standardized:
      ax.set_xticklabels(mean+SD*ax.get_xticks())
      ax.set_xlabel(units)

   annotation = ax.annotate(ann_text, xy=(ndist.ppf(q),0),
                            xytext=(0,0.45), fontsize=20,
                            arrowprops=dict(facecolor='black'),
                            horizontalalignment='center')


