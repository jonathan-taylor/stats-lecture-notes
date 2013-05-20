import numpy as np

class GLM(object):
    
    def __init__(self, Y, X, family):
        self.Y = Y
        self.X = X
        self.n, self.p = X.shape
        self.family = family(Y)
        
    def value(self, beta):
        '''
        .. math::
            
            \Lambda^{(n)}(X\beta) - (X\beta)^TY
        '''
        eta = np.dot(self.X, beta)
        return self.family.value(eta)
    
    def grad(self, beta):
        '''
        .. math::

            X^T \left(\nabla \CGF^{(n)}(X\beta) - Y)
        '''
        eta = np.dot(self.X, beta)
        return np.dot(self.X.T, self.family.grad(eta))
    
    def hess(self, beta):
        '''
        .. math::

            X^T \nabla^2 \CGF^{(n)}(X\beta)X

        '''
        eta = np.dot(self.X, beta)
        D = self.family.hess(eta)
        return np.dot(self.X.T, D[:,np.newaxis] * self.X)
    
    def constraint(self, beta):
        '''
        Check to see whether the constraint is satisfied or not.
        Most GLMs will have no constraint on $\beta$.
        '''
        return True

class poisson(object):
    
    def __init__(self, Y):
        self.Y = Y
        
    def value(self, eta):
        '''
        .. math::
            
            \Lambda^{(n)}(\eta)-\eta^T Y

        '''
        return (np.exp(eta) - eta*self.Y).sum()  
    
    def grad(self, eta):
        '''
        .. math::

            \dot{\Lambda}(\eta) - Y

        '''
        mu = np.exp(eta)
        return mu - self.Y
    
    def hess(self, eta):
        '''
        .. math::
            
            \ddot{\Lambda}(\eta)

        '''
        dmu_deta = np.exp(eta)
        return dmu_deta

class binomial(poisson):
    
    def __init__(self, YN):
        self.Y, self.N = np.asarray(YN).T
        
    def value(self, eta):
        return (self.N * np.log(1.+np.exp(eta)) - eta*self.Y).sum()
    
    def grad(self, eta):
        E = np.exp(eta)
        return self.N * E / (1. + E) - self.Y
    
    def hess(self, eta):
        E = np.exp(eta)
        mu = E / (1. + E)
        return self.N * mu * (1 - mu)
    
    @classmethod
    def bernoulli(cls, Y):
        n = np.asarray(Y).shape[0]
        YN = np.ones((n,2))
        YN[:,0] = Y
        return cls(YN)

def fit(model, niter=10):

    beta = np.ones(model.p)
    value = model.value(beta)

    for _ in range(niter):
        step = 1.
        count = 0
        while True:
            proposed_beta = beta - step * np.dot(np.linalg.pinv(model.hess(beta)), model.grad(beta))
            if (model.value(proposed_beta) > value 
                and model.constraint(proposed_beta)):
                step *= 0.5
            else:
                break
        beta = proposed_beta
        value = model.value(beta)
    return beta


