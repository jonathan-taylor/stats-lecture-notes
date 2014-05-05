from base64 import encodestring
from itertools import product
import matplotlib.pyplot as plt
import numpy as np
from IPython.core.display import HTML

from probability import BoxModel,ProbabilitySpace

class Sample(ProbabilitySpace):

    figsize = (5.5, 5.5)
    alpha = 0.3
    ptsize = 5
    sample_ptsize = 60

    def __init__(self, nblue, nred, ndraw, draw_fig=True):
        self.nblue, self.nred, self.ndraw = nblue, nred, ndraw
        self.box = BoxModel(['B']*nblue + ['R']*nred, replace=False)
        self.X = np.random.sample((nblue+nred, 2))
        self.draw_fig = draw_fig
        if draw_fig:
            self.draw()

    def draw(self, color={'R':'red','B':'blue'}):
        self.figure.clf()
        ax, X = self.axes, self.X
        ax.scatter(X[:self.nblue,0], X[:self.nblue,1], s=self.ptsize, color=color['B'], alpha=self.alpha)            
        ax.scatter(X[self.nblue:,0], X[self.nblue:,1], s=self.ptsize, color=color['R'], alpha=self.alpha)            
        ax.set_xticks([]);    ax.set_xlim([-0.01,1.01])            
        ax.set_yticks([]);    ax.set_ylim([-0.01,1.01])       

    @property
    def figure(self):
        if not hasattr(self, "_figure"):
            self._figure = plt.figure(figsize=self.figsize)
        self._axes = self._figure.gca()
        return self._figure
    
    @property
    def axes(self):
        self.figure
        return self._axes

    def draw_sample_pts(self, bgcolor={'R':'red','B':'blue'},
                        color={'R':'red','B':'blue'}):
        self.draw(color=bgcolor)
        ax, X = self.axes, self.X
        sample = self.box.sample(self.ndraw)
        nblue = np.sum([s == 'B' for s in sample])
        nred = self.ndraw - nblue
        ax.scatter(X[:nblue,0], X[:nblue,1], s=self.sample_ptsize, color=color['B'], alpha=.8, edgecolor='gray', linewidth=2)            
        ax.scatter(X[-nred:,0], X[-nred:,1], s=self.sample_ptsize, color=color['R'], alpha=.8, edgecolor='gray', linewidth=2)           
        return self.figure

    def trial(self, bgcolor={'R':'red','B':'blue'},
              color={'R':'red','B':'blue'}):
        sample = self.box.sample(self.ndraw)
        if self.draw_fig:
            self.draw_sample_pts(color=color, bgcolor=bgcolor)
        self.outcome = np.mean([s == 'B' for s in sample])
        return self.outcome
