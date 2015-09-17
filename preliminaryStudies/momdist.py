#!/usr/bin/env python

import sys, os
from CompareTreeVars import getHisto, CompareTreeVars
import ROOT as r
from ROOT import TTree, TH2D, TH1D, TString, gStyle, TMath, TLatex, gROOT
import LHCbStyle
from Style import rootStyle

gROOT.SetMacroPath("~/phi2KsKs/phi2KsKs/preliminaryStudies/");
# gROOT.ProcessLine(".x LHCbStyle.C")
# # LHCbStyle()

from Style import rootStyle, printLHCb
lhcbStyle = rootStyle(False)


f = r.TFile.Open("/afs/cern.ch/work/s/sbartkow/files/data2012.root", "read")
t = f.Get("TuplePhi2KsKs/DecayTree")
# gStyle.SetOptFit(111)
# gStyle.SetOptTitle(0)

lhcbStyle.SetOptTitle(0)


t.Draw("Ks1_PT/1000. >>histo(100,0,10)","Ks1_TAU>0.005 && Ks1_TAU <0.1")#,"pi1_TRACK_Type==3 && pi2_TRACK_Type==3")
histo=r.gROOT.FindObject("histo")
histo.SetDirectory(0)
t.Draw("Ks2_PT/1000.>>histo2(100,0,10)","Ks2_TAU>0.005 && Ks2_TAU <0.1")#,"pi3_TRACK_Type==3 && pi4_TRACK_Type==3")
histo2=r.gROOT.FindObject("histo2")
histo2.SetDirectory(0)
histo.Add(histo2)

canvas = r.TCanvas("canvas","Canvas Title")
canvas.cd()
histo.Draw()
histo.GetXaxis().SetTitle("p_{T}(K_{S}) [GeV]");
histo.GetYaxis().SetTitle("[a.u.]");
# funct1 = r.TF1("f1","[0]*(pow(x*1000,[1])*exp(-1000*[2]*x))",0,10)
funct1 = r.TF1("f1","30*(pow(x*1000,1.52)*exp(-1000*2.19e-3*x))",0,10)
funct1.SetLineColor(2)
funct1.SetParLimits(0,0,50)
funct1.SetParLimits(1,0,10)
funct1.SetParLimits(2,0,10)
funct1.SetParameters(1,1.52)
funct1.SetParameters(2,2.19e-3)
funct1.SetParameters(0,.3)
# funct1.Draw("same")
# funct2 = r.TF1("f2",".2*(pow(x*1000,2.19)*exp(-1.52e-3*1000*x)) ",0,10);
# funct2.SetLineColor(2)
# funct2.Draw("same")
# histo.Fit(funct1,"I0","",0,10);
funct1.Draw("same")
printLHCb()
canvas.Print("mommodel.pdf")




