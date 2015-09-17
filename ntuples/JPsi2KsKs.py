#This file will write out a tuple from the inclusive J/psi stripping line.


#This is the location of where your stripped candidates are locatated on the DST.
#The locations can normally be found on the stripping twiki under "stream definitions"
#location = "/Event/Charm/Phys/PhiToKSKS_PhiToKsKsLine/Particles"


isMC = False;



from PhysSelPython.Wrappers import Selection, SelectionSequence, DataOnDemand, MergedSelection, AutomaticData
from StandardParticles import StdLoosePions, StdLooseKsLL, StdLooseKsDD
from Configurables import FilterDesktop, CombineParticles
from DecayTreeTuple.Configuration import *
from GaudiKernel.SystemOfUnits import MeV, GeV, mrad, picosecond


location = "/Event/Charm/Phys/PhiToKSKS_JPsiToKsKsLine/Particles"

JPsiSel = DataOnDemand(Location = location)

jpsiFilter = FilterDesktop('jpsiFilter', Code = 'PT > 400')


JPsiFilterSel = Selection(name = 'jpsiFilterSel', Algorithm = jpsiFilter, RequiredSelections = [JPsiSel] )

seq = SelectionSequence("Seq", TopSelection=JPsiFilterSel)


#This filter is used just to speed up the process, nothing happens if there
# # is no stripped candidates at that location.
# from PhysConf.Filters import LoKi_Filters
# fltrs = LoKi_Filters(
#   STRIP_Code = "HLT_PASS('StrippingPhiToKSKS_PhiToKsKsLineDecision')")


from Configurables import FitDecayTrees, DecayTreeTuple, TupleToolDecayTreeFitter, TupleToolDecay, TupleToolTrigger, TupleToolTISTOS, TupleToolPropertime, PropertimeFitter, TupleToolKinematic, TupleToolGeometry, TupleToolEventInfo, TupleToolPrimaries, TupleToolPid, TupleToolTrackInfo, TupleToolRecoStats, TupleToolMCTruth,  LoKi__Hybrid__TupleTool, LoKi__Hybrid__EvtTupleTool


tuple = DecayTreeTuple("TupleJPsi2KsKs")

#Give DecayTreeTuple the location of your stripped candidates
#If you apply a selection, this will be the output of a selection sequence object.
tuple.Inputs = [seq.outputLocation()]
tuple.ToolList =  ['TupleToolKinematic',
                    'TupleToolEventInfo', 
                    'TupleToolTrackInfo',
                    'TupleToolPid',
                    'TupleToolGeometry', 
                    'TupleToolAngles',
]

tuple.InputPrimaryVertices = '/Event/Charm/Rec/Vertex/Primary'


# # Other event infos

tuple.addTupleTool('LoKi::Hybrid::EvtTupleTool/LoKi_Evt')
tuple.LoKi_Evt.VOID_Variables = {
                "nTracks"  : "CONTAINS('/Event/Charm/Rec/Track/Best')",
                "nPVs"    : "CONTAINS('/Event/Charm/Rec/Vertex/Primary')"
                }


 # Other variables
tuple.addTupleTool('LoKi::Hybrid::TupleTool/LoKi_All')
tuple.LoKi_All.Variables = {
            'Eta' : 'ETA',
            'Phi' : 'PHI',         
            } 


#Tell DecayTreeTuple the structure of your decay, you must put ^ in front 
#of particles that you want to write out (apart from head). J/psi->mu+mu-
# is a CP eigenstate so we don't need []CC here.
tuple.Decay = '[J/psi(1S) -> ^(KS0 -> ^pi+ ^pi-) ^(KS0 -> ^pi+ ^pi-)]CC'
tuple.Branches = {'JPsi' : '[J/psi(1S) -> (KS0 -> pi+ pi-) (KS0 -> pi+ pi-)]CC',
                                        'Ks1' : '[J/psi(1S) -> ^(KS0 -> pi+ pi-) (KS0 -> pi+ pi-)CC',
                                        'Ks2' : '[J/psi(1S) -> (KS0 -> pi+ pi-) ^(KS0 -> pi+ pi-)]CC',
                                        'pi1' : '[J/psi(1S) -> (KS0 -> ^pi+ pi-) (KS0 -> pi+ pi-)]CC',
                                        'pi2' : '[J/psi(1S) -> (KS0 -> pi+ ^pi-) (KS0 -> pi+ pi-)]CC',
                                        'pi3' : '[J/psi(1S) -> (KS0 -> pi+ pi-) (KS0 -> ^pi+ pi-)]CC',
                                        'pi4' : '[J/psi(1S) -> (KS0 -> pi+ pi-) (KS0 -> pi+ ^pi-)]CC',
                                          }

tuple.addBranches(tuple.Branches)


tuple.JPsi.addTupleTool("LoKi::Hybrid::TupleTool/LoKi_JPsi")
tuple.JPsi.LoKi_JPsi.Variables =  {
            'DOCAMAX' : 'DOCAMAX',
            "MassDiff_JPsi" : "DMASS('J/psi(1S)')",
            "BPVDIRA" : "BPVDIRA",
            "IPS_JPsi" : "MIPCHI2DV(PRIMARY)",
            "VFASPF_CHI2DOF" : "VFASPF(VCHI2/VDOF)",
            "VFASPF_CHI2" : "VFASPF(VCHI2)",
            "BPVIPCHI2" : "BPVIPCHI2()",
            "ADOCA" : "DOCA(1,2)",
            "ADOCACHI2" : "DOCACHI2(1,2)", 
            "DTF_CHI2_PV"   : "DTF_CHI2( True, 'KS0' )",
            "DTF_NDOF_PV"   : "DTF_NDOF( True, 'KS0' )",
            "DTF_M_JPsi"      : "DTF_FUN ( M, True, 'KS0' )",

            "DTF_CTAU_Ks1"    : "DTF_CTAU(1, True, strings('KS0') )",
            "DTF_CTAU_Ks2"    : "DTF_CTAU(2, True, strings('KS0') )",
            "DTF_DT" : "DTF_CTAU(1, True, strings('KS0') )- DTF_CTAU(2, True, strings('KS0') )" ,
            "DTF_ADT" : "abs(DTF_CTAU(1, True, strings('KS0') )- DTF_CTAU(2, True, strings('KS0') ))"  
            }

def mySharedConf_Ks(branch):
  atool=branch.addTupleTool('LoKi::Hybrid::TupleTool/LoKi_Ks')
  atool.Variables =  {
                "BPVDIRA" : "BPVDIRA",
                "VFASPF_CHI2DOF" : "VFASPF(VCHI2/VDOF)",
                "VFASPF_CHI2" : "VFASPF(VCHI2)",
                "BPVIPCHI2" : "BPVIPCHI2()",
                "BPVVD" : "BPVVD",
                "BPVVDCHI2" : "BPVVDCHI2",
                "ADOCA" : "DOCA(1,2)",
                "ADOCACHI2" : "DOCACHI2(1,2)",
                'BPVLTIME' : 'BPVLTIME()',
                }
  PropertimeTool = branch.addTupleTool("TupleToolPropertime/Propertime_Ks")
            

mySharedConf_Ks(tuple.Ks1)
mySharedConf_Ks(tuple.Ks2)

def mySharedConf_pi(branch):
  atool=branch.addTupleTool('LoKi::Hybrid::TupleTool/LoKi_pi')
  atool.Variables =  {
                'TRCHI2DOF' : 'TRCHI2DOF',
                'TRGHOSTPROB' : 'TRGHOSTPROB',
                }

mySharedConf_pi(tuple.pi1)
mySharedConf_pi(tuple.pi2)     
mySharedConf_pi(tuple.pi3)
mySharedConf_pi(tuple.pi4)


L0_list = ['L0HadronDecision', 'L0MuonDecision', 'L0ElectronDecision']
HLT1_list = ['Hlt1TrackAllL0Decision', 'Hlt1TrackPhotonDecision', 'Hlt1TrackMuonDecision']
HLT2_list = ['Hlt2ExpressKSDecision', 'Hlt2CharmHadD02HHXDst_BaryonhhXWideMassDecision']


HLT1_full_list = ['Hlt::Line/Hlt1DiMuonHighMass', 'Hlt::Line/Hlt1DiMuonLowMass', 'Hlt::Line/Hlt1SingleMuonNoIP', 'Hlt::Line/Hlt1SingleMuonHighPT', 'Hlt::Line/Hlt1SingleElectronNoIP', 'Hlt::Line/Hlt1TrackAllL0', 'Hlt::Line/Hlt1TrackAllL0Tight', 'Hlt::Line/Hlt1TrackMuon', 'Hlt::Line/Hlt1TrackPhoton', 'Hlt::Line/Hlt1TrackForwardPassThrough', 'Hlt::Line/Hlt1TrackForwardPassThroughLoose', 'Hlt::Line/Hlt1Lumi', 'Hlt::Line/Hlt1LumiMidBeamCrossing', 'Hlt::Line/Hlt1MBNoBias', 'Hlt::Line/Hlt1CharmCalibrationNoBias', 'Hlt::Line/Hlt1MBMicroBiasVelo', 'Hlt::Line/Hlt1MBMicroBiasTStation', 'Hlt::Line/Hlt1HighPtJetsSinglePV', 'Hlt::Line/Hlt1L0Any', 'Hlt::Line/Hlt1L0AnyNoSPD', 'Hlt::Line/Hlt1L0HighSumETJet', 'Hlt::Line/Hlt1NoPVPassThrough', 'Hlt::Line/Hlt1DiProton', 'Hlt::Line/Hlt1DiProtonLowMult', 'Hlt::Line/Hlt1BeamGasNoBeamBeam1', 'Hlt::Line/Hlt1BeamGasNoBeamBeam2', 'Hlt::Line/Hlt1BeamGasBeam1', 'Hlt::Line/Hlt1BeamGasBeam2', 'Hlt::Line/Hlt1BeamGasCrossingEnhancedBeam1', 'Hlt::Line/Hlt1BeamGasCrossingEnhancedBeam2', 'Hlt::Line/Hlt1BeamGasCrossingForcedReco', 'Hlt::Line/Hlt1BeamGasCrossingForcedRecoFullZ', 'Hlt::Line/Hlt1BeamGasHighRhoVertices', 'Hlt::Line/Hlt1ODINTechnical', 'Hlt::Line/Hlt1Tell1Error', 'Hlt::Line/Hlt1VeloClosingMicroBias', 'Hlt::Line/Hlt1VertexDisplVertex', 'Hlt::Line/Hlt1BeamGasCrossingParasitic', 'Hlt::Line/Hlt1ErrorEvent', 'Hlt::Line/Hlt1Global']
HLT2_full_list = ['Hlt::Line/Hlt2DiMuonJPsi', 'Hlt::Line/Hlt2DiMuonJPsiHighPT', 'Hlt::Line/Hlt2DiMuonPsi2S', 'Hlt::Line/Hlt2DiMuonPsi2SHighPT', 'Hlt::Line/Hlt2DiMuonB', 'Hlt::Line/Hlt2DiMuonZ', 'Hlt::Line/Hlt2DiMuonDY1', 'Hlt::Line/Hlt2DiMuonDY2', 'Hlt::Line/Hlt2DiMuonDY3', 'Hlt::Line/Hlt2DiMuonDY4', 'Hlt::Line/Hlt2DiMuonDetached', 'Hlt::Line/Hlt2DiMuonDetachedHeavy', 'Hlt::Line/Hlt2DiMuonDetachedJPsi', 'Hlt::Line/Hlt2DiMuonDetachedPsi2S', 'Hlt::Line/Hlt2TriMuonDetached', 'Hlt::Line/Hlt2DoubleDiMuon', 'Hlt::Line/Hlt2DiMuonAndMuon', 'Hlt::Line/Hlt2TriMuonTau', 'Hlt::Line/Hlt2DiMuonAndGamma', 'Hlt::Line/Hlt2DiMuonAndD0', 'Hlt::Line/Hlt2DiMuonAndDp', 'Hlt::Line/Hlt2DiMuonAndDs', 'Hlt::Line/Hlt2DiMuonAndLc', 'Hlt::Line/Hlt2SingleTFElectron', 'Hlt::Line/Hlt2SingleElectronTFLowPt', 'Hlt::Line/Hlt2SingleElectronTFHighPt', 'Hlt::Line/Hlt2SingleTFVHighPtElectron', 'Hlt::Line/Hlt2DiElectronHighMass', 'Hlt::Line/Hlt2DiElectronB', 'Hlt::Line/Hlt2B2HHLTUnbiased', 'Hlt::Line/Hlt2B2HHLTUnbiasedDetached', 'Hlt::Line/Hlt2Topo2BodySimple', 'Hlt::Line/Hlt2Topo3BodySimple', 'Hlt::Line/Hlt2Topo4BodySimple', 'Hlt::Line/Hlt2Topo2BodyBBDT', 'Hlt::Line/Hlt2Topo3BodyBBDT', 'Hlt::Line/Hlt2Topo4BodyBBDT', 'Hlt::Line/Hlt2TopoMu2BodyBBDT', 'Hlt::Line/Hlt2TopoMu3BodyBBDT', 'Hlt::Line/Hlt2TopoMu4BodyBBDT', 'Hlt::Line/Hlt2TopoE2BodyBBDT', 'Hlt::Line/Hlt2TopoE3BodyBBDT', 'Hlt::Line/Hlt2TopoE4BodyBBDT', 'Hlt::Line/Hlt2TopoRad2BodyBBDT', 'Hlt::Line/Hlt2TopoRad2plus1BodyBBDT', 'Hlt::Line/Hlt2IncPhi', 'Hlt::Line/Hlt2IncPhiSidebands', 'Hlt::Line/Hlt2CharmHadD02HHKsLL', 'Hlt::Line/Hlt2CharmHadD02HHKsDD', 'Hlt::Line/Hlt2Dst2PiD02PiPi', 'Hlt::Line/Hlt2Dst2PiD02MuMu', 'Hlt::Line/Hlt2Dst2PiD02KMu', 'Hlt::Line/Hlt2Dst2PiD02KPi', 'Hlt::Line/Hlt2PassThrough', 'Hlt::Line/Hlt2Transparent', 'Hlt::Line/Hlt2Lumi', 'Hlt::Line/Hlt2Forward', 'Hlt::Line/Hlt2DebugEvent', 'Hlt::Line/Hlt2CharmHadD2KS0KS0', 'Hlt::Line/Hlt2CharmHadD2KS0KS0WideMass', 'Hlt::Line/Hlt2CharmHadD02HH_D02PiPi', 'Hlt::Line/Hlt2CharmHadD02HH_D02PiPiWideMass', 'Hlt::Line/Hlt2CharmHadD02HH_D02KK', 'Hlt::Line/Hlt2CharmHadD02HH_D02KKWideMass', 'Hlt::Line/Hlt2CharmHadD02HH_D02KPi', 'Hlt::Line/Hlt2CharmHadD02HH_D02KPiWideMass', 'Hlt::Line/Hlt2ExpressJPsi', 'Hlt::Line/Hlt2ExpressJPsiTagProbe', 'Hlt::Line/Hlt2ExpressLambda', 'Hlt::Line/Hlt2ExpressKS', 'Hlt::Line/Hlt2ExpressDs2PhiPi', 'Hlt::Line/Hlt2ExpressBeamHalo', 'Hlt::Line/Hlt2ExpressDStar2D0Pi', 'Hlt::Line/Hlt2ExpressD02KPi', 'Hlt::Line/Hlt2CharmHadD2HHHKsLL', 'Hlt::Line/Hlt2CharmHadD2HHHKsDD', 'Hlt::Line/Hlt2CharmHadLambdaC2KPPi', 'Hlt::Line/Hlt2CharmHadLambdaC2KPPiWideMass', 'Hlt::Line/Hlt2CharmHadLambdaC2KPK', 'Hlt::Line/Hlt2CharmHadLambdaC2KPKWideMass', 'Hlt::Line/Hlt2CharmHadLambdaC2PiPPi', 'Hlt::Line/Hlt2CharmHadLambdaC2PiPPiWideMass', 'Hlt::Line/Hlt2CharmHadLambdaC2PiPK', 'Hlt::Line/Hlt2CharmHadLambdaC2PiPKWideMass', 'Hlt::Line/Hlt2Bs2PhiGamma', 'Hlt::Line/Hlt2Bs2PhiGammaWideBMass', 'Hlt::Line/Hlt2Bd2KstGamma', 'Hlt::Line/Hlt2Bd2KstGammaWideKMass', 'Hlt::Line/Hlt2Bd2KstGammaWideBMass', 'Hlt::Line/Hlt2CharmHadD2KS0H_D2KS0Pi', 'Hlt::Line/Hlt2CharmHadD2KS0H_D2KS0K', 'Hlt::Line/Hlt2CharmHadD2KS0H_D2KS0DDPi', 'Hlt::Line/Hlt2CharmHadD2KS0H_D2KS0DDK', 'Hlt::Line/Hlt2DiPhi', 'Hlt::Line/Hlt2KshortToMuMuPiPi', 'Hlt::Line/Hlt2CharmRareDecayD02MuMu', 'Hlt::Line/Hlt2B2HH', 'Hlt::Line/Hlt2LowMultD2KPi', 'Hlt::Line/Hlt2LowMultD2KPiPi', 'Hlt::Line/Hlt2LowMultD2K3Pi', 'Hlt::Line/Hlt2LowMultChiC2HH', 'Hlt::Line/Hlt2LowMultChiC2HHHH', 'Hlt::Line/Hlt2LowMultChiC2PP', 'Hlt::Line/Hlt2LowMultD2KPiWS', 'Hlt::Line/Hlt2LowMultD2KPiPiWS', 'Hlt::Line/Hlt2LowMultD2K3PiWS', 'Hlt::Line/Hlt2LowMultChiC2HHWS', 'Hlt::Line/Hlt2LowMultChiC2HHHHWS', 'Hlt::Line/Hlt2LowMultDDIncCP', 'Hlt::Line/Hlt2LowMultDDIncVF', 'Hlt::Line/Hlt2LowMultLMR2HH', 'Hlt::Line/Hlt2SingleMuon', 'Hlt::Line/Hlt2SingleMuonHighPT', 'Hlt::Line/Hlt2SingleMuonVHighPT', 'Hlt::Line/Hlt2SingleMuonLowPT', 'Hlt::Line/Hlt2DiProton', 'Hlt::Line/Hlt2DiProtonLowMult', 'Hlt::Line/Hlt2CharmSemilepD02HMuNu_D02KMuNuWS', 'Hlt::Line/Hlt2CharmSemilepD02HMuNu_D02PiMuNuWS', 'Hlt::Line/Hlt2CharmSemilepD02HMuNu_D02KMuNu', 'Hlt::Line/Hlt2CharmSemilepD02HMuNu_D02KMuNuTight', 'Hlt::Line/Hlt2CharmSemilepD02HMuNu_D02PiMuNu', 'Hlt::Line/Hlt2CharmHadMinBiasLambdaC2KPPi', 'Hlt::Line/Hlt2CharmHadMinBiasD02KPi', 'Hlt::Line/Hlt2CharmHadMinBiasD02KK', 'Hlt::Line/Hlt2CharmHadMinBiasDplus2hhh', 'Hlt::Line/Hlt2CharmHadMinBiasLambdaC2LambdaPi', 'Hlt::Line/Hlt2HighPtJets', 'Hlt::Line/Hlt2TFBc2JpsiMuX', 'Hlt::Line/Hlt2TFBc2JpsiMuXSignal', 'Hlt::Line/Hlt2diPhotonDiMuon', 'Hlt::Line/Hlt2LowMultMuon', 'Hlt::Line/Hlt2LowMultHadron', 'Hlt::Line/Hlt2LowMultHadron_nofilter', 'Hlt::Line/Hlt2LowMultPhoton', 'Hlt::Line/Hlt2LowMultElectron', 'Hlt::Line/Hlt2LowMultElectron_nofilter', 'Hlt::Line/Hlt2ChargedHyperon_Xi2Lambda0LLPi', 'Hlt::Line/Hlt2ChargedHyperon_Xi2Lambda0LLMu', 'Hlt::Line/Hlt2ChargedHyperon_Omega2Lambda0LLK', 'Hlt::Line/Hlt2ChargedHyperon_Xi2Lambda0DDPi', 'Hlt::Line/Hlt2ChargedHyperon_Xi2Lambda0DDMu', 'Hlt::Line/Hlt2ChargedHyperon_Omega2Lambda0DDK', 'Hlt::Line/Hlt2CharmHadD02HHXDst_hhX', 'Hlt::Line/Hlt2CharmHadD02HHXDst_hhXWideMass', 'Hlt::Line/Hlt2CharmHadD02HHXDst_BaryonhhX', 'Hlt::Line/Hlt2CharmHadD02HHXDst_BaryonhhXWideMass', 'Hlt::Line/Hlt2CharmHadD02HHXDst_BaryonhhXWithKSLL', 'Hlt::Line/Hlt2CharmHadD02HHXDst_BaryonhhXWithKSLLWideMass', 'Hlt::Line/Hlt2CharmHadD02HHXDst_BaryonhhXWithLambda0LL', 'Hlt::Line/Hlt2CharmHadD02HHXDst_BaryonhhXWithLambda0LLWideMass', 'Hlt::Line/Hlt2CharmHadD02HHXDst_BaryonhhXWithKSDD', 'Hlt::Line/Hlt2CharmHadD02HHXDst_BaryonhhXWithKSDDWideMass', 'Hlt::Line/Hlt2CharmHadD02HHXDst_BaryonhhXWithLambda0DD', 'Hlt::Line/Hlt2CharmHadD02HHXDst_BaryonhhXWithLambda0DDWideMass', 'Hlt::Line/Hlt2CharmHadD02HHXDst_LeptonhhX', 'Hlt::Line/Hlt2CharmHadD02HHXDst_LeptonhhXWideMass', 'Hlt::Line/Hlt2CharmHadD02HHXDst_LeptonhhXWithKSLL', 'Hlt::Line/Hlt2CharmHadD02HHXDst_LeptonhhXWithKSLLWideMass', 'Hlt::Line/Hlt2CharmHadD02HHXDst_LeptonhhXWithLambda0LL', 'Hlt::Line/Hlt2CharmHadD02HHXDst_LeptonhhXWithLambda0LLWideMass', 'Hlt::Line/Hlt2CharmHadD02HHXDst_LeptonhhXWithKSDD', 'Hlt::Line/Hlt2CharmHadD02HHXDst_LeptonhhXWithKSDDWideMass', 'Hlt::Line/Hlt2CharmHadD02HHXDst_LeptonhhXWithLambda0DD', 'Hlt::Line/Hlt2CharmHadD02HHXDst_LeptonhhXWithLambda0DDWideMass', 'Hlt::Line/Hlt2DisplVerticesSingleLoosePS', 'Hlt::Line/Hlt2DisplVerticesSingle', 'Hlt::Line/Hlt2DisplVerticesSingleHighFD', 'Hlt::Line/Hlt2DisplVerticesSingleDown', 'Hlt::Line/Hlt2DisplVerticesSingleVeryHighFD', 'Hlt::Line/Hlt2DisplVerticesSingleHighMass', 'Hlt::Line/Hlt2DisplVerticesSinglePS', 'Hlt::Line/Hlt2DisplVerticesDouble', 'Hlt::Line/Hlt2DisplVerticesDoublePS', 'Hlt::Line/Hlt2CharmSemilep3bodyD2PiMuMu', 'Hlt::Line/Hlt2CharmSemilep3bodyD2PiMuMuSS', 'Hlt::Line/Hlt2CharmSemilep3bodyD2KMuMu', 'Hlt::Line/Hlt2CharmSemilep3bodyD2KMuMuSS', 'Hlt::Line/Hlt2CharmSemilep3bodyLambdac2PMuMu', 'Hlt::Line/Hlt2CharmSemilep3bodyLambdac2PMuMuSS', 'Hlt::Line/Hlt2LambdaC_LambdaC2Lambda0LLPi', 'Hlt::Line/Hlt2LambdaC_LambdaC2Lambda0LLK', 'Hlt::Line/Hlt2LambdaC_LambdaC2Lambda0DDPi', 'Hlt::Line/Hlt2LambdaC_LambdaC2Lambda0DDK', 'Hlt::Line/Hlt2RadiativeTopoTrack', 'Hlt::Line/Hlt2RadiativeTopoPhoton', 'Hlt::Line/Hlt2B2HHPi0_Merged', 'Hlt::Line/Hlt2CharmHadD2HHH', 'Hlt::Line/Hlt2CharmHadD2HHHWideMass', 'Hlt::Line/Hlt2CharmHadD02HHHHDst_4pi', 'Hlt::Line/Hlt2CharmHadD02HHHHDst_4piWideMass', 'Hlt::Line/Hlt2CharmHadD02HHHH_4pi', 'Hlt::Line/Hlt2CharmHadD02HHHH_4piWideMass', 'Hlt::Line/Hlt2CharmHadD02HHHHDst_K3pi', 'Hlt::Line/Hlt2CharmHadD02HHHHDst_K3piWideMass', 'Hlt::Line/Hlt2CharmHadD02HHHH_K3pi', 'Hlt::Line/Hlt2CharmHadD02HHHH_K3piWideMass', 'Hlt::Line/Hlt2CharmHadD02HHHHDst_KKpipi', 'Hlt::Line/Hlt2CharmHadD02HHHHDst_KKpipiWideMass', 'Hlt::Line/Hlt2CharmHadD02HHHH_KKpipi', 'Hlt::Line/Hlt2CharmHadD02HHHH_KKpipiWideMass', 'Hlt::Line/Hlt2CharmHadD02HHHHDst_2K2pi', 'Hlt::Line/Hlt2CharmHadD02HHHHDst_2K2piWideMass', 'Hlt::Line/Hlt2CharmHadD02HHHH_2K2pi', 'Hlt::Line/Hlt2CharmHadD02HHHH_2K2piWideMass', 'Hlt::Line/Hlt2CharmHadD02HHHHDst_3Kpi', 'Hlt::Line/Hlt2CharmHadD02HHHHDst_3KpiWideMass', 'Hlt::Line/Hlt2CharmHadD02HHHH_3Kpi', 'Hlt::Line/Hlt2CharmHadD02HHHH_3KpiWideMass', 'Hlt::Line/Hlt2CharmSemilepD02PiPiMuMu', 'Hlt::Line/Hlt2CharmSemilepD02KKMuMu', 'Hlt::Line/Hlt2CharmSemilepD02KPiMuMu', 'Hlt::Line/Hlt2ErrorEvent', 'Hlt::Line/Hlt2Global']


HLT1_list = []
HLT2_list = []

for a in HLT1_full_list:
  if (not 'PassThrough' in a):
    HLT1_list.append(a.replace('Hlt::Line/','')+'Decision')
for b in HLT2_full_list:
  if(not 'PassThrough' in b):
    HLT2_list.append(b.replace('Hlt::Line/','')+'Decision')

trigger_list = L0_list + HLT1_list + HLT2_list


tuple.JPsi.addTupleTool('TupleToolTISTOS/TISTOS')
tuple.JPsi.TISTOS.TriggerList = trigger_list
tuple.JPsi.TISTOS.VerboseL0   = True
tuple.JPsi.TISTOS.VerboseHlt1 = True
tuple.JPsi.TISTOS.VerboseHlt2 = True



                
if isMC:
  from Configurables import MCDecayTreeTuple, MCTupleToolKinematic, TupleToolMCTruth, MCTupleToolHierarchy, MCTupleToolReconstructed, MCTupleToolAngles, TupleToolMCBackgroundInfo
  tuple.addTupleTool('TupleToolMCTruth/MCTruth')
  tuple.MCTruth.ToolList = ['MCTupleToolKinematic',
                                      'MCTupleToolHierarchy',
                                      'MCTupleToolReconstructed',
                                      'MCTupleToolAngles',
                                      ]
  tuple.JPsi.addTupleTool("TupleToolMCBackgroundInfo")


  mcTuple = MCDecayTreeTuple("MCTupleJPsi2KsKs") # I can put as an argument a name if I use more than a MCDecayTreeTuple
  mcTuple.Decay = '[J/psi(1S) -> ^(KS0 -> ^pi+ ^pi-) ^(KS0 -> ^pi+ ^pi-)]CC'
  mcTuple.Branches = {'JPsi' : '[J/psi(1S) -> (KS0 -> pi+ pi-) (KS0 -> pi+ pi-)]CC',
                                        'Ks1' : '[J/psi(1S) -> ^(KS0 -> pi+ pi-) (KS0 -> pi+ pi-)]CC',
                                        'Ks2' : '[J/psi(1S) -> (KS0 -> pi+ pi-) ^(KS0 -> pi+ pi-)]CC',
                                        'pi1' : '[J/psi(1S) -> (KS0 -> ^pi+ pi-) (KS0 -> pi+ pi-)]CC',
                                        'pi2' : '[J/psi(1S) -> (KS0 -> pi+ ^pi-) (KS0 -> pi+ pi-)]CC',
                                        'pi3' : '[J/psi(1S) -> (KS0 -> pi+ pi-) (KS0 -> ^pi+ pi-)]CC',
                                        'pi4' : '[J/psi(1S) -> (KS0 -> pi+ pi-) (KS0 -> pi+ ^pi-)]CC',
                                          }


  mcTuple.addBranches(mcTuple.Branches)
  mcTuple.ToolList = ['MCTupleToolKinematic',
                        'TupleToolEventInfo',
                        'MCTupleToolHierarchy',
                        "TupleToolMCBackgroundInfo",
                      ]




from Configurables import DaVinci

#Name of tuple file you want to write out.
DaVinci().TupleFile = "JPsi2KsKs.root"
DaVinci().EvtMax = -1
DaVinci().DataType = '2012'
DaVinci().Simulation = isMC

#This is very useful to make sure you didn't accidently miss some data. 
#Adds tuple in same file with lumi (units are pb-1).
DaVinci().Lumi = not isMC

#These database tags are used to specify the relevent conditions for your dataset.
#They can normally be found on the bookkeeping.

from Configurables import CondDB
#Here is a trick we just use the latest tags for 2012 data rather than hardocding them in
#, which is what we want to run on.
CondDB().LatestGlobalTagByDataType = "2012"

#Here we actually tell DaVinci what to run, this will often have a 
#'selection seuqence' before the ntuple stage.
DaVinci().appendToMainSequence( [seq.sequence(),tuple])
if isMC:
  DaVinci().UserAlgorithms += [mcTuple]