#!/usr/bin/env python
'''
Example on how to plot different variables from different trees to make comparisons

to use

git clone ssh://git@gitlab.cern.ch:7999/gdujany/pyUtils.git

then add to you .bashrc the line
export PYTHONPATH=<folder where downloaded pyUtils>/pyUtils:$PYTHONPATH
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

trees = {}
for key, inFile in inFiles.items():
    trees[key] = inFile.Get('TuplePhi2KsKs/DecayTree')


tree_incl = trees['phi2KsKs_incl']

# index says which tracks end in an phi that was reconstructed inside the beampipe

print(tree_incl.GetEntries())



truthmatch = 'abs(pi1_TRUEID)==211&&abs(pi2_TRUEID)==211&&abs(pi3_TRUEID)==211&&abs(pi4_TRUEID)==211&&abs(Ks1_TRUEID)==310&&abs(Ks2_TRUEID)==310&&abs(phi_TRUEID)==333'

print(tree_incl.GetEntries(truthmatch))

truthmatch = ''


LLLL = tree_incl.GetEntries('pi1_TRACK_Type ==3 && pi2_TRACK_Type == 3 && pi3_TRACK_Type == 3 && pi4_TRACK_Type == 3' +truthmatch)
LLLL_both = tree_incl.GetEntries('pi1_TRACK_Type ==3 && pi2_TRACK_Type == 3 && pi3_TRACK_Type == 3 && pi4_TRACK_Type == 3 && sqrt(Ks2_ENDVERTEX_X*Ks2_ENDVERTEX_X+Ks2_ENDVERTEX_Y*Ks2_ENDVERTEX_Y)<7&&sqrt(Ks1_ENDVERTEX_X*Ks1_ENDVERTEX_X+Ks1_ENDVERTEX_Y*Ks1_ENDVERTEX_Y)<7' +truthmatch)
LLLL_none = tree_incl.GetEntries('pi1_TRACK_Type ==3 && pi2_TRACK_Type == 3 && pi3_TRACK_Type == 3 && pi4_TRACK_Type == 3 && sqrt(Ks2_ENDVERTEX_X*Ks2_ENDVERTEX_X+Ks2_ENDVERTEX_Y*Ks2_ENDVERTEX_Y)>=7&&sqrt(Ks1_ENDVERTEX_X*Ks1_ENDVERTEX_X+Ks1_ENDVERTEX_Y*Ks1_ENDVERTEX_Y)>=7' +truthmatch)
LLLL_one = tree_incl.GetEntries('pi1_TRACK_Type ==3 && pi2_TRACK_Type == 3 && pi3_TRACK_Type == 3 && pi4_TRACK_Type == 3 && sqrt(Ks2_ENDVERTEX_X*Ks2_ENDVERTEX_X+Ks2_ENDVERTEX_Y*Ks2_ENDVERTEX_Y)<7&&sqrt(Ks1_ENDVERTEX_X*Ks1_ENDVERTEX_X+Ks1_ENDVERTEX_Y*Ks1_ENDVERTEX_Y)>=7' +truthmatch)+ tree_incl.GetEntries('pi1_TRACK_Type ==3 && pi2_TRACK_Type == 3 && pi3_TRACK_Type == 3 && pi4_TRACK_Type == 3 && sqrt(Ks2_ENDVERTEX_X*Ks2_ENDVERTEX_X+Ks2_ENDVERTEX_Y*Ks2_ENDVERTEX_Y)>=7&&sqrt(Ks1_ENDVERTEX_X*Ks1_ENDVERTEX_X+Ks1_ENDVERTEX_Y*Ks1_ENDVERTEX_Y)<7' +truthmatch)

LLDD = tree_incl.GetEntries('pi1_TRACK_Type==5 && pi2_TRACK_Type==5 && pi3_TRACK_Type==3 && pi4_TRACK_Type== 3' +truthmatch) + tree_incl.GetEntries('pi1_TRACK_Type ==3 && pi2_TRACK_Type == 3 && pi3_TRACK_Type == 5 && pi4_TRACK_Type == 5' +truthmatch)
LLDD_both = tree_incl.GetEntries('pi1_TRACK_Type==5 && pi2_TRACK_Type==5 && pi3_TRACK_Type==3 && pi4_TRACK_Type== 3 && sqrt(Ks1_ENDVERTEX_X*Ks1_ENDVERTEX_X+Ks1_ENDVERTEX_Y*Ks1_ENDVERTEX_Y)<7&&sqrt(Ks2_ENDVERTEX_X*Ks2_ENDVERTEX_X+Ks2_ENDVERTEX_Y*Ks2_ENDVERTEX_Y)<7' +truthmatch) + tree_incl.GetEntries('pi1_TRACK_Type ==3 && pi2_TRACK_Type == 3 && pi3_TRACK_Type == 5 && pi4_TRACK_Type == 5 && sqrt(Ks1_ENDVERTEX_X*Ks1_ENDVERTEX_X+Ks1_ENDVERTEX_Y*Ks1_ENDVERTEX_Y)<7&&sqrt(Ks2_ENDVERTEX_X*Ks2_ENDVERTEX_X+Ks2_ENDVERTEX_Y*Ks2_ENDVERTEX_Y)<7' +truthmatch)
LLDD_none = tree_incl.GetEntries('pi1_TRACK_Type==5 && pi2_TRACK_Type==5 && pi3_TRACK_Type==3 && pi4_TRACK_Type== 3 && sqrt(Ks1_ENDVERTEX_X*Ks1_ENDVERTEX_X+Ks1_ENDVERTEX_Y*Ks1_ENDVERTEX_Y)>=7&&sqrt(Ks2_ENDVERTEX_X*Ks2_ENDVERTEX_X+Ks2_ENDVERTEX_Y*Ks2_ENDVERTEX_Y)>=7' +truthmatch) + tree_incl.GetEntries('pi1_TRACK_Type ==3 && pi2_TRACK_Type == 3 && pi3_TRACK_Type == 5 && pi4_TRACK_Type == 5 && sqrt(Ks1_ENDVERTEX_X*Ks1_ENDVERTEX_X+Ks1_ENDVERTEX_Y*Ks1_ENDVERTEX_Y)>=7&&sqrt(Ks2_ENDVERTEX_X*Ks2_ENDVERTEX_X+Ks2_ENDVERTEX_Y*Ks2_ENDVERTEX_Y)>=7' +truthmatch)
LLDD_long = tree_incl.GetEntries('pi1_TRACK_Type==5 && pi2_TRACK_Type==5 && pi3_TRACK_Type==3 && pi4_TRACK_Type== 3 && sqrt(Ks1_ENDVERTEX_X*Ks1_ENDVERTEX_X+Ks1_ENDVERTEX_Y*Ks1_ENDVERTEX_Y)>=7&&sqrt(Ks2_ENDVERTEX_X*Ks2_ENDVERTEX_X+Ks2_ENDVERTEX_Y*Ks2_ENDVERTEX_Y)<7' +truthmatch) + tree_incl.GetEntries('pi1_TRACK_Type ==3 && pi2_TRACK_Type == 3 && pi3_TRACK_Type == 5 && pi4_TRACK_Type == 5 && sqrt(Ks1_ENDVERTEX_X*Ks1_ENDVERTEX_X+Ks1_ENDVERTEX_Y*Ks1_ENDVERTEX_Y)<7&&sqrt(Ks2_ENDVERTEX_X*Ks2_ENDVERTEX_X+Ks2_ENDVERTEX_Y*Ks2_ENDVERTEX_Y)>=7' +truthmatch)
LLDD_down = tree_incl.GetEntries('pi1_TRACK_Type==5 && pi2_TRACK_Type==5 && pi3_TRACK_Type==3 && pi4_TRACK_Type== 3 && sqrt(Ks1_ENDVERTEX_X*Ks1_ENDVERTEX_X+Ks1_ENDVERTEX_Y*Ks1_ENDVERTEX_Y)<7&&sqrt(Ks2_ENDVERTEX_X*Ks2_ENDVERTEX_X+Ks2_ENDVERTEX_Y*Ks2_ENDVERTEX_Y)>=7' +truthmatch) + tree_incl.GetEntries('pi1_TRACK_Type ==3 && pi2_TRACK_Type == 3 && pi3_TRACK_Type == 5 && pi4_TRACK_Type == 5 && sqrt(Ks1_ENDVERTEX_X*Ks1_ENDVERTEX_X+Ks1_ENDVERTEX_Y*Ks1_ENDVERTEX_Y)>=7&&sqrt(Ks2_ENDVERTEX_X*Ks2_ENDVERTEX_X+Ks2_ENDVERTEX_Y*Ks2_ENDVERTEX_Y)<7' +truthmatch)

DDDD = tree_incl.GetEntries('pi1_TRACK_Type ==5 && pi2_TRACK_Type == 5 && pi3_TRACK_Type == 5 && pi4_TRACK_Type == 5' +truthmatch)
DDDD_both = tree_incl.GetEntries('pi1_TRACK_Type ==5 && pi2_TRACK_Type == 5 && pi3_TRACK_Type == 5 && pi4_TRACK_Type == 5 && sqrt(Ks2_ENDVERTEX_X*Ks2_ENDVERTEX_X+Ks2_ENDVERTEX_Y*Ks2_ENDVERTEX_Y)<7&&sqrt(Ks1_ENDVERTEX_X*Ks1_ENDVERTEX_X+Ks1_ENDVERTEX_Y*Ks1_ENDVERTEX_Y)<7' +truthmatch)
DDDD_none = tree_incl.GetEntries('pi1_TRACK_Type ==5 && pi2_TRACK_Type == 5 && pi3_TRACK_Type == 5 && pi4_TRACK_Type == 5 && sqrt(Ks2_ENDVERTEX_X*Ks2_ENDVERTEX_X+Ks2_ENDVERTEX_Y*Ks2_ENDVERTEX_Y)>=7&&sqrt(Ks1_ENDVERTEX_X*Ks1_ENDVERTEX_X+Ks1_ENDVERTEX_Y*Ks1_ENDVERTEX_Y)>=7' +truthmatch)
DDDD_one = tree_incl.GetEntries('pi1_TRACK_Type ==5 && pi2_TRACK_Type == 5 && pi3_TRACK_Type == 5 && pi4_TRACK_Type == 5 && sqrt(Ks2_ENDVERTEX_X*Ks2_ENDVERTEX_X+Ks2_ENDVERTEX_Y*Ks2_ENDVERTEX_Y)<7&&sqrt(Ks1_ENDVERTEX_X*Ks1_ENDVERTEX_X+Ks1_ENDVERTEX_Y*Ks1_ENDVERTEX_Y)>=7' +truthmatch)+ tree_incl.GetEntries('pi1_TRACK_Type ==5 && pi2_TRACK_Type == 5 && pi3_TRACK_Type == 5 && pi4_TRACK_Type == 5 && sqrt(Ks2_ENDVERTEX_X*Ks2_ENDVERTEX_X+Ks2_ENDVERTEX_Y*Ks2_ENDVERTEX_Y)>=7&&sqrt(Ks1_ENDVERTEX_X*Ks1_ENDVERTEX_X+Ks1_ENDVERTEX_Y*Ks1_ENDVERTEX_Y)<7' +truthmatch)


# headline_LLLL_DDDD = ('# both in BP', 'both outside of BP', 'only on Ks in', 'Sum')
# headline_LLDD = ('# both in BP', 'both outside of BP', 'only L Ks in','only D Ks in', 'Sum')
# LLLL_compact = (LLLL,LLLL_both,LLLL_none,LLLL_one)
# DDDD_compact = (DDDD,DDDD_both,DDDD_none,DDDD_one)
# LLDD_compact = (LLDD,LLDD_both,LLDD_none,LLDD_long,LLDD_down)



print("LLLL", LLLL)
print("LLLL_both", LLLL_both)
print("LLLL_none", LLLL_none)
print("LLLL_one", LLLL_one)

print("LLDD", LLDD)
print("LLDD_both", LLDD_both)
print("LLDD_none", LLDD_none)
print("LLDD_long", LLDD_long)
print("LLDD_down", LLDD_down)

print("DDDD", DDDD)
print("DDDD_both", DDDD_both)
print("DDDD_none", DDDD_none)
print("DDDD_one", DDDD_one)