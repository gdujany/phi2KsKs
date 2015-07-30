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

store_dir = os.path.join(eos_root, 'lhcb/user/g/gdujany/phi2KsKs/')

inFiles = {}
inFiles['data2012'] = r.TFile(os.path.join(store_dir, 'data2012.root'))
inFiles['phi2KsKs_incl'] = r.TFile(os.path.join(store_dir, 'phi2KsKs_incl.root'))
inFiles['phi2KsKs_Ds'] = r.TFile(os.path.join(store_dir, 'phi2KsKs_Ds.root'))
inFiles['minbias_1'] = r.TFile(os.path.join(store_dir, 'minbias1.root'))
inFiles['minbias_2'] = r.TFile(os.path.join(store_dir, 'minbias2.root'))
inFiles['minbias_3'] = r.TFile(os.path.join(store_dir, 'minbias3.root'))


trees = {}
for key, inFile in inFiles.items():
    trees[key] = inFile.Get('TuplePhi2KsKs/DecayTree')


for key, inFile in inFiles.items():
	print(key)
	tree = trees[key]

	# index says which tracks end in an phi that was reconstructed inside the beampipe

	print('Total entries: ', tree.GetEntries())

	truthmatch ='abs(pi1_TRUEID)==211&&abs(pi2_TRUEID)==211&&abs(pi3_TRUEID)==211&&abs(pi4_TRUEID)==211&&abs(Ks1_TRUEID)==310&&abs(Ks2_TRUEID)==310&&abs(phi_TRUEID)==333'

	if(key=='data2012' or key == 'minbias_1' or key == 'minbias_2' or key == 'minbias_3'):
		truthmatch = ''

	nEntriesTM = tree.GetEntries(truthmatch)
	print('Truthmatched: ',nEntriesTM)

	if(truthmatch!=''):
		truthmatch = '&&'+truthmatch

	LLLL = tree.GetEntries('pi1_TRACK_Type ==3 && pi2_TRACK_Type == 3 && pi3_TRACK_Type == 3 && pi4_TRACK_Type == 3' +truthmatch)
	LLLL_both = tree.GetEntries('pi1_TRACK_Type ==3 && pi2_TRACK_Type == 3 && pi3_TRACK_Type == 3 && pi4_TRACK_Type == 3 && sqrt(Ks2_ENDVERTEX_X*Ks2_ENDVERTEX_X+Ks2_ENDVERTEX_Y*Ks2_ENDVERTEX_Y)<7&&sqrt(Ks1_ENDVERTEX_X*Ks1_ENDVERTEX_X+Ks1_ENDVERTEX_Y*Ks1_ENDVERTEX_Y)<7' +truthmatch)
	LLLL_none = tree.GetEntries('pi1_TRACK_Type ==3 && pi2_TRACK_Type == 3 && pi3_TRACK_Type == 3 && pi4_TRACK_Type == 3 && sqrt(Ks2_ENDVERTEX_X*Ks2_ENDVERTEX_X+Ks2_ENDVERTEX_Y*Ks2_ENDVERTEX_Y)>=7&&sqrt(Ks1_ENDVERTEX_X*Ks1_ENDVERTEX_X+Ks1_ENDVERTEX_Y*Ks1_ENDVERTEX_Y)>=7' +truthmatch)
	LLLL_one = tree.GetEntries('pi1_TRACK_Type ==3 && pi2_TRACK_Type == 3 && pi3_TRACK_Type == 3 && pi4_TRACK_Type == 3 && sqrt(Ks2_ENDVERTEX_X*Ks2_ENDVERTEX_X+Ks2_ENDVERTEX_Y*Ks2_ENDVERTEX_Y)<7&&sqrt(Ks1_ENDVERTEX_X*Ks1_ENDVERTEX_X+Ks1_ENDVERTEX_Y*Ks1_ENDVERTEX_Y)>=7' +truthmatch)+ tree.GetEntries('pi1_TRACK_Type ==3 && pi2_TRACK_Type == 3 && pi3_TRACK_Type == 3 && pi4_TRACK_Type == 3 && sqrt(Ks2_ENDVERTEX_X*Ks2_ENDVERTEX_X+Ks2_ENDVERTEX_Y*Ks2_ENDVERTEX_Y)>=7&&sqrt(Ks1_ENDVERTEX_X*Ks1_ENDVERTEX_X+Ks1_ENDVERTEX_Y*Ks1_ENDVERTEX_Y)<7' +truthmatch)

	LLDD = tree.GetEntries('pi1_TRACK_Type==5 && pi2_TRACK_Type==5 && pi3_TRACK_Type==3 && pi4_TRACK_Type== 3' +truthmatch) + tree.GetEntries('pi1_TRACK_Type ==3 && pi2_TRACK_Type == 3 && pi3_TRACK_Type == 5 && pi4_TRACK_Type == 5' +truthmatch)
	LLDD_both = tree.GetEntries('pi1_TRACK_Type==5 && pi2_TRACK_Type==5 && pi3_TRACK_Type==3 && pi4_TRACK_Type== 3 && sqrt(Ks1_ENDVERTEX_X*Ks1_ENDVERTEX_X+Ks1_ENDVERTEX_Y*Ks1_ENDVERTEX_Y)<7&&sqrt(Ks2_ENDVERTEX_X*Ks2_ENDVERTEX_X+Ks2_ENDVERTEX_Y*Ks2_ENDVERTEX_Y)<7' +truthmatch) + tree.GetEntries('pi1_TRACK_Type ==3 && pi2_TRACK_Type == 3 && pi3_TRACK_Type == 5 && pi4_TRACK_Type == 5 && sqrt(Ks1_ENDVERTEX_X*Ks1_ENDVERTEX_X+Ks1_ENDVERTEX_Y*Ks1_ENDVERTEX_Y)<7&&sqrt(Ks2_ENDVERTEX_X*Ks2_ENDVERTEX_X+Ks2_ENDVERTEX_Y*Ks2_ENDVERTEX_Y)<7' +truthmatch)
	LLDD_none = tree.GetEntries('pi1_TRACK_Type==5 && pi2_TRACK_Type==5 && pi3_TRACK_Type==3 && pi4_TRACK_Type== 3 && sqrt(Ks1_ENDVERTEX_X*Ks1_ENDVERTEX_X+Ks1_ENDVERTEX_Y*Ks1_ENDVERTEX_Y)>=7&&sqrt(Ks2_ENDVERTEX_X*Ks2_ENDVERTEX_X+Ks2_ENDVERTEX_Y*Ks2_ENDVERTEX_Y)>=7' +truthmatch) + tree.GetEntries('pi1_TRACK_Type ==3 && pi2_TRACK_Type == 3 && pi3_TRACK_Type == 5 && pi4_TRACK_Type == 5 && sqrt(Ks1_ENDVERTEX_X*Ks1_ENDVERTEX_X+Ks1_ENDVERTEX_Y*Ks1_ENDVERTEX_Y)>=7&&sqrt(Ks2_ENDVERTEX_X*Ks2_ENDVERTEX_X+Ks2_ENDVERTEX_Y*Ks2_ENDVERTEX_Y)>=7' +truthmatch)
	LLDD_long = tree.GetEntries('pi1_TRACK_Type==5 && pi2_TRACK_Type==5 && pi3_TRACK_Type==3 && pi4_TRACK_Type== 3 && sqrt(Ks1_ENDVERTEX_X*Ks1_ENDVERTEX_X+Ks1_ENDVERTEX_Y*Ks1_ENDVERTEX_Y)>=7&&sqrt(Ks2_ENDVERTEX_X*Ks2_ENDVERTEX_X+Ks2_ENDVERTEX_Y*Ks2_ENDVERTEX_Y)<7' +truthmatch) + tree.GetEntries('pi1_TRACK_Type ==3 && pi2_TRACK_Type == 3 && pi3_TRACK_Type == 5 && pi4_TRACK_Type == 5 && sqrt(Ks1_ENDVERTEX_X*Ks1_ENDVERTEX_X+Ks1_ENDVERTEX_Y*Ks1_ENDVERTEX_Y)<7&&sqrt(Ks2_ENDVERTEX_X*Ks2_ENDVERTEX_X+Ks2_ENDVERTEX_Y*Ks2_ENDVERTEX_Y)>=7' +truthmatch)
	LLDD_down = tree.GetEntries('pi1_TRACK_Type==5 && pi2_TRACK_Type==5 && pi3_TRACK_Type==3 && pi4_TRACK_Type== 3 && sqrt(Ks1_ENDVERTEX_X*Ks1_ENDVERTEX_X+Ks1_ENDVERTEX_Y*Ks1_ENDVERTEX_Y)<7&&sqrt(Ks2_ENDVERTEX_X*Ks2_ENDVERTEX_X+Ks2_ENDVERTEX_Y*Ks2_ENDVERTEX_Y)>=7' +truthmatch) + tree.GetEntries('pi1_TRACK_Type ==3 && pi2_TRACK_Type == 3 && pi3_TRACK_Type == 5 && pi4_TRACK_Type == 5 && sqrt(Ks1_ENDVERTEX_X*Ks1_ENDVERTEX_X+Ks1_ENDVERTEX_Y*Ks1_ENDVERTEX_Y)>=7&&sqrt(Ks2_ENDVERTEX_X*Ks2_ENDVERTEX_X+Ks2_ENDVERTEX_Y*Ks2_ENDVERTEX_Y)<7' +truthmatch)

	DDDD = tree.GetEntries('pi1_TRACK_Type ==5 && pi2_TRACK_Type == 5 && pi3_TRACK_Type == 5 && pi4_TRACK_Type == 5' +truthmatch)
	DDDD_both = tree.GetEntries('pi1_TRACK_Type ==5 && pi2_TRACK_Type == 5 && pi3_TRACK_Type == 5 && pi4_TRACK_Type == 5 && sqrt(Ks2_ENDVERTEX_X*Ks2_ENDVERTEX_X+Ks2_ENDVERTEX_Y*Ks2_ENDVERTEX_Y)<7&&sqrt(Ks1_ENDVERTEX_X*Ks1_ENDVERTEX_X+Ks1_ENDVERTEX_Y*Ks1_ENDVERTEX_Y)<7' +truthmatch)
	DDDD_none = tree.GetEntries('pi1_TRACK_Type ==5 && pi2_TRACK_Type == 5 && pi3_TRACK_Type == 5 && pi4_TRACK_Type == 5 && sqrt(Ks2_ENDVERTEX_X*Ks2_ENDVERTEX_X+Ks2_ENDVERTEX_Y*Ks2_ENDVERTEX_Y)>=7&&sqrt(Ks1_ENDVERTEX_X*Ks1_ENDVERTEX_X+Ks1_ENDVERTEX_Y*Ks1_ENDVERTEX_Y)>=7' +truthmatch)
	DDDD_one = tree.GetEntries('pi1_TRACK_Type ==5 && pi2_TRACK_Type == 5 && pi3_TRACK_Type == 5 && pi4_TRACK_Type == 5 && sqrt(Ks2_ENDVERTEX_X*Ks2_ENDVERTEX_X+Ks2_ENDVERTEX_Y*Ks2_ENDVERTEX_Y)<7&&sqrt(Ks1_ENDVERTEX_X*Ks1_ENDVERTEX_X+Ks1_ENDVERTEX_Y*Ks1_ENDVERTEX_Y)>=7' +truthmatch)+ tree.GetEntries('pi1_TRACK_Type ==5 && pi2_TRACK_Type == 5 && pi3_TRACK_Type == 5 && pi4_TRACK_Type == 5 && sqrt(Ks2_ENDVERTEX_X*Ks2_ENDVERTEX_X+Ks2_ENDVERTEX_Y*Ks2_ENDVERTEX_Y)>=7&&sqrt(Ks1_ENDVERTEX_X*Ks1_ENDVERTEX_X+Ks1_ENDVERTEX_Y*Ks1_ENDVERTEX_Y)<7' +truthmatch)


# headline_LLLL_DDDD = ('# both in BP', 'both outside of BP', 'only on Ks in', 'Sum')
# headline_LLDD = ('# both in BP', 'both outside of BP', 'only L Ks in','only D Ks in', 'Sum')
# LLLL_compact = (LLLL,LLLL_both,LLLL_none,LLLL_one)
# DDDD_compact = (DDDD,DDDD_both,DDDD_none,DDDD_one)
# LLDD_compact = (LLDD,LLDD_both,LLDD_none,LLDD_long,LLDD_down)

	print("LLLL",LLLL, round(100*float(LLLL)/nEntriesTM,2))
	print("LLLL_both",LLLL_both, round(100*float(LLLL_both)/nEntriesTM,2))
	print("LLLL_none",LLLL_none, round(100*float(LLLL_none)/nEntriesTM,2))
	print("LLLL_one",LLLL_both, round(100*float(LLLL_one)/nEntriesTM,2))

	print("LLDD",LLDD, round(100*float(LLDD)/nEntriesTM,2))
	print("LLDD_both",LLDD_both, round(100*float(LLDD_both)/nEntriesTM,2))
	print("LLDD_none",LLDD_none, round(100*float(LLDD_none)/nEntriesTM,2))
	print("LLDD_long",LLDD_long, round(100*float(LLDD_long)/nEntriesTM,2))
	print("LLDD_down",LLDD_down, round(100*float(LLDD_down)/nEntriesTM,2))

	# print("DDDD", round(100*float(DDDD)/nEntriesTM,2))
	# print("DDDD_both", round(100*float(DDDD_both)/nEntriesTM,2))
	# print("DDDD_none", round(100*float(DDDD_none)/nEntriesTM,2))
	# print("DDDD_one", round(100*float(DDDD_one)/nEntriesTM,2))