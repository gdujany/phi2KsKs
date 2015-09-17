#!/usr/bin/env python

import sys, os
from CompareTreeVars import getHisto, CompareTreeVars
import ROOT as r
from ROOT import TTree, TH2D, TH1D, TString, gStyle, TMath, gROOT

gROOT.SetMacroPath("~/phi2KsKs/phi2KsKs/preliminaryStudies/");


from Style import rootStyle, printLHCb
rootStyle(False)

for track in ["LL","DD","DD-DTF", "LL-DTF","DeltaTauLL","DeltaTauLD","DeltaTauLL-DTF"]:
	f = r.TFile.Open("/afs/cern.ch/work/s/sbartkow/files/phi2KsKs_incl.root", "read")
	t = f.Get("TuplePhi2KsKs/DecayTree")
	gStyle.SetOptFit(111)
	#gStyle.SetOptTitle(0)
	gStyle.SetOptTitle(1)
	gStyle.SetOptStat("e")

	canvas = r.TCanvas("canvas","Canvas Title")
	canvas.cd()
	if track == "LL-DTF":
		t.Draw("(phi_DTF_CTAU_Ks1/299.792458-Ks1_TRUETAU)*1000. >>histo(50,0,.5)","phi_DTF_CTAU_Ks1 >= 0 && phi_BKGCAT==0 && pi1_TRACK_Type ==3 && pi2_TRACK_Type ==3")
		histo=r.gROOT.FindObject("histo")
		histo.SetDirectory(0)
		t.Draw("(phi_DTF_CTAU_Ks2/299.792458-Ks2_TRUETAU)*1000. >>histo2(50,0,.5)","phi_DTF_CTAU_Ks2 >= 0 && phi_BKGCAT==0 && pi3_TRACK_Type ==3 && pi3_TRACK_Type ==3")
		histo2=r.gROOT.FindObject("histo2")
		histo2.SetDirectory(0)
		histo.Add(histo2)
	elif track == "DD-DTF":
		t.Draw("(phi_DTF_CTAU_Ks1/299.792458-Ks1_TRUETAU)*1000. >>histo(100,0,10)","phi_DTF_CTAU_Ks1 >= 0 && phi_BKGCAT==0 && pi1_TRACK_Type ==5 && pi2_TRACK_Type ==5")
		histo=r.gROOT.FindObject("histo")
		histo.SetDirectory(0)
		t.Draw("(phi_DTF_CTAU_Ks2/299.792458-Ks2_TRUETAU)*1000. >>histo2(100,0,10)","phi_DTF_CTAU_Ks2 >= 0 && phi_BKGCAT==0 && pi3_TRACK_Type ==5 && pi3_TRACK_Type ==5")
		histo2=r.gROOT.FindObject("histo2")
		histo2.SetDirectory(0)
		histo.Add(histo2)
	elif track == "LL":
		t.Draw("(Ks1_TAU-Ks1_TRUETAU)*1000. >>histo(60,-3,3)","Ks1_TAU >= 0 && phi_BKGCAT==0 && pi1_TRACK_Type ==3 && pi2_TRACK_Type ==3")
		histo=r.gROOT.FindObject("histo")
		histo.SetDirectory(0)
		t.Draw("(Ks2_TAU-Ks2_TRUETAU)*1000. >>histo2(60,-3,3)","Ks2_TAU >= 0 && phi_BKGCAT==0 && pi3_TRACK_Type ==3 && pi3_TRACK_Type ==3")
		histo2=r.gROOT.FindObject("histo2")
		histo2.SetDirectory(0)
		histo.Add(histo2)
	elif track == "DD":
		t.Draw("(Ks1_TAU-Ks1_TRUETAU)*1000. >>histo(60,-30,30)","Ks1_TAU >= 0 && phi_BKGCAT==0 && pi1_TRACK_Type ==5 && pi2_TRACK_Type ==5")
		histo=r.gROOT.FindObject("histo")
		histo.SetDirectory(0)
		t.Draw("(Ks2_TAU-Ks2_TRUETAU)*1000. >>histo2(60,-30,30)","Ks2_TAU >= 0 && phi_BKGCAT==0 && pi3_TRACK_Type ==5 && pi3_TRACK_Type ==5")
		histo2=r.gROOT.FindObject("histo2")
		histo2.SetDirectory(0)
		histo.Add(histo2)
	elif track == "DeltaTauLL":
		t.Draw("(Ks1_TAU-Ks2_TAU)*1000.-(Ks1_TRUETAU-Ks2_TRUETAU)*1000.>>histo(40,-2,2)","Ks1_TAU >= 0 && Ks2_TAU >=0 && phi_BKGCAT==0 && pi1_TRACK_Type ==3 && pi2_TRACK_Type ==3  && pi3_TRACK_Type ==3 && pi4_TRACK_Type ==3")
		histo=r.gROOT.FindObject("histo")
		histo.SetDirectory(0)
	elif track == "DeltaTauLD":
		t.Draw("(Ks1_TAU-Ks2_TAU)*1000.-(Ks1_TRUETAU-Ks2_TRUETAU)*1000.>>histo(60,-30,30)","Ks1_TAU >= 0 && Ks2_TAU >=0 && phi_BKGCAT==0 && ((pi1_TRACK_Type ==5 && pi2_TRACK_Type ==5  && pi3_TRACK_Type ==3 && pi4_TRACK_Type ==3)||(pi1_TRACK_Type ==3 && pi2_TRACK_Type ==3  && pi3_TRACK_Type ==5 && pi4_TRACK_Type ==5))")
		histo=r.gROOT.FindObject("histo")
		histo.SetDirectory(0)
	elif track == "DeltaTauLL-DTF":
		t.Draw("(phi_DTF_CTAU_Ks1/299.792458-phi_DTF_CTAU_Ks2/299.792458)*1000.-(Ks1_TRUETAU-Ks2_TRUETAU)*1000.>>histo(40,-10,10)","Ks1_TAU >= 0 && Ks2_TAU >=0 && phi_BKGCAT==0 && ((pi1_TRACK_Type ==5 && pi2_TRACK_Type ==5  && pi3_TRACK_Type ==3 && pi4_TRACK_Type ==3)||(pi1_TRACK_Type ==3 && pi2_TRACK_Type ==3  && pi3_TRACK_Type ==5 && pi4_TRACK_Type ==5))")
		histo=r.gROOT.FindObject("histo")
		histo.SetDirectory(0)
	histo.SetName("Time resolution - "+track)
	histo.SetTitle("Prompt #phi")
             
	if track == "LL-DTF":
		f = r.TF1("f","[0]/(x^2 + [1]^2/4)  ",0,10)
		f.SetParameter(0, 3.28120e-04)
		f.SetParameter(1,1.43076e-01)
		f.SetParName(0,"a")
		f.SetParName(1,"#Gamma")
	elif track == "DD-DTF":
		f = r.TF1("f","[0]/(x^2 + [1]^2/4)  ",0,10)
		f.SetParameter(0, 3.28120e-04)
		f.SetParameter(1,1.43076e-01)
		f.SetParName(0,"a")
		f.SetParName(1,"#Gamma")
	elif track == "LL":
		f = r.TF1("f","[0]/((x-[2])^2 + [1]^2/4)  ",-3,3)
		f.SetParameter(0,1.28285e-03)
		f.SetParameter(1,2.81552)
		f.SetParameter(2,1.43076e-03)
		f.SetParameter(3,5)
		f.SetParLimits(1,0,3)
		f.SetParName(0,"a")
		f.SetParName(1,"#Gamma")
		f.SetParName(2,"#mu")
		f.SetParName(3,"b") 
	elif track == "DD":
		f = r.TF1("f","[0]/((x-[2])^2 + [1]^2/4)",-30,30)
		f.SetParameter(0, 3.28120e-2)
		f.SetParameter(1,5)
		f.SetParameter(2,0)
		f.SetParLimits(1,0,30)
		f.SetParName(0,"a")
		f.SetParName(1,"#Gamma")
		f.SetParName(2,"#mu")
	elif track == "DeltaTauLL":
		f = r.TF1("f","[0]/((x-[2])^2 + [1]^2/4) ",-2,2);
		f.SetParameter(0, 3.28120e-04)
		f.SetParameter(1,1.43076)
		f.SetParLimits(1,0,1)
		f.SetParameter(2,1.43076e-03)
		f.SetParName(0,"a")
		f.SetParName(1,"#Gamma")
		f.SetParName(2,"#mu")
	elif track == "DeltaTauLL-DTF":
		f = r.TF1("f","[0]/((x-[2])^2 + [1]^2/4) ",-4,4);
		f.SetParameter(0, 3.28120e-04)
		f.SetParameter(1,3)
		f.SetParLimits(1,1,10)
		f.SetParameter(2,0)
		f.SetParLimits(2,-.001,.001)
		f.SetParName(0,"a")
		f.SetParName(1,"#Gamma")
		f.SetParName(2,"#mu")
	elif track == "DeltaTauLD":
		f = r.TF1("f","[0]/((x-[2])^2 + [1]^2/4) ",-30,30);
		f.SetParameter(0, 3.28120e-2)
		f.SetParameter(1,5)
		f.SetParameter(2,0)
		f.SetParLimits(1,0,3)
		f.SetParName(0,"a")
		f.SetParName(1,"#Gamma")
		f.SetParName(2,"#mu")

	if "DTF" in track and not "Delta" in track:
		histo.Fit(f,"I0","",-1,5);
		histo.GetXaxis().SetTitle("|t(reconstructed)-t(true)| [ps]");
		if "LL" in track:
			histo.GetYaxis().SetTitle("MC events/0.001ps");
		else:
			histo.GetYaxis().SetTitle("MC events/0.1ps");
		
	elif track == "DD":
		histo.Fit(f,"I0","",-30,30);
		histo.GetXaxis().SetTitle("t(reconstructed)-t(true) [ps]");
		histo.GetYaxis().SetTitle("MC events/ps");
	elif track == "LL":
		histo.Fit(f,"I0","",-2,2);
		histo.GetXaxis().SetTitle("t(reconstructed)-t(true) [ps]");
		histo.GetYaxis().SetTitle("MC events/0.2ps");
	elif "DeltaTauLL" ==track:
		histo.GetYaxis().SetTitle("MC events/0.1ps")
		histo.Fit(f,"I","",-1,1);
		histo.GetXaxis().SetTitle("#Delta t(reconstructed)- #Delta t(true) [ps]");
	elif "DeltaTauLL-DTF" == track:
		histo.GetYaxis().SetTitle("MC events/0.5ps")
		histo.Fit(f,"I","",-10,10);
		histo.GetXaxis().SetTitle("#Delta t(reconstructed)- #Delta t(true) [ps]");
	elif track == "DeltaTauLD" :
		histo.GetYaxis().SetTitle("MC events/ps")
		histo.Fit(f,"I","",-200,200);
		histo.GetXaxis().SetTitle("#Delta t(reconstructed)- #Delta t(true) [ps]");
	

	histo.Draw()
 


	#f.SetParameters(1200,0.001,1,0.000)
	f.SetLineColor(2)
	f.Draw("same")
	canvas.Update()
	printLHCb(x=0.35)
	canvas.Print("time_res_incl/timeResolution-"+track+".pdf")

	del t
	#del f
	del canvas
	del histo
	if not ("DeltaTauLL" in track or track == "DeltaTauLD"):
		del histo2


dictionary = {
	"LL1" : "&& pi1_TRACK_Type ==3 && pi2_TRACK_Type == 3",
	"LL2" : "&& pi3_TRACK_Type ==3 && pi4_TRACK_Type ==3",
	"DD1" : "&& pi1_TRACK_Type ==5 && pi2_TRACK_Type == 5",
	"DD2" : "&& pi3_TRACK_Type ==5 && pi4_TRACK_Type ==5",
	"all1": "",
	"all2": "",
	"LL-DTF1" : "&& pi1_TRACK_Type ==3 && pi2_TRACK_Type == 3",
	"LL-DTF2" : "&& pi3_TRACK_Type ==3 && pi4_TRACK_Type ==3",
	"DD-DTF1" : "&& pi1_TRACK_Type ==5 && pi2_TRACK_Type == 5",
	"DD-DTF2" : "&& pi3_TRACK_Type ==5 && pi4_TRACK_Type ==5",
	"all-DTF1": "",
	"all-DTF2": "",
}
f = r.TFile.Open("/afs/cern.ch/work/s/sbartkow/files/phi2KsKs_incl.root", "read")
t = f.Get("TuplePhi2KsKs/DecayTree")
for track in ["LL","DD","all","DD-DTF", "LL-DTF","all-DTF"]:#
	gStyle.SetOptFit(111)
	gStyle.SetOptTitle(1)
	gStyle.SetOptStat(0)
	if "LL" in track:
		maximum = "110"
		maximum_f = 110.
	else:
		maximum = "450"
		maximum_f = 450.

	if "DTF" in track:
		if "LL" in track:
			h_a = TH2D("h_a", track, 1, 0, maximum_f,1,-100,400)
		else:
			h_a = TH2D("h_a", track, 1, 0, maximum_f,1,-400,400)
	else:
		h_a = TH2D("h_a", track, 1, 0, maximum_f,1,-20,20)	

	
	h_a.GetXaxis().SetTitle("t(true) [ps]") 
  	h_a.GetYaxis().SetTitle("t(reconstructed)-t(true) [ps]")
  	h_a.SetTitle("Prompt #phi")
  	canvas = r.TCanvas("canvas","Canvas Title")
  	h_a.Draw("p");
	canvas.cd()
	ntrack1 = "{"+track+"1}"
	ntrack2 = "{"+track+"2}"
	nntrack1 = ntrack1.format(**dictionary)
	nntrack2 = ntrack2.format(**dictionary)

	if "DTF" in track:
		t.Draw("(phi_DTF_CTAU_Ks1/299.792458-Ks1_TRUETAU)*1000:Ks1_TRUETAU*1000","phi_DTF_CTAU_Ks1 >= 0 && phi_BKGCAT==0"+nntrack1, "same")
		t.Draw("(phi_DTF_CTAU_Ks2/299.792458-Ks2_TRUETAU)*1000:Ks2_TRUETAU*1000","phi_DTF_CTAU_Ks2 >= 0 && phi_BKGCAT==0"+nntrack2, "same")
	else:
		t.Draw("(Ks1_TAU-Ks1_TRUETAU)*1000:Ks1_TRUETAU*1000","phi_BKGCAT==0"+nntrack1, "same")
		t.Draw("(Ks2_TAU-Ks2_TRUETAU)*1000:Ks2_TRUETAU*1000","phi_BKGCAT==0"+nntrack2, "same")
	canvas.Update()
	printLHCb()
	canvas.Print("time_res_incl/"+track+".pdf")
	del canvas
	del h_a

	if "DTF" in track:
		t.Draw("(phi_DTF_CTAU_Ks1/299.792458-Ks1_TRUETAU)*1000:Ks1_TRUETAU*1000 >>histo(20,0,"+maximum+")","phi_DTF_CTAU_Ks1 >= 0 && phi_BKGCAT==0"+nntrack1, "P0 prof")
		histo=r.gROOT.FindObject("histo")
		histo.SetDirectory(0)
		t.Draw("(phi_DTF_CTAU_Ks2/299.792458-Ks2_TRUETAU)*1000:Ks2_TRUETAU*1000 >>histo2(20,0,"+maximum+")","phi_DTF_CTAU_Ks2 >= 0 && phi_BKGCAT==0"+nntrack2, "P0 prof")
		histo2=r.gROOT.FindObject("histo2")
		histo2.SetDirectory(0)
		histo.Add(histo2)
		histo.SetTitle("Prompt #phi")
		histo.GetXaxis().SetTitle("t(true) [ps]") 
  		histo.GetYaxis().SetTitle("t(reconstructed)-t(true) [ps]")
		canvas = r.TCanvas("canvas","Canvas Title")
		canvas.cd()
		histo.Draw("same")
		printLHCb(x=0.35,y=.4)
		canvas.Update()
		canvas.Print("time_res_incl/"+track+"-prof.pdf")
	else:
		t.Draw("(Ks1_TAU-Ks1_TRUETAU)*1000:Ks1_TRUETAU*1000 >>histo(20,0,"+maximum+")","phi_BKGCAT==0"+nntrack1, "e prof")
		histo=r.gROOT.FindObject("histo")
		histo.SetDirectory(0)
		t.Draw("(Ks2_TAU-Ks2_TRUETAU)*1000:Ks2_TRUETAU*1000 >>histo2(20,0,"+maximum+")","phi_BKGCAT==0"+nntrack2, "e prof")
		histo2=r.gROOT.FindObject("histo2")
		histo2.SetDirectory(0)
		histo.Add(histo2)
		histo.SetTitle("Prompt #phi")
		histo.GetXaxis().SetTitle("t(true) [ps]") 
  		histo.GetYaxis().SetTitle("t(reconstructed)-t(true) [ps]")
		canvas = r.TCanvas("canvas","Canvas Title")
		canvas.cd()
		histo.Draw("same")
		canvas.Update()
		printLHCb(x=0.35)
		canvas.Print("time_res_incl/"+track+"-prof.pdf")

	del canvas
	del histo2
	del histo

h_c = TH2D("h_c", track, 1, -20,20,1,-20,20)
h_c.GetXaxis().SetTitle("t_{1}(reconstructed)-t_{1}(true) [ps]")
h_c.GetYaxis().SetTitle("t_{2}(reconstructed)-t_{2}(true) [ps]")
h_c.GetYaxis().SetTitleOffset(1.5)
canvas = r.TCanvas("canvas","Canvas Title",5)
#h_c.SetTitle("DTF")
h_c.SetTitle("Prompt #phi")
h_c.Draw("p");
t.Draw("(phi_DTF_CTAU_Ks2/299.792458-Ks2_TRUETAU)*1000:(phi_DTF_CTAU_Ks1/299.792458-Ks1_TRUETAU)*1000","phi_DTF_CTAU_Ks1 >= 0 && phi_DTF_CTAU_Ks2 >= 0 && phi_BKGCAT==0","same")
canvas.Print("time_res_incl/DTF_2D.pdf")
del canvas
canvas = r.TCanvas("canvas","Canvas Title",5)
h_c.SetTitle("Prompt #phi")
h_c.SetTitleSize(0.5,"t")
h_c.Draw("p")
t.Draw("(Ks2_TAU-Ks2_TRUETAU)*1000:(Ks1_TAU-Ks1_TRUETAU)*1000","phi_BKGCAT==0", "same")
printLHCb(x=0.35)
canvas.Print("time_res_incl/UReco_2D.pdf")


