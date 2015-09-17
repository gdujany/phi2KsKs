from numpy import sum, sqrt, log, exp, cos, linspace
from scipy.integrate import dblquad, quad
from matplotlib import pyplot as plt
import numpy as np

Gamma_L = 1/5.116e4
Gamma_S = 1/0.89564e2
Delta_m = 0.5289e-2
propPiPiKs = .692/(1+(2.228e-3)**2)
eta = 2.232e-3
zeta = 0.098

BrKs = .692
BrKl = 1.967e-3

def prob_decay_smbkg(t1a,t1e,t2a,t2e):
	Constant = BrKs*BrKl# propPiPiKs**2*eta**2
	def intensity(t1,t2):
		Part1 = exp(-Gamma_L*t1-Gamma_S*t2)
		Part2 = exp(-Gamma_L*t2-Gamma_S*t1)
		Part3 = -2*exp(-.5*(Gamma_L+Gamma_S)*(t1+t2))*cos(Delta_m*(t1-t2))
		return Part1+Part2+Part3
	Int = dblquad(intensity, 0, np.inf, # limits t2
                  lambda x : 0, # limits t1
                  lambda x: np.inf)[0]
	Part = dblquad(intensity, t1a, t1e, # limits t2
                  lambda x : t2a, # limits t1
                  lambda x: t2e)[0]
	return Constant*Part/Int


def prob_decay_signal(t1a,t1e,t2a,t2e):
	Constant = BrKl*BrKs#propPiPiKs**2*eta**2
	def intensity(t1,t2):
		Part1 = exp(-Gamma_L*t1-Gamma_S*t2)
		Part2 = exp(-Gamma_L*t2-Gamma_S*t1)
		Part3 = -2*(1-zeta)*exp(-.5*(Gamma_L+Gamma_S)*(t1+t2))*cos(Delta_m*(t1-t2))
		return Part1+Part2+Part3
	Int = dblquad(intensity, 0, np.inf, # limits t2
                  lambda x : 0, # limits t1
                  lambda x: np.inf)[0]
	Part = dblquad(intensity, t1a, t1e, # limits t2
                  lambda x : t2a, # limits t1
                  lambda x: t2e)[0]
	return Constant*Part/Int


def prob_decay_KsKs(t1a,t1e,t2a,t2e):
	def f(t1,t2):
		return exp(-Gamma_S*t1-Gamma_S*t2)
	Int = dblquad(f, 0, np.inf, # limits t2
                  lambda x : 0, # limits t1
                  lambda x: np.inf)[0]
	Part = dblquad(f, t1a, t1e, # limits t2
                  lambda x : t2a, # limits t1
                  lambda x: t2e)[0]
	return (BrKs)**2*Part/Int

def intensity(t1,t2):
	Constant = Gamma_L*Gamma_S*propPiPiKs**2*eta**2/2.
	Part1 = exp(-Gamma_L*t1-Gamma_S*t2)
	Part2 = exp(-Gamma_L*t2-Gamma_S*t1)
	Part3 = -2*(1-zeta)*exp(-.5*(Gamma_L+Gamma_S)*(t1+t2))*cos(Delta_m*(t1-t2))
	return Constant*(Part1+Part2+Part3)	



print('SMbkg')
print('both',prob_decay_smbkg(0,25,0,25))
print('one 1',2*prob_decay_smbkg(25,200,0,25))

print('signal')
print('both',prob_decay_signal(0,25,0,25))
print('one 1', 2*prob_decay_signal(25,200,0,25))

print('KsKs')
print('both',prob_decay_KsKs(0,25,0,25))
print('one 1', 2*prob_decay_KsKs(25,200,0,25))





# x = np.linspace(0,10e-7,100)
# a = []
# for y in x:
# 	a.append(numintegral(0,y,0.025e-9,1))

# plt.plot(x,a,label = 'signal')
# plt.legend()
# # plt.yscale('log')
# # plt.xscale('log')
# plt.show()
# plt.clf()
# # plt.plot(x,prob_

print prob_decay_smbkg(0,0,0,0)
print intensity(0,0)

from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np

plt.ion()

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
X, Y = np.mgrid[0:1e-7:0.01e-7, 0:1e-7:0.01e-7]#np.mgrid[0:1e-9:0.1e-10, 0:1e-9:0.1e-10]
Z = intensity(X,Y)
#Z = prob_decay_signal(0,X,0,Y)

plt.show()
	


surf = ax.plot_surface(X, Y, Z, cmap='autumn', cstride=2, rstride=2)



#plt.savefig("test.pdf")
#plt.clf()
#surf = ax.plot_surface(X, Y, Z, cmap='autumn', cstride=2, rstride=2)
plt.savefig("intensity.pdf")
