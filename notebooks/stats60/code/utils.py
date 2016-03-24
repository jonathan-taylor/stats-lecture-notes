import numpy as np
import scipy.interpolate
import matplotlib.pyplot as plt
IP = get_ipython()
IP.magic('load_ext rpy2.ipython')

def sample_density(data_sample, 
                   bins=10, 
                   facecolor='#820000',
                   alpha=0.8, 
                   edgecolor='black', 
                   ax=None,
                   regions=(),
                   **opts):
   """
   Form a density from observing mass in
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

   data_sample = np.asarray(data_sample)

   # try using R's binpoints
   if type(bins) == type(3): # is an integer
      IP.magic("R -i data_sample,bins")
      bins = IP.magic("R pretty(range(data_sample), bins)")

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

def probability_histogram(sampler, facecolor='#820000',
                          alpha=0.8, edgecolor='black', 
                          ax=None,
                          ndraws=None,
                          bins=None,
                          xlabel='',
                          ylabel='',
                          draw_color='orange',
                          width=1,
                          **opts):
   vals = np.array(sorted(sampler.mass_function.keys()))
   mass = np.array([sampler.mass_function[z] for z in vals])
   k = (mass >= 1e-3*mass.max())

   if ax is None:
      fig = plt.gcf()
      ax = fig.add_subplot(111)

   ax.bar(vals[k],mass[k]/width, width=width, align='center', alpha=alpha,
          facecolor=facecolor, label='Probability histogram')
   ax.set_yticklabels(100*ax.get_yticks())
   ax.set_ylim([0, 1.2 * mass.max()/width])
   dx = vals.max() - vals.min()

   avg = np.sum([k*p for k, p in sampler.mass_function.items()])
   second_moment = np.sum([k**2*p for k, p in sampler.mass_function.items()])
   sd = np.sqrt(second_moment - avg**2)

   ax.set_xlim([avg-3*sd,avg+3*sd])
   if xlabel:
      ax.set_xlabel(xlabel, fontsize=15)
   if ylabel:
      ax.set_ylabel(ylabel, fontsize=15)

   if ndraws is not None:
      draws = sampler.sample(ndraws)
      sample_density(draws, alpha=0.5, bins=bins, ax=ax,
                     label='Sample (n=%d)' % ndraws, facecolor=draw_color)
      
   return ax, avg, sd
