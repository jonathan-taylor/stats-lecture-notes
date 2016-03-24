import numpy as np
import scipy.stats
import matplotlib.pylab as plt
from pylab import poly_between

ndist = scipy.stats.norm

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

def standardize_interval(lower, upper, mean, SD, ax=None,
                         data=True,
                         units='Units',
                         standardized=False,
                         include_mean=False,
                         fontsize=15,
                         **fill_opts):
   from pylab import poly_between

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
                                                          (lower-mean)/SD), 
                                                          fontsize=fontsize, 
                                                          horizontalalignment='left', 
                                                          color='red')
      ax.text(upper, -0.5, '(%0.1f-%0.1f)/%0.1f=%0.2f' % (upper, mean, SD,
                                                          (upper-mean)/SD), 
                                                          fontsize=fontsize, 
                                                          horizontalalignment='right', 
                                                          color='red')
   if data:
      ax.set_title('Mean=%0.1f, SD=%0.1f' % (mean, SD), fontsize=20)
   else:
      ax.set_title('Mean=%0.1f, SE=%0.1f' % (mean, SD), fontsize=20)
   return ax

def standardize_interval(lower, upper, mean, SD, ax=None,
                         data=True,
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
   if data:
      ax.set_title('Mean=%0.1f, SD=%0.1f' % (mean, SD), fontsize=20)
   else:
      ax.set_title('Mean=%0.1f, SE=%0.1f' % (mean, SD), fontsize=20)
   return ax

def standardize_right(point, mean, SD, ax=None,
                      data=True,
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
   if data:
      ax.set_title('Mean=%0.1f, SD=%0.1f' % (mean, SD), fontsize=20)
   else:
      ax.set_title('Mean=%0.1f, SE=%0.1f' % (mean, SD), fontsize=20)
   return ax

def standardize_left(point, mean, SD, ax=None,
                     data=True,
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
   if data:
      ax.set_title('Mean=%0.1f, SD=%0.1f' % (mean, SD), fontsize=20)
   else:
      ax.set_title('Mean=%0.1f, SE=%0.1f' % (mean, SD), fontsize=20)
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

def normal_curve(ax=None, linewidth=4, color='k', mean=0, SD=1,
                 facecolor='gray',
                 xlabel='standardized units',
                 ylabel='% per standardized unit',
                 alpha=0.5,
                 **plot_opts):

   if ax is None:
      fig = plt.gcf()
      ax = fig.add_subplot(111)

   plot_opts['linewidth'] = linewidth
   plot_opts['color'] = color

   Z = np.linspace(-4,4,101)
   X = mean+SD*Z
   Y = ndist.pdf(Z) / SD
   ax.plot(X, Y, **plot_opts)
   ax.fill_between(X, 0*X, Y, alpha=alpha, facecolor=facecolor)
   if xlabel:
      ax.set_xlabel(xlabel, fontsize=20)
   if ylabel:
      ax.set_ylabel(ylabel, fontsize=20)
   ax.set_ylim([0,0.45/SD])
   ax.set_xlim([X.min(),X.max()])
   return ax

def CAdensity(figsize=(8,8)):
    bins = [0,20,55,75,100]
    count = [29,52,13,6]
    hist_fig = plt.figure(figsize=figsize)
    data = np.array([10]*29 + [30]*52 + [60]*13 + [80.]*6)
    hist_plot, dens, CDF = sample_density(data, bins=bins, alpha=0.5, ax=hist_fig.gca(),
                            facecolor='gray')
    hist_plot.set_ylabel('Percentage per year (%/year)', fontsize=20)
    hist_plot.set_xlabel('Age (years)', fontsize=20)
    hist_plot.set_title('California population by age groups', fontsize=22)
    def area(a, b):
        return np.round(100*(CDF(b) - CDF(a)), 1)
    return hist_fig, dens, area
