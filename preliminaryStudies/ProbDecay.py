from numpy import sum, sqrt, log, exp, cos, linspace
from scipy.integrate import dblquad
from matplotlib import pyplot as plt
import numpy as np

Gamma_L = 1/5.116e-8
Gamma_S = 1/0.89564e-10
Delta_m = 0.5289e10
propPiPiKs = 0.692
eta = 2.232e-3

def prob_decay_smbkg(t1a,t1e,t2a,t2e):
	Constant = propPiPiKs**2*eta**2/2.
	Part1 = exp(-Gamma_L*t1e-Gamma_S*t2e)-exp(-Gamma_L*t1e-Gamma_S*t2a)-exp(-Gamma_L*t1a-Gamma_S*t2e)+exp(-Gamma_L*t1a-Gamma_S*t2a)
	Part2 = exp(-Gamma_S*t1e-Gamma_L*t2e)-exp(-Gamma_S*t1e-Gamma_L*t2a)-exp(-Gamma_S*t1a-Gamma_L*t2e)+exp(-Gamma_S*t1a-Gamma_L*t2a)
	Part3Constant = (2*(4*Gamma_L*Gamma_S)/(Gamma_S**2+2*Gamma_S*Gamma_L+Gamma_L**2+4*Delta_m))
	Part3 = exp(-(Gamma_L+Gamma_S)*(t1e+t2e)/2.)*cos(Delta_m*(t2e-t1e)) - exp(-(Gamma_L+Gamma_S)*(t1a+t2e)/2.)*cos(Delta_m*(t2e-t1a)) - exp(-(Gamma_L+Gamma_S)*(t1e+t2a)/2.)*cos(Delta_m*(t2e-t1a))  + exp(-(Gamma_L+Gamma_S)*(t1a+t2a)/2.)*cos(Delta_m*(t2a-t1a))
	return Constant*(Part1+Part2+Part3Constant*Part3)




def prob_decay_signal(t1a,t1e,t2a,t2e):
	# return (exp(-Gamma_S*(t1a+t2a))-exp(-Gamma_S*(t1e+t2a))-exp(-Gamma_S*(t1a+t2e))+exp(-Gamma_S*(t1e+t2e)))*propPiPiKs**2
	Constant = propPiPiKs**2*eta**2/2.
	Part1 = exp(-Gamma_L*t1e-Gamma_S*t2e)-exp(-Gamma_L*t1e-Gamma_S*t2a)-exp(-Gamma_L*t1a-Gamma_S*t2e)+exp(-Gamma_L*t1a-Gamma_S*t2a)
	Part2 = exp(-Gamma_S*t1e-Gamma_L*t2e)-exp(-Gamma_S*t1e-Gamma_L*t2a)-exp(-Gamma_S*t1a-Gamma_L*t2e)+exp(-Gamma_S*t1a-Gamma_L*t2a)
	Part3Constant = (1- 0.098)*(2*(4*Gamma_L*Gamma_S)/(Gamma_S**2+2*Gamma_S*Gamma_L+Gamma_L**2+4*Delta_m))
	Part3 = exp(-(Gamma_L+Gamma_S)*(t1e+t2e)/2.)*cos(Delta_m*(t2e-t1e)) - exp(-(Gamma_L+Gamma_S)*(t1a+t2e)/2.)*cos(Delta_m*(t2e-t1a)) - exp(-(Gamma_L+Gamma_S)*(t1e+t2a)/2.)*cos(Delta_m*(t2e-t1a))  + exp(-(Gamma_L+Gamma_S)*(t1a+t2a)/2.)*cos(Delta_m*(t2a-t1a))
	return Constant*(Part1+Part2+Part3Constant*Part3)	


x = np.linspace(0,.05e-8,100)

plt.plot(x,prob_decay_smbkg(0,x,0,.025e-9),label = 'sm bkg')
plt.plot(x,prob_decay_signal(0,x,0,.025e-9),label = 'signal')
plt.legend()
#plt.yscale('log')
plt.show()
plt.clf()
plt.plot(x,prob_decay_smbkg(0,x,.025e-9,1),label = 'sm bkg')
plt.plot(x,prob_decay_signal(0,x,.025e-9,1),label = 'signal')
plt.legend()
plt.yscale('log')
plt.show()
plt.clf()



print('SMbkg')
print('both',prob_decay_smbkg(0,0.025e-9,0,0.025e-9))
print('one 1',2*prob_decay_smbkg(0.025e-9,1,0,0.025e-9))

print('signal')
print('both',prob_decay_signal(0,0.025e-9,0,0.025e-9))
print('one 1', 2*prob_decay_signal(0.025e-9,1,0,0.025e-9))

