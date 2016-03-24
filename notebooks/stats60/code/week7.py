import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import t as tdist

def studentT_curve(ax=None, linewidth=4, color='k', mean=0, SD=1, 
                   df=20,
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
   Y = tdist.pdf(Z, df) / SD
   ax.plot(X, Y, **plot_opts)
   ax.fill_between(X, 0*X, Y, alpha=alpha, facecolor=facecolor)
   if xlabel:
      ax.set_xlabel(xlabel, fontsize=20)
   if ylabel:
      ax.set_ylabel(ylabel, fontsize=20)
   ax.set_ylim([0,0.45/SD])
   ax.set_xlim([X.min(),X.max()])
   return ax
