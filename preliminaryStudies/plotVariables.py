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

#store_dir = os.path.join(eos_root, 'lhcb/user/g/gdujany/phi2KsKs/')
store_dir = '~/phi2KsKs/files/'

inFiles = {}
inFiles['data2012'] = r.TFile(os.path.join(store_dir, 'Ds_Phi2KsKs_MagUp.root'))
#inFiles['phi2KsKs_incl'] = r.TFile(os.path.join(store_dir, 'Ds_Phi2KsKs_incl.root'))
inFiles['phi2KsKs_Ds'] = r.TFile(os.path.join(store_dir, 'Ds_Phi2KsKs_Ds.root'))




trees = {}
for key, inFile in inFiles.items():
    trees[key] = inFile.Get('TuplePhi2KsKs/DecayTree')

#cut = 'phi_PT<5100 && pi1_PT>200 && pi2_PT> 200 && pi3_PT>200 && pi4_PT>200 &&(sqrt(Ks1_ENDVERTEX_X*Ks1_ENDVERTEX_X + Ks1_ENDVERTEX_Y*Ks1_ENDVERTEX_Y) < 7 ||sqrt(Ks2_ENDVERTEX_X*Ks2_ENDVERTEX_X + Ks2_ENDVERTEX_Y*Ks2_ENDVERTEX_Y) < 7 )'

#cut = 'phi_M > 1010 && phi_M < 1030'

names = [b.GetName() for b in trees['data2012'].GetListOfBranches()]

names = ['Ds_ENDVERTEX_X', 'Ds_ENDVERTEX_Y', 'Ds_ENDVERTEX_Z',  'Ds_ENDVERTEX_CHI2', 'Ds_OWNPV_X', 'Ds_OWNPV_Y', 'Ds_OWNPV_Z', 'Ds_OWNPV_XERR', 'Ds_OWNPV_YERR', 'Ds_OWNPV_ZERR', 'Ds_OWNPV_CHI2', 'Ds_OWNPV_NDOF', 'Ds_IP_OWNPV', 'Ds_IPCHI2_OWNPV', 'Ds_FD_OWNPV', 'Ds_P', 'Ds_PT', 'Ds_PE', 'Ds_PX', 'Ds_PY', 'Ds_PZ', 'Ds_MMERR', 'phi_CosTheta', 'phi_ENDVERTEX_X', 'phi_ENDVERTEX_Y', 'phi_ENDVERTEX_Z', 'phi_ENDVERTEX_XERR', 'phi_ENDVERTEX_YERR', 'phi_ENDVERTEX_ZERR', 'phi_ENDVERTEX_CHI2', 'phi_OWNPV_X', 'phi_OWNPV_Y', 'phi_OWNPV_Z', 'phi_OWNPV_XERR', 'phi_OWNPV_YERR', 'phi_OWNPV_ZERR', 'phi_OWNPV_CHI2', 'phi_OWNPV_NDOF',  'phi_IP_OWNPV', 'phi_IPCHI2_OWNPV', 'phi_FD_OWNPV', 'phi_FDCHI2_OWNPV', 'phi_DIRA_OWNPV', 'phi_ORIVX_X', 'phi_ORIVX_Y', 'phi_ORIVX_Z',  'phi_ORIVX_CHI2',  'phi_FD_ORIVX', 'phi_FDCHI2_ORIVX', 'phi_P', 'phi_PT', 'phi_PE', 'phi_PX', 'phi_PY', 'phi_PZ', 'phi_MM', 'phi_MMERR', 'phi_M',  'phi_ADOCA', 'phi_ADOCACHI2', 'phi_BPVDIRA', 'phi_BPVIPCHI2', 'phi_DOCAMAX', 'phi_DTF_CHI2_PV', 'phi_DTF_M_Ks1_PV', 'phi_DTF_M_Ks2_PV', 'phi_DTF_M_PV', 'phi_VFASPF_CHI2', 'phi_VFASPF_CHI2DOF', 'phi_L0Global_Dec', 'phi_L0Global_TIS', 'phi_L0Global_TOS', 'phi_Hlt1Global_Dec', 'phi_Hlt1Global_TIS', 'phi_Hlt1Global_TOS', 'phi_Hlt1Phys_Dec', 'phi_Hlt1Phys_TIS', 'phi_Hlt1Phys_TOS', 'phi_Hlt2Global_Dec', 'phi_Hlt2Global_TIS', 'phi_Hlt2Global_TOS', 'phi_Hlt2Phys_Dec', 'phi_Hlt2Phys_TIS', 'phi_Hlt2Phys_TOS', 'phi_L0HadronDecision_Dec', 'phi_L0HadronDecision_TIS', 'phi_L0HadronDecision_TOS', 'phi_L0MuonDecision_Dec', 'phi_L0MuonDecision_TIS', 'phi_L0MuonDecision_TOS', 'phi_L0ElectronDecision_Dec', 'phi_L0ElectronDecision_TIS', 'phi_L0ElectronDecision_TOS', 'phi_Hlt1TrackAllL0Decision_Dec', 'phi_Hlt1TrackAllL0Decision_TIS', 'phi_Hlt1TrackAllL0Decision_TOS', 'phi_Hlt1TrackPhotonDecision_Dec', 'phi_Hlt1TrackPhotonDecision_TIS', 'phi_Hlt1TrackPhotonDecision_TOS', 'phi_Hlt1TrackMuonDecision_Dec', 'phi_Hlt1TrackMuonDecision_TIS', 'phi_Hlt1TrackMuonDecision_TOS', 'phi_Hlt2ExpressKSDecision_Dec', 'phi_Hlt2ExpressKSDecision_TIS', 'phi_Hlt2ExpressKSDecision_TOS', 'phi_Hlt2CharmHadD02HHXDst_BaryonhhXWideMassDecision_Dec', 'phi_Hlt2CharmHadD02HHXDst_BaryonhhXWideMassDecision_TIS', 'phi_Hlt2CharmHadD02HHXDst_BaryonhhXWideMassDecision_TOS', 'Ks1_CosTheta', 'Ks1_ENDVERTEX_X', 'Ks1_ENDVERTEX_Y', 'Ks1_ENDVERTEX_Z', 'Ks1_ENDVERTEX_XERR', 'Ks1_ENDVERTEX_YERR', 'Ks1_ENDVERTEX_ZERR', 'Ks1_ENDVERTEX_CHI2','Ks1_OWNPV_X', 'Ks1_OWNPV_Y', 'Ks1_OWNPV_Z', 'Ks1_OWNPV_XERR', 'Ks1_OWNPV_YERR', 'Ks1_OWNPV_ZERR', 'Ks1_OWNPV_CHI2', 'Ks1_OWNPV_NDOF',  'Ks1_IP_OWNPV', 'Ks1_IPCHI2_OWNPV', 'Ks1_FD_OWNPV', 'Ks1_FDCHI2_OWNPV', 'Ks1_DIRA_OWNPV', 'Ks1_ORIVX_CHI2', 'Ks1_FD_ORIVX', 'Ks1_FDCHI2_ORIVX', 'Ks1_P', 'Ks1_PT', 'Ks1_PE', 'Ks1_PX', 'Ks1_PY', 'Ks1_PZ', 'Ks1_MM', 'Ks1_MMERR', 'Ks1_M', 'Ks1_ADOCA', 'Ks1_ADOCACHI2', 'Ks1_BPVDIRA', 'Ks1_BPVIPCHI2', 'Ks1_BPVLTIME', 'Ks1_BPVVD', 'Ks1_BPVVDCHI2', 'Ks1_VFASPF_CHI2', 'Ks1_VFASPF_CHI2DOF', 'Ks1_TAU', 'Ks1_TAUERR', 'Ks1_TAUCHI2', 'pi1_CosTheta', 'pi1_OWNPV_X', 'pi1_OWNPV_Y', 'pi1_OWNPV_Z', 'pi1_OWNPV_XERR', 'pi1_OWNPV_YERR', 'pi1_OWNPV_ZERR', 'pi1_OWNPV_CHI2', 'pi1_OWNPV_NDOF', 'pi1_IP_OWNPV', 'pi1_IPCHI2_OWNPV', 'pi1_ORIVX_X', 'pi1_ORIVX_Y', 'pi1_ORIVX_Z', 'pi1_ORIVX_XERR', 'pi1_ORIVX_YERR', 'pi1_ORIVX_ZERR', 'pi1_ORIVX_CHI2', 'pi1_P', 'pi1_PT', 'pi1_PE', 'pi1_PX', 'pi1_PY', 'pi1_PZ', 'pi1_M', 'pi1_ProbNNe', 'pi1_ProbNNk', 'pi1_ProbNNp', 'pi1_ProbNNpi', 'pi1_ProbNNmu', 'pi1_ProbNNghost', 'pi1_hasMuon', 'pi1_isMuon', 'pi1_hasRich', 'pi1_hasCalo', 'pi1_TRACK_Type', 'pi1_TRACK_Key', 'pi1_TRACK_CHI2NDOF', 'pi1_TRACK_PCHI2', 'pi1_TRACK_MatchCHI2', 'pi1_TRACK_GhostProb', 'pi1_TRACK_Likelihood', 'pi1_TRCHI2DOF', 'pi1_TRGHOSTPROB', 'pi2_CosTheta', 'pi2_OWNPV_X', 'pi2_OWNPV_Y', 'pi2_OWNPV_Z', 'pi2_OWNPV_XERR', 'pi2_OWNPV_YERR', 'pi2_OWNPV_ZERR', 'pi2_OWNPV_CHI2', 'pi2_OWNPV_NDOF', 'pi2_IP_OWNPV', 'pi2_IPCHI2_OWNPV', 'pi2_ORIVX_X', 'pi2_ORIVX_Y', 'pi2_ORIVX_Z', 'pi2_ORIVX_XERR', 'pi2_ORIVX_YERR', 'pi2_ORIVX_ZERR', 'pi2_ORIVX_CHI2', 'pi2_P', 'pi2_PT', 'pi2_PE', 'pi2_PX', 'pi2_PY', 'pi2_PZ', 'pi2_M', 'pi2_ProbNNe', 'pi2_ProbNNk', 'pi2_ProbNNp', 'pi2_ProbNNpi', 'pi2_ProbNNmu', 'pi2_ProbNNghost', 'pi2_hasMuon', 'pi2_isMuon', 'pi2_hasRich', 'pi2_hasCalo', 'pi2_TRACK_Type', 'pi2_TRACK_Key', 'pi2_TRACK_CHI2NDOF', 'pi2_TRACK_PCHI2', 'pi2_TRACK_MatchCHI2', 'pi2_TRACK_GhostProb', 'pi2_TRACK_Likelihood', 'pi2_TRCHI2DOF', 'pi2_TRGHOSTPROB', 'Ks2_CosTheta', 'Ks2_ENDVERTEX_X', 'Ks2_ENDVERTEX_Y', 'Ks2_ENDVERTEX_Z', 'Ks2_ENDVERTEX_XERR', 'Ks2_ENDVERTEX_YERR', 'Ks2_ENDVERTEX_ZERR', 'Ks2_ENDVERTEX_CHI2', 'Ks2_ENDVERTEX_NDOF', 'Ks2_OWNPV_X', 'Ks2_OWNPV_Y', 'Ks2_OWNPV_Z', 'Ks2_OWNPV_XERR', 'Ks2_OWNPV_YERR', 'Ks2_OWNPV_ZERR', 'Ks2_OWNPV_CHI2', 'Ks2_OWNPV_NDOF', 'Ks2_IP_OWNPV', 'Ks2_IPCHI2_OWNPV', 'Ks2_FD_OWNPV', 'Ks2_FDCHI2_OWNPV', 'Ks2_DIRA_OWNPV', 'Ks2_ORIVX_X', 'Ks2_ORIVX_Y', 'Ks2_ORIVX_Z', 'Ks2_ORIVX_XERR', 'Ks2_ORIVX_YERR', 'Ks2_ORIVX_ZERR', 'Ks2_ORIVX_CHI2', 'Ks2_ORIVX_NDOF', 'Ks2_FD_ORIVX', 'Ks2_FDCHI2_ORIVX', 'Ks2_P', 'Ks2_PT', 'Ks2_PE', 'Ks2_PX', 'Ks2_PY', 'Ks2_PZ', 'Ks2_MM', 'Ks2_MMERR', 'Ks2_M', 'Ks2_ADOCA', 'Ks2_ADOCACHI2', 'Ks2_BPVDIRA', 'Ks2_BPVIPCHI2', 'Ks2_BPVVD', 'Ks2_BPVVDCHI2', 'Ks2_VFASPF_CHI2', 'Ks2_VFASPF_CHI2DOF', 'Ks2_TAU', 'Ks2_TAUERR', 'Ks2_TAUCHI2', 'pi3_CosTheta', 'pi3_OWNPV_X', 'pi3_OWNPV_Y', 'pi3_OWNPV_Z', 'pi3_OWNPV_XERR', 'pi3_OWNPV_YERR', 'pi3_OWNPV_ZERR', 'pi3_OWNPV_CHI2', 'pi3_OWNPV_NDOF', 'pi3_IP_OWNPV', 'pi3_IPCHI2_OWNPV', 'pi3_ORIVX_X', 'pi3_ORIVX_Y', 'pi3_ORIVX_Z', 'pi3_ORIVX_XERR', 'pi3_ORIVX_YERR', 'pi3_ORIVX_ZERR', 'pi3_ORIVX_CHI2', 'pi3_P', 'pi3_PT', 'pi3_PE', 'pi3_PX', 'pi3_PY', 'pi3_PZ', 'pi3_M', 'pi3_ProbNNe', 'pi3_ProbNNk', 'pi3_ProbNNp', 'pi3_ProbNNpi', 'pi3_ProbNNmu', 'pi3_ProbNNghost', 'pi3_hasMuon', 'pi3_isMuon', 'pi3_hasRich', 'pi3_hasCalo', 'pi3_TRACK_Type', 'pi3_TRACK_Key', 'pi3_TRACK_CHI2NDOF', 'pi3_TRACK_PCHI2', 'pi3_TRACK_MatchCHI2', 'pi3_TRACK_GhostProb', 'pi3_TRACK_Likelihood', 'pi3_TRCHI2DOF', 'pi3_TRGHOSTPROB', 'pi4_CosTheta', 'pi4_OWNPV_X', 'pi4_OWNPV_Y', 'pi4_OWNPV_Z', 'pi4_OWNPV_XERR', 'pi4_OWNPV_YERR', 'pi4_OWNPV_ZERR', 'pi4_OWNPV_CHI2', 'pi4_OWNPV_NDOF', 'pi4_IP_OWNPV', 'pi4_IPCHI2_OWNPV', 'pi4_ORIVX_X', 'pi4_ORIVX_Y', 'pi4_ORIVX_Z', 'pi4_ORIVX_XERR', 'pi4_ORIVX_YERR', 'pi4_ORIVX_ZERR', 'pi4_ORIVX_CHI2', 'pi4_P', 'pi4_PT', 'pi4_PE', 'pi4_PX', 'pi4_PY', 'pi4_PZ', 'pi4_M', 'pi4_ProbNNe', 'pi4_ProbNNk', 'pi4_ProbNNp', 'pi4_ProbNNpi', 'pi4_ProbNNmu', 'pi4_ProbNNghost', 'pi4_hasMuon', 'pi4_isMuon', 'pi4_hasRich', 'pi4_hasCalo', 'pi4_TRACK_Type', 'pi4_TRACK_Key', 'pi4_TRACK_CHI2NDOF', 'pi4_TRACK_PCHI2', 'pi4_TRACK_MatchCHI2', 'pi4_TRACK_GhostProb', 'pi4_TRACK_Likelihood', 'pi4_TRCHI2DOF', 'pi4_TRGHOSTPROB', 'pis_CosTheta', 'pis_OWNPV_X', 'pis_OWNPV_Y', 'pis_OWNPV_Z', 'pis_OWNPV_XERR', 'pis_OWNPV_YERR', 'pis_OWNPV_ZERR', 'pis_OWNPV_CHI2', 'pis_OWNPV_NDOF', 'pis_IP_OWNPV', 'pis_IPCHI2_OWNPV', 'pis_ORIVX_X', 'pis_ORIVX_Y', 'pis_ORIVX_Z', 'pis_ORIVX_XERR', 'pis_ORIVX_YERR', 'pis_ORIVX_ZERR', 'pis_ORIVX_CHI2', 'pis_P', 'pis_PT', 'pis_PE', 'pis_PX', 'pis_PY', 'pis_PZ', 'pis_M', 'pis_ProbNNe', 'pis_ProbNNk', 'pis_ProbNNp', 'pis_ProbNNpi', 'pis_ProbNNmu', 'pis_ProbNNghost', 'pis_hasMuon', 'pis_isMuon', 'pis_hasRich', 'pis_hasCalo', 'pis_TRACK_Type', 'pis_TRACK_Key', 'pis_TRACK_CHI2NDOF', 'pis_TRACK_PCHI2', 'pis_TRACK_MatchCHI2', 'pis_TRACK_GhostProb', 'pis_TRACK_Likelihood', 'nCandidate', 'totCandidates']

cut = '(sqrt(Ks1_ENDVERTEX_X*Ks1_ENDVERTEX_X+Ks1_ENDVERTEX_Y*Ks1_ENDVERTEX_Y)<7 ||sqrt(Ks2_ENDVERTEX_X*Ks2_ENDVERTEX_X+Ks2_ENDVERTEX_Y*Ks2_ENDVERTEX_Y)<7)'

cut = cut + "&& Ds_M > 1950 && Ds_M <1990"

cut += "&& Ks1_M > 485 && Ks1_M < 510 && Ks2_M > 485 && Ks2_M < 510 "


ct = CompareTreeVars(normalise=True)
ct.addTree('data2012', trees['data2012'], evtMax=50000, tree_cut = cut)
ct.addTree('phi2KsKs_Ds', trees['phi2KsKs_Ds'], tree_cut = cut)
#ct.addTree('phi2KsKs_incl', trees['phi2KsKs_incl'], tree_cut = cut)


# Choose variables to plot

# N.B. normalization does not work if region is not given

binnumber = 100


ct.addVariable("Ds_M", region = [1820,2120])
# ct.addVariable('phi_M', region = [950, 1080])
# ct.addVariable('phi_PT', region = [0, 15000])
# ct.addVariable('phi_P', region = [0, 300000])
# ct.addVariable('phi_PE', region = [0, 300e3])
# ct.addVariable('phi_ENDVERTEX_CHI2', region = [0, 80])
# ct.addVariable('Ks1_CosTheta', region = [-1, 1])
# ct.addVariable('Ks1_ENDVERTEX_CHI2', region = [0, 4])
# ct.addVariable('Ks1_M', region = [497.55, 497.65])
# ct.addVariable('Ks1_PT', region = [0, 10000])
# ct.addVariable('Ks1_P', region = [0, 200e3])
# ct.addVariable('Ks2_CosTheta', region = [-1, 1])
# ct.addVariable('Ks2_ENDVERTEX_CHI2', region = [0, 4])
# ct.addVariable('Ks2_M', region = [497.55, 497.65])
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

for name in names:
	ct.addVariable(name)


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
