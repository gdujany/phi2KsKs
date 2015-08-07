#!/usr/bin/env python

import ROOT as r
from math import sqrt
import os


eos_root = os.path.expanduser('~/eos/')
if not os.listdir(eos_root):
    raise OSError('EOS not mounted, please type:\n eosmount '+eos_root)

store_dir_g = os.path.join(eos_root, 'lhcb/user/g/gdujany/phi2KsKs_noTrigger/')
store_dir_s = '~/phi2KsKs/files/'

inFiles = {}
#inFile = r.TFile(os.path.join(store_dir_g, 'data2012.root'))
inFile = r.TFile(os.path.join(store_dir_s, 'Ds_Phi2KsKs_2012.root'))
lumi_tree = inFile.Get('GetIntegratedLuminosity/LumiTuple')


lumi = 0
s2_lumi = 0
for evt in lumi_tree:
    lumi += evt.IntegratedLuminosity
    s2_lumi += evt.IntegratedLuminosityErr

print 'lumi =', lumi, '+-', sqrt(s2_lumi),'ipb'
