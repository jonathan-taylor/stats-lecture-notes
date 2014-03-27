import numpy as np

class example(object):

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

    def trial(self, numeric=False):
        """
        Run a trial, incrementing success counter and updating
        html output.

        If numeric is True, it should return a numeric value
        that can be averaged.
        
        It should store an outcome in `self.outcome` and
        a numeric version in `self.numeric_outcome`.

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

    def _repr_html_(self):
        raise NotImplementedError
