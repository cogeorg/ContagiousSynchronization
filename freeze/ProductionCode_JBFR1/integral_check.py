import numpy as np
import matplotlib.pylab as pl
from scipy import integrate as scint

def fun0(p,mu0 = 0.3, sigma = np.sqrt(0.1)):

	mu1 = 1-mu0
	x1 = ((mu0-mu1)*(-1+p)*p*np.sqrt(2*np.pi))
	x2 = ((mu0-mu1)**2 - 2*sigma**2*np.log(-1+1/p))**2
	x3 = 8*(mu0 - mu1)**2*sigma**2

	out = np.exp(-x2/x3)*sigma/x1
	return out

def fun1(p,mu0 = 0.3, sigma = np.sqrt(0.1)):

	mu1 = 1-mu0
	x1 = ((mu0-mu1)*(-1+p)*p*np.sqrt(2*np.pi))
	x2 = ((mu0-mu1)**2 + 2*sigma**2*np.log(-1+1/p))**2
	x3 = 8*(mu0 - mu1)**2*sigma**2

	out = np.exp(-x2/x3)*sigma/x1
	return out

p = np.linspace(0.01,0.99,num = 1000)
fp0 = fun0(p)
fp1 = fun1(p)

q = 0.7
print(scint.quad(fun0,0,1-q)[0])
print(scint.quad(fun1,q,1)[0])

pl.figure()
pl.plot(p,fp0)
pl.plot(p,fp1)
pl.show()