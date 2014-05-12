from base64 import encodestring
from itertools import product
import matplotlib.pyplot as plt
import numpy as np
from IPython.core.display import HTML

from probability import BoxModel,ProbabilitySpace

class BloodPressure(ProbabilitySpace):

    figsize = (5.5, 5.5)
    alpha = 0.1
    ptsize = 5
    sample_ptsize = 60

    def __init__(self, draw_fig=True):
        self.npop, self.ndraw = 5000, 50
        self.box = BoxModel(np.random.random_integers(-15, 0,
                                                       size=(self.npop,)),
                                                       replace=True)
        self.X = (np.mgrid[0:1:10j,0:1:5j].reshape((2,50)) + 
                  np.random.sample((2,50)) * 0.05)
        self.BG = np.random.sample((self.npop,2))
        self.X = self.X.T
        self.draw_fig = draw_fig
        if draw_fig:
            self.draw()

    def draw(self, color={'R':'red','B':'blue'}):
        self.figure.clf()
        ax, X, BG = self.axes, self.X, self.BG
        ax.scatter(BG[:,0], BG[:,1], s=self.ptsize, color='gray', alpha=self.alpha)            
        ax.set_xticks([]);    ax.set_xlim([-0.1,1.1])            
        ax.set_yticks([]);    ax.set_ylim([-0.1,1.1])       

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
        ax, X, sample = self.axes, self.X, self._sample
        mean, sd = self.outcome
        for i in range(50):
            ax.text(X[i,0], X[i,1], '%d' % sample[i], color='red')
        ax.set_title("average(sample)=%0.1f, SD(sample)=%0.1f" % (np.mean(sample), np.std(sample)), fontsize=15)
        return self.figure

    def trial(self, bgcolor={'R':'red','B':'blue'},
              color={'R':'red','B':'blue'}):
        self._sample = self.box.sample(self.ndraw)
        self.outcome = np.mean(self._sample), np.std(self._sample)
        if self.draw_fig:
            self.draw_sample_pts(color=color, bgcolor=bgcolor)
        return self.outcome
