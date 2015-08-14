from numpy import sum, sqrt, log, exp, cos, linspace
from scipy.integrate import dblquad, quad
from matplotlib import pyplot as plt
import numpy as np

Gamma_L = 1/5.116e-8
Gamma_S = 1/0.89564e-10
Delta_m = 0.5289e10
propPiPiKs = 1/(1+(2.228e-3)**2)
eta = 2.232e-3
zeta = 0.098

BrKs = .692
BrKl = 1.967e-3

def prob_decay_smbkg(t1a,t1e,t2a,t2e):
	Constant = propPiPiKs**2*eta**2/2.
	print(Constant)
	Constant = BrKl*BrKs/2.
	Part1 = exp(-Gamma_L*t1e-Gamma_S*t2e)-exp(-Gamma_L*t1e-Gamma_S*t2a)-exp(-Gamma_L*t1a-Gamma_S*t2e)+exp(-Gamma_L*t1a-Gamma_S*t2a)
	Part2 = exp(-Gamma_S*t1e-Gamma_L*t2e)-exp(-Gamma_S*t1e-Gamma_L*t2a)-exp(-Gamma_S*t1a-Gamma_L*t2e)+exp(-Gamma_S*t1a-Gamma_L*t2a)
	Part3Constant = ((4*Gamma_L*Gamma_S)/(Gamma_S**2+2*Gamma_S*Gamma_L+Gamma_L**2+4*Delta_m**2))
	Part3 = exp(-(Gamma_L+Gamma_S)*(t1e+t2e)/2.)*cos(Delta_m*(t2e-t1e)) - exp(-(Gamma_L+Gamma_S)*(t1a+t2e)/2.)*cos(Delta_m*(t2e-t1a)) - exp(-(Gamma_L+Gamma_S)*(t1e+t2a)/2.)*cos(Delta_m*(t2e-t1a))  + exp(-(Gamma_L+Gamma_S)*(t1a+t2a)/2.)*cos(Delta_m*(t2a-t1a))
	return Constant*(Part1+Part2+Part3Constant*Part3)




def prob_decay_signal(t1a,t1e,t2a,t2e):
	# return (exp(-Gamma_S*(t1a+t2a))-exp(-Gamma_S*(t1e+t2a))-exp(-Gamma_S*(t1a+t2e))+exp(-Gamma_S*(t1e+t2e)))*propPiPiKs**2
	Constant = propPiPiKs**2*eta**2/2.
	Part1 = exp(-Gamma_L*t1e-Gamma_S*t2e)-exp(-Gamma_L*t1e-Gamma_S*t2a)-exp(-Gamma_L*t1a-Gamma_S*t2e)+exp(-Gamma_L*t1a-Gamma_S*t2a)
	Part2 = exp(-Gamma_S*t1e-Gamma_L*t2e)-exp(-Gamma_S*t1e-Gamma_L*t2a)-exp(-Gamma_S*t1a-Gamma_L*t2e)+exp(-Gamma_S*t1a-Gamma_L*t2a)
	Part3Constant = (1- 0.098)*((4*Gamma_L*Gamma_S)/(Gamma_S**2+2*Gamma_S*Gamma_L+Gamma_L**2+4*Delta_m**2))
	Part3 = exp(-(Gamma_L+Gamma_S)*(t1e+t2e)/2.)*cos(Delta_m*(t2e-t1e)) - exp(-(Gamma_L+Gamma_S)*(t1a+t2e)/2.)*cos(Delta_m*(t2e-t1a)) - exp(-(Gamma_L+Gamma_S)*(t1e+t2a)/2.)*cos(Delta_m*(t2e-t1a))  + exp(-(Gamma_L+Gamma_S)*(t1a+t2a)/2.)*cos(Delta_m*(t2a-t1a))
	return Constant*(Part1+Part2+Part3Constant*Part3)	


def intensity(t1,t2):
	Constant = Gamma_L*Gamma_S*propPiPiKs**2*eta**2/2.
	Part1 = exp(-Gamma_L*t1-Gamma_S*t2)
	Part2 = exp(-Gamma_L*t2-Gamma_S*t1)
	Part3 = -2*(1-zeta)*exp(-.5*(Gamma_L+Gamma_S)*(t1+t2))*cos(Delta_m*(t1-t2))
	return Constant*(Part1+Part2+Part3)	



print('SMbkg')
print('both',prob_decay_smbkg(0,0.025e-9,0,0.025e-9))
print('one 1',2*prob_decay_smbkg(0.025e-9,1,0,0.025e-9))

print('signal')
print('both',prob_decay_signal(0,0.025e-9,0,0.025e-9))
print('one 1', 2*prob_decay_signal(0.025e-9,1,0,0.025e-9))


def numintegral(t1a,t1e,t2a,t2e):
	return dblquad(lambda t1, t2: intensity(t1,t2), t1a, t1e, lambda t2: t2a, lambda t2: t2e)



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
