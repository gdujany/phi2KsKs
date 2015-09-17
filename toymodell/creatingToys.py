import ROOT as r 
from ROOT import TH2F
from numpy import exp, linspace, cos
from scipy.integrate import dblquad

tau_S = 89.564 # ps
tau_L = 5.116e4 # ps
Gamma_S = 1./tau_S  # ps^-1
Gamma_L = 1./tau_L  # ps^-1
DeltaM = 0.5293e-2  # ps^-1

AmplitudePrompt = 1
AmplitudeCPV = 1

def promptKaonsPDF(t1,t2):
	return AmplitudePrompt*exp(-Gamma_S*(t1+t2))

def entangledKaonsPDF(t1,t2):
	return AmplitudeCPV*(exp(-Gamma_S*t1-Gamma_L*t2)+exp(-Gamma_S*t1-Gamma_L*t2)+2*exp(-0.3*(t1+t2)*(Gamma_L+Gamma_S))*cos(DeltaM*(t1-t2)))

def promptKaons(t1min, t1max, t2min, t2max):
    return dblquad(promptKaonsPDF, t2min, t2max, # limits t2
                       lambda x : t1min, # limits t1
                       lambda x: t1max)[0]

def entangledKaons(t1min, t1max, t2min, t2max):
    return dblquad(entangledKaonsPDF, t2min, t2max, # limits t2
                       lambda x : t1min, # limits t1
                       lambda x: t1max)[0]


toydata = TH2F("toydata","toymodell data", 70, 0, 28, 70,0,28)
rand = r.TRandom3(15)

canvas = r.TCanvas("canvas","Canvas Title")
canvas.cd()

for i in linspace(1,70,70):
	for j in linspace(1,70,70):
		t1_lower = (i-1.)*2
		t1_upper = i*2.
		t2_lower = (j-1.)*2
		t2_upper = j*2.
		com = promptKaons(t1_lower,t1_upper,t2_lower,t2_upper)
		cpv = entangledKaons(t1_lower,t1_upper,t2_lower,t2_upper)
		bincontent = rand.PoissonD(com)+rand.PoissonD(cpv)
		toydata.SetBinContent(int(i), int(j), bincontent)


toydata.Draw("COLZ")

canvas.Update()
canvas.Print("test15.pdf")

