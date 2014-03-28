from __future__ import division
import itertools
import numpy as np

class example(object):

    desc = 'A probability example.'
    true_mean = None

    def __init__(self):
        raise NotImplementedError

    # API

    def reset(self):
        """
        Reset example.
        """
        self.outcome = None
        self.numeric_outcome = None
        self.ntrial = 0
        self.total = 0
        self.total2 = 0

    def trial(self, numeric=False):
        """
        Run a trial, incrementing success counter and updating
        html output.

        If numeric is True, it should return a numeric value
        that can be averaged.
        
        It should store an outcome in `self.outcome` and
        a numeric version in `self.numeric_outcome`.

        To compute the mean, the numeric outcome should be
        incremented in `self.total`.

        To compute the SD, the squared numeric outcome should
        also increment `self.total2`.

        """
        raise NotImplementedError

    def sample(self, ntrial, numeric=False):
        """
        Form a sample of the example.
        """
        return [self.trial(numeric=numeric) for _ in range(ntrial)]

    @property
    def mean(self):
        return self.total / self.ntrial

    @property
    def sample_space(self):
        return []

    @property
    def numeric_sample_space(self):
        return []

    @property
    def mass_function(self):
        return {}

    @property
    def SD(self):
        return np.sqrt((self.total2 / self.ntrial - self.mean**2))

    @property
    def confidence_interval(self):
        return [self.mean - 2*self.SD / np.sqrt(self.ntrial), 
                self.mean + 2*self.SD / np.sqrt(self.ntrial)]

    def _repr_html_(self):
        raise NotImplementedError

    @property
    def html_summary(self):
        # description of the results of repeated trials
        raise NotImplementedError

class bernoulli(example):

    '''
    Bernoulli based on a uniform draw from
    sample space.
    '''

    def __init__(self, testfn):
        self.true_mean = np.mean([testfn(item) for item in self.sample_space])
        self.testfn = testfn
        self.reset()
    
    @property
    def html_summary(self):
        return '<h3>Success rate: %d out of %d: %d%%</h3>' % (self.total, self.ntrial, 100*self.mean)

    @property
    def mass_function(self):
        ss = self.sample_space
        return dict([(v, 1./len(ss)) for v in ss])


class geometric(example):

    '''
    Geometric distribution derived from a bernoulli example
    '''

    def __init__(self, bernoulli):
        self.bernoulli = bernoulli
        self.true_mean = 1. / bernoulli.true_mean
        self.reset()

    @property
    def sample_space(self):
        return Latex('$\mathbb{N} = \{1,2,\dots\}$')
     
    @property
    def mass_function(self):
        def mass_fn(j, prob=self.prob):
            return prob * (1.-prob)**(j-1)
        return mass_fn

    def trial(self, numeric=True):
        """
        Run a trial, incrementint success counter and updating
        html output
        """
        nwait = 0
        while True:
            nwait += 1
            if self.bernoulli.trial(numeric=True):
                break

        self.ntrial += 1
        self.total += nwait
        self.total2 += nwait**2
        self.outcome = nwait
        return self.outcome

    @property
    def html_summary(self):
        return '<h3>It took %d trials until the first success.</h3>' % (self.outcome, )

    def _repr_html_(self):
        base = self.bernoulli._repr_html()
        if self.ntrial > 0:
            base += self.html_summary
        return base

class multinomial(object):

    desc = 'A probability example.'
    true_mean = None

    def __init__(self, counts, rows=None, columns=None):
        counts = np.array(counts)
        if counts.ndim > 2:
            raise ValueError('only up to 2d tables')
        self.rows = rows or range(1, counts.shape[0]+1)
        self.columns = columns or range(1, counts.shape[1]+1)
        self.P = counts / (1. * counts.sum())
        self.total = 0
        self.ntrial = 0
    # API

    @property
    def sample_space(self):
        if not hasattr(self, "_sample_space"):
            self._sample_space = [(r,c) for r, c in itertools.product(self.rows, self.columns)]
        return self._sample_space

    @property
    def mass_function(self):
        # Mass function for a draw of size 1
        return self.P

    def reset(self):
        """
        Reset example.
        """
        self.outcome = None
        self.ntrial = 0
        self.total = np.zeros(self.P.shape)
        self.total2 = 0

    def trial(self, numeric=False):
        """
        Run a trial, incrementing success counter and updating
        html output.

        If numeric is True, it should return a numeric value
        that can be averaged.
        
        It should store an outcome in `self.outcome` and
        a numeric version in `self.numeric_outcome`.

        To compute the mean, the numeric outcome should be
        incremented in `self.total`.

        To compute the SD, the squared numeric outcome should
        also increment `self.total2`.

        """
        V = np.random.multinomial(1, self.P.reshape(-1))
        I = np.nonzero(V)[0]
        self.outcome = self.sample_space[I]
        self.total += V
        self.ntrial += 1
        return self.outcome

    def sample(self, ntrial, numeric=False):
        """
        Form a sample of the example.
        """
        return [self.trial(numeric=numeric) for _ in range(ntrial)]

    @property
    def mean(self):
        return (self.total / self.ntrial).reshape(self.P.shape)

    def _repr_html_(self):
        #TODO: an html table
        raise NotImplementedError

    @property
    def html_summary(self):
        # description of the results of repeated trials
        raise NotImplementedError
