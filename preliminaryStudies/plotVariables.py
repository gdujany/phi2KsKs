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

store_dir_g = os.path.join(eos_root, 'lhcb/user/g/gdujany/phi2KsKs/')
store_dir_s = '~/phi2KsKs/files/'

inFiles = {}
inFiles['data2012'] = r.TFile(os.path.join(store_dir_s, 'Ds_Phi2KsKs_2012.root'))
# inFiles['minbias'] = r.TFile(os.path.join(store_dir_s, 'Ds_Phi2KsKs_MBcomb.root'))
inFiles['phi2KsKs_incl'] = r.TFile(os.path.join(store_dir_g, 'phi2KsKs_incl.root'))
inFiles['phi2KsKs_Ds'] = r.TFile(os.path.join(store_dir_s, 'Ds_Phi2KsKs_Ds.root'))




trees = {}
for key, inFile in inFiles.items():
    trees[key] = inFile.Get('TuplePhi2KsKs/DecayTree')

#cut = 'phi_PT<5100 && pi1_PT>200 && pi2_PT> 200 && pi3_PT>200 && pi4_PT>200 &&(sqrt(Ks1_ENDVERTEX_X*Ks1_ENDVERTEX_X + Ks1_ENDVERTEX_Y*Ks1_ENDVERTEX_Y) < 7 ||sqrt(Ks2_ENDVERTEX_X*Ks2_ENDVERTEX_X + Ks2_ENDVERTEX_Y*Ks2_ENDVERTEX_Y) < 7 )'

#cut = 'phi_M > 1010 && phi_M < 1030'

names = [b.GetName() for b in trees['data2012'].GetListOfBranches()]

cut = '(sqrt(Ks1_ENDVERTEX_X*Ks1_ENDVERTEX_X+Ks1_ENDVERTEX_Y*Ks1_ENDVERTEX_Y)<7&&sqrt(Ks2_ENDVERTEX_X*Ks2_ENDVERTEX_X+Ks2_ENDVERTEX_Y*Ks2_ENDVERTEX_Y)>7)'

cut_Ds = cut + '&& Ds_M > 1955 && Ds_M < 1985&& phi_IPCHI2_OWNPV >=50'

ct = CompareTreeVars(normalise=True)
ct.addTree('data2012', trees['data2012'], tree_cut = cut_Ds) #evtMax=50000
# ct.addTree('data2012', trees['data2012_incl'], tree_cut = cut) #evtMax=50000
ct.addTree('phi2KsKs_Ds', trees['phi2KsKs_Ds'], tree_cut = cut_Ds)
#ct.addTree('minbias', trees['minbias'], tree_cut = cut)
ct.addTree('phi2KsKs_incl', trees['phi2KsKs_incl'], tree_cut = cut)


# Choose variables to plot

# N.B. normalization does not work if region is not given

binnumber = 50


# ct.addVariable("Ds_M", region = [1820,2120])
ct.addVariable('phi_M', region = [950, 1080])
# ct.addVariable('phi_PT', region = [0, 15000])
# ct.addVariable('phi_P', region = [0, 300000])
# ct.addVariable('phi_PE', region = [0, 300e3])
# ct.addVariable('phi_ENDVERTEX_CHI2', region = [0, 80])
# ct.addVariable('Ks1_CosTheta', region = [-1, 1])
# ct.addVariable('Ks1_ENDVERTEX_CHI2', region = [0, 4])
# ct.addVariable('Ks1_M', region = [400, 600])
# ct.addVariable('Ks1_PT', region = [0, 10000])
# ct.addVariable('Ks1_P', region = [0, 200e3])
# ct.addVariable('Ks2_CosTheta', region = [-1, 1])
# ct.addVariable('Ks2_ENDVERTEX_CHI2', region = [0, 4])
# ct.addVariable('Ks2_M', region = [400, 600])
# ct.addVariable('Ks2_PT', region = [0, 10000])
# ct.addVariable('Ks2_P', region = [0, 200e3])
# ct.addVariable('pi1_CosTheta', region = [-1, 1])
# ct.addVariable('pi1_PT', region = [0, 6000])
# ct.addVariable('pi1_P', region = [0, 100e3])
# ct.addVariable('pi2_CosTheta', region = [-1, 1])
# ct.addVariable('pi2_PT', region = [0, 6000])
# ct.addVariable('pi2_P', region = [0, 100e3])
# ct.addVariable('pi3_CosTheta', region = [-1, 1])
# ct.addVariable('pi3_PT', region = [0, 6000])
# ct.addVariable('pi3_P', region = [0, 100e3])
# ct.addVariable('pi4_CosTheta', region = [-1, 1])
# ct.addVariable('pi4_PT', region = [0, 1020], opts='e0')
# ct.addVariable('pi4_P', region = [0, 100e3])

# for name in names:
# 	ct.addVariable(name)


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
