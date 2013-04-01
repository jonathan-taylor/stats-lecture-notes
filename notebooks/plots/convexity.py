import numpy as np
import matplotlib.pyplot as plt

eta1 = 1.5
d_eta1 = 1
eta2 = eta1 + d_eta1

def CGF(eta):
    return 5*eta**2 - np.log(eta)

def dotCGF(eta):
    return 10*eta - 1/eta

def deviance(eta2, eta1=eta1):
    return 2 * (CGF(eta2) - CGF(eta1) + (eta1-eta2) * dotCGF(eta1))

eta = np.linspace(eta1- d_eta1,eta1+1.5 * d_eta1,101)
plt.figure(figsize=(8,8))
plt.plot(eta, CGF(eta), label=r'$\Lambda(\eta)$')
plt.plot(eta, CGF(eta1) + (eta-eta1) * dotCGF(eta1), label=r'$\Lambda(\eta_1) + \dot{\Lambda}(\eta_1) (\eta-\eta_1)$')
plt.plot([eta2,eta2],[CGF(eta2), CGF(eta1) + d_eta1 * dotCGF(eta1)], label=r'$D(\eta_1;\eta_2)/2$')
plt.scatter([eta1], [CGF(eta1)], color='blue', s=35)
plt.scatter([eta2], [CGF(eta2)-deviance(eta2,eta1)/2], color='purple', s=35)
plt.scatter([eta2], [CGF(eta2)], color='red', s=35)
plt.plot([eta1,eta1],[0,CGF(eta1)], linestyle='--', color='gray')
plt.plot([eta2,eta2],[0,CGF(eta2)-deviance(eta2,eta1)/2], linestyle='--', color='gray')

a = plt.gca()
a.set_xticks([eta1,eta2])
a.set_xticklabels([r'$\eta_1$', r'$\eta_2$'], size=15)
a.set_xlim(sorted([eta1-1.2*d_eta1, eta1+1.2*d_eta1]))
a.set_ylim([0,40])
a.set_xlabel(r'$\eta \in {\cal D}$', size=20)
plt.legend(loc='upper left')
a.set_title(r'Convexity picture on ${\cal D}$ at $(\eta_1,\eta_2)=(%0.1f,%0.1f)$' % (eta1,eta2), size=20)

if __name__ == "__main__":
    plt.savefig('convexity.png')
