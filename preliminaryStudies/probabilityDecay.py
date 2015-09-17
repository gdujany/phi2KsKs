#!/usr/bin/env python

# Couple of imports
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import sympy
from scipy.integrate import dblquad
from math import *

# Various constants
tauKS = 89.564 # ps
tauKL = 5.116e4 # ps
GKS = 1./tauKS  # ps^-1
GKL = 1./tauKL  # ps^-1
Dm =  0.5293e-2  # ps^-1

BKs2PiPi = 0.692
BKl2PiPi = 1.967e-3

# Times for a Ks to be in the beampipe or reconstructed
tBeamPipe = 25
tReco = 200

# Max value decoherence parameter from KLOE
Z_sl = 0.098

def I_entangled(t1, t2):
    return np.exp(-GKL*t1-GKS*t2)+np.exp(-GKS*t1-GKL*t2)-2*np.exp(-(GKS+GKL)*(t1+t2)/2)*np.cos(Dm*(t1-t2))

def I_CPTV(t1, t2):
    return np.exp(-GKL*t1-GKS*t2)+np.exp(-GKS*t1-GKL*t2)-2*(1-Z_sl)*np.exp(-(GKS+GKL)*(t1+t2)/2)*np.cos(Dm*(t1-t2))

def I_KsKs(t1, t2):
    return np.exp(-GKS*t1-GKS*t2)


def getPdfCdf(f):
    '''
    Get a function as input and return the pdf apropriately normalised and a function to compute definite integrals
    '''
    Int = dblquad(f, 0, np.inf, # limits t2
                  lambda x : 0, # limits t1
                  lambda x: np.inf)[0]

    def pdf(t1, t2):
        return f(t1, t2)/Int

    def cdf(t1min, t1max, t2min, t2max):
        return dblquad(pdf, t2min, t2max, # limits t2
                       lambda x : t1min, # limits t1
                       lambda x: t1max)[0]

    return pdf, cdf


pdf_entangled, cdf_entangled = getPdfCdf(I_entangled)
pdf_CPTV, cdf_CPTV = getPdfCdf(I_CPTV)
pdf_KsKs, cdf_KsKs = getPdfCdf(I_KsKs)

print
print '{:<20}{:^40}{:^40}'.format('', 'only 1 Ks inside the beam-pipe','2 Ks Inside the beam-pipe')
print '{:<20}{:^40.2e}{:^40.2e}'.format('CPV Background',2*cdf_entangled(tBeamPipe, tReco, 0, tBeamPipe)*BKs2PiPi*BKl2PiPi,  cdf_entangled(0, tBeamPipe, 0, tBeamPipe)*BKs2PiPi*BKl2PiPi)
print '{:<20}{:^40.2e}{:^40.2e}'.format('With CPTV', 2*cdf_CPTV(tBeamPipe, tReco, 0, tBeamPipe)*BKs2PiPi*BKl2PiPi, cdf_CPTV(0, tBeamPipe, 0, tBeamPipe)*BKs2PiPi*BKl2PiPi)
print '{:<20}{:^40.2e}{:^40.2e}'.format('KsKs', 2*cdf_KsKs(tBeamPipe, tReco, 0, tBeamPipe)*BKs2PiPi*BKs2PiPi, cdf_KsKs(0, tBeamPipe, 0, tBeamPipe)*BKs2PiPi*BKs2PiPi)
