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

ct = CompareTreeVars(normalise=True)
ct.addTree('data2012', trees['data2012'], evtMax=50000, tree_cut = '')
ct.addTree('phi2KsKs_incl', trees['phi2KsKs_incl'], tree_cut = '')

# Choose variables to plot

# N.B. normalization does not work if region is not given

ct.addVariable('phi_M', region = [990, 1110])
ct.addVariable('phi_PT', region = [0, 15000])
ct.addVariable('phi_P', region = [0, 300000])


# Output names

outName = 'plots_variables'
outFile_name = outName+'.pdf'
outDir = outName

if not os.path.exists(outDir):
    os.mkdir(outDir)


# make plots

c = r.TCanvas('c','c')
c.Print(outFile_name+'[')

mp = ct.getMultiPlots()

for key, plot in sorted(mp.items()):
    plot.Draw()
    c.Update()
    c.Print(outFile_name)
    c.Print(os.path.join(outDir, key+'.pdf'))


c.Print(outFile_name+']')
