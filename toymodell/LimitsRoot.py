#!/usr/bin/env python
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pylab
import scipy.optimize
from matplotlib.ticker import AutoMinorLocator
import sys, os
import ROOT as r
from ROOT import TTree, TH2D, TH1D, TString, gStyle, TMath, TLatex, gROOT, TGraph, TF1
gROOT.SetMacroPath("~/phi2KsKs/phi2KsKs/toymodell/");
from Style import rootStyle, printLHCb
rootStyle(False)


from numpy import sum, sqrt, log

from matplotlib import rc
rc("font", family="serif")


def fkt(x,a,b,c):
    return a*sqrt(x+b)+c


L = np.array([70.,75.,80.,85.,90.,95.,100.])
Limit = np.array([0.997737,0.93648,0.893126,0.845087,0.816641,0.772411,0.745026])


canvas = r.TCanvas("canvas","Canvas Title")
canvas.cd()
h_a = TH1D("h_a", "Prompt #phi", 1, 70., 100.)
h_a.GetYaxis().SetRangeUser(0.6, 1.)
h_a.Draw("p")
limits = TGraph(7,L,Limit)
limits.SetMarkerStyle(20);
limits.SetMarkerSize(1.);
limits.SetMarkerColor(4);
limits.SetLineColor(0);
limits.Draw("")
print limits.GetMinimum()
limits.SetTitle("Prompt #phi")
limits.GetXaxis().SetTitle("Integrated luminosity [fb^{-1}]")
limits.GetYaxis().SetTitle("95% C.L. #zeta_{SL} ")


fit, fehler = scipy.optimize.curve_fit(fkt,L,Limit, p0 = (1,1,1))
print(fit, fehler)

fitresults = (fit[0],fit[1],fit[2])

a = "{0[0]}*sqrt(x+{0[1]})+{0[2]}".format(fitresults)

print a

# function = TF1("fit",TString(a))

function = TF1("fit","[0]*sqrt(x+[1])+[2]",60.,110.)
function.SetParameters(0,-0.07665853)
function.SetParLimits(0,-0.1,-0.05)
function.SetParameters(1,-61.5831009)
function.SetParLimits(1,-70,-65)
function.SetParameters(2,1.21951002)
limits.Fit(function,"I0","",70.,100.);
function.Draw("same")
printLHCb()
# function.Draw("same")
canvas.Print("limits.pdf")