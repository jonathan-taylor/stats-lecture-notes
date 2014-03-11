import pylab
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.path as path

# histogram our data with numpy

patchopt = {'facecolor':'blue',
           'alpha':0.8,
           'edgecolor':'gray'}

def PL_density(mass, binpoints, facecolor='red',
            alpha=0.8, edgecolor='gray', 
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
      fig = pylab.gcf()
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

