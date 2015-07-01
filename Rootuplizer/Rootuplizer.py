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

class strippingLine:
    """
    Class to store information about stripping line that I will need to make nTuple
    """
    def __init__(self,name, lineName, dec, branches):
        self.name = name
        self.lineName = lineName
        self.dec = dec 
        self.branches = branches 

        if dataSample.isMC:
            self.lineLocation = "Phys/"+lineName+"/Particles"
        else:
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

        if dataSample.isPrescaled:
            prescaler =  DeterministicPrescaler("Prescaler", AcceptFraction = 0.1)
            evtPreselectors.append(prescaler)


        # # Stripping filter
        strippingFilter = LoKi__HDRFilter( 'StripPassFilter', Code="HLT_PASS('Stripping"+self.lineName+"Decision')", Location="/Event/Strip/Phys/DecReports" )
        evtPreselectors.append(strippingFilter)


        Candidate_selection = AutomaticData(Location = self.lineLocation)

        self.sequence = SelectionSequence('Seq'+self.name,
                                 TopSelection = Candidate_selection,
                                 EventPreSelector = evtPreselectors)

    def makeTuple(self):
        """
        Make tuple
        """

        from Configurables import FitDecayTrees, DecayTreeTuple, TupleToolDecayTreeFitter, TupleToolDecay, TupleToolTrigger, TupleToolTISTOS, TupleToolPropertime, PropertimeFitter, TupleToolKinematic, TupleToolGeometry, TupleToolEventInfo, TupleToolPrimaries, TupleToolPid, TupleToolTrackInfo, TupleToolRecoStats, TupleToolMCTruth, TupleToolMCBackgroundInfo, LoKi__Hybrid__TupleTool, LoKi__Hybrid__EvtTupleTool
        

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


        # # Other event infos
        # tuple.addTupleTool('LoKi::Hybrid::EvtTupleTool/LoKi_Evt')
        # tuple.LoKi_Evt.VOID_Variables = {
        #     #"nSPDHits" :  " CONTAINS('Raw/Spd/Digits')  " ,
        #     'nTracks' :  " CONTAINS ('Bhadron/Rec/Track/Best') "  ,
        #     }
        
        # Other variables
        # tuple.addTupleTool('LoKi::Hybrid::TupleTool/LoKi_All')
        # tuple.LoKi_All.Variables = {
        #     'BPVIPCHI2' : 'BPVIPCHI2()',
        #     'BPVDIRA' : 'BPVDIRA',
        #     'BPVLTFITCHI2' : 'BPVLTFITCHI2()',           
        #     } 
        
        tuple.addBranches(self.branches)
        
        # tuple.B.addTupleTool("LoKi::Hybrid::TupleTool/LoKi_B")
        # tuple.B.LoKi_B.Preambulo = [
        #     "from LoKiCore.math import sqrt",
        #     "p_E  = CHILD(E,  {})".format(1),
        #     "p_PX  = CHILD(PX,  {})".format(1),
        #     "p_PY  = CHILD(PY,  {})".format(1),
        #     "p_PZ  = CHILD(PZ,  {})".format(1),
        #     "pbar_E  = CHILD(E,  {})".format(2),
        #     "pbar_PX  = CHILD(PX,  {})".format(2),
        #     "pbar_PY  = CHILD(PY,  {})".format(2),
        #     "pbar_PZ  = CHILD(PZ,  {})".format(2),
        #     "h1_E  = CHILD(E,  {})".format(3),
        #     "h1_PX  = CHILD(PX,  {})".format(3),
        #     "h1_PY  = CHILD(PY,  {})".format(3),
        #     "h1_PZ  = CHILD(PZ,  {})".format(3),
        #     "h2_E  = CHILD(E,  {})".format(4),
        #     "h2_PX  = CHILD(PX,  {})".format(4),
        #     "h2_PY  = CHILD(PY,  {})".format(4),
        #     "h2_PZ  = CHILD(PZ,  {})".format(4),
        #     "ppbar_M = sqrt( (p_E + pbar_E)**2 - (p_PX + pbar_PX)**2 - (p_PY + pbar_PY)**2 - (p_PZ + pbar_PZ)**2 )",
        #     "h1h2_M = sqrt( (h1_E + h2_E)**2 - (h1_PX + h2_PX)**2 - (h1_PY + h2_PY)**2 - (h1_PZ + h2_PZ)**2 )",
        #     "ph1h2_M = sqrt( (p_E + h1_E + h2_E)**2 - (p_PX + h1_PX + h2_PX)**2 - (p_PY + h1_PY + h2_PY)**2 - (p_PZ + h1_PZ + h2_PZ)**2 )",
        #     "pbarh1h2_M = sqrt( (pbar_E + h1_E + h2_E)**2 - (pbar_PX + h1_PX + h2_PX)**2 - (pbar_PY + h1_PY + h2_PY)**2 - (pbar_PZ + h1_PZ + h2_PZ)**2 )",
        #     "ppbarh1_M = sqrt( (p_E + pbar_E + h1_E)**2 - (p_PX + pbar_PX + h1_PX)**2 - (p_PY + pbar_PY + h1_PY)**2 - (p_PZ + pbar_PZ + h1_PZ)**2 )",
        #     "ppbarh2_M = sqrt( (p_E + pbar_E + h2_E)**2 - (p_PX + pbar_PX + h2_PX)**2 - (p_PY + pbar_PY + h2_PY)**2 - (p_PZ + pbar_PZ + h2_PZ)**2 )",
        #     ]
        # tuple.B.LoKi_B.Variables =  {
        #     'DOCAMAX' : 'DOCAMAX',
        #     'ppbar_M' : 'ppbar_M',
        #     'h1h2_M' : 'h1h2_M',
        #     'ph1h2_M' : 'ph1h2_M',
        #     'pbarh1h2_M' : 'pbarh1h2_M',
        #     'ppbarh1_M' : 'ppbarh1_M',
        #     'ppbarh2_M' : 'ppbarh2_M',
        #     # 'DOCAMIN' : 'DOCAMIN', doesn't work, maybe it's a different functor
        #     # 'MpPi' : "WM('p+', 'pi-')",
        #     # 'MpK' : "WM('p+', 'K-')",
        #     }
        

        # def mySharedConf_p(branch):
        #     atool=branch.addTupleTool('LoKi::Hybrid::TupleTool/LoKi_p')
        #     atool.Variables =  {
        #         'TRCHI2DOF' : 'TRCHI2DOF',
        #         'TRGHOSTPROB' : 'TRGHOSTPROB',
        #         }

        # mySharedConf_p(tuple.p)
        # mySharedConf_p(tuple.pbar)

        # def mySharedConf_h(branch):
        #     atool=branch.addTupleTool('LoKi::Hybrid::TupleTool/LoKi_h')
        #     atool.Variables =  {
        #         'TRCHI2DOF' : 'TRCHI2DOF',
        #         'TRGHOSTPROB' : 'TRGHOSTPROB',
        #         }

        # mySharedConf_h(tuple.h1)
        # mySharedConf_h(tuple.h2)     
        
        
        
        # # Triggers:
        # L0_list = ['L0HadronDecision']
        # HLT1_list = ['Hlt1TrackAllL0Decision']
        # HLT2_list = ['Hlt2Topo{0}Body{1}Decision'.format(i,j) for i in (2,3,4) for j in ('BBDT', 'Simple')]
        
        # tuple.B.addTupleTool('TupleToolTISTOS/TISTOS')
        # tuple.B.TISTOS.TriggerList = L0_list + HLT1_list + HLT2_list
        # tuple.B.TISTOS.VerboseL0   = True
        # tuple.B.TISTOS.VerboseHlt1 = True
        # tuple.B.TISTOS.VerboseHlt2 = True
                
        # if dataSample.isMC:
        #     from Configurables import MCDecayTreeTuple, MCTupleToolKinematic, TupleToolMCTruth
        #     tuple.addTupleTool('TupleToolMCTruth/MCTruth')
        #     tuple.MCTruth.ToolList = ['MCTupleToolKinematic',
        #                               'MCTupleToolHierarchy',
        #                               'MCTupleToolReconstructed',
        #                               ]
        #     tuple.B.addTupleTool( "TupleToolMCBackgroundInfo")

        
        self.sequence.sequence().Members += [tuple]

        # tuple.OutputLevel = DEBUG


############################################################
## Configure DaVinci
from Configurables import DaVinci

DaVinci.RootInTES = '/Event/Charm'
DaVinci().Simulation = dataSample.isMC
DaVinci().DataType = dataSample.dataType
DaVinci().InputType= 'MDST'
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


Phi2KsKs_line = strippingLine(name = 'Phi2KsKs',
                              lineName = 'PhiToKSKS_PhiToKsKsLine',
                              dec = '[phi(1020) -> ^(KS0 -> ^pi+ ^pi-) ^(KS0 -> ^pi+ ^pi-)]CC',
                              branches = {'Phi' : '[phi(1020) -> (KS0 -> pi+ pi-) (KS0 -> pi+ pi-)]CC',
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

   
    # MC TUPLE
    # if 'phi2ppKK' in dataSample.name:
    #     MC_DecayDescriptor = '[B_s0 -> ^p+ ^p~- ^K+ ^K-]CC'
    #     MC_branches = {'B' : '[B_s0 -> p+ p~- K+ K-]CC',
    #                    'p' : '[B_s0 -> ^p+ p~- K+ K-]CC',
    #                    'pbar' : '[B_s0 -> p+ ^p~- K+ K-]CC',
    #                    'h1' : '[B_s0 -> p+ p~- ^K+ K-]CC',
    #                    'h2' : '[B_s0 -> p+ p~- K+ ^K-]CC',
    #                    }
    
        
    mcTuple = MCDecayTreeTuple() # I can put as an argument a name if I use more than a MCDecayTreeTuple
    mcTuple.Decay = MC_DecayDescriptor
    mcTuple.ToolList = ['MCTupleToolKinematic',
                        'TupleToolEventInfo',
                        'MCTupleToolHierarchy',
                      ]

    mcTuple.addTupleTool("LoKi::Hybrid::MCTupleTool/LoKi_All")
    mcTuple.LoKi_All.Variables =  {
        'TRUEID' : 'MCID'
        }
    
    # mcTuple.addBranches(MC_branches)

    # mcTuple.Head.addTupleTool("LoKi::Hybrid::MCTupleTool/LoKi_Head")
    # mcTuple.Head.LoKi_Head.Preambulo = [
    #     "from LoKiCore.math import sqrt",
    #     "Phi_E  = MCCHILD(MCE,  {})".format(numbers_phi_X[0]),
    #     "Phi_PX = MCCHILD(MCPX, {})".format(numbers_phi_X[0]),
    #     "Phi_PY = MCCHILD(MCPY, {})".format(numbers_phi_X[0]),
    #     "Phi_PZ = MCCHILD(MCPZ, {})".format(numbers_phi_X[0]),
    #     "X_P  = MCCHILD(MCP,  {})".format(numbers_phi_X[1]),
    #     "X_E_asMu  = sqrt(105.6583715**2 + X_P**2)",
    #     "X_E_asPi  = sqrt(139.57018**2 + X_P**2)",
    #     "X_PX = MCCHILD(MCPX, {})".format(numbers_phi_X[1]),
    #     "X_PY = MCCHILD(MCPY, {})".format(numbers_phi_X[1]),
    #     "X_PZ = MCCHILD(MCPZ, {})".format(numbers_phi_X[1]),
    #     "PhiMu_M = sqrt( (Phi_E + X_E_asMu)**2 - (Phi_PX + X_PX)**2 - (Phi_PY + X_PY)**2 - (Phi_PZ + X_PZ)**2 )",
    #     "PhiPi_M = sqrt( (Phi_E + X_E_asPi)**2 - (Phi_PX + X_PX)**2 - (Phi_PY + X_PY)**2 - (Phi_PZ + X_PZ)**2 )",
    #     ]
    # mcTuple.Head.LoKi_Head.Variables =  {
    #     'CHILD_1_ID' : "MCCHILD(MCID,1)",
    #     'CHILD_2_ID' : "MCCHILD(MCID,2)",
    #     'PhiMu_M' : 'PhiMu_M',
    #     'PhiPi_M' : 'PhiPi_M',
    #     }

    DaVinci().UserAlgorithms += [mcTuple]
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


