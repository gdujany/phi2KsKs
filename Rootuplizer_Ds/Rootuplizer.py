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
        from Configurables import TisTosParticleTagger
        _tisTosFilter = TisTosParticleTagger( self.name + "Triggered" )
        _tisTosFilter.TisTosSpecs = { 'L0Global%TUS' : 0,
                                      'L0Global%TIS' : 0,
                                      }
        for trigger in trigger_list:
            for tistos in ['TIS', 'TUS']:
                _tisTosFilter.TisTosSpecs['{0}%{1}'.format(trigger, tistos)] = 0
        
        triggered_data =  Selection( self.name+'TriggerSelection',
                                     Algorithm = _tisTosFilter,
                                     RequiredSelections = [ stripped_data ],
                                     )
        
        Candidate_selection = stripped_data #triggered_data 
        
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

        
        tuple.InputPrimaryVertices = '/Event/Charm/Rec/Vertex/Primary'


        # Other event infos
        tuple.addTupleTool('LoKi::Hybrid::EvtTupleTool/LoKi_Evt')
        tuple.LoKi_Evt.VOID_Variables = {
            #"nSPDHits" :  " CONTAINS('Raw/Spd/Digits')  " ,
            'nTracks' :  " CONTAINS ('Charm/Rec/Track/Best') "  ,
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

            "DTF_CHI2_PV"   : "DTF_CHI2( True, 'phi(1020)' )",
            "DTF_NDOF_PV"   : "DTF_NDOF( True, 'phi(1020)' )",
            "DTF_M_PV"      : "DTF_FUN ( M, True, 'phi(1020)' )",
            "DTF_M_Ks1_PV"    : "DTF_FUN ( CHILD(M,1), True, 'phi(1020)' )",
            "DTF_M_Ks2_PV"    : "DTF_FUN ( CHILD(M,2), True, 'phi(1020)' )",
           
            # "DTF_CTAU_Ks1"    : "DTF_CTAU(1, False, 'phi(1020)' )",
            # "DTF_CTAU_Ks2"    : "DTF_CTAU(2, False, 'phi(1020)' )",
            
           
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
DaVinci().EvtMax = nEvents # 100000
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


Phi2KsKs_line = strippingLine(name = 'Ds_Phi2KsKs',
                              lineName = 'PhiToKSKS_PhiToKsKsLine',
                              dec = '[D_s+ -> ^(phi(1020) -> ^(KS0 -> ^pi+ ^pi-) ^(KS0 -> ^pi+ ^pi-)) ^pi+]CC',
                              branches = {'Ds' : '[D_s+ -> (phi(1020) -> (KS0 -> pi+ pi-) (KS0 -> pi+ pi-)) pi+]CC',
                                        'phi' : '[D_s+ -> ^(phi(1020) -> (KS0 -> pi+ pi-) (KS0 -> pi+ pi-)) pi+]CC',
                                        'Ks1' : '[D_s+ -> (phi(1020) -> ^(KS0 -> pi+ pi-) (KS0 -> pi+ pi-)) pi+]CC',
                                        'Ks2' : '[D_s+ -> (phi(1020) -> (KS0 -> pi+ pi-) ^(KS0 -> pi+ pi-)) pi+]CC',
                                        'pi1' : '[D_s+ -> (phi(1020) -> (KS0 -> ^pi+ pi-) (KS0 -> pi+ pi-)) pi+]CC',
                                        'pi2' : '[D_s+ -> (phi(1020) -> (KS0 -> pi+ ^pi-) (KS0 -> pi+ pi-)) pi+]CC',
                                        'pi3' : '[D_s+ -> (phi(1020) -> (KS0 -> pi+ pi-) (KS0 -> ^pi+ pi-)) pi+]CC',
                                        'pi4' : '[D_s+ -> (phi(1020) -> (KS0 -> pi+ pi-) (KS0 -> pi+ ^pi-)) pi+]CC',
                                        'pis' : '[D_s+ -> (phi(1020) -> (KS0 -> pi+ pi-) (KS0 -> pi+ pi-)) ^pi+]CC',
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
    addMCTuple('Ds_phi2KsKl', '[D_s+ -> ^(phi(1020) -> ^(KS0 -> ^pi+ ^pi-) ^(KS0 -> ^pi+ ^pi-)) ^pi+]CC')
    if 'minbias' in dataSample.name:
        addMCTuple('phi2KK', '[phi(1020) -> ^K- ^K-]CC')
        # addMCTuple('KsKs', '[(KS0 -> ^pi+ ^pi-)cc && (KS0 -> ^pi+ ^pi-)cc]')
        addMCTuple('Ks', '[KS0 -> ^pi+ ^pi-]CC')

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


