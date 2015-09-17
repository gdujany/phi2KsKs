#!/usr/bin/env python

import sys, os
from CompareTreeVars import getHisto, CompareTreeVars
import ROOT as r
from ROOT import TTree, TH2D, TH1D, TString, gStyle, TMath, TLatex, gROOT, TCanvas, TLegend, kRed, kBlue
import LHCbStyle
from Style import rootStyle

gROOT.SetMacroPath("~/phi2KsKs/phi2KsKs/preliminaryStudies/");
# gROOT.ProcessLine(".x LHCbStyle.C")
# # LHCbStyle()

from Style import rootStyle, printLHCb
lhcbStyle = rootStyle(False)



mc_incl = r.TFile.Open("/afs/cern.ch/work/s/sbartkow/files/phi2KsKs_incl.root", "read")
mc_Ds = r.TFile.Open("/afs/cern.ch/work/s/sbartkow/files/Ds_Phi2KsKs_Ds.root", "read")
data_incl = r.TFile.Open("/afs/cern.ch/work/s/sbartkow/files/data2012.root", "read")
data_Ds = r.TFile.Open("/afs/cern.ch/work/s/sbartkow/files/Ds_Phi2KsKs_2012.root", "read")

mc_incl_t = mc_incl.Get("TuplePhi2KsKs/DecayTree")
mc_Ds_t = mc_Ds.Get("TuplePhi2KsKs/DecayTree")
data_incl_t = data_incl.Get("TuplePhi2KsKs/DecayTree")	
data_Ds_t = data_Ds.Get("TuplePhi2KsKs/DecayTree")


mc_incl_t.Draw("phi_M >>h_m_phi_mc_incl(50,990,1050)","(sqrt(Ks1_ENDVERTEX_X*Ks1_ENDVERTEX_X+Ks1_ENDVERTEX_Y*Ks1_ENDVERTEX_Y)<7||sqrt(Ks2_ENDVERTEX_X*Ks2_ENDVERTEX_X+Ks2_ENDVERTEX_Y*Ks2_ENDVERTEX_Y)<7)");
h_m_phi_mc_incl=gROOT.FindObject("h_m_phi_mc_incl");
h_m_phi_mc_incl.SetDirectory(0);
data_incl_t.Draw("phi_M >>h_m_phi_data_incl(50,990,1050)","(sqrt(Ks1_ENDVERTEX_X*Ks1_ENDVERTEX_X+Ks1_ENDVERTEX_Y*Ks1_ENDVERTEX_Y)<7||sqrt(Ks2_ENDVERTEX_X*Ks2_ENDVERTEX_X+Ks2_ENDVERTEX_Y*Ks2_ENDVERTEX_Y)<7)");
h_m_phi_data_incl=gROOT.FindObject("h_m_phi_data_incl");
h_m_phi_data_incl.SetDirectory(0);
mc_Ds_t.Draw("phi_M >>h_m_phi_mc_Ds(40,990,1050)","(sqrt(Ks1_ENDVERTEX_X*Ks1_ENDVERTEX_X+Ks1_ENDVERTEX_Y*Ks1_ENDVERTEX_Y)<7||sqrt(Ks2_ENDVERTEX_X*Ks2_ENDVERTEX_X+Ks2_ENDVERTEX_Y*Ks2_ENDVERTEX_Y)<7)&& Ds_M > 1955 && Ds_M < 1985&& phi_IPCHI2_OWNPV >=50");
h_m_phi_mc_Ds=gROOT.FindObject("h_m_phi_mc_Ds");
h_m_phi_mc_Ds.SetDirectory(0);
data_Ds_t.Draw("phi_M >>h_m_phi_data_Ds(40,990,1050)","(sqrt(Ks1_ENDVERTEX_X*Ks1_ENDVERTEX_X+Ks1_ENDVERTEX_Y*Ks1_ENDVERTEX_Y)<7||sqrt(Ks2_ENDVERTEX_X*Ks2_ENDVERTEX_X+Ks2_ENDVERTEX_Y*Ks2_ENDVERTEX_Y)<7)&& Ds_M > 1955 && Ds_M < 1985&& phi_IPCHI2_OWNPV >=50");
h_m_phi_data_Ds=gROOT.FindObject("h_m_phi_data_Ds");
h_m_phi_data_Ds.SetDirectory(0);	
mc_Ds_t.Draw("Ds_M >>h_m_Ds_mc_Ds(50,1920,2020)","(sqrt(Ks1_ENDVERTEX_X*Ks1_ENDVERTEX_X+Ks1_ENDVERTEX_Y*Ks1_ENDVERTEX_Y)<7||sqrt(Ks2_ENDVERTEX_X*Ks2_ENDVERTEX_X+Ks2_ENDVERTEX_Y*Ks2_ENDVERTEX_Y)<7)&& phi_M > 1010 && phi_M < 1030");
h_m_Ds_mc_Ds=gROOT.FindObject("h_m_Ds_mc_Ds");
h_m_Ds_mc_Ds.SetDirectory(0);	
data_Ds_t.Draw("Ds_M >>h_m_Ds_data_Ds(50,1920,2020)","(sqrt(Ks1_ENDVERTEX_X*Ks1_ENDVERTEX_X+Ks1_ENDVERTEX_Y*Ks1_ENDVERTEX_Y)<7||sqrt(Ks2_ENDVERTEX_X*Ks2_ENDVERTEX_X+Ks2_ENDVERTEX_Y*Ks2_ENDVERTEX_Y)<7)&& phi_M > 1010 && phi_M < 1030");
h_m_Ds_data_Ds=gROOT.FindObject("h_m_Ds_data_Ds");
h_m_Ds_data_Ds.SetDirectory(0);		
c_m_phi_incl = TCanvas("c_m_phi_incl","m_phi",1);
l_m_phi_incl = TLegend(0.65, 0.70, .85, .85);
c_m_phi_Ds = TCanvas("c_m_phi_Ds","m_phi",2);
l_m_phi_Ds = TLegend(0.6, 0.70, .85, .85);
c_m_Ds = TCanvas("c_m_Ds","m_Ds",2);
l_m_Ds_Ds = TLegend(0.6, 0.70, .85, .85);
c_m_phi_incl.cd();
h_m_phi_mc_incl.GetXaxis().SetTitle("m(#phi)[MeV]");
h_m_phi_mc_incl.SetLineColor(kRed);
h_m_phi_mc_incl.GetYaxis().SetTitle("Entries normalized to unit area");
h_m_phi_mc_incl.GetYaxis().SetTitleOffset(1.3);
h_m_phi_mc_incl.DrawNormalized("");
l_m_phi_incl.AddEntry(h_m_phi_mc_incl, "MC prompt #phi", "l");
h_m_phi_data_incl.SetLineColor(kBlue);
h_m_phi_data_incl.DrawNormalized("same");
l_m_phi_incl.AddEntry(h_m_phi_data_incl, "2012 data", "l");
l_m_phi_incl.Draw();
printLHCb(x=0.35)
c_m_phi_incl.Print("m_phi_incl.pdf");
c_m_phi_Ds.cd();
h_m_phi_mc_Ds.GetXaxis().SetTitle("m(#phi)[MeV]");
h_m_phi_mc_Ds.SetLineColor(kRed);
h_m_phi_mc_Ds.GetYaxis().SetTitle("Entries normalized to unit area");
h_m_phi_mc_Ds.GetYaxis().SetTitleOffset(1.5);
h_m_phi_mc_Ds.DrawNormalized("");
l_m_phi_Ds.AddEntry(h_m_phi_mc_Ds, "MC D_{S} #rightarrow #phi #pi", "l");
h_m_phi_data_Ds.SetLineColor(kBlue);
h_m_phi_data_Ds.DrawNormalized("same");
l_m_phi_Ds.AddEntry(h_m_phi_data_Ds, "2012 data", "l");
l_m_phi_Ds.Draw();
printLHCb(x=0.35)
c_m_phi_Ds.Print("m_phi_Ds.pdf");
c_m_Ds.cd();
h_m_Ds_mc_Ds.GetXaxis().SetTitle("m(D_{S})[MeV]");
h_m_Ds_mc_Ds.SetLineColor(kRed);
h_m_Ds_mc_Ds.GetYaxis().SetTitle("Entries normalized to unit area");
h_m_Ds_mc_Ds.GetYaxis().SetTitleOffset(1.5);
h_m_Ds_mc_Ds.DrawNormalized("");
l_m_Ds_Ds.AddEntry(h_m_Ds_mc_Ds, "MC D_{S} #rightarrow #phi #pi", "l");
h_m_Ds_data_Ds.SetLineColor(kBlue);
h_m_Ds_data_Ds.DrawNormalized("same");
l_m_Ds_Ds.AddEntry(h_m_Ds_data_Ds, "2012 data", "l");
l_m_Ds_Ds.Draw();
printLHCb(x=0.35)
c_m_Ds.Print("m_Ds_Ds.pdf");


