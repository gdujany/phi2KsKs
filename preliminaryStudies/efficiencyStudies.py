#!/usr/bin/env python
'''
Finding out whether how many Ks decay in the beampipe
'''

import sys, os
from CompareTreeVars import getHisto, CompareTreeVars
import ROOT as r
import numpy as np

r.gROOT.SetBatch(True)

# Get trees

eos_root = os.path.expanduser('~/eos/')
if not os.listdir(eos_root):
    raise OSError('EOS not mounted, please type:\n eosmount '+eos_root)

#store_dir = os.path.join(eos_root, 'lhcb/user/g/gdujany/phi2KsKs/')
store_dir = '~/phi2KsKs/files/'

inFiles = {}
#inFiles['data2012'] = r.TFile(os.path.join(store_dir, 'data2012.root'))
inFiles['phi2KsKs_incl'] = r.TFile(os.path.join(store_dir, 'Ds_Phi2KsKs_incl.root'))
inFiles['phi2KsKs_Ds'] = r.TFile(os.path.join(store_dir, 'Ds_Phi2KsKs_Ds.root'))
#inFiles['minbias'] = r.TFile(os.path.join(store_dir, 'minbias1.root'))


trees = {}
for key, inFile in inFiles.items():
    trees[key] = inFile.Get('TuplePhi2KsKs/DecayTree')

L0 = ['phi_L0HadronDecision_Dec', 'phi_L0MuonDecision_Dec', 'phi_L0ElectronDecision_Dec']
Hlt1 = ['phi_Hlt1TrackAllL0Decision_Dec', 'phi_Hlt1TrackPhotonDecision_Dec', 'phi_Hlt1TrackMuonDecision_Dec']
Hlt2 = ['phi_Hlt2ExpressKSDecision_Dec', 'phi_Hlt2CharmHadD02HHXDst_BaryonhhXWideMassDecision_Dec']

Triggers = []
toAppend = '('
for i in L0:
	Triggers.append(i)
	if (toAppend == '('):
		toAppend = toAppend+i
	else:
		toAppend = toAppend+'||'+i
toAppend = toAppend + ')&&'
toAppend2 = toAppend + '('
for j in Hlt1:
	Triggers.append(toAppend+j)
	if(toAppend2 == toAppend+'('):
		toAppend2 = toAppend2 + j
	else:
		toAppend2 = toAppend2 + '||' + j
toAppend2 = toAppend2 + ')&&'
for k in Hlt2:
	Triggers.append(toAppend2+k)

truthlevel = ["","&&abs(pi1_TRUEID)==211&&abs(pi2_TRUEID)==211&&abs(pi3_TRUEID)==211&&abs(pi4_TRUEID)==211&&abs(pis_TRUEID)==211","&&abs(pi1_TRUEID)==211&&abs(pi2_TRUEID)==211&&abs(pi3_TRUEID)==211&&abs(pi4_TRUEID)==211&&abs(pis_TRUEID)==211&&Ks1_TRUEID==310&&Ks1_TRUEID==310","&abs(pi1_TRUEID)==211&&abs(pi2_TRUEID)==211&&abs(pi3_TRUEID)==211&&abs(pi4_TRUEID)==211&&abs(pis_TRUEID)==211&&Ks1_TRUEID==310&&Ks1_TRUEID==310&&phi_TRUEID==333"]



for key, inFile in inFiles.items():
	print(key)
	tree = trees[key]

	# index says which tracks end in an phi that was reconstructed inside the beampipe

	print('Total entries: ', tree.GetEntries())





	for trig in Triggers:
		print(trig)
		bkg000 = []
		bkg010 = []
		bkg020 = []
		bkg030 = []
		bkg040 = []
		bkg050 = []
		bkg060 = []
		bkg070 = []
		bkg080 = []
		bkg100 = []
		bkg110 = []
		bkg120 = []
		bkg130 = []
		for truth in truthlevel:
			bkg000.append(tree.GetEntries(trig+truth+'&&phi_BKGCAT==0'))
			bkg010.append(tree.GetEntries(trig+truth+'&&phi_BKGCAT==10'))
			bkg020.append(tree.GetEntries(trig+truth+'&&phi_BKGCAT==20'))
			bkg030.append(tree.GetEntries(trig+truth+'&&phi_BKGCAT==30'))
			bkg040.append(tree.GetEntries(trig+truth+'&&phi_BKGCAT==40'))
			bkg050.append(tree.GetEntries(trig+truth+'&&phi_BKGCAT==50'))
			bkg060.append(tree.GetEntries(trig+truth+'&&phi_BKGCAT==60'))
			bkg070.append(tree.GetEntries(trig+truth+'&&phi_BKGCAT==70'))
			bkg080.append(tree.GetEntries(trig+truth+'&&phi_BKGCAT==80'))
			bkg100.append(tree.GetEntries(trig+truth+'&&phi_BKGCAT==100'))
			bkg110.append(tree.GetEntries(trig+truth+'&&phi_BKGCAT==110'))
			bkg120.append(tree.GetEntries(trig+truth+'&&phi_BKGCAT==120'))
			bkg130.append(tree.GetEntries(trig+truth+'&&phi_BKGCAT==130'))
		print('\t', 'all', 'true pions', 'true kaons', 'true phis')
		print('Signal',bkg000)
		print('Quasi-signall',bkg010)
		print('Phys. back. (full rec.)',bkg020)
		print('Reflection (mis-ID)',bkg030)
		print('Phys. back. (part. rec.)',bkg040)
		print('Low-mass background',bkg050)
		print('Ghost',bkg060)
		print('FromPV',bkg070)
		print('AllFromSamePV',bkg080)
		print('Pileup/FromDifferentPV',bkg100)
		print('bb event',bkg110)
		print('cc event',bkg120)
		print('light-flavour event',bkg130)







		
		
