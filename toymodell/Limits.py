import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pylab
import scipy.optimize
from matplotlib.ticker import AutoMinorLocator

from numpy import sum, sqrt, log

from matplotlib import rc
rc("font", family="serif")


def fkt(x,a,b,c):
    return a*sqrt(x+b)+c

# x= np.linspace(0,200,1000)
# a = np.loadtxt("Daten/704/gamma_Cu.txt", unpack=True)
# plt.plot(x,y,'b.', label="Messpunkte")
# plt.legend()
# plt.xlabel("...")
# plt.ylable("...")
# plt.show()
# fit, fehler = scipy.optimize.curve_fit(fkt,x,y, p0 = (1,1,1))
# plt.savefig("plot.pdf", bbox = "tight")

L = (70,75,80,85,90,95,100)
Limit = (0.997737,0.93648,0.893126,0.845087,0.816641,0.772411,0.745026)
#Kloe = (.098,.098,.098,.098,.098,.098,.098)

fit, fehler = scipy.optimize.curve_fit(fkt,L,Limit, p0 = (1,1,1))
print(fit, fehler)
fig, ax = plt.subplots()
plt.plot(L,Limit,'b.')
#plt.plot(L,Kloe,label='KLOE 95\%CL')
plt.plot(L,fkt(L,fit[0],fit[1],fit[2]),'k-',label='Predicted 95\%CL')
# plt.legend(loc=1,frameon=False)
   
plt.xlabel('                                   Integrated Luminosity [fb$^{-1}$]',size=18)

plt.ylabel('                               $\zeta_{SL}$, predicted 95%CL  ',size=18)
minorLocatorx   = AutoMinorLocator()
minorLocatory   = AutoMinorLocator()
plt.tick_params(axis='both', which='major', labelsize=15)
rc("font", family="serif")
plt.text(90, 0.95,'LHCb Unofficial', ha='center', va='center', size = 20)
ax.xaxis.set_minor_locator(minorLocatorx)
ax.yaxis.set_minor_locator(minorLocatory)
plt.tick_params(which='both', width=2)
plt.tick_params(which='major', length=7)
plt.tick_params(which='minor', length=4, color='b')
# plt.show()
plt.savefig("limits.pdf", bbox = "tight")


