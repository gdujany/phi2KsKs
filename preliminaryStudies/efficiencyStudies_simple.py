#!/usr/bin/env python
'''
Finding out whether how many Ks decay in the beampipe
'''

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
#inFiles['data2012'] = r.TFile(os.path.join(store_dir, 'data2012.root'))
inFiles['phi2KsKs_incl'] = r.TFile(os.path.join(store_dir_g, 'phi2KsKs_incl.root'))
inFiles['phi2KsKs_Ds'] = r.TFile(os.path.join(store_dir_s, 'Ds_Phi2KsKs_Ds_fulltrigger.root'))# 'Ds_Phi2KsKs_Ds.root'))
#inFiles['minbias'] = r.TFile(os.path.join(store_dir, 'minbias1.root'))


trees = {}
treesMC = {}
for key, inFile in inFiles.items():
    print(key)
    trees[key] = inFile.Get('TuplePhi2KsKs/DecayTree')
    if(key=='phi2KsKs_incl'):
        treesMC[key] = inFile.Get('MCTuplephi2KsKs/MCDecayTree')
    else:
        treesMC[key] = inFile.Get('MCTuplePhi2KsKs/MCDecayTree')

    names = [b.GetName() for b in trees[key].GetListOfBranches()]

    truthmatch = 'phi_BKGCAT==0'
    L0trigger = 'phi_L0Global_Dec'
    Hlt1trigger = '('

    for i in names:
        if('Hlt1' in i and '_Dec' in i and not 'Global' in i and not 'Phys' in i and not 'Hlt1LumiDecision' in i):
            if Hlt1trigger == '(':
                Hlt1trigger+=i
            else:
                Hlt1trigger += '||'+i
    Hlt1trigger += ')'

    beampipe = '&& (sqrt(Ks1_ENDVERTEX_X*Ks1_ENDVERTEX_X+Ks1_ENDVERTEX_Y*Ks1_ENDVERTEX_Y)<7||sqrt(Ks2_ENDVERTEX_X*Ks2_ENDVERTEX_X+Ks2_ENDVERTEX_Y*Ks2_ENDVERTEX_Y)<7)'


    
    
    MC = treesMC[key].GetEntries()
    Reco = trees[key].GetEntries(truthmatch)
    RecoL0 = trees[key].GetEntries(truthmatch+'&&'+L0trigger)
    RecoL0Hlt1 = trees[key].GetEntries(truthmatch+'&&'+L0trigger+'&&'+Hlt1trigger)
    RecoL0Hlt1BP = trees[key].GetEntries(truthmatch+'&&'+L0trigger+'&&'+Hlt1trigger+beampipe)
    print('Reconstruction efficiency + truth',float(Reco)/float(MC))
    print('L0 efficiency',float(RecoL0)/float(Reco))
    print('Hlt1 efficiency', float(RecoL0Hlt1)/float(RecoL0))
    print('1 Ks decays in beampipe', float(RecoL0Hlt1BP)/float(RecoL0Hlt1))








