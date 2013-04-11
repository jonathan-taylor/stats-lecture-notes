'''
This is a script that is a solution to the Lagrange multipler exercise
in multivariate_families_partI
'''

import numpy as np, pylab

# Normal CGFs

C = np.log(2*np.pi)

def CGFnormal(eta, N=10):
    """
    The univariate normal CGF for a sample of size N

    .. math::

        \frac{1}{2} \left[\log(2\pi)- \log(\eta_2) + \frac{\eta_1^2 }{\eta_2} \right]
    """
    eta = np.asarray(eta)
    return N * (C - np.log(eta[1]) + eta[0]**2 / eta[1]) / 2.


def dotCGFnormal(eta, N=10):
    """
    The gradient of the univariate normal CGF for a sample of size N
    """
    eta = np.asarray(eta)
    return N * np.array([eta[0] / eta[1], (-eta[0]**2/eta[1]**2 - 1. / eta[1]) / 2.])

def ddotCGFnormal(eta, N=10):
    """
    The Hessian of the univariate normal CGF for a sample of size N
    """
    eta = np.asarray(eta)
    H = np.zeros((2,2))
    H[0,0] = 1. / eta[1]
    H[0,1] = H[1,0] = - eta[0] / eta[1]**2
    H[1,1] = 0.5 / eta[1]**2 + eta[0]**2 / eta[1]**3
    return N*H

class normal(object):
    """
    The univariate normal family for a sample of size N
    """
    def __init__(self, N):
        self.N = N
        
    def value(self, eta):
        return CGFnormal(eta, self.N)
    
    def grad(self, eta, v=None):
        """
        The gradient at eta in the direction v, if v is not None
        """
        g = dotCGFnormal(eta, self.N)
        if v is not None:
            return (v*g).sum()
        return g
    
    def hess(self, eta, vw=None):
        """
        The hessian at eta in the directions v,w = vw
        """
        h = ddotCGFnormal(eta, self.N)
        if vw is not None:
            v, w = vw
            return (v * np.dot(h, w)).sum()
        return h



class normalconj(object):
    """
    The univariate normal family for a sample of size N
    """
    def __init__(self, N):
        self.N = N
        
    def value(self, t):
        return self.N * 0.5 * (1 + np.sqrt(2*np.pi) - np.log(-2*t[1]-t[0]**2))
    
    def grad(self, t, v=None):
        """
        The gradient at t in the direction v, if v is not None
        """
        sigma2 = -2*t[1]-t[0]**2
        mu = t[0]
        g = self.N * np.array([mu/sigma2, 1./sigma2])
        if v is not None:
            return (v * g).sum()
        return g

    def hess(self, t, vw=None):
        """
        The hessian at t in the directions v,w = vw
        """
        den = (2*t[0]+t[0]**2)**2
        H = np.zeros((2,2))
        H[0,1] = H[1,0] = 2*t[0]
        H[1,1] = 2
        H[0,0] = -(2*t[0]+t[0]**2) + 2*t[0]**2
        H = self.N * H / den
        if vw is not None:
            v, w = vw
            return (v * np.dot(H, w)).sum()
        return H

# given problem info
    
tx = np.array([.2,-2])
eta_0 = np.array([10,2])
v = np.array([11, .2])
a = np.array([-v[1],v[0]])
b = (a*eta_0).sum()

# control parameters

max_iters = 1000
step_tries = 300
step_increase_time = 5
tol = 1.e-14
min_iters = 300

# the instances of the CGF and its conjugate

family = normal(1)
familyc = normalconj(1)

s = 10 # initial point
s_iterates = [s] # sequence of values of s

value = np.inf # initial value
value_iterates = [value] # sequence of objective
step_size = 1 # how big a step do we try to take

# the primal minimization

for i in range(max_iters):
    grad = (v*(family.grad(eta_0+s*v)-tx)).sum()
    hess = family.hess(eta_0+s*v,(v,v))
    count = 0
    while True:
        proposed_s =  s - step_size * grad / hess
        proposed_eta = eta_0 + proposed_s * v
        proposed_value = family.value(proposed_eta) - (tx*proposed_eta).sum()
        
        # if the step is leads outside the domain, or is not a descent, take
        # a smaller step
        
        if proposed_eta[1] < 0 or proposed_value > value:
            step_size *= 0.9
        else:
            break  

    # when do we stop?
    if (i > 1 and np.fabs((value - proposed_value) / value) < tol
        and i > min_iters):
        break
    
    value = proposed_value
    s = proposed_s
    s_iterates.append(s)
    value_iterates.append(family.value(eta_0+s*v)-(tx*(eta_0+s*v)).sum())
    
    # try to take a bigger step, if possible   
    if i % step_increase_time == 0:
        step_size *= 2
        

s = 10 # initial point
s_iterates = [s] # sequence of values of s

value = np.inf # initial value
value_iterates = [value] # sequence of objective
step_size = 1 # how big a step do we try to take

step_increase_time = 5 # how often do we try to take a bigger step
tol = 1.e-7 # tolerance for stopping -- based on objective

max_iters = 100

# the dual minimization

u = 0.
step_size = 1.
value = np.inf

u_iterates = [u]
value_iterates = [value]

for i in range(max_iters):
    grad = familyc.grad(tx+u*a,a)-b
    hess = familyc.hess(tx+u*a,(a,a))-b
    count = 0
    step_size = 1.
    for j in range(step_tries):
        proposed_u =  u - step_size * grad / hess
        proposed_t = tx + proposed_u*a
        proposed_value = familyc.value(proposed_t)-u*b

        # the constraint
        if 2*proposed_t[1] + proposed_t[0]**2 >= 0 or proposed_value > value:
            step_size *= 0.9
        else:
            break  
        if j == step_tries - 1:
            print 'failed to find a small enough step: %d, %0.4e, %0.3e ' % (i, step_size, np.fabs((proposed_value - value) / value))

    # when do we stop?
    if ((i > 1 and np.fabs((value - proposed_value) / value) < tol) 
        and (i > min_iters)):
        break
    
    value = proposed_value
    u = proposed_u
    u_iterates.append(u)
    value_iterates.append(value)
    
    # try to take a bigger step, if possible   
    if i % step_increase_time == 0:
        step_size *= 2

#pylab.plot(value_iterates)
#ax = pylab.gca()
#ax.set_xlabel('Iteration $k$')
#ax.set_ylabel(r'$\log(\Lambda(\eta_0+s^{(k)}v) - (\eta_0+s^{(k)}v)^T t(x))$')

print 'original solution:', proposed_eta
print 'dual solution:', familyc.grad(proposed_t)


