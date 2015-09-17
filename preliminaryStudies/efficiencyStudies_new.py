#!/usr/bin/env python

import sys, os
from CompareTreeVars import getHisto, CompareTreeVars
import ROOT as r
from ROOT import TTree
import numpy as np

r.gROOT.SetBatch(True)

# Get trees

eos_root = os.path.expanduser('~/eos/')
if not os.listdir(eos_root):
    raise OSError('EOS not mounted, please type:\n eosmount '+eos_root)

store_dir_g = os.path.join(eos_root, 'lhcb/user/g/gdujany/phi2KsKs/')
store_dir_s = '/afs/cern.ch/work/s/sbartkow/files/'

inFiles = {}
inFiles['data2012_Ds'] = r.TFile(os.path.join(store_dir_s, 'Ds_Phi2KsKs_2012.root'))
inFiles['data2012_incl'] = r.TFile(os.path.join(store_dir_g, '../phi2KsKs_noTrigger/data2012.root'))
inFiles['phi2KsKs_incl'] = r.TFile(os.path.join(store_dir_g, 'phi2KsKs_incl.root'))
inFiles['phi2KsKs_Ds'] = r.TFile(os.path.join(store_dir_s, 'Ds_Phi2KsKs_Ds_fulltrigger.root'))# 'Ds_Phi2KsKs_Ds.root'))
inFiles['minbias_incl'] = r.TFile(os.path.join(store_dir_s, 'Phi2KsKs_MBcomb.root'))
inFiles['minbias_Ds'] = r.TFile(os.path.join(store_dir_s, 'Ds_Phi2KsKs_MBcomb.root'))

trees = {}
treesMC = {}


xsec_incl = 3516
xsec_Ds = 388
BR_incl = .342
BR_Ds_Ds = .045
BR_Ds = BR_Ds_Ds*BR_incl
GenCut_incl = .025
GenCut_Ds = .070
PropKsKl_bp1 = 3.9792836074923865e-07
PropKsKl_bp2 = 4.985315252445719e-10
PropKsKs_bp1 = 5.125122811889336e-07
PropKsKs_bp2 = 1.6374842740761122e-08





def format_e(n):
    a = '{:.2e}'.format(n)
    if(not '+00' in a.split('e')[1]):
        x = a.split('e')[1]
        if(x.startswith('+')):
            x = x.replace('x','')
        while(x.startswith('0')):
            x = x.replace('0','')
        while(x.startswith('-0')):
            x = x.replace('-0','-')
        return a.split('e')[0].rstrip('0').rstrip('.') + '\cdot 10^{' + x + '}'
    else:
        return a.split('e')[0].rstrip('0').rstrip('.')

def isint(b):
    if(b>2.):
        return int(round(b,0))
    else:
        return format_e(b)



effi_Reco_incl = [0.0,0.0] #[1bp,2bp]
effi_Reco_Ds = [0.0,0.0] #[1bp,2bp]

effi_L0_incl = [(0.0,0.0,0.0),(0.0,0.0,0.0)] #[(1bp,1bp_TIS,1bp_TOS),(2bp,2bp_TIS,2bp_TOS)]
effi_L0_Ds = [(0.0,0.0,0.0),(0.0,0.0,0.0)] #[(1bp,1bp_TIS,1bp_TOS),(2bp,2bp_TIS,2bp_TOS)]

effi_Hlt1_incl = [(0.0,0.0,0.0),(0.0,0.0,0.0)] #[(1bp,1bp_TIS,1bp_TOS),(2bp,2bp_TIS,2bp_TOS)]
effi_Hlt1_Ds = [(0.0,0.0,0.0),(0.0,0.0,0.0)] #[(1bp,1bp_TIS,1bp_TOS),(2bp,2bp_TIS,2bp_TOS)]

effi_Hlt2_incl = [(0.0,0.0,0.0),(0.0,0.0,0.0)] #[(1bp,1bp_TIS,1bp_TOS),(2bp,2bp_TIS,2bp_TOS)]
effi_Hlt2_Ds = [(0.0,0.0,0.0),(0.0,0.0,0.0)] #[(1bp,1bp_TIS,1bp_TOS),(2bp,2bp_TIS,2bp_TOS)]

retention_incl = [0.0,0.0] #[1bp,2bp]
retention_Ds = [0.0,0.0] #[1bp,2bp]

exp_combbkg_incl = [0.0,0.0] #[1bp,2bp]
exp_combbkg_Ds = [0.0,0.0] #[1bp,2bp]
exp_SMbkg_incl = [0.0,0.0] #[1bp,2bp]
exp_SMbkg_Ds = [0.0,0.0] #[1bp,2bp]


for key, inFile in inFiles.items():
    print('********************'+key+'********************')
    trees[key] = inFile.Get('TuplePhi2KsKs/DecayTree')
    if(key=='phi2KsKs_incl' and not 'data2012' in key):
        treesMC[key] = inFile.Get('MCTuplephi2KsKs/MCDecayTree')
    elif(not 'data2012' in key or not 'minbias' in key ):
        treesMC[key] = inFile.Get('MCTuplePhi2KsKs/MCDecayTree')

    #Figuring out the cuts

    names = [b.GetName() for b in trees[key].GetListOfBranches()]

    truthmatch = 'phi_BKGCAT==0'
    L0trigger = 'phi_L0Global_Dec'
    L0trigger_TIS = 'phi_L0Global_TIS'
    L0trigger_TOS = 'phi_L0Global_TOS'
    Hlt1trigger = '('
    Hlt1trigger_TIS = '('
    Hlt1trigger_TOS = '('


    for i in names:
        if('Hlt1' in i and not 'Global' in i and not 'Phys' in i and not 'Hlt1LumiDecision' in i):
            testif0 = 0
            for j in ['phi_Hlt1LumiMidBeamCrossingDecision_Dec','phi_Hlt1MBNoBiasDecision_Dec','phi_Hlt1CharmCalibrationNoBiasDecision_Dec',
                        'phi_Hlt1MBMicroBiasVeloDecision_Dec','phi_Hlt1MBMicroBiasTStationDecision_Dec','phi_Hlt1HighPtJetsSinglePVDecision_Dec',
                        'phi_Hlt1L0AnyDecision_Dec','phi_Hlt1L0AnyNoSPDDecision_Dec','phi_Hlt1L0HighSumETJetDecision_Dec','phi_Hlt1DiProtonLowMultDecision_Dec',
                        'phi_Hlt1BeamGasNoBeamBeam1Decision_Dec','phi_Hlt1BeamGasNoBeamBeam2Decision_Dec','phi_Hlt1BeamGasBeam1Decision_Dec',
                        'phi_Hlt1BeamGasBeam2Decision_Dec','phi_Hlt1BeamGasCrossingEnhancedBeam1Decision_Dec','phi_Hlt1BeamGasCrossingEnhancedBeam2Decision_Dec',
                        'phi_Hlt1BeamGasCrossingForcedRecoDecision_Dec','phi_Hlt1BeamGasCrossingForcedRecoFullZDecision_Dec','phi_Hlt1BeamGasHighRhoVerticesDecision_Dec',
                        'phi_Hlt1ODINTechnicalDecision_Dec','phi_Hlt1Tell1ErrorDecision_Dec','phi_Hlt1VeloClosingMicroBiasDecision_Dec',
                        'phi_Hlt1BeamGasCrossingParasiticDecision_Dec','phi_Hlt1ErrorEventDecision_Dec','phi_Hlt1GlobalDecision_Dec']:
                if(j == i):
                    testif0 = 1
            if(testif0 == 1): continue
            if '_Dec' in i:
                if Hlt1trigger == '(':
                    Hlt1trigger+=i
                else: 
                    Hlt1trigger += '||'+i
            elif '_TIS' in i:
                if Hlt1trigger_TIS == '(':
                    Hlt1trigger_TIS+=i
                else:
                    Hlt1trigger_TIS += '||'+i
            elif '_TOS' in i:
                if Hlt1trigger_TOS == '(':
                    Hlt1trigger_TOS+=i
                else:
                    Hlt1trigger_TOS += '||'+i
                    
                
    Hlt1trigger += ')'
    Hlt1trigger_TOS += ')'
    Hlt1trigger_TIS += ')' 

    Hlt1trigger = '('+Hlt1trigger_TIS + '||' + Hlt1trigger_TOS + ')'

    Hlt2trigger = '('
    Hlt2trigger_TIS = '('
    Hlt2trigger_TOS = '('




    for i in names:
        if('Hlt2' in i and not 'Global' in i and not 'Phys' in i and not 'LumiDecision' in i and not 'ForwardDecision' in i):
            testif0 = 0
            for j in ['phi_Hlt2DiMuonJPsiDecision_Dec','phi_Hlt2DiMuonJPsiHighPTDecision_Dec','phi_Hlt2DiMuonPsi2SDecision_Dec','phi_Hlt2DiMuonPsi2SHighPTDecision_Dec','phi_Hlt2DiMuonBDecision_Dec',
                        'phi_Hlt2DiMuonZDecision_Dec','phi_Hlt2DiMuonDY2Decision_Dec','phi_Hlt2DiMuonDY3Decision_Dec','phi_Hlt2DiMuonDY4Decision_Dec','phi_Hlt2DiMuonDetachedHeavyDecision_Dec',
                        'phi_Hlt2DiMuonDetachedJPsiDecision_Dec','phi_Hlt2DiMuonDetachedPsi2SDecision_Dec','phi_Hlt2TriMuonDetachedDecision_Dec','phi_Hlt2DoubleDiMuonDecision_Dec',
                        'phi_Hlt2DiMuonAndMuonDecision_Dec','phi_Hlt2TriMuonTauDecision_Dec','phi_Hlt2DiMuonAndGammaDecision_Dec','phi_Hlt2DiMuonAndD0Decision_Dec','phi_Hlt2DiMuonAndDpDecision_Dec',
                        'phi_Hlt2DiMuonAndDsDecision_Dec','phi_Hlt2DiMuonAndLcDecision_Dec','phi_Hlt2SingleTFElectronDecision_Dec','phi_Hlt2SingleElectronTFHighPtDecision_Dec',
                        'phi_Hlt2SingleTFVHighPtElectronDecision_Dec','phi_Hlt2DiElectronHighMassDecision_Dec','phi_Hlt2DiElectronBDecision_Dec','phi_Hlt2B2HHLTUnbiasedDetachedDecision_Dec','phi_Hlt2IncphiDecision_Dec',
                        'phi_Hlt2Dst2PiD02MuMuDecision_Dec','phi_Hlt2Dst2PiD02KMuDecision_Dec','phi_Hlt2TransparentDecision_Dec','phi_Hlt2DebugEventDecision_Dec','phi_Hlt2CharmHadD2KS0KS0Decision_Dec',
                        'phi_Hlt2CharmHadD2KS0KS0WideMassDecision_Dec','phi_Hlt2ExpressJPsiDecision_Dec','phi_Hlt2ExpressDs2phiPiDecision_Dec','phi_Hlt2ExpressDStar2D0PiDecision_Dec',
                        'phi_Hlt2CharmHadLambdaC2PiPPiDecision_Dec','phi_Hlt2CharmHadLambdaC2PiPPiWideMassDecision_Dec','phi_Hlt2Bs2phiGammaDecision_Dec','phi_Hlt2Bs2phiGammaWideBMassDecision_Dec',
                        'phi_Hlt2Bd2KstGammaDecision_Dec','phi_Hlt2Bd2KstGammaWideKMassDecision_Dec','phi_Hlt2Bd2KstGammaWideBMassDecision_Dec','phi_Hlt2DiphiDecision_Dec','phi_Hlt2KshortToMuMuPiPiDecision_Dec',
                        'phi_Hlt2CharmRareDecayD02MuMuDecision_Dec','phi_Hlt2LowMultD2KPiDecision_Dec','phi_Hlt2LowMultD2KPiPiDecision_Dec','phi_Hlt2LowMultD2K3PiDecision_Dec','phi_Hlt2LowMultChiC2HHDecision_Dec',
                        'phi_Hlt2LowMultChiC2HHHHDecision_Dec','phi_Hlt2LowMultChiC2PPDecision_Dec','phi_Hlt2LowMultD2KPiWSDecision_Dec','phi_Hlt2LowMultD2KPiPiWSDecision_Dec','phi_Hlt2LowMultD2K3PiWSDecision_Dec',
                        'phi_Hlt2LowMultChiC2HHWSDecision_Dec','phi_Hlt2LowMultChiC2HHHHWSDecision_Dec','phi_Hlt2LowMultDDIncCPDecision_Dec','phi_Hlt2LowMultDDIncVFDecision_Dec','phi_Hlt2LowMultLMR2HHDecision_Dec',
                        'phi_Hlt2SingleMuonVHighPTDecision_Dec','phi_Hlt2DiProtonDecision_Dec','phi_Hlt2DiProtonLowMultDecision_Dec','phi_Hlt2CharmHadMinBiasLambdaC2KPPiDecision_Dec','phi_Hlt2CharmHadMinBiasD02KPiDecision_Dec',
                        'phi_Hlt2CharmHadMinBiasD02KKDecision_Dec','phi_Hlt2CharmHadMinBiasDplus2hhhDecision_Dec','phi_Hlt2CharmHadMinBiasLambdaC2LambdaPiDecision_Dec','phi_Hlt2HighPtJetsDecision_Dec',
                        'phi_Hlt2TFBc2JpsiMuXDecision_Dec','phi_Hlt2TFBc2JpsiMuXSignalDecision_Dec','phi_Hlt2diPhotonDiMuonDecision_Dec','phi_Hlt2LowMultMuonDecision_Dec','phi_Hlt2LowMultHadronDecision_Dec',
                        'phi_Hlt2LowMultHadron_nofilterDecision_Dec','phi_Hlt2LowMultPhotonDecision_Dec','phi_Hlt2LowMultElectronDecision_Dec','phi_Hlt2LowMultElectron_nofilterDecision_Dec',
                        'phi_Hlt2ChargedHyperon_Xi2Lambda0LLPiDecision_Dec','phi_Hlt2ChargedHyperon_Xi2Lambda0LLMuDecision_Dec','phi_Hlt2ChargedHyperon_Omega2Lambda0LLKDecision_Dec',
                        'phi_Hlt2ChargedHyperon_Xi2Lambda0DDPiDecision_Dec','phi_Hlt2ChargedHyperon_Xi2Lambda0DDMuDecision_Dec','phi_Hlt2DisplVerticesSingleDecision_Dec','phi_Hlt2DisplVerticesSingleHighFDDecision_Dec',
                        'phi_Hlt2DisplVerticesSingleDownDecision_Dec','phi_Hlt2DisplVerticesSingleVeryHighFDDecision_Dec','phi_Hlt2DisplVerticesSingleHighMassDecision_Dec',
                        'phi_Hlt2DisplVerticesDoubleDecision_Dec','phi_Hlt2DisplVerticesDoublePSDecision_Dec','phi_Hlt2CharmSemilep3bodyD2PiMuMuDecision_Dec','phi_Hlt2CharmSemilep3bodyD2PiMuMuSSDecision_Dec',
                        'phi_Hlt2CharmSemilep3bodyD2KMuMuDecision_Dec','phi_Hlt2CharmSemilep3bodyD2KMuMuSSDecision_Dec','phi_Hlt2CharmSemilep3bodyLambdac2PMuMuDecision_Dec','phi_Hlt2CharmSemilep3bodyLambdac2PMuMuSSDecision_Dec',
                        'phi_Hlt2LambdaC_LambdaC2Lambda0LLPiDecision_Dec','phi_Hlt2LambdaC_LambdaC2Lambda0LLKDecision_Dec','phi_Hlt2B2HHPi0_MergedDecision_Dec']:
                if(j == i):
                    testif0 = 1
            if(testif0 == 1): continue
            if '_Dec' in i:
                if Hlt2trigger == '(':
                    Hlt2trigger+=i
                else: 
                    Hlt2trigger += '||'+i
            elif '_TIS' in i:
                if Hlt2trigger_TIS == '(':
                    Hlt2trigger_TIS+=i
                else:
                    Hlt2trigger_TIS += '||'+i
            elif '_TOS' in i:
                if Hlt2trigger_TOS == '(':
                    Hlt2trigger_TOS+=i
                else:
                    Hlt2trigger_TOS += '||'+i
                    
                
    Hlt2trigger += ')'
    Hlt2trigger_TOS += ')'
    Hlt2trigger_TIS += ')'
    
    # Hlt2trigger = '('+Hlt2trigger_TIS + '||' + Hlt2trigger_TOS + ')'



    

    beampipe1 = '((sqrt(Ks1_ENDVERTEX_X*Ks1_ENDVERTEX_X+Ks1_ENDVERTEX_Y*Ks1_ENDVERTEX_Y)<7&&sqrt(Ks2_ENDVERTEX_X*Ks2_ENDVERTEX_X+Ks2_ENDVERTEX_Y*Ks2_ENDVERTEX_Y)>7)||(sqrt(Ks1_ENDVERTEX_X*Ks1_ENDVERTEX_X+Ks1_ENDVERTEX_Y*Ks1_ENDVERTEX_Y)>7&&sqrt(Ks2_ENDVERTEX_X*Ks2_ENDVERTEX_X+Ks2_ENDVERTEX_Y*Ks2_ENDVERTEX_Y)<7))'
    beampipe2 = '((sqrt(Ks1_ENDVERTEX_X*Ks1_ENDVERTEX_X+Ks1_ENDVERTEX_Y*Ks1_ENDVERTEX_Y)<7&&sqrt(Ks2_ENDVERTEX_X*Ks2_ENDVERTEX_X+Ks2_ENDVERTEX_Y*Ks2_ENDVERTEX_Y)<7))' 
    

    
    selection = ''
    selection +='abs(1019.445-phi_M) < .2' 
    if(not 'incl' in key):
        selection += ' && Ds_M > 1955 && Ds_M < 1985'
        selection += '&& phi_IPCHI2_OWNPV >=15'#'&& phi_IPCHI2_OWNPV >=50'
        if('data' in key):
            print 'Selection: ', selection
    # print '*************************************************************************************************************'


    ###########################################################################################

    if('data2012' in key):
        if 'Ds' in key:
            exp_combbkg_Ds[0] = trees[key].GetEntries(selection+'&&'+beampipe1)/2.03
            exp_combbkg_Ds[1] = trees[key].GetEntries(selection+'&&'+beampipe2)/2.03
        if 'incl' in key:
            exp_combbkg_incl[0] = trees[key].GetEntries(selection+'&&'+beampipe1)*2.66
            exp_combbkg_incl[1] = trees[key].GetEntries(selection+'&&'+beampipe2)*2.66
    elif('minbias' in key):
        MC = 42122929.
        Reco = trees[key].GetEntries(selection)
        Reco1 = trees[key].GetEntries(selection+'&&'+beampipe1)
        Reco2 = trees[key].GetEntries(selection+'&&'+beampipe2)
        # RecoL0 = trees[key].GetEntries(selection+'&&'+L0trigger)
        #RecoL0Hlt1 = trees[key].GetEntries(selection+'&&'+L0trigger+'&&'+Hlt1trigger)
        RecoL0Hlt1BP1 = trees[key].GetEntries(selection+'&&'+L0trigger+'&&'+Hlt1trigger+'&&'+beampipe1)
        RecoL0Hlt1BP2 = trees[key].GetEntries(selection+'&&'+L0trigger+'&&'+Hlt1trigger+'&&'+beampipe2)
        if(Reco-Reco2 > 0):
            ret1 = float(RecoL0Hlt1BP1*Reco)/float(MC*(Reco-Reco2))
        else:
            ret1 = 0.0
        if(Reco-Reco1 > 0):
            ret2 = float(RecoL0Hlt1BP2*Reco)/float(MC*(Reco-Reco1))
        else:
            ret2 = 0.0
        if 'Ds' in key:
            retention_Ds = [ret1,ret2] #[1bp,2bp]
        if 'incl' in key:
            retention_incl = [ret1,ret2] #[1bp,2bp]

        canv = r.TCanvas("bla","blub")
        trees[key].Draw("phi_BKGCAT",selection+'&&'+L0trigger+'&&'+Hlt1trigger, "text")
        if 'Ds' in key:
            canv.Print("Ds_bkgcat.pdf")
        else:
            canv.Print("incl_bkgcat.pdf")
        del canv

        canv2 = r.TCanvas("bla","blub")
        trees[key].Draw("phi_BKGCAT",selection+'&&'+L0trigger+'&&'+Hlt1trigger+'&&Ks1_TRUEID==310&&Ks2_TRUEID==310', "text")
        if 'Ds' in key:
            canv2.Print("Ds_bkgcat_TK.pdf")
        else:
            canv2.Print("incl_bkgcat_TK.pdf")
        del canv2



    elif('phi2KsKs' in key):
        if(key=='phi2KsKs_incl'):
            MC1 = treesMC[key].GetEntries('(sqrt(KS0_TRUEENDVERTEX_X*KS0_TRUEENDVERTEX_X+KS0_TRUEENDVERTEX_Y*KS0_TRUEENDVERTEX_Y)<7&&sqrt(KS00_TRUEENDVERTEX_X*KS00_TRUEENDVERTEX_X+KS00_TRUEENDVERTEX_Y*KS00_TRUEENDVERTEX_Y)>7)||(sqrt(KS0_TRUEENDVERTEX_X*KS0_TRUEENDVERTEX_X+KS0_TRUEENDVERTEX_Y*KS0_TRUEENDVERTEX_Y)>7&&sqrt(KS00_TRUEENDVERTEX_X*KS00_TRUEENDVERTEX_X+KS00_TRUEENDVERTEX_Y*KS00_TRUEENDVERTEX_Y)<7)')
            MC2 = treesMC[key].GetEntries('(sqrt(KS0_TRUEENDVERTEX_X*KS0_TRUEENDVERTEX_X+KS0_TRUEENDVERTEX_Y*KS0_TRUEENDVERTEX_Y)<7&&sqrt(KS00_TRUEENDVERTEX_X*KS00_TRUEENDVERTEX_X+KS00_TRUEENDVERTEX_Y*KS00_TRUEENDVERTEX_Y)<7)' )
        else:
            MC1 = treesMC[key].GetEntries('(sqrt(Ks1_TRUEENDVERTEX_X*Ks1_TRUEENDVERTEX_X+Ks1_TRUEENDVERTEX_Y*Ks1_TRUEENDVERTEX_Y)<7&&sqrt(Ks2_TRUEENDVERTEX_X*Ks2_TRUEENDVERTEX_X+Ks2_TRUEENDVERTEX_Y*Ks2_TRUEENDVERTEX_Y)>7)||(sqrt(Ks1_TRUEENDVERTEX_X*Ks1_TRUEENDVERTEX_X+Ks1_TRUEENDVERTEX_Y*Ks1_TRUEENDVERTEX_Y)>7&&sqrt(Ks2_TRUEENDVERTEX_X*Ks2_TRUEENDVERTEX_X+Ks2_TRUEENDVERTEX_Y*Ks2_TRUEENDVERTEX_Y)<7)')
            MC2 = treesMC[key].GetEntries('(sqrt(Ks1_TRUEENDVERTEX_X*Ks1_TRUEENDVERTEX_X+Ks1_TRUEENDVERTEX_Y*Ks1_TRUEENDVERTEX_Y)<7&&sqrt(Ks2_TRUEENDVERTEX_X*Ks2_TRUEENDVERTEX_X+Ks2_TRUEENDVERTEX_Y*Ks2_TRUEENDVERTEX_Y)<7)' )

        Reco1 = trees[key].GetEntries(selection+'&&'+truthmatch+'&&'+beampipe1)
        Reco2 = trees[key].GetEntries(selection+'&&'+truthmatch+'&&'+beampipe2)
        RecoL01 = trees[key].GetEntries(selection+'&&'+truthmatch+'&&'+L0trigger+'&&'+beampipe1)
        RecoL01_TIS = trees[key].GetEntries(selection+'&&'+truthmatch+'&&'+L0trigger_TIS+'&&'+beampipe1)
        RecoL01_TOS = trees[key].GetEntries(selection+'&&'+truthmatch+'&&'+L0trigger_TOS+'&&'+beampipe1)
        RecoL02 = trees[key].GetEntries(selection+'&&'+truthmatch+'&&'+L0trigger+'&&'+beampipe2)
        RecoL02_TIS = trees[key].GetEntries(selection+'&&'+truthmatch+'&&'+L0trigger_TIS+'&&'+beampipe2)
        RecoL02_TOS = trees[key].GetEntries(selection+'&&'+truthmatch+'&&'+L0trigger_TOS+'&&'+beampipe2)
        RecoL0Hlt11 = trees[key].GetEntries(selection+'&&'+truthmatch+'&&'+L0trigger+'&&'+Hlt1trigger+'&&'+beampipe1)
        RecoL0Hlt11_TIS = trees[key].GetEntries(selection+'&&'+truthmatch+'&&'+L0trigger+'&&'+Hlt1trigger_TIS+'&&'+beampipe1)
        RecoL0Hlt11_TOS = trees[key].GetEntries(selection+'&&'+truthmatch+'&&'+L0trigger+'&&'+Hlt1trigger_TOS+'&&'+beampipe1)
        RecoL0Hlt12 = trees[key].GetEntries(selection+'&&'+truthmatch+'&&'+L0trigger+'&&'+Hlt1trigger+'&&'+beampipe2)
        RecoL0Hlt12_TIS = trees[key].GetEntries(selection+'&&'+truthmatch+'&&'+L0trigger+'&&'+Hlt1trigger_TIS+'&&'+beampipe2)
        RecoL0Hlt12_TOS = trees[key].GetEntries(selection+'&&'+truthmatch+'&&'+L0trigger+'&&'+Hlt1trigger_TOS+'&&'+beampipe2)
        RecoL0Hlt1Hlt21 = trees[key].GetEntries(selection+'&&'+truthmatch+'&&'+L0trigger+'&&'+Hlt1trigger+'&&'+Hlt2trigger+'&&'+beampipe1)
        RecoL0Hlt1Hlt21_TIS = trees[key].GetEntries(selection+'&&'+truthmatch+'&&'+L0trigger+'&&'+Hlt1trigger+'&&'+Hlt2trigger_TIS+'&&'+beampipe1)
        RecoL0Hlt1Hlt21_TOS = trees[key].GetEntries(selection+'&&'+truthmatch+'&&'+L0trigger+'&&'+Hlt1trigger+'&&'+Hlt2trigger_TOS+'&&'+beampipe1)
        RecoL0Hlt1Hlt22 = trees[key].GetEntries(selection+'&&'+truthmatch+'&&'+L0trigger+'&&'+Hlt1trigger+'&&'+Hlt2trigger+'&&'+beampipe2)
        RecoL0Hlt1Hlt22_TIS = trees[key].GetEntries(selection+'&&'+truthmatch+'&&'+L0trigger+'&&'+Hlt1trigger+'&&'+Hlt2trigger_TIS+'&&'+beampipe2)
        RecoL0Hlt1Hlt22_TOS = trees[key].GetEntries(selection+'&&'+truthmatch+'&&'+L0trigger+'&&'+Hlt1trigger+'&&'+Hlt2trigger_TOS+'&&'+beampipe2)






        if('Ds' in key):
            effi_Reco_Ds = [float(Reco1)/float(MC1),float(Reco2)/float(MC2)] #[1bp,2bp]
            effi_L0_Ds = [(-9999.9 if Reco1 == 0 else float(RecoL01)/float(Reco1), -9999.9 if RecoL01 == 0 else float(RecoL01_TIS)/float(RecoL01), -9999.9 if RecoL01 == 0 else float(RecoL01_TOS)/float(RecoL01)),(-9999.9 if Reco2 == 0 else float(RecoL02)/float(Reco2), -9999.9 if RecoL02 == 0 else float(RecoL02_TIS)/float(RecoL02), -9999.9 if RecoL02 == 0 else float(RecoL02_TOS)/float(RecoL02))] #[(1bp,1bp_TIS,1bp_TOS),(2bp,2bp_TIS,2bp_TOS)]
            effi_Hlt1_Ds = [(-9999.9 if RecoL01 == 0 else float(RecoL0Hlt11)/float(RecoL01), -9999.9 if RecoL0Hlt11 == 0 else float(RecoL0Hlt11_TIS)/float(RecoL0Hlt11), -9999.9 if RecoL0Hlt11 == 0 else float(RecoL0Hlt11_TOS)/float(RecoL0Hlt11)),(-9999.9 if RecoL02 == 0 else float(RecoL0Hlt12)/float(RecoL02), -9999.9 if RecoL0Hlt12 == 0 else float(RecoL0Hlt12_TIS)/float(RecoL0Hlt12), -9999.9 if RecoL0Hlt12 == 0 else float(RecoL0Hlt12_TOS)/float(RecoL0Hlt12))] #[(1bp,1bp_TIS,1bp_TOS),(2bp,2bp_TIS,2bp_TOS)]
            effi_Hlt2_Ds = [(-9999.9 if RecoL0Hlt11 == 0 else float(RecoL0Hlt1Hlt21)/float(RecoL0Hlt11), -9999.9 if RecoL0Hlt1Hlt21 == 0 else float(RecoL0Hlt1Hlt21_TIS)/float(RecoL0Hlt1Hlt21), -9999.9 if RecoL0Hlt1Hlt21 == 0 else float(RecoL0Hlt1Hlt21_TOS)/float(RecoL0Hlt1Hlt21)),(-9999.9 if RecoL0Hlt12 == 0 else float(RecoL0Hlt1Hlt22)/float(RecoL0Hlt12), -9999.9 if RecoL0Hlt1Hlt22 == 0 else float(RecoL0Hlt1Hlt22_TIS)/float(RecoL0Hlt1Hlt22), -9999.9 if RecoL0Hlt1Hlt22 == 0 else float(RecoL0Hlt1Hlt22_TOS)/float(RecoL0Hlt1Hlt22))] #[(1bp,1bp_TIS,1bp_TOS),(2bp,2bp_TIS,2bp_TOS)]
        elif('incl' in key):
            effi_Reco_incl = [float(Reco1)/float(MC1),float(Reco2)/float(MC2)] #[1bp,2bp]
            effi_L0_incl = [(-9999.9 if Reco1 == 0 else float(RecoL01)/float(Reco1), -9999.9 if RecoL01 == 0 else float(RecoL01_TIS)/float(RecoL01), -9999.9 if RecoL01 == 0 else float(RecoL01_TOS)/float(RecoL01)),(-9999.9 if Reco2 == 0 else float(RecoL02)/float(Reco2), -9999.9 if RecoL02 == 0 else float(RecoL02_TIS)/float(RecoL02), -9999.9 if RecoL02 == 0 else float(RecoL02_TOS)/float(RecoL02))] #[(1bp,1bp_TIS,1bp_TOS),(2bp,2bp_TIS,2bp_TOS)]
            effi_Hlt1_incl = [(-9999.9 if RecoL01 == 0 else float(RecoL0Hlt11)/float(RecoL01), -9999.9 if RecoL0Hlt11 == 0 else float(RecoL0Hlt11_TIS)/float(RecoL0Hlt11), -9999.9 if RecoL0Hlt11 == 0 else float(RecoL0Hlt11_TOS)/float(RecoL0Hlt11)),(-9999.9 if RecoL02 == 0 else float(RecoL0Hlt12)/float(RecoL02), -9999.9 if RecoL0Hlt12 == 0 else float(RecoL0Hlt12_TIS)/float(RecoL0Hlt12), -9999.9 if RecoL0Hlt12 == 0 else float(RecoL0Hlt12_TOS)/float(RecoL0Hlt12))] #[(1bp,1bp_TIS,1bp_TOS),(2bp,2bp_TIS,2bp_TOS)]
            effi_Hlt2_incl = [(-9999.9 if RecoL0Hlt11 == 0 else float(RecoL0Hlt1Hlt21)/float(RecoL0Hlt11), -9999.9 if RecoL0Hlt1Hlt21 == 0 else float(RecoL0Hlt1Hlt21_TIS)/float(RecoL0Hlt1Hlt21), -9999.9 if RecoL0Hlt1Hlt21 == 0 else float(RecoL0Hlt1Hlt21_TOS)/float(RecoL0Hlt1Hlt21)),(-9999.9 if RecoL0Hlt12 == 0 else float(RecoL0Hlt1Hlt22)/float(RecoL0Hlt12), -9999.9 if RecoL0Hlt1Hlt22 == 0 else float(RecoL0Hlt1Hlt22_TIS)/float(RecoL0Hlt1Hlt22), -9999.9 if RecoL0Hlt1Hlt22 == 0 else float(RecoL0Hlt1Hlt22_TOS)/float(RecoL0Hlt1Hlt22))] #[(1bp,1bp_TIS,1bp_TOS),(2bp,2bp_TIS,2bp_TOS)]
        






#output
##################################################################################


print '************************************************'



print '\\begin{tabular}{ccc}'
print '&Inclusive $\phi$ & $D_s \\rightarrow \phi \pi$ \\\\' 
print '\hline '
print 'Cross section (\SI{14}{TeV}), LHCb acceptance & \SI{',xsec_incl,'}{\micro\\barn} & \SI{',xsec_Ds,'}{\micro\\barn} \\\\' 
print 'Branching fractions &',BR_incl*100,'\% &',BR_Ds_Ds*100,' \% $\cdot$ ',BR_incl*100,'\% \\\\'
print 'Generator cut efficiency &',GenCut_incl*100,'\% &', GenCut_Ds*100 ,'\%\\\\'
print 'Probability of $K_sK_L \\rightarrow 4\pi$ with exactly 1 (2) decays in the beam pipe  with limit on decoherence of KLOE&\multicolumn{2}{c}{$ ',format_e(PropKsKs_bp1),'$($',format_e(PropKsKs_bp2),'$)} \\\\'
print 'Probability of $K_sK_L \\rightarrow 4\pi$ with exactly 1 (2) decays in the beam pipe &\multicolumn{2}{c}{$',format_e(PropKsKl_bp1),'$($',format_e(PropKsKl_bp2),'$)} \\\\'
print 'Probability of $K_sK_s \\rightarrow 4\pi$ with exactly 1 (2) decays in the beam pipe &\multicolumn{2}{c}{$', 15.1,'\%','$($',2.8,'\%','$)} \\\\'
print 'Reconstruction \& selection efficiency & ',round(effi_Reco_incl[0]*100,1),'\%(',round(effi_Reco_incl[1]*100,1),'\%)  &',round(effi_Reco_Ds[0]*100,1),'\%(',round(effi_Reco_Ds[1]*100,1),'\%)\\\\'
print 'L0 efficiency& ',round(effi_L0_incl[0][0]*100,1),'\%(',round(effi_L0_incl[1][0]*100,1),'\%)& ',round(effi_L0_Ds[0][0]*100,1),'\%(',round(effi_L0_Ds[1][0]*100,1),'\%)\\\\'
print 'HLT1 efficiency& ',round(effi_Hlt1_incl[0][0]*100,1),'\%(',round(effi_Hlt1_incl[1][0]*100,1),'\%)&',round(effi_Hlt1_Ds[0][0]*100,1),'\%(',round(effi_Hlt1_Ds[1][0]*100,1),'\%)\\\\'
print 'HLT2 efficiency& ',round(effi_Hlt2_incl[0][0]*100,1),'\%(',round(effi_Hlt2_incl[1][0]*100,1),'\%)&',round(effi_Hlt2_Ds[0][0]*100,1),'\%(',round(effi_Hlt2_Ds[1][0]*100,1),'\%)\\\\'
print '\hline'
print 'Total efficiency SM background &$',format_e(GenCut_incl*effi_Reco_incl[0]*effi_L0_incl[0][0]*effi_Hlt1_incl[0][0]),'$($',format_e(GenCut_incl*effi_Reco_incl[1]*effi_L0_incl[1][0]*effi_Hlt1_incl[1][0]),'$)&$',format_e(GenCut_Ds*effi_Reco_Ds[0]*effi_L0_Ds[0][0]*effi_Hlt1_Ds[0][0]),'$($',format_e(GenCut_Ds*effi_Reco_Ds[1]*effi_L0_Ds[1][0]*effi_Hlt1_Ds[1][0]),'$)\\\\'
print 'Expected events SM background / fb$^{-1}$ &$', isint(1e9*xsec_incl*BR_incl*GenCut_incl*PropKsKl_bp1*effi_Reco_incl[0]*effi_L0_incl[0][0]*effi_Hlt1_incl[0][0]) ,'$($', isint(1e9*xsec_incl*BR_incl*GenCut_incl*PropKsKl_bp2*effi_Reco_incl[1]*effi_L0_incl[1][0]*effi_Hlt1_incl[1][0]),'$)&$',isint(1e9*xsec_Ds*BR_Ds*GenCut_Ds*PropKsKl_bp1*effi_Reco_Ds[0]*effi_L0_Ds[0][0]*effi_Hlt1_Ds[0][0]),'$($',isint(1e9*xsec_Ds*BR_Ds*GenCut_Ds*PropKsKl_bp2*effi_Reco_Ds[1]*effi_L0_Ds[1][0]*effi_Hlt1_Ds[1][0]),'$)\\\\'
print 'Upper limit for signal (KLOE) &$', isint(1e9*xsec_incl*BR_incl*GenCut_incl*PropKsKs_bp1*effi_Reco_incl[0]*effi_L0_incl[0][0]*effi_Hlt1_incl[0][0]) ,'$($', isint(1e9*xsec_incl*BR_incl*GenCut_incl*PropKsKs_bp2*effi_Reco_incl[1]*effi_L0_incl[1][0]*effi_Hlt1_incl[1][0]),'$)&$',isint(1e9*xsec_Ds*BR_Ds*GenCut_Ds*PropKsKs_bp1*effi_Reco_Ds[0]*effi_L0_Ds[0][0]*effi_Hlt1_Ds[0][0]),'$($',isint(1e9*xsec_Ds*BR_Ds*GenCut_Ds*PropKsKs_bp2*effi_Reco_Ds[1]*effi_L0_Ds[1][0]*effi_Hlt1_Ds[1][0]),'$)\\\\'
# print 'Total background retention & $',format_e(retention_incl[0]),'$($',format_e(retention_incl[1]),'$) &$', format_e(retention_Ds[0]),'$($',retention_Ds[1],'$)\\\\'
print 'Background (data 2012) / fb$^{-1}$ &', int(round(exp_combbkg_incl[0],-1)) ,'(',int(round(exp_combbkg_incl[1],-1)),') & ',int(round(exp_combbkg_Ds[0],-1)),'(',int(round(exp_combbkg_Ds[1],-1)),')\\\\'
print '\end{tabular}' 




print '**************************************************************************'
print '\\begin{tabular}{c|c|c|c|c|c|c|c|c}'
print '& \multicolumn{4}{c|}{Inclusive $\phi$} & \multicolumn{4}{c}{$D_s\\rightarrow \phi\pi$} \\\\ '
print '& \multicolumn{2}{c|}{1 decay in beampipe} & \multicolumn{2}{c|}{2 decays in beampipe} & \multicolumn{2}{c|}{1 decay in beampipe} & \multicolumn{2}{c}{2 decays in beampipe}\\\\ '
print '& TIS & TOS & TIS & TOS & TIS & TOS & TIS & TOS\\\\' 
print '\hline '
print 'L0 efficiency & ',round(effi_L0_incl[0][1],2),' & ',round(effi_L0_incl[0][2],2),' & ',round(effi_L0_incl[1][1],2),' & ',round(effi_L0_incl[1][2],2),' & ',round(effi_L0_Ds[0][1],2),' & ',round(effi_L0_Ds[0][2],2),' & ',round(effi_L0_Ds[1][1],2),' & ',round(effi_L0_Ds[1][2],2),' \\\\ '
print 'HLT1 efficiency & ',round(effi_Hlt1_incl[0][1],2),' & ',round(effi_Hlt1_incl[0][2],2),' & ', round(effi_Hlt1_incl[1][1],2),' & ',round(effi_Hlt1_incl[1][2],2),' & ',round(effi_Hlt1_Ds[0][1],2),' & ',round(effi_Hlt1_Ds[0][2],2),' & ',round(effi_Hlt1_Ds[1][1],2),' & ',round(effi_Hlt1_Ds[1][2],2),' \\\\ '
print 'HLT2 efficiency & ',round(effi_Hlt2_incl[0][1],2),' & ',round(effi_Hlt2_incl[0][2],2),' & ', round(effi_Hlt2_incl[1][1],2),' & ',round(effi_Hlt2_incl[1][2],2),' & ',round(effi_Hlt2_Ds[0][1],2),' & ',round(effi_Hlt2_Ds[0][2],2),' & ',round(effi_Hlt2_Ds[1][1],2),' & ',round(effi_Hlt2_Ds[1][2],2),' \\\\ '
print '\end{tabular}' 

