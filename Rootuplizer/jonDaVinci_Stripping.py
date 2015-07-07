#DaVinci v36r1p1
from Gaudi.Configuration import *
from Configurables import DaVinci, CombineParticles, LHCbApp, FilterDesktop, CondDB, L0Conf

#L0Conf().EnsureKnownTCK=False

filename = "gauss"
#filename = "gauss_full"

DaVinci().TupleFile = filename+'.root'
DaVinci().DataType = "2012"  
DaVinci().InputType = "DST"  
DaVinci().PrintFreq = 10000
DaVinci().EvtMax = 300 #-1 
DaVinci().Simulation = True 
LHCbApp().DDDBtag   = "dddb-20130312-1"
LHCbApp().CondDBtag = "sim-20130222-1-vc-md100"
CondDB().UseLatestTags = ["2012"]

#EventSelector().Input = ["DATAFILE='PFN:file:"+filename+".dst' TYP='POOL_ROOTTREE' Opt='READ'"]

from StrippingConf.Configuration import StrippingConf, StrippingStream
from StrippingSettings.Utils import strippingConfiguration
from StrippingArchive.Utils import buildStreams
from StrippingArchive import strippingArchive

stripping='stripping21'
config  = strippingConfiguration(stripping)
archive = strippingArchive(stripping)
streams = buildStreams(stripping=config, archive=archive) 

# Select my line
MyStream = StrippingStream("MyStream")
MyLines = [ 'StrippingPhiToKSKS_PhiToKsKsLine' ]

for stream in streams: 
    for line in stream.lines:
        if line.name() in MyLines:
            MyStream.appendLines( [ line ] ) 

# Configure Stripping
from Configurables import ProcStatusCheck
filterBadEvents = ProcStatusCheck()

sc = StrippingConf( Streams = [ MyStream ],
                    MaxCandidates = 2000,
                    AcceptBadEvents = False,
                    BadEventSelection = filterBadEvents )

#######################################################################
# 3) Configure DecayTreeTuple

from DecayTreeTuple.Configuration import *
from Configurables import EvtTypeSvc, TupleToolDecay, LoKi__Hybrid__TupleTool, TupleToolGeometry, TupleToolTrackInfo, TupleToolKinematic, TupleToolMCTruth, TupleToolMCBackgroundInfo, TupleToolSubMass, TupleToolGeneration, TupleToolTrigger, TupleToolTISTOS

tuple = DecayTreeTuple()
tuple.Inputs = [ "Phys/PhiToKSKS_PhiToKsKsLine/Particles" ]
tuple.Decay = '[phi(1020) -> ^(KS0 -> ^pi+ ^pi-) ^(KS0 -> ^pi+ ^pi-)]CC'
#tuple.Decay = '[phi(1020) -> ^(KS0 => ^pi+ ^pi-) ^(KS0 => ^pi+ ^pi-)]CC' 
tuple.addBranches ({
        "Phi": "[phi(1020) -> (KS0 -> pi+ pi-) (KS0 -> pi+ pi-)]CC",
        "Ks1": "[phi(1020) -> ^(KS0 -> pi+ pi-) (KS0 -> pi+ pi-)]CC",
        "Ks2": "[phi(1020) -> (KS0 -> pi+ pi-) ^(KS0 -> pi+ pi-)]CC",
        "pi1": "[phi(1020) -> (KS0 -> ^pi+ pi-) (KS0 -> pi+ pi-)]CC",
        "pi2": "[phi(1020) -> (KS0 -> pi+ ^pi-) (KS0 -> pi+ pi-)]CC",
        "pi3": "[phi(1020) -> (KS0 -> pi+ pi-) (KS0 -> ^pi+ pi-)]CC",
        "pi4": "[phi(1020) -> (KS0 -> pi+ pi-) (KS0 -> pi+ ^pi-)]CC",
        #"Phi": "[phi(1020) -> (KS0 => pi+ pi-) (KS0 => pi+ pi-)]CC",
        #"Ks1": "[phi(1020) -> ^(KS0 => pi+ pi-) (KS0 => pi+ pi-)]CC",
        #"Ks2": "[phi(1020) -> (KS0 => pi+ pi-) ^(KS0 => pi+ pi-)]CC",
        #"pi1": "[phi(1020) -> (KS0 => ^pi+ pi-) (KS0 => pi+ pi-)]CC",
        #"pi2": "[phi(1020) -> (KS0 => pi+ ^pi-) (KS0 => pi+ pi-)]CC",
        #"pi3": "[phi(1020) -> (KS0 => pi+ pi-) (KS0 => ^pi+ pi-)]CC",
        #"pi4": "[phi(1020) -> (KS0 => pi+ pi-) (KS0 => pi+ ^pi-)]CC",
        })
#tuple.Decay = '[phi(1020) -> ^pi+ ^pi- ^pi+ ^pi-]CC'
#tuple.addBranches ({
#        "Phi": "[phi(1020) -> pi+ pi- pi+ pi-]CC",
#        "pi1": "[phi(1020) -> ^pi+ pi- pi+ pi-]CC",
#        "pi2": "[phi(1020) -> pi+ ^pi- pi+ pi-]CC",
#        "pi3": "[phi(1020) -> pi+ pi- ^pi+ pi-]CC",
#        "pi4": "[phi(1020) -> pi+ pi- pi+ ^pi-]CC",
#        })

tuple.ToolList = ["TupleToolGeometry",
                  "TupleToolEventInfo",
                  "TupleToolKinematic",
                  "TupleToolPrimaries",
                  "TupleToolPropertime",
                  "TupleToolAngles",
                  "TupleToolPid",
                  #"TupleToolRICHPid",
                  "TupleToolDecay",
                  "TupleToolTrackPosition",
                  "TupleToolTrackInfo",
		  #"TupleToolRecoStats",
                  "TupleToolTrigger",
                  "TupleToolDira",
                  #"TupleToolDalitz",
                  #"TupleToolSubMass",
                  "TupleToolMCBackgroundInfo",
                  "TupleToolMCTruth",
                 ]

tuple.addTool(TupleToolTISTOS())
tuple.TupleToolTISTOS.VerboseL0 = True
tuple.TupleToolTISTOS.VerboseHlt1 = True
tuple.TupleToolTISTOS.VerboseHlt2 = True
tuple.TupleToolTISTOS.Verbose = True
tuple.ToolList += ["TupleToolTISTOS"]

tuple.TupleToolTISTOS.TriggerList = [ trigger_name+"Decision" for trigger_name in 
["L0CALO","L0ElectronNoSPD","L0PhotonNoSPD","L0HadronNoSPD","L0MuonNoSPD","L0DiMuonNoSPD","L0Electron","L0ElectronHi","L0Photon","L0PhotonHi","L0Hadron","L0Muon","L0DiMuon","L0HighSumETJet","L0B1gas","L0B2gas", 
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
"Hlt2CharmHadD02HHXDst_BaryonhhXWithKSDDWideMass","Hlt2CharmHadD02HHXDst_BaryonhhXWithLambda0DD","Hlt2CharmHadD02HHXDst_BaryonhhXWithLambda0DDWideMass","Hlt2CharmHadD02HHXDst_LeptonhhX","Hlt2CharmHadD02HHXDst_LeptonhhXWideMass","Hlt2CharmHadD02HHXDst_LeptonhhXWithKSLL","Hlt2CharmHadD02HHXDst_LeptonhhXWithKSLLWideMass","Hlt2CharmHadD02HHXDst_LeptonhhXWithLambda0LL","Hlt2CharmHadD02HHXDst_LeptonhhXWithLambda0LLWideMass","Hlt2CharmHadD02HHXDst_LeptonhhXWithKSDD","Hlt2CharmHadD02HHXDst_LeptonhhXWithKSDDWideMass","Hlt2CharmHadD02HHXDst_LeptonhhXWithLambda0DD","Hlt2CharmHadD02HHXDst_LeptonhhXWithLambda0DDWideMass"]]

LoKi_DTFMASS_Phi_noPV = LoKi__Hybrid__TupleTool("LoKi_DTFMASS_Phi_noPV")
LoKi_DTFMASS_Phi_noPV.Variables = {
        "DTF_CHI2_noPV"   : "DTF_CHI2( False, 'phi(1020)' )",
        "DTF_NDOF_noPV"   : "DTF_NDOF( False, 'phi(1020)' )",
        "DTF_M_noPV"      : "DTF_FUN ( M, False, 'phi(1020)' )",
        "DTF_M_Ks1_noPV"    : "DTF_FUN ( CHILD(M,1), False, 'phi(1020)' )",
        "DTF_M_Ks2_noPV"    : "DTF_FUN ( CHILD(M,2), False, 'phi(1020)' )",
        }
tuple.Phi.ToolList+=["LoKi::Hybrid::TupleTool/LoKi_DTFMASS_Phi_noPV"]
tuple.Phi.addTool(LoKi_DTFMASS_Phi_noPV)

LoKi_DTFMASS_Phi_PV = LoKi__Hybrid__TupleTool("LoKi_DTFMASS_Phi_PV")
LoKi_DTFMASS_Phi_PV.Variables = {
        "DTF_CHI2_PV"   : "DTF_CHI2( True, 'phi(1020)' )",
        "DTF_NDOF_PV"   : "DTF_NDOF( True, 'phi(1020)' )",
        "DTF_M_PV"      : "DTF_FUN ( M, True, 'phi(1020)' )",
        "DTF_M_Ks1_PV"    : "DTF_FUN ( CHILD(M,1), True, 'phi(1020)' )",
        "DTF_M_Ks2_PV"    : "DTF_FUN ( CHILD(M,2), True, 'phi(1020)' )",
        }
tuple.Phi.ToolList+=["LoKi::Hybrid::TupleTool/LoKi_DTFMASS_Phi_PV"]
tuple.Phi.addTool(LoKi_DTFMASS_Phi_PV)

LoKi_Phi=LoKi__Hybrid__TupleTool("LoKi_Phi")
LoKi_Phi.Variables =  {
        "MassDiff_Phi" : "DMASS('phi(1020)')"
        , "BPVDIRA" : "BPVDIRA"
        , "IPS_Phi" : "MIPCHI2DV(PRIMARY)"
        , "VFASPF_CHI2DOF" : "VFASPF(VCHI2/VDOF)"
        , "VFASPF_CHI2" : "VFASPF(VCHI2)"
        , "BPVIPCHI2" : "BPVIPCHI2()"
        , "ADOCA" : "DOCA(1,2)"
        , "ADOCACHI2" : "DOCACHI2(1,2)"
                                  }
tuple.Phi.ToolList+=["LoKi::Hybrid::TupleTool/LoKi_Phi"]
tuple.Phi.addTool(LoKi_Phi)

LoKi_Ks1=LoKi__Hybrid__TupleTool("LoKi_Ks1")
LoKi_Ks1.Variables =  {
          "BPVDIRA" : "BPVDIRA"
        , "VFASPF_CHI2DOF" : "VFASPF(VCHI2/VDOF)"
        , "VFASPF_CHI2" : "VFASPF(VCHI2)"
        , "BPVIPCHI2" : "BPVIPCHI2()"
        , "BPVVD" : "BPVVD"
        , "BPVVDCHI2" : "BPVVDCHI2"
        , "ADOCA" : "DOCA(1,2)"
        , "ADOCACHI2" : "DOCACHI2(1,2)"
                                  }
tuple.Ks1.ToolList+=["LoKi::Hybrid::TupleTool/LoKi_Ks1"]
tuple.Ks1.addTool(LoKi_Ks1)

LoKi_Ks2=LoKi__Hybrid__TupleTool("LoKi_Ks2")
LoKi_Ks2.Variables =  {
          "BPVDIRA" : "BPVDIRA"
        , "VFASPF_CHI2DOF" : "VFASPF(VCHI2/VDOF)"
        , "VFASPF_CHI2" : "VFASPF(VCHI2)"
        , "BPVIPCHI2" : "BPVIPCHI2()"
        , "BPVVD" : "BPVVD"
        , "BPVVDCHI2" : "BPVVDCHI2"
        , "ADOCA" : "DOCA(1,2)"
        , "ADOCACHI2" : "DOCACHI2(1,2)"
                                  }
tuple.Ks2.ToolList+=["LoKi::Hybrid::TupleTool/LoKi_Ks2"]
tuple.Ks2.addTool(LoKi_Ks2)

MCTruth = TupleToolMCTruth() 
MCTruth.ToolList = ["MCTupleToolKinematic",
	 	"MCTupleToolHierarchy"]
tuple.addTool(MCTruth)

mctuple = MCDecayTreeTuple()
mctuple.Decay = '[phi(1020) -> ^(KS0 => ^pi+ ^pi-) ^(KS0 => ^pi+ ^pi-)]CC' 
mctuple.ToolList += [ "MCTupleToolKinematic",
			"MCTupleToolHierarchy",
			"MCTupleToolReconstructed",
			#"MCTupleToolDalitz",
			"MCTupleToolAngles"
 ]

from Configurables import PrintMCTree, PrintMCDecayTreeTool
mctree = PrintMCTree("PrintTruePhi")
mctree.addTool(PrintMCDecayTreeTool, name = "PrintMC")
mctree.PrintMC.Information = "Name"
mctree.ParticleNames = [ "phi(1020)" ]
mctree.Depth = 2

#EvtTypeSvc().EvtTypesFile="/afs/cern.ch/user/j/jrharris/ParticleTable.txt"
tuple.TupleName = "Phi2KsKs"
mctuple.TupleName = "Phi2KsKs"
#######################################################################
#######################################################################
DaVinci().appendToMainSequence( [ sc.sequence() ] )
DaVinci().UserAlgorithms = [ mctuple, tuple]
