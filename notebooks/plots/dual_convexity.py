import numpy as np
import matplotlib.pyplot as plt

def dotCGFstar(mu):
    return (mu + np.sqrt(mu**2+40)) / 20.

def CGFstar(mu):
    return dotCGFstar(mu)*mu-CGF(dotCGFstar(mu))

def deviance_mu(mu1, mu2):
    return 2 * (CGFstar(mu1) - CGFstar(mu2) + (mu2-mu1) * dotCGFstar(mu2))

mu1 = dotCGF(eta1)
mu2 = dotCGF(eta2)
d_mu2 = mu1 - mu2

mu = np.linspace(mu2- d_mu2,mu2+1.5 * d_mu2,101)
plt.figure(figsize=(8,8))
plt.plot(mu, CGFstar(mu), label=r'$\Lambda^*(\mu)$')
plt.plot(mu, CGFstar(mu2) + (mu-mu2) * dotCGFstar(mu2), label=r'$\Lambda^*(\mu_2) + \dot{\Lambda}^*(\mu_2) (\mu-\mu_2)$')
plt.plot([mu1,mu1],[CGFstar(mu1), CGFstar(mu2) + d_mu2 * dotCGFstar(mu2)], label=r'$\tilde{D}(\mu_1;\mu_2)/2$')
plt.scatter([mu2], [CGFstar(mu2)], color='blue', s=35)
plt.scatter([mu1], [CGFstar(mu1)-deviance_mu(mu1,mu2)/2], color='purple', s=35)
plt.scatter([mu1], [CGFstar(mu1)], color='red', s=35)

plt.plot([mu1,mu1],[0,CGFstar(mu1)-deviance_mu(mu1,mu2)/2], linestyle='--', color='gray')
plt.plot([mu2,mu2],[0,CGFstar(mu2)], linestyle='--', color='gray')

a = plt.gca()
a.set_xticks([mu1,mu2])
a.set_xticklabels([r'$\mu_1$', r'$\mu_2$'], size=15)
a.set_xlim(sorted([mu2-1.2*d_mu2, mu2+1.2*d_mu2]))
a.set_xlabel(r'$\mu \in {\cal M}$', size=20)
a.set_ylim([0,50])
plt.legend(loc='upper left')
a.set_title(r"""Convexity picture  on ${\cal M}$ at 
$(\mu_1,\mu_2)=(\dot{\Lambda}^*(%0.1f), \dot{\Lambda}^*(%0.1f)\approxeq(%0.2f,%0.2f))$""" % (eta1,eta2,mu1,mu2), size=20)

