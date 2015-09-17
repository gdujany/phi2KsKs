import ROOT as r
from ROOT import TTree, TFile, gStyle, TH1D,TCanvas
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt


f = r.TFile.Open("/afs/cern.ch/work/s/sbartkow/files/Ds_Phi2KsKs_Dsnew.root", "read")
t = f.Get("TuplePhi2KsKs/DecayTree")
gStyle.SetOptFit(111)
gStyle.SetOptTitle(0)

canv1 = TCanvas("canvcorr", "correlated", 1);
h_correlated = TH1D("h_correlated", "correlated",1,0,1);
h_correlated.GetXaxis().SetTitle("");
h_correlated.GetYaxis().SetTitle("Events");
#h_correlated.SetBit(TH1::kCanRebin);

canv2 = TCanvas("canvanticorr", "anticorrelated", 1);
h_acorrelated = TH1D("h_acorrelated", "anticorrelated",1,0,1);
h_acorrelated.GetXaxis().SetTitle("");
h_acorrelated.GetYaxis().SetTitle("Events");
#h_acorrelated.SetBit(TH1::kCanRebin);

for event in t:
	BKG = event.phi_BKGCAT
	CHI2 = event.Ds_DTF_CHI2_PV
	if (not BKG == 0) or CHI2 < 0:
		continue
	pi1_DTF = (event.Ds_DTF_VX_pi1,event.Ds_DTF_VY_pi1,event.Ds_DTF_VZ_pi1)
	pi1_TRUE = (event.pi1_TRUEENDVERTEX_X,event.pi1_TRUEENDVERTEX_Y,event.pi1_TRUEENDVERTEX_Z)
	pi2_DTF = (event.Ds_DTF_VX_pi2,event.Ds_DTF_VY_pi2,event.Ds_DTF_VZ_pi2)
	pi2_TRUE = (event.pi2_TRUEENDVERTEX_X,event.pi2_TRUEENDVERTEX_Y,event.pi2_TRUEENDVERTEX_Z)	
	pi3_DTF = (event.Ds_DTF_VX_pi3,event.Ds_DTF_VY_pi3,event.Ds_DTF_VZ_pi3)
	pi3_TRUE = (event.pi3_TRUEENDVERTEX_X,event.pi3_TRUEENDVERTEX_Y,event.pi3_TRUEENDVERTEX_Z)
	pi4_DTF = (event.Ds_DTF_VX_pi4,event.Ds_DTF_VY_pi4,event.Ds_DTF_VZ_pi4)
	pi4_TRUE = (event.pi4_TRUEENDVERTEX_X,event.pi4_TRUEENDVERTEX_Y,event.pi4_TRUEENDVERTEX_Z)
	pis_DTF = (event.Ds_DTF_VX_pis,event.Ds_DTF_VY_pis,event.Ds_DTF_VZ_pis)
	pis_TRUE = (event.pis_TRUEENDVERTEX_X,event.pis_TRUEENDVERTEX_Y,event.pis_TRUEENDVERTEX_Z)
	Ks1_DTF = (event.Ds_DTF_VX_Ks1,event.Ds_DTF_VY_Ks1,event.Ds_DTF_VZ_Ks1)
	Ks1_TRUE = (event.Ks1_TRUEENDVERTEX_X,event.Ks1_TRUEENDVERTEX_Y,event.Ks1_TRUEENDVERTEX_Z)
	Ks2_DTF = (event.Ds_DTF_VX_Ks2,event.Ds_DTF_VY_Ks2,event.Ds_DTF_VZ_Ks2)
	Ks2_TRUE = (event.Ks2_TRUEENDVERTEX_X,event.Ks2_TRUEENDVERTEX_Y,event.Ks2_TRUEENDVERTEX_Z)
	phi_DTF = (event.Ds_DTF_VX_phi,event.Ds_DTF_VY_phi,event.Ds_DTF_VZ_phi)
	phi_TRUE = (event.phi_TRUEENDVERTEX_X,event.phi_TRUEENDVERTEX_Y,event.phi_TRUEENDVERTEX_Z)
	Ds_DTF = (event.Ds_DTF_VX_Ds,event.Ds_DTF_VY_Ds,event.Ds_DTF_VZ_Ds)
	Ds_TRUE = (event.Ds_TRUEENDVERTEX_X,event.Ds_TRUEENDVERTEX_Y,event.Ds_TRUEENDVERTEX_Z)

	DeltaTAUKs1 = event.Ds_DTF_TAU_Ks1/299.792458-event.Ks1_TRUETAU
	DeltaTAUKs2 = event.Ds_DTF_TAU_Ks2/299.792458-event.Ks2_TRUETAU

	if (Ks1_DTF[0]-phi_DTF[0])**2 + (Ks1_DTF[1]-phi_DTF[1])**2 + (Ks1_DTF[2]-phi_DTF[2])**2 > (Ks1_TRUE[0]-phi_TRUE[0])**2 + (Ks1_TRUE[1]-phi_TRUE[1])**2 + (Ks1_TRUE[2]-phi_TRUE[2])**2:
		Track_Ks1 = 1
	else:
		Track_Ks1 = -1
	if (Ks2_DTF[0]-phi_DTF[0])**2 + (Ks2_DTF[1]-phi_DTF[1])**2 + (Ks2_DTF[2]-phi_DTF[2])**2 > (Ks2_TRUE[0]-phi_TRUE[0])**2 + (Ks2_TRUE[1]-phi_TRUE[1])**2 + (Ks2_TRUE[2]-phi_TRUE[2])**2:
		Track_Ks2 = 1
	else:
		Track_Ks2 = -1
	if event.Ds_DTF_P_Ks1 > event.Ks1_P:
		Momentum_Ks1 = 1
	else:
		Momentum_Ks1 = -1
	if event.Ds_DTF_P_Ks2 > event.Ks2_P:
		Momentum_Ks2 = 1
	else:
		Momentum_Ks2 = -1

	if (DeltaTAUKs1 > 0.05 and DeltaTAUKs2 > 0.05) or (DeltaTAUKs1 < -0.05 and DeltaTAUKs2 < -0.05):
		if Track_Ks1 == 1 and Track_Ks2 == 1:
			if Momentum_Ks1 == 1 and Momentum_Ks2 ==1:
				h_correlated.Fill("2lt2gm",1)
			if Momentum_Ks1 == 1 and Momentum_Ks2 ==-1:
				h_correlated.Fill("2lt1gm1lm",1)
			if Momentum_Ks1 == -1 and Momentum_Ks2 ==-1:
				h_correlated.Fill("2lt2lm",1)
		if Track_Ks1 == -1 and Track_Ks2 == -1:
			if Momentum_Ks1 == 1 and Momentum_Ks2 ==1:
				h_correlated.Fill("2st2gm",1)
			if Momentum_Ks1 == 1 and Momentum_Ks2 ==-1:
				h_correlated.Fill("2st1gm1lm",1)
			if Momentum_Ks1 == -1 and Momentum_Ks2 ==-1:
				h_correlated.Fill("2st2lm",1)
		if (Track_Ks1 == -1 and Track_Ks2 == 1) or (Track_Ks1 == 1 and Track_Ks2 == -1):
			if Momentum_Ks1 == 1 and Momentum_Ks2 ==1:
				h_correlated.Fill("1lt1st2gm",1)
			if Momentum_Ks1 == -1 and Momentum_Ks2 ==-1:
				h_correlated.Fill("1lt1st2lm",1)
		if (Track_Ks1 == -1 and Track_Ks2 == 1 and Momentum_Ks1 ==1 and Momentum_Ks2 == -1) or (Track_Ks1 == 1 and Track_Ks2 == -1 and Momentum_Ks1 ==-1 and Momentum_Ks2 == 1):
			h_correlated.Fill("1ltlm1stgm",1)
		if (Track_Ks1 == 1 and Track_Ks2 == -1 and Momentum_Ks1 ==1 and Momentum_Ks2 == -1) or (Track_Ks1 == -1 and Track_Ks2 == 1 and Momentum_Ks1 ==-1 and Momentum_Ks2 == 1):
			h_correlated.Fill("1ltgm1stlm",1)	
	elif (DeltaTAUKs1 > 0.1 and DeltaTAUKs2 < -0.1) or (DeltaTAUKs1 < -0.1 and DeltaTAUKs2 > 0.1):
		if Track_Ks1 == 1 and Track_Ks2 == 1:
			if Momentum_Ks1 == 1 and Momentum_Ks2 ==1:
				h_acorrelated.Fill("2lt2gm",1)
			if Momentum_Ks1 == 1 and Momentum_Ks2 ==-1:
				h_acorrelated.Fill("2lt1gm1lm",1)
			if Momentum_Ks1 == -1 and Momentum_Ks2 ==-1:
				h_acorrelated.Fill("2lt2lm",1)
		if Track_Ks1 == -1 and Track_Ks2 == -1:
			if Momentum_Ks1 == 1 and Momentum_Ks2 ==1:
				h_acorrelated.Fill("2st2gm",1)
			if Momentum_Ks1 == 1 and Momentum_Ks2 ==-1:
				h_acorrelated.Fill("2st1gm1lm",1)
			if Momentum_Ks1 == -1 and Momentum_Ks2 ==-1:
				h_acorrelated.Fill("2st2lm",1)
		if (Track_Ks1 == -1 and Track_Ks2 == 1) or (Track_Ks1 == 1 and Track_Ks2 == -1):
			if Momentum_Ks1 == 1 and Momentum_Ks2 ==1:
				h_acorrelated.Fill("1lt1st2gm",1)
			if Momentum_Ks1 == -1 and Momentum_Ks2 ==-1:
				h_acorrelated.Fill("1lt1st2lm",1)
		if (Track_Ks1 == -1 and Track_Ks2 == 1 and Momentum_Ks1 ==1 and Momentum_Ks2 == -1) or (Track_Ks1 == 1 and Track_Ks2 == -1 and Momentum_Ks1 ==-1 and Momentum_Ks2 == 1):
			h_acorrelated.Fill("1ltlm1stgm",1)
		if (Track_Ks1 == 1 and Track_Ks2 == -1 and Momentum_Ks1 ==1 and Momentum_Ks2 == -1) or (Track_Ks1 == -1 and Track_Ks2 == 1 and Momentum_Ks1 ==-1 and Momentum_Ks2 == 1):
			h_acorrelated.Fill("1ltgm1stlm",1)	





canv2.cd()
h_acorrelated.Draw()
canv2.Print("acorrelated.pdf")
canv1.cd()
h_correlated.Draw()
canv1.Print("correlated.pdf")
	




