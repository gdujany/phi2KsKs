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
store_dir_s = '~/phi2KsKs/files/'

inFiles = {}
inFiles['data2012_Ds'] = r.TFile(os.path.join(store_dir_s, 'Ds_Phi2KsKs_2012.root'))
inFiles['data2012_incl'] = r.TFile(os.path.join(store_dir_g, '../phi2KsKs_noTrigger/data2012.root'))
inFiles['phi2KsKs_incl'] = r.TFile(os.path.join(store_dir_g, 'phi2KsKs_incl.root'))
inFiles['phi2KsKs_Ds'] = r.TFile(os.path.join(store_dir_s, 'Ds_Phi2KsKs_Ds_fulltrigger.root'))# 'Ds_Phi2KsKs_Ds.root'))
#inFiles['minbias'] = r.TFile(os.path.join(store_dir_s, 'Phi2KsKs_MBcomb.root'))
inFiles['minbias'] = r.TFile(os.path.join(store_dir_s, 'Ds_Phi2KsKs_MBcomb.root'))

trees = {}
treesMC = {}
for key, inFile in inFiles.items():
    print('********************'+key+'********************')
    trees[key] = inFile.Get('TuplePhi2KsKs/DecayTree')
    if(key=='phi2KsKs_incl' and not 'data2012' in key):
        treesMC[key] = inFile.Get('MCTuplephi2KsKs/MCDecayTree')
    elif(not 'data2012' in key or not key=='minbias'):
        treesMC[key] = inFile.Get('MCTuplePhi2KsKs/MCDecayTree')

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

    beampipe1 = '(sqrt(Ks1_ENDVERTEX_X*Ks1_ENDVERTEX_X+Ks1_ENDVERTEX_Y*Ks1_ENDVERTEX_Y)<7&&sqrt(Ks2_ENDVERTEX_X*Ks2_ENDVERTEX_X+Ks2_ENDVERTEX_Y*Ks2_ENDVERTEX_Y)>7)||(sqrt(Ks1_ENDVERTEX_X*Ks1_ENDVERTEX_X+Ks1_ENDVERTEX_Y*Ks1_ENDVERTEX_Y)>7&&sqrt(Ks2_ENDVERTEX_X*Ks2_ENDVERTEX_X+Ks2_ENDVERTEX_Y*Ks2_ENDVERTEX_Y)<7)'
    beampipe2 = '(sqrt(Ks1_ENDVERTEX_X*Ks1_ENDVERTEX_X+Ks1_ENDVERTEX_Y*Ks1_ENDVERTEX_Y)<7&&sqrt(Ks2_ENDVERTEX_X*Ks2_ENDVERTEX_X+Ks2_ENDVERTEX_Y*Ks2_ENDVERTEX_Y)<7)' 


    selection = 'Ks1_M > 490 && Ks1_M < 505 && Ks2_M > 490 && Ks2_M < 505'+'&&phi_M>1000&&phi_M<1040'+'&&nCandidate==0' 
    if(not 'incl' in key):
        selection += ' && Ds_M > 1940 && Ds_M < 2000'
    
    if(not 'data2012' in key):
        if(key=='minbias'):
            MC = 42122929
            Reco = trees[key].GetEntries(selection)
            RecoL0 = trees[key].GetEntries(selection+'&&'+L0trigger)
            RecoL0Hlt1 = trees[key].GetEntries(selection+'&&'+L0trigger+'&&'+Hlt1trigger)
            RecoL0Hlt1BP1 = trees[key].GetEntries(selection+'&&'+L0trigger+'&&'+Hlt1trigger+'&&'+beampipe1)
            RecoL0Hlt1BP2 = trees[key].GetEntries(selection+'&&'+L0trigger+'&&'+Hlt1trigger+'&&'+beampipe2)
        else:
            MC = treesMC[key].GetEntries()
            Reco = trees[key].GetEntries(selection+'&&'+truthmatch)
            RecoL0 = trees[key].GetEntries(selection+'&&'+truthmatch+'&&'+L0trigger)
            RecoL0_TIS = trees[key].GetEntries(selection+'&&'+truthmatch+'&&'+L0trigger_TIS)
            RecoL0_TOS = trees[key].GetEntries(selection+'&&'+truthmatch+'&&'+L0trigger_TOS)
            RecoL0Hlt1 = trees[key].GetEntries(selection+'&&'+truthmatch+'&&'+L0trigger+'&&'+Hlt1trigger)
            RecoL0Hlt1_TIS = trees[key].GetEntries(selection+'&&'+truthmatch+'&&'+L0trigger+'&&'+Hlt1trigger_TIS)
            RecoL0Hlt1_TOS = trees[key].GetEntries(selection+'&&'+truthmatch+'&&'+L0trigger+'&&'+Hlt1trigger_TOS)
            RecoL0Hlt1BP1 = trees[key].GetEntries(selection+'&&'+truthmatch+'&&'+L0trigger+'&&'+Hlt1trigger+'&&'+beampipe1)
            RecoL0Hlt1BP2 = trees[key].GetEntries(selection+'&&'+truthmatch+'&&'+L0trigger+'&&'+Hlt1trigger+'&&'+beampipe2)
        print('Reconstruction efficiency + truth',float(Reco)/float(MC))
        print('L0 efficiency',float(RecoL0)/float(Reco))
        if(not key=='minbias'):
            print('Percentage in TIS:',float(RecoL0_TIS)/float(RecoL0)*100,'%')
            print('Percentage in TOS:',float(RecoL0_TOS)/float(RecoL0)*100,'%')
        print('Hlt1 efficiency', float(RecoL0Hlt1)/float(RecoL0))
        if(not key=='minbias'):
            print('Percentage in TIS:',float(RecoL0Hlt1_TIS)/float(RecoL0Hlt1)*100,'%')
            print('Percentage in TOS:',float(RecoL0Hlt1_TOS)/float(RecoL0Hlt1)*100,'%')
        print('1 Ks decays in beampipe', float(RecoL0Hlt1BP1)/float(RecoL0Hlt1), 'Total efficiency: ',float(RecoL0Hlt1BP1)/float(MC))
        print('2 Ks decays in beampipe', float(RecoL0Hlt1BP2)/float(RecoL0Hlt1), 'Total efficiency: ',float(RecoL0Hlt1BP2)/float(MC))

        if(not key=="minbias"):
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

            # RecoL0Hlt1BP1 = trees[key].GetEntries(truthmatch+'&&'+L0trigger+'&&'+Hlt1trigger+'&&'+beampipe1)
            # RecoL0Hlt1BP2 = trees[key].GetEntries(truthmatch+'&&'+L0trigger+'&&'+Hlt1trigger+'&&'+beampipe2)
            print('Reconstruction efficiency + truth:')
            print('1 decay in bp: ',float(Reco1)/float(MC1))
            print('2 decays in bp: ',float(Reco2)/float(MC2))
            print('L0 efficiency:')
            print('1 decay in bp: ',float(RecoL01)/float(Reco1),', TIS: ',float(RecoL01_TIS)/float(RecoL01),',TOS: ',float(RecoL01_TOS)/float(RecoL01))
            print('2 decays in bp: ',float(RecoL02)/float(Reco2),', TIS: ',float(RecoL02_TIS)/float(RecoL02),',TOS: ',float(RecoL02_TOS)/float(RecoL02))
            print('Hlt1 efficiency:')
            print('1 decay in bp: ',float(RecoL0Hlt11)/float(RecoL01),', TIS: ',float(RecoL0Hlt11_TIS)/float(RecoL0Hlt11),',TOS: ',float(RecoL0Hlt11_TOS)/float(RecoL0Hlt11))
            print('2 decays in bp: ',float(RecoL0Hlt12)/float(RecoL02),', TIS: ',float(RecoL0Hlt12_TIS)/float(RecoL0Hlt12),',TOS: ',float(RecoL0Hlt12_TOS)/float(RecoL0Hlt12))            # print('1 Ks decays in beampipe', float(RecoL0Hlt1BP1)/float(RecoL0Hlt1))
            # print('2 Ks decays in beampipe', float(RecoL0Hlt1BP2)/float(RecoL0Hlt1))
    else:
        if 'Ds' in key:
            print('data, 1 Ks decays in beampipe', trees[key].GetEntries(selection+'&&'+'phi_M>1000 && phi_M < 1040'+'&&'+beampipe1)/2.03)
            print('data, 2 Ks decays in beampipe', trees[key].GetEntries(selection+'&&'+'phi_M>1000 && phi_M < 1040'+'&&'+beampipe2)/2.03)
        if 'incl' in key:
            print('data, 1 Ks decays in beampipe', trees[key].GetEntries(selection+'&&'+'phi_M>1000 && phi_M < 1040'+'&&'+beampipe1)*2.66)
            print('data, 2 Ks decays in beampipe', trees[key].GetEntries(selection+'&&'+'phi_M>1000 && phi_M < 1040'+'&&'+beampipe2)*2.66)








