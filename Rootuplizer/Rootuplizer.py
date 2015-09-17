# Use DaVinci v33r8 and ganga 6
import sys, os
# to be able to import jobSetup using gaudirun
sys.path.append(os.getcwd())
from jobSetup import *

try:
    dataSample = dataSamples[open('dataSample.txt').readline()] 
except IOError:
    pass # keep dataSample defined in jobSetup.py and loaded with from import *


from Gaudi.Configuration import *
from DecayTreeTuple.Configuration import *
import GaudiKernel.SystemOfUnits as Units
from Configurables import DeterministicPrescaler

# Triggers
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

class strippingLine:
    """
    Class to store information about stripping line that I will need to make nTuple
    """
    def __init__(self,name, lineName, dec, branches):
        self.name = name
        self.lineName = lineName
        self.dec = dec 
        self.branches = branches 
        self.lineLocation = "Phys/"+lineName+"/Particles"
        
         
    def select(self):
        """
        Get data and selection
        """

        from PhysSelPython.Wrappers import Selection, SelectionSequence, DataOnDemand, AutomaticData
        # from StandardParticles import StdLooseMuons, StdLooseKaons
        from Configurables import FilterDesktop, CombineParticles, OfflineVertexFitter, LoKi__HDRFilter 
        from GaudiKernel.PhysicalConstants import c_light

        evtPreselectors = []

        if dataSample.isPrescaled != False:
            if dataSample.isPrescaled == True:
                dataSample.isPrescaled = 0.1
            prescaler =  DeterministicPrescaler("Prescaler", AcceptFraction = dataSample.isPrescaled)
            evtPreselectors.append(prescaler)


        # # Stripping filter
        strippingFilter = LoKi__HDRFilter( 'StripPassFilter', Code="HLT_PASS('Stripping"+self.lineName+"Decision')", Location="/Event/Strip/Phys/DecReports" )
        evtPreselectors.append(strippingFilter)


        stripped_data = AutomaticData(Location = self.lineLocation)
        
        # Trigger selection
        # from Configurables import TisTosParticleTagger
        # _tisTosFilter = TisTosParticleTagger( self.name + "Triggered" )
        # _tisTosFilter.TisTosSpecs = { 'L0Global%TUS' : 0,
        #                               'L0Global%TIS' : 0,
        #                               }
        # for trigger in trigger_list:
        #     for tistos in ['TIS', 'TUS']:
        #         _tisTosFilter.TisTosSpecs['{0}%{1}'.format(trigger, tistos)] = 0
        
        # triggered_data =  Selection( self.name+'TriggerSelection',
        #                              Algorithm = _tisTosFilter,
        #                              RequiredSelections = [ stripped_data ],
        #                              )
        
        Candidate_selection = stripped_data # triggered_data
        
        self.sequence = SelectionSequence('Seq'+self.name,
                                          TopSelection = Candidate_selection,
                                          EventPreSelector = evtPreselectors)
        
    def makeTuple(self):
        """
        Make tuple
        """

        from Configurables import FitDecayTrees, DecayTreeTuple, TupleToolDecayTreeFitter, TupleToolDecay, TupleToolTrigger, TupleToolTISTOS, TupleToolPropertime, PropertimeFitter, TupleToolKinematic, TupleToolGeometry, TupleToolEventInfo, TupleToolPrimaries, TupleToolPid, TupleToolTrackInfo, TupleToolRecoStats, TupleToolMCTruth,  LoKi__Hybrid__TupleTool, LoKi__Hybrid__EvtTupleTool
        

        tuple = DecayTreeTuple('Tuple'+self.name) # I can put as an argument a name if I use more than a DecayTreeTuple
        tuple.Inputs = [ self.sequence.outputLocation() ]
        tuple.Decay = self.dec
        tuple.ToolList = ['TupleToolKinematic',
                          'TupleToolEventInfo', 
                          'TupleToolTrackInfo',
                          'TupleToolPid',
                          'TupleToolGeometry', 
                          'TupleToolAngles', # Helicity angle
                          # 'TupleToolPropertime', #proper time TAU of reco particles
                          ]

        

        # Other event infos
        tuple.addTupleTool('LoKi::Hybrid::EvtTupleTool/LoKi_Evt')
        if dataSample.isMC:
            tuple.LoKi_Evt.VOID_Variables = {
                # "nSPDHits" :  " CONTAINS('Raw/Spd/Digits')  " ,
                "nTracks" : "TrSOURCE('Rec/Track/Best') >> TrSIZE"
                ,"nPVs"   : "CONTAINS('Rec/Vertex/Primary')"
                }
        else:
            tuple.LoKi_Evt.VOID_Variables = {
                # "nSPDHits" :  " CONTAINS('Raw/Spd/Digits')  " ,
                "nTracks"  : "CONTAINS('/Event/Charm/Rec/Track/Best')"
                ,"nPVs"    : "CONTAINS('/Event/Charm/Rec/Vertex/Primary')"
                }
            
        # # Other variables
        # tuple.addTupleTool('LoKi::Hybrid::TupleTool/LoKi_All')
        # tuple.LoKi_All.Variables = {
        #     'BPVIPCHI2' : 'BPVIPCHI2()',
        #     'BPVDIRA' : 'BPVDIRA',
        #     'BPVLTFITCHI2' : 'BPVLTFITCHI2()',           
        #     } 
        
        tuple.addBranches(self.branches)
        
        tuple.phi.addTupleTool("LoKi::Hybrid::TupleTool/LoKi_phi")
        tuple.phi.LoKi_phi.Variables =  {
            'DOCAMAX' : 'DOCAMAX',
            "MassDiff_Phi" : "DMASS('phi(1020)')",
            "BPVDIRA" : "BPVDIRA",
            "IPS_Phi" : "MIPCHI2DV(PRIMARY)",
            "VFASPF_CHI2DOF" : "VFASPF(VCHI2/VDOF)",
            "VFASPF_CHI2" : "VFASPF(VCHI2)",
            "BPVIPCHI2" : "BPVIPCHI2()",
            "ADOCA" : "DOCA(1,2)",
            "ADOCACHI2" : "DOCACHI2(1,2)",

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

        
        # Triggers:   
        tuple.phi.addTupleTool('TupleToolTISTOS/TISTOS')
        tuple.phi.TISTOS.TriggerList = trigger_list
        tuple.phi.TISTOS.VerboseL0   = True
        tuple.phi.TISTOS.VerboseHlt1 = True
        tuple.phi.TISTOS.VerboseHlt2 = True
        
                
        if dataSample.isMC:
            from Configurables import MCDecayTreeTuple, MCTupleToolKinematic, TupleToolMCTruth, MCTupleToolHierarchy, MCTupleToolReconstructed, MCTupleToolAngles, TupleToolMCBackgroundInfo
            tuple.addTupleTool('TupleToolMCTruth/MCTruth')
            tuple.MCTruth.ToolList = ['MCTupleToolKinematic',
                                      'MCTupleToolHierarchy',
                                      'MCTupleToolReconstructed',
                                      'MCTupleToolAngles',
                                      ]
            tuple.phi.addTupleTool( "TupleToolMCBackgroundInfo")

        
        self.sequence.sequence().Members += [tuple]

        # tuple.OutputLevel = DEBUG

############################################################
def addMCTuple(name, decayDescriptor):
    '''
    Given name and decay descriptor, add MCTuple to the main DaVinci Sequence
    '''
     # MC    
    mcTuple = MCDecayTreeTuple('MCTuple'+name) # I can put as an argument a name if I use more than a MCDecayTreeTuple
    mcTuple.Decay = decayDescriptor #'[phi(1020) -> ^(KS0 -> ^pi+ ^pi-) ^(KS0 -> ^pi+ ^pi-)]CC'
    mcTuple.ToolList = ['MCTupleToolKinematic',
                        'TupleToolEventInfo',
                        'MCTupleToolHierarchy',
                        "TupleToolMCBackgroundInfo",
                      ]
    DaVinci().UserAlgorithms += [mcTuple]
    


############################################################
## Configure DaVinci
from Configurables import DaVinci

if not dataSample.isMC:
    DaVinci.RootInTES = '/Event/Charm'
    DaVinci().InputType= 'MDST'
else:
    DaVinci().InputType= 'DST'
    
DaVinci().Simulation = dataSample.isMC
DaVinci().DataType = dataSample.dataType
DaVinci().EvtMax = -1#nEvents # 100000
DaVinci().Lumi = not dataSample.isMC

from Configurables import CondDB
CondDB(LatestGlobalTagByDataType=dataSample.dataType)
if dataSample.DDDBtag: DaVinci().DDDBtag = dataSample.DDDBtag 
if dataSample.CondDBtag: DaVinci().CondDBtag = dataSample.CondDBtag 

#DaVinci().EventPreFilters += [strippingFilter]
#if dataSample.isMC: DaVinci().UserAlgorithms += [mcTuple]


##Debug Background#
# from Configurables import PrintDecayTree
# printTree = PrintDecayTree(Inputs = [ location ])
# DaVinci().appendToMainSequence( [ printTree ] )
# from Configurables import PrintMCTree, PrintMCDecayTreeTool
# mctree = PrintMCTree("PrintDs")
# mctree.addTool(PrintMCDecayTreeTool, name = "PrintMC")
# mctree.PrintMC.Information = "Name M P Px Py Pz Pt"
# mctree.ParticleNames = [ "D_s+", "D_s-"]
# mctree.Depth = 3
# Xib_sequence.sequence().Members += [ mctree ] 
##################


Phi2KsKs_line = strippingLine(name = 'Phi2KsKs',
                              lineName = 'PhiToKSKS_PhiToKsKsLine',
                              dec = '[phi(1020) -> ^(KS0 -> ^pi+ ^pi-) ^(KS0 -> ^pi+ ^pi-)]CC',
                              branches = {'phi' : '[phi(1020) -> (KS0 -> pi+ pi-) (KS0 -> pi+ pi-)]CC',
                                          'Ks1' : '[phi(1020) -> ^(KS0 -> pi+ pi-) (KS0 -> pi+ pi-)]CC',
                                          'Ks2' : '[phi(1020) -> (KS0 -> pi+ pi-) ^(KS0 -> pi+ pi-)]CC',
                                          'pi1' : '[phi(1020) -> (KS0 -> ^pi+ pi-) (KS0 -> pi+ pi-)]CC',
                                          'pi2' : '[phi(1020) -> (KS0 -> pi+ ^pi-) (KS0 -> pi+ pi-)]CC',
                                          'pi3' : '[phi(1020) -> (KS0 -> pi+ pi-) (KS0 -> ^pi+ pi-)]CC',
                                          'pi4' : '[phi(1020) -> (KS0 -> pi+ pi-) (KS0 -> pi+ ^pi-)]CC',
                                          })


if dataSample.isMC: # Kill banks with old stripping
    from Configurables import EventNodeKiller
    eventNodeKiller = EventNodeKiller('Stripkiller')
    eventNodeKiller.Nodes = [ '/Event/AllStreams', '/Event/Strip' ]

    #   Rerun the stripping selection if MC


    from StrippingConf.Configuration import StrippingConf, StrippingStream
    from StrippingSettings.Utils import strippingConfiguration
    from StrippingArchive.Utils import buildStreams
    from StrippingArchive import strippingArchive
    
    # Standard stripping21 
    stripping='stripping21'
    config  = strippingConfiguration(stripping)
    archive = strippingArchive(stripping)
    streams = buildStreams(stripping=config, archive=archive)
    
    # Select my line   
    MyStream = StrippingStream("MyStream")
    MyLines = [ 'Stripping'+line.lineName for line in [Phi2KsKs_line] ]
    
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

    DaVinci().appendToMainSequence( [ eventNodeKiller, sc.sequence() ] )

    # MC Tuples
    addMCTuple('phi2KsKs', '[phi(1020) -> ^(KS0 -> ^pi+ ^pi-) ^(KS0 -> ^pi+ ^pi-)]CC')
    addMCTuple('phi2KsKl', '[phi(1020) -> ^(KS0 -> ^pi+ ^pi-) ^(KL0 -> ^pi+ ^pi-)]CC')
    # if 'minbias' in dataSample.name:
    #     addMCTuple('phi2KK', '[phi(1020) -> ^K+ ^K-]CC')
    #     addMCTuple('phi2K0K0', '[phi(1020) -> ^KS0 ^KL0]CC')
    #     # addMCTuple('KsKs', '[(KS0 -> ^pi+ ^pi-)cc && (KS0 -> ^pi+ ^pi-)cc]')
    #     addMCTuple('Ks', '[KS0 -> ^pi+ ^pi-]CC')

    from Configurables import PrintMCTree, PrintMCDecayTreeTool
    mctree = PrintMCTree("PrintTruePhi")
    mctree.addTool(PrintMCDecayTreeTool, name = "PrintMC")
    mctree.PrintMC.Information = "Name"
    mctree.ParticleNames = [ "phi(1020)", 'KS0' ]
    mctree.Depth = 2
   
    
###########################################################

for strLine in [Phi2KsKs_line]:
    strLine.select()
    strLine.makeTuple()

    DaVinci().appendToMainSequence( [ strLine.sequence.sequence() ])


DaVinci().HistogramFile = "DVHistos.root"
DaVinci().TupleFile = dataSample.outputNtupleName

# ###################################################
# #
# # Configuration of uDSTWriter
# #

# from DSTWriters.Configuration import SelDSTWriter, stripMicroDSTStreamConf, stripMicroDSTElements

# SelDSTWriterConf = {'default' : stripMicroDSTStreamConf(pack=False)}

# SelDSTWriterElements = {'default' : stripMicroDSTElements(pack=False)}

# udstWriter = SelDSTWriter('MyMicroDSTWriter',
#                           StreamConf = SelDSTWriterConf,
#                           MicroDSTElements = SelDSTWriterElements,
#                           OutputFileSuffix = dataSample.outputNtupleName.split('.')[0],
#                           SelectionSequences = sc.activeStreams(),
#                           )

# DaVinci().appendToMainSequence( [ udstWriter.sequence() ] )

# ###################################################

from Configurables import Gaudi__IODataManager as IODataManager
IODataManager( "IODataManager" ).UseGFAL = False


