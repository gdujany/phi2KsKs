#!/usr/bin/env python
'''
Trigger efficiencies of Jon's MC
'''

import sys, os
from CompareTreeVars import getHisto, CompareTreeVars
import ROOT as r
import ROOT

r.gROOT.SetBatch(True)

# Get trees

eos_root = os.path.expanduser('~/eos/')
if not os.listdir(eos_root):
    raise OSError('EOS not mounted, please type:\n eosmount '+eos_root)

store_dir = os.path.join(eos_root, 'lhcb/user/g/gdujany/phi2KsKs/old/')

inFiles = {}
inFiles['phi2KsKs_incl'] = r.TFile(os.path.join(store_dir, 'Phi2KsKs_MC_GenCut_inclusive_stripped.root'))


trees = {}
for key, inFile in inFiles.items():
    trees[key] = inFile.Get('DecayTreeTuple/Phi2KsKs')

allEntries = trees['phi2KsKs_incl'].GetEntries()

L0_trigger = []
Hlt1_trigger = []
Hlt2_trigger = []


for triggername in ["L0CALO","L0ElectronNoSPD","L0PhotonNoSPD","L0HadronNoSPD","L0MuonNoSPD","L0DiMuonNoSPD","L0Electron","L0ElectronHi","L0Photon","L0PhotonHi","L0Hadron","L0Muon","L0DiMuon","L0HighSumETJet","L0B1gas","L0B2gas", 
"Hlt1MBMicroBiasVelo","Hlt1Global","Hlt1DiMuonHighMass","Hlt1DiMuonLowMass","Hlt1SingleMuonNoIP","Hlt1SingleMuonHighPT","Hlt1TrackAllL0","Hlt1TrackMuon","Hlt1TrackPhoton","Hlt1Lumi","Hlt1LumiMidBeamCrossing","Hlt1MBNoBias","Hlt1MBMicroBiasVeloRateLimited","Hlt1MBMicroBiasTStation","Hlt1MBMicroBiasTStationRateLimited","Hlt1L0Any","Hlt1L0AnyRateLimited","Hlt1L0AnyNoSPD","Hlt1L0AnyNoSPDRateLimited","Hlt1NoPVPassThrough","Hlt1DiProton","Hlt1DiProtonLowMult","Hlt1BeamGasNoBeamBeam1","Hlt1BeamGasNoBeamBeam2","Hlt1BeamGasBeam1","Hlt1BeamGasBeam2","Hlt1BeamGasCrossingEnhancedBeam1","Hlt1BeamGasCrossingEnhancedBeam2","Hlt1BeamGasCrossingForcedReco","Hlt1ODINTechnical","Hlt1Tell1Error","Hlt1VeloClosingMicroBias","Hlt1BeamGasCrossingParasitic","Hlt1ErrorEvent","Hlt1SingleElectronNoIP","Hlt1TrackForwardPassThrough","Hlt1TrackForwardPassThroughLoose","Hlt1CharmCalibrationNoBias","Hlt1L0HighSumETJet","Hlt1BeamGasCrossingForcedRecoFullZ","Hlt1BeamGasHighRhoVertices","Hlt1VertexDisplVertex","Hlt1TrackAllL0Tight","Hlt1HighPtJetsSinglePV","Hlt1L0PU",
"Hlt1L0CALO","Hlt2SingleElectronTFLowPt","Hlt2SingleElectronTFHighPt","Hlt2DiElectronHighMass","Hlt2DiElectronB","Hlt2B2HHLTUnbiased","Hlt2Topo2BodySimple","Hlt2Topo3BodySimple","Hlt2Topo4BodySimple","Hlt2Topo2BodyBBDT","Hlt2Topo3BodyBBDT","Hlt2Topo4BodyBBDT","Hlt2TopoMu2BodyBBDT","Hlt2TopoMu3BodyBBDT","Hlt2TopoMu4BodyBBDT","Hlt2TopoE2BodyBBDT","Hlt2TopoE3BodyBBDT","Hlt2TopoE4BodyBBDT","Hlt2IncPhi","Hlt2IncPhiSidebands","Hlt2CharmHadD02HHKsLL","Hlt2Dst2PiD02PiPi","Hlt2Dst2PiD02MuMu","Hlt2Dst2PiD02KMu","Hlt2Dst2PiD02KPi","Hlt2PassThrough","Hlt2Transparent","Hlt2Forward","Hlt2DebugEvent","Hlt2CharmHadD02HH_D02PiPi",
"Hlt2CharmHadD02HH_D02PiPiWideMass","Hlt2CharmHadD02HH_D02KK","Hlt2CharmHadD02HH_D02KKWideMass","Hlt2CharmHadD02HH_D02KPi","Hlt2CharmHadD02HH_D02KPiWideMass","Hlt2ExpressJPsi","Hlt2ExpressJPsiTagProbe","Hlt2ExpressLambda","Hlt2ExpressKS","Hlt2ExpressDs2PhiPi","Hlt2ExpressBeamHalo","Hlt2ExpressDStar2D0Pi","Hlt2ExpressHLT1Physics","Hlt2Bs2PhiGamma","Hlt2Bs2PhiGammaWideBMass","Hlt2Bd2KstGamma","Hlt2Bd2KstGammaWideKMass","Hlt2Bd2KstGammaWideBMass","Hlt2CharmHadD2KS0H_D2KS0Pi","Hlt2CharmHadD2KS0H_D2KS0K","Hlt2CharmRareDecayD02MuMu","Hlt2B2HH","Hlt2MuonFromHLT1","Hlt2SingleMuon","Hlt2SingleMuonHighPT","Hlt2SingleMuonLowPT",
"Hlt2DiProton","Hlt2DiProtonTF","Hlt2DiProtonLowMult","Hlt2DiProtonLowMultTF","Hlt2CharmSemilepD02HMuNu_D02KMuNuWS","Hlt2CharmSemilepD02HMuNu_D02PiMuNuWS","Hlt2CharmSemilepD02HMuNu_D02KMuNu","Hlt2CharmSemilepD02HMuNu_D02PiMuNu","Hlt2TFBc2JpsiMuX","Hlt2TFBc2JpsiMuXSignal","Hlt2DisplVerticesLowMassSingle","Hlt2DisplVerticesHighMassSingle","Hlt2DisplVerticesDouble","Hlt2DisplVerticesSinglePostScaled","Hlt2DisplVerticesHighFDSingle","Hlt2DisplVerticesSingleDown","Hlt2CharmSemilepD2HMuMu","Hlt2CharmSemilepD2HMuMuWideMass","Hlt2B2HHPi0_Merged","Hlt2CharmHadD2HHH","Hlt2CharmHadD2HHHWideMass","Hlt2DiMuon","Hlt2DiMuonLowMass",
"Hlt2DiMuonJPsi","Hlt2DiMuonJPsiHighPT","Hlt2DiMuonPsi2S","Hlt2DiMuonB","Hlt2DiMuonZ","Hlt2DiMuonDY1","Hlt2DiMuonDY2","Hlt2DiMuonDY3","Hlt2DiMuonDY4","Hlt2DiMuonDetached","Hlt2DiMuonDetachedHeavy","Hlt2DiMuonDetachedJPsi","Hlt2DiMuonNoPV","Hlt2TriMuonDetached","Hlt2TriMuonTau","Hlt2CharmSemilepD02HHMuMu","Hlt2CharmSemilepD02HHMuMuWideMass","Hlt2CharmHadD02HHHH","Hlt2CharmHadD02HHHHWideMass","Hlt2ErrorEvent","Hlt2Global","Hlt2diPhotonDiMuon","Hlt2LowMultMuon","Hlt2LowMultHadron","Hlt2LowMultPhoton","Hlt2LowMultElectron","Hlt2SingleTFElectron","Hlt2SingleTFVHighPtElectron","Hlt2B2HHLTUnbiasedDetached","Hlt2CharmHadLambdaC2KPPi",
"Hlt2SingleMuonVHighPT","Hlt2CharmSemilepD02HMuNu_D02KMuNuTight","Hlt2CharmHadMinBiasLambdaC2KPPi","Hlt2CharmHadMinBiasD02KPi","Hlt2CharmHadMinBiasD02KK","Hlt2CharmHadMinBiasDplus2hhh","Hlt2CharmHadMinBiasLambdaC2LambdaPi","Hlt2DisplVerticesSingle","Hlt2DisplVerticesDoublePostScaled","Hlt2DisplVerticesSingleHighMassPostScaled","Hlt2DisplVerticesSingleHighFDPostScaled","Hlt2DisplVerticesSingleMVPostScaled","Hlt2RadiativeTopoTrackTOS","Hlt2RadiativeTopoPhotonL0","Hlt2DiMuonPsi2SHighPT","Hlt2DoubleDiMuon","Hlt2DiMuonAndMuon","Hlt2DiMuonAndGamma","Hlt2DiMuonAndD0","Hlt2DiMuonAndDp","Hlt2DiMuonAndDs","Hlt2DiMuonAndLc",
"Hlt2CharmSemilepD02HHMuMuHardHadronsSoftMuons","Hlt2CharmSemilepD02HHMuMuHardHadronsSoftMuonsWideMass","Hlt2CharmSemilepD02HHMuMuHardHadronsAndMuons","Hlt2CharmSemilepD02HHMuMuHardHadronsAndMuonsWideMass","Hlt2TopoRad2BodyBBDT","Hlt2TopoRad2plus1BodyBBDT","Hlt2Lumi","Hlt2LowMultHadron_nofilter","Hlt2LowMultElectron_nofilter","Hlt2CharmHadD02HHKsDD","Hlt2CharmHadD2KS0KS0","Hlt2CharmHadD2KS0KS0WideMass","Hlt2ExpressD02KPi","Hlt2CharmHadLambdaC2KPPiWideMass","Hlt2CharmHadLambdaC2KPK","Hlt2CharmHadLambdaC2KPKWideMass","Hlt2CharmHadLambdaC2PiPPi","Hlt2CharmHadLambdaC2PiPPiWideMass","Hlt2CharmHadLambdaC2PiPK",
"Hlt2CharmHadLambdaC2PiPKWideMass","Hlt2CharmHadD2KS0H_D2KS0DDPi","Hlt2CharmHadD2KS0H_D2KS0DDK","Hlt2DiPhi","Hlt2CharmHadD02HHHHDstNoHltOne_4pi","Hlt2CharmHadD02HHHHDstNoHltOne_4piWideMass","Hlt2CharmHadD02HHHHDstNoHltOne_K3pi","Hlt2CharmHadD02HHHHDstNoHltOne_K3piWideMass","Hlt2CharmHadD02HHHHDstNoHltOne_KKpipi","Hlt2CharmHadD02HHHHDstNoHltOne_KKpipiWideMass","Hlt2CharmHadD02HHHHDstNoHltOne_2K2pi","Hlt2CharmHadD02HHHHDstNoHltOne_2K2piWideMass","Hlt2CharmHadD02HHHHDstNoHltOne_3Kpi","Hlt2CharmHadD02HHHHDstNoHltOne_3KpiWideMass","Hlt2CharmHadD02HHHHDstNoHltOne_Ch2","Hlt2CharmHadD02HHHHDstNoHltOne_Ch2WideMass",
"Hlt2CharmSemilep3bodyD2PiMuMu","Hlt2CharmSemilep3bodyD2PiMuMuSS","Hlt2CharmSemilep3bodyD2KMuMu","Hlt2CharmSemilep3bodyD2KMuMuSS","Hlt2CharmSemilep3bodyLambdac2PMuMu","Hlt2CharmSemilep3bodyLambdac2PMuMuSS","Hlt2LambdaC_LambdaC2Lambda0LLPi","Hlt2LambdaC_LambdaC2Lambda0LLK","Hlt2LambdaC_LambdaC2Lambda0DDPi","Hlt2LambdaC_LambdaC2Lambda0DDK","Hlt2RadiativeTopoTrack","Hlt2RadiativeTopoPhoton","Hlt2CharmHadD02HHHHDst_4pi","Hlt2CharmHadD02HHHHDst_4piWideMass","Hlt2CharmHadD02HHHHDst_K3pi","Hlt2CharmHadD02HHHHDst_K3piWideMass","Hlt2CharmHadD02HHHHDst_KKpipi","Hlt2CharmHadD02HHHHDst_KKpipiWideMass","Hlt2CharmHadD02HHHHDst_2K2pi",
"Hlt2CharmHadD02HHHHDst_2K2piWideMass","Hlt2CharmHadD02HHHHDst_3Kpi","Hlt2CharmHadD02HHHHDst_3KpiWideMass","Hlt2CharmHadD02HHHHDst_Ch2","Hlt2CharmHadD02HHHHDst_Ch2WideMass","Hlt2CharmSemilepD02PiPiMuMu","Hlt2CharmSemilepD02KKMuMu","Hlt2CharmSemilepD02KPiMuMu","Hlt2CharmHadD02HHHH_4pi","Hlt2CharmHadD02HHHH_4piWideMass","Hlt2CharmHadD02HHHH_K3pi","Hlt2CharmHadD02HHHH_K3piWideMass","Hlt2CharmHadD02HHHH_KKpipi","Hlt2CharmHadD02HHHH_KKpipiWideMass","Hlt2CharmHadD02HHHH_2K2pi","Hlt2CharmHadD02HHHH_2K2piWideMass","Hlt2CharmHadD02HHHH_3Kpi","Hlt2CharmHadD02HHHH_3KpiWideMass","Hlt2CharmHadD02HHHH_Ch2","Hlt2CharmHadD02HHHH_Ch2WideMass",
"Hlt2DiMuonDetachedPsi2S","Hlt2CharmHadD02HHXDst_hhX","Hlt2CharmHadD02HHXDst_hhXWideMass","Hlt2LowMultD2KPi","Hlt2LowMultD2KPiPi","Hlt2LowMultD2K3Pi","Hlt2LowMultChiC2HH","Hlt2LowMultChiC2HHHH","Hlt2LowMultD2KPiWS","Hlt2LowMultD2KPiPiWS","Hlt2LowMultD2K3PiWS","Hlt2LowMultChiC2HHWS","Hlt2LowMultChiC2HHHHWS","Hlt2LowMultDDInc","Hlt2DisplVerticesSingleLoosePS","Hlt2DisplVerticesSingleHighFD","Hlt2DisplVerticesSingleVeryHighFD","Hlt2DisplVerticesSingleHighMass","Hlt2DisplVerticesSinglePS","Hlt2DisplVerticesDoublePS","Hlt2CharmHadD2HHHKsLL","Hlt2CharmHadD2HHHKsDD","Hlt2KshortToMuMuPiPi","Hlt2LowMultChiC2PP","Hlt2LowMultDDIncCP",
"Hlt2LowMultDDIncVF","Hlt2LowMultLMR2HH","Hlt2HighPtJets","Hlt2ChargedHyperon_Xi2Lambda0LLPi","Hlt2ChargedHyperon_Xi2Lambda0LLMu","Hlt2ChargedHyperon_Omega2Lambda0LLK","Hlt2ChargedHyperon_Xi2Lambda0DDPi","Hlt2ChargedHyperon_Xi2Lambda0DDMu","Hlt2ChargedHyperon_Omega2Lambda0DDK","Hlt2CharmHadD02HHXDst_BaryonhhX","Hlt2CharmHadD02HHXDst_BaryonhhXWideMass","Hlt2CharmHadD02HHXDst_BaryonhhXWithKSLL","Hlt2CharmHadD02HHXDst_BaryonhhXWithKSLLWideMass","Hlt2CharmHadD02HHXDst_BaryonhhXWithLambda0LL","Hlt2CharmHadD02HHXDst_BaryonhhXWithLambda0LLWideMass","Hlt2CharmHadD02HHXDst_BaryonhhXWithKSDD",
"Hlt2CharmHadD02HHXDst_BaryonhhXWithKSDDWideMass","Hlt2CharmHadD02HHXDst_BaryonhhXWithLambda0DD","Hlt2CharmHadD02HHXDst_BaryonhhXWithLambda0DDWideMass","Hlt2CharmHadD02HHXDst_LeptonhhX","Hlt2CharmHadD02HHXDst_LeptonhhXWideMass","Hlt2CharmHadD02HHXDst_LeptonhhXWithKSLL","Hlt2CharmHadD02HHXDst_LeptonhhXWithKSLLWideMass","Hlt2CharmHadD02HHXDst_LeptonhhXWithLambda0LL","Hlt2CharmHadD02HHXDst_LeptonhhXWithLambda0LLWideMass","Hlt2CharmHadD02HHXDst_LeptonhhXWithKSDD","Hlt2CharmHadD02HHXDst_LeptonhhXWithKSDDWideMass","Hlt2CharmHadD02HHXDst_LeptonhhXWithLambda0DD","Hlt2CharmHadD02HHXDst_LeptonhhXWithLambda0DDWideMass"]:
	if(triggername.startswith("L0")):
		L0_trigger.append(triggername)
	elif(triggername.startswith("Hlt1")):
		Hlt1_trigger.append(triggername)
	elif(triggername.startswith("Hlt2")):
		Hlt2_trigger.append(triggername)




print "Trigger for phi(1020)"

triggersPassedL0 = ""
isfirsttrigger = 1

print "L0 trigger"

for tistos in ["TIS","TOS"]:
	for varname in L0_trigger:	
		if(isfirsttrigger==1):
			triggersPassedL0 = triggersPassedL0 + "Phi_"+varname+"Decision_"+tistos+"==1"
			isfirsttrigger = 0
		else:
			triggersPassedL0 = triggersPassedL0 + " || " + "Phi_"+varname+"Decision_"+tistos+"==1"
		if trees['phi2KsKs_incl'].GetEntries("Phi_"+varname+"Decision_"+tistos+"==1")> 0:
			print round(100*float(trees['phi2KsKs_incl'].GetEntries("Phi_"+varname+"Decision_"+tistos+"==1"))/float(allEntries),2), " \t", varname

sum_triggered_entriesL0 = trees['phi2KsKs_incl'].GetEntries(triggersPassedL0)

print "Total: ", sum_triggered_entriesL0, "(L0) of ", allEntries, " events "



triggersPassedL0 = "&&("+triggersPassedL0+")" 

isfirsttrigger = 1

triggersPassedHlt1 = ""


print "Hlt1 trigger"

for tistos in ["TIS","TOS"]:
	print "Hlt1_"+tistos+" phi(1020)"
	for varname in Hlt1_trigger:
		if trees['phi2KsKs_incl'].GetEntries("Phi_"+varname+"Decision_"+tistos+"==1"+triggersPassedL0)> 0:			
			if(isfirsttrigger==1):
				triggersPassedHlt1 = triggersPassedHlt1+ "Phi_"+varname+"Decision_"+tistos+"==1"
				isfirsttrigger = 0
			else:
				triggersPassedHlt1 = triggersPassedHlt1 + " || " + "Phi_"+varname+"Decision_"+tistos+"==1"
			print round(100*float(trees['phi2KsKs_incl'].GetEntries("Phi_"+varname+"Decision_"+tistos+"==1"+triggersPassedL0))/float(allEntries),2), " \t", varname



sum_triggered_entriesHlt1 = trees['phi2KsKs_incl'].GetEntries("("+triggersPassedHlt1+")"+triggersPassedL0)
print sum_triggered_entriesHlt1, " (Hlt1) of ", sum_triggered_entriesL0, " (L0) of ", allEntries, " events"

triggersPassedHlt1 = "&&(" + triggersPassedHlt1 + ")"

isfirsttrigger = 1

triggersPassedHlt2 = ""


print "Hlt2 trigger"

for tistos in ["TIS","TOS"]:
	print "Hlt2_"+tistos+" phi(1020)"
	for varname in Hlt2_trigger:
		if trees['phi2KsKs_incl'].GetEntries("Phi_"+varname+"Decision_"+tistos+"==1"+triggersPassedL0+triggersPassedHlt1)> 0:			
			if(isfirsttrigger==1):
				triggersPassedHlt2 = triggersPassedHlt2+ "Phi_"+varname+"Decision_"+tistos+"==1"
				isfirsttrigger = 0
			else:
				triggersPassedHlt2 = triggersPassedHlt2 + " || " + "Phi_"+varname+"Decision_"+tistos+"==1"
			print round(100*float(trees['phi2KsKs_incl'].GetEntries("Phi_"+varname+"Decision_"+tistos+"==1"+triggersPassedL0+triggersPassedHlt1))/float(allEntries),2), " \t", varname



sum_triggered_entriesHlt2 = trees['phi2KsKs_incl'].GetEntries("("+triggersPassedHlt2+")"+triggersPassedL0+triggersPassedHlt1)
print sum_triggered_entriesHlt2, " (Hlt2) of ", sum_triggered_entriesHlt1, " (Hlt1) of ", sum_triggered_entriesL0, " (L0) of ", allEntries, " events"