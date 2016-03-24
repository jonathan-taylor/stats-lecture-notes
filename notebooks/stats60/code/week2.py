import numpy as np
import matplotlib.pyplot as plt
from matplotlib.mlab import csv2rec
from pylab import poly_between
import os.path

class pearson_lee(object):

    marker_color = 'red'
    strip_color = 'gray'
    marker_size = 100

    def __init__(self, strip=None):
        absdir = os.path.dirname(os.path.abspath(__file__))
        self.data = csv2rec(os.path.join(absdir, '..', 'data', 'pearson_lee.csv'))
        self.M = self.data['mother']
        self.D = self.data['daughter']

        self.strip = strip
        
    def draw(self):
        self.figure.clf()
        self.axes.scatter(self.M, self.D, c=self.marker_color,
                          s=self.marker_size,
                          edgecolor='gray')
        self.axes.set_xlabel("Mother's height (inches)", fontsize=15)
        self.axes.set_ylabel("Daughter's height (inches)", fontsize=15)
        if self.strip is not None:
            s = self.strip
            xf, yf = poly_between([s-.5,s+.5], [50,50], [75, 75])
            self.axes.fill(xf, yf, facecolor=self.strip_color, alpha=0.4, hatch='/')

    @property
    def figure(self):
        if not hasattr(self, "_figure"):
            self._figure = plt.figure()
        self._axes = self._figure.gca()
        return self._figure
    
    @property
    def axes(self):
        self.figure
        return self._axes

    def set_strip(self, strip):
        self._strip = strip

    def get_strip(self):
        return self._strip

    strip = property(get_strip, set_strip)

    @property
    def mean_strip(self):
        if self.strip is not None:
            s = self.strip
            V = (self.M >= s - 0.5) * (self.M <= s + 0.5)
            return self.D[V].mean()

    def SDline(self, draw=True):
        if draw:
            self.draw()
        xlim, ylim = self.axes.get_xlim(), self.axes.get_ylim()
        Dbar = self.D.mean()
        Dsd = self.D.std()
        Mbar = self.M.mean()
        Msd = self.M.std()
        self.axes.plot([Mbar-3.5*Msd,Mbar,Mbar+3.5*Msd],
                       [Dbar-3.5*Dsd,Dbar,Dbar+3.5*Dsd], 'b--', linewidth=5, label='SD line')
        self.axes.legend()
        self.axes.set_xlim(xlim)
        self.axes.set_ylim(ylim)

    def regline(self, draw=True, label='Regression line'):
        '''
        Regression line
        '''
        if draw:
            self.draw()
        xlim, ylim = self.axes.get_xlim(), self.axes.get_ylim()
        Dbar = self.D.mean()
        Dsd = self.D.std()
        Mbar = self.M.mean()
        Msd = self.M.std()
        r = np.corrcoef([self.M, self.D])[0,1]
        self.axes.plot([Mbar-3.5*Msd,Mbar,Mbar+3.5*Msd],
                       [Dbar-r*3.5*Dsd,Dbar,Dbar+r*3.5*Dsd], 'k--', linewidth=5, label=label)
        self.axes.legend()
        self.axes.set_xlim(xlim)
        self.axes.set_ylim(ylim)

    def invregline(self, draw=True, label='Regression line',
                   linestyle='--',
                   color='yellow'):
        '''
        Regression line
        '''
        if draw:
            self.draw()
        xlim, ylim = self.axes.get_xlim(), self.axes.get_ylim()
        Dbar = self.D.mean()
        Dsd = self.D.std()
        Mbar = self.M.mean()
        Msd = self.M.std()
        r = np.corrcoef([self.M, self.D])[0,1]
        self.axes.plot([Mbar-r*5*Msd,Mbar,Mbar+r*5*Msd],
                       [Dbar-5*Dsd,Dbar,Dbar+5*Dsd], 
                       linestyle=linestyle,
                       color=color, linewidth=5, label=label)
        self.axes.legend()
        self.axes.set_xlim(xlim)
        self.axes.set_ylim(ylim)

