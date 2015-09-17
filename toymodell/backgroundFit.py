#!/usr/bin/env python
import sys, os
from CompareTreeVars import getHisto, CompareTreeVars
import ROOT as r
from ROOT import TTree
from ROOT import gStyle
from ROOT import TMath


f = r.TFile.Open("../../files/Ds_Phi2KsKs_2012.root", "read")
t = f.Get("TuplePhi2KsKs/DecayTree")
gStyle.SetOptFit(111)
gStyle.SetOptTitle(0)
canvas = r.TCanvas("canvas","Canvas Title")
canvas.cd()
t.Draw("abs(Ks1_TAU-Ks2_TAU)>>histo(10,0,0.004)","Ks1_TAU < 0.2 && Ks2_TAU < 0.2 && abs(Ks1_TAU-Ks2_TAU)<.004 && sqrt(Ks1_ENDVERTEX_X^2 + Ks1_ENDVERTEX_Y^2) < 7 && (Ks2_ENDVERTEX_X^2 + Ks2_ENDVERTEX_Y^2)<7")
histo=r.gROOT.FindObject("histo")
histo.SetDirectory(0)
histo.SetName("#Delta#tau")

f = r.TF1("f"," [0]*TMath::Exp([1]*(x+0.0002))",0.0000,.004)
# f.SetParameter(0,7232)
# f.SetParameter(1,2.57143e-04 )
# f.SetParameter(2,1.75292e-04)
# f.SetParameter(3,5)
f.SetParName(0,"N")
f.SetParName(1,"#Gamma_{S}")
histo.Fit(f,"I0","",0,0.004);
histo.GetXaxis().SetTitle("|#tau_{1}-#tau_{2}|[ns]");
histo.GetYaxis().SetTitle("MC events / 0.4 ps");
histo.GetYaxis().SetTitleOffset(1.3)


histo.Draw()

#f.SetParameters(1200,0.001,1,0.000)
f.Draw("same")
canvas.Update()
canvas.Print("BackgroundModell.pdf")

