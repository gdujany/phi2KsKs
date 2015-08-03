from numpy import sum, sqrt, log, exp, cos, linspace
from scipy.integrate import dblquad

Gamma_L = 1/5.116e-8
Gamma_S = 1/0.89564e-10
Delta_m = 0.5289e10
propPiPiKs = 0.692
eta = 2.232e-3

def prob_deday(t_1,t_2):
	Constant = propPiPiKs**2#*eta**2/2.
	Part1 = exp(-Gamma_L*t_1-Gamma_S*t_2)-exp(-Gamma_S*t_2)-exp(-Gamma_L*t_1)+1
	Part2 = exp(-Gamma_L*t_2-Gamma_S*t_1)-exp(-Gamma_S*t_1)-exp(-Gamma_L*t_2)+1
	Part1a = exp(-Gamma_S*t_2-Gamma_S*t_1)-exp(-Gamma_S*t_1)-exp(-Gamma_S*t_2)+1
	Part3Constant = (2*(4*Gamma_L*Gamma_S)/(Gamma_S**2+2*Gamma_S*Gamma_L+Gamma_L**2+4*Delta_m))
	Part3 = exp(-(Gamma_L+Gamma_S)*(t_1+t_2)/2.)*cos(Delta_m*(t_2-t_1)) - exp(-(Gamma_L+Gamma_S)*t_1/2.)*cos(Delta_m*t_1) - exp(-(Gamma_L+Gamma_S)*t_2/2.)*cos(Delta_m*t_2)  + 1
	return Constant*(Part1a)#+Part2)#+Part3Constant*Part3)


def intensity(t1,t2):
	return 0.5*propPiPiKs**2*eta**2*(exp(-Gamma_L*t1-Gamma_S*t2) + exp(-Gamma_L*t2-Gamma_S*t1) - 2*exp(-(Gamma_S+Gamma_L)*(t1+t2)/2.)*cos(Delta_m*(t1-t2)))




print('both',prob_deday(0.025e-9,0.025e-9))
print('one 1', prob_deday(1,0.025e-9))

