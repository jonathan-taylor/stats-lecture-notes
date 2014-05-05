from __future__ import division
import itertools
import numpy as np
from copy import copy
from scipy.stats import binom
from .conv import conv_integer_rv

class ProbabilitySpace(object):

    desc = 'A probability space.'

    def __init__(self, rng):
        """
        Default constructor takes a callable that draws samples
        from __some__ distribution.

        Parameters
        ----------

        rng : callable
            Generate points in some sample space.

        """
        self.rng = rng
        self.outcome = None

    def trial(self):
        """
        Run a trial, returning an
        outcome from the sample space.
        """
        self.outcome = self.rng()
        return self.outcome

    def sample(self, ntrial):
        """
        Form a sample of the example.
        """
        return [self.trial() for _ in range(ntrial)]

    @property
    def sample_space(self):
        if hasattr(self, "_sample_space"):
            return self._sample_space

    @property
    def mass_function(self):
        if hasattr(self, "_mass_function"):
            return self._mass_function

    def _repr_html_(self):
        raise NotImplementedError

    @property
    def summary(self):
        raise NotImplementedError

class RandomVariable(ProbabilitySpace):

    def __init__(self, probability_space, random_variable):
        self.random_variable = random_variable
        self.probability_space = probability_space
        if probability_space.sample_space is not None:
            self._sample_space = np.unique([random_variable(point) for point
                                            in probability_space.sample_space])
            if probability_space.mass_function is not None:
                self._mass_function = {}
                for point in self.probability_space.sample_space:
                    image = random_variable(point)
                    p = self._mass_function.setdefault(image, 0)
                    self._mass_function[image] += probability_space.mass_function[point]
        self.outcome = None

    def trial(self):
        self.outcome = self.random_variable(self.probability_space.trial())
        return self.outcome

class SampleMean(ProbabilitySpace):

    def __init__(self, random_variable, nsample):
        self.random_variable = random_variable
        self.nsample = nsample
        self.outcome = None

    def trial(self):
        sample = self.random_variable.sample(self.nsample)
        self.outcome = [np.mean(sample), np.std(sample)]
        return self.outcome

    def confidence_interval(self):
        """
        Simulate a confidence interval for the population mean
        """
        mean, SD = self.trial()
        return [mean - 2*SD / np.sqrt(self.nsample), 
                mean + 2*SD / np.sqrt(self.nsample)]

class SumOfDraws(ProbabilitySpace):

    def __init__(self, random_variable, ndraws):
        self.random_variable = random_variable
        self.ndraws = ndraws

    def trial(self):
        sample = self.random_variable.sample(self.ndraws)
        self.outcome = np.sum(sample)
        return self.outcome

class BoxModel(ProbabilitySpace):

    """
    A discrete uniform sample space: samples are drawn
    with or without replacement from a list of items.
    """

    def __init__(self, values, replace=True):
        self.replace = replace
        self.values = list(values)
        self._nvalues = len(self.values)
        self._sample_space = list(set(self.values))
        self._mass_function = {}
        n = len(self.values)
        for item in self.values:
            self._mass_function.setdefault(item, 0)
            self._mass_function[item] += 1. / n
        self.outcome = None

    def sample(self, ntrial):
        idx = np.random.choice(len(self.values), ntrial, replace=self.replace)
        return [self.values[i] for i in idx]

    def trial(self):
        idx = np.random.choice(len(self.values), 1, replace=self.replace)
        self.outcome = self.values[idx]
        return self.outcome

    def event(self, event_spec):
        if callable(event_spec):
            return RandomVariable(self, event_spec)
        else: # assuming it is a sequence
            _event_spec = lambda point: point in event_spec
            return RandomVariable(self, _event_spec)
    
    def conditional(self, event_spec):
        if not callable(event_spec):
            E = list(event_spec)
            event_spec = lambda i: i in E
        mass_fn = {}
        total = 0
        for k in self.mass_function:
            if event_spec(k):
                mass_fn[k] = self.mass_function[k]
                total += self.mass_function[k]
        for k in mass_fn:
            mass_fn[k] /= total
        return WeightedBox(mass_fn)

class WeightedBox(BoxModel):

    def __init__(self, mass_function, replace=True):
        """
        Specified by a dict: {item:probability}
        """
        self.replace = replace
        self._mass_function = mass_function
        self._sample_space = self._mass_function.keys()
        self._sample_space = sorted(self._sample_space)
        self._P = np.array([mass_function[k] for k in self._sample_space])
        self._P /= self._P.sum()
        self.outcome = None

    def trial(self):
        choice = np.random.choice(len(self._sample_space), 1, replace=self.replace)
        self.outcome = self._sample_space[choice]
        return self.outcome

    def sample(self, ntrial):
        choice = np.random.choice(len(self._sample_space), ntrial, replace=self.replace, p=self._P)
        return [self._sample_space[c] for c in choice]


class Geometric(ProbabilitySpace):

    '''
    Geometric distribution derived from a bernoulli example
    '''

    def __init__(self, box_model, event_spec):
        self.bernoulli = box_model.event(event_spec)

    @property
    def sample_space(self):
        return Latex('$\mathbb{N} = \{1,2,\dots\}$')
     
    @property
    def mass_function(self):
        def mass_fn(j, prob=self.prob):
            return prob * (1.-prob)**(j-1)
        mass_fn._repr_latex_ = lambda s: Latex('$f(j) = p(1-p)^{j-1}$')

    def trial(self):
        """
        Run a trial, incrementint success counter and updating
        html output
        """
        nwait = 0
        while True:
            nwait += 1
            if self.bernoulli.trial():
                break
        self.outcome = nwait
        return self.outcome

    def _repr_html_(self):
        base = self.bernoulli._repr_html_()

class Binomial(ProbabilitySpace):

    '''
    Binomial distribution derived from a bernoulli example
    '''

    def __init__(self, ndraws, box_model, event_spec=None):
        if event_spec is not None:
            self.bernoulli = box_model.event(event_spec)
        else:
            self.bernoulli = box_model
            if sorted(np.array(box_model.sample_space, np.int)) != [0,1]:
                raise ValueError('expecting a bernoulli random variable')

        self._P = P = self.bernoulli.mass_function[True]
        self.ndraws = ndraws
        self._sample_space = range(self.ndraws+1)
        self._mass_function = dict([(i, binom.pmf(i, self.ndraws, P))
                                    for i in self._sample_space])

    def trial(self):
        """
        Run a trial, incrementint success counter and updating
        html output
        """
        self.outcome = binom.rvs(self.ndraws, self._P)
        return self.outcome

    def _repr_html_(self):
        base = self.bernoulli._repr_html_()

class Multinomial(WeightedBox):

    desc = 'A multinomial specified by a table.'
    replace = True

    def __init__(self, counts, labels=None):
        counts = np.array(counts)
        self.labels = labels or [range(j) for j in counts.shape]
        self.labels = labels or [range(j) for j in counts.shape]
        self.prob = counts / (1. * counts.sum())
        self._P = self.prob
        self.shape = counts.shape
        self._sample_space = [l for l in itertools.product(*self.labels)]
        self._mass_function = dict([(l, p) for l, p in zip( \
                    itertools.product(*self.labels),
                    self.prob.reshape(-1))])

        self.outcome = None

    def trial(self):
        V = np.random.multinomial(1, self.prob.reshape(-1))
        I = np.nonzero(V)[0]
        self.outcome = self.sample_space[I]
        return self.outcome

    def sample(self, ntrial):
        V = np.random.multinomial(ntrial, self.prob.reshape(-1))
        I = np.nonzero(V)[0]
        outcome = [self.sample_space[c] for c in I]
        np.random.shuffle(outcome)
        return outcome

    def condition_margin(self, margin, value):
        vars = range(len(self.shape))
        vars.pop(margin)
        idx = list(self.labels[margin]).index(value)
        _slice = [slice(None)] * margin + [slice(idx,idx+1)]
        labels = copy(list(self.labels))
        labels.pop(margin)
        P = self.prob[_slice]
        return Multinomial(P, labels=labels)

def Normal(mean, SD):
    rng = lambda : np.random.standard_normal() * SD + mean
    return ProbabilitySpace(rng)

class SumIntegerRV(RandomVariable):

    """
    Given a mass function on non-negative integers,
    form the random variable that is the convolution
    of this mass function `ndraw` times

    The mass function specifies a random variable that 
    is i with probability proportional to mass_function[i] is specifi
    """

    def __init__(self, mass_function, ndraw):
        mass_function = np.array(mass_function)
        mass_function /= mass_function.sum()
        self._rv = Multinomial(mass_function)
        self._mass_fn = mass_function
        self._mass_function = dict(zip(*conv_integer_rv(self._mass_fn, ndraw)))
        self._sample_space = self._mass_function.keys()
        self._ndraw = ndraw

    def trial(self):
        return np.sum(self._rv.sample(self._ndraw))
