from Gaudi.Configuration import *

eos_root = os.path.expanduser('~/eos/')

import os
if not os.listdir(eos_root):
    raise OSError('EOS not mounted, please type:\n eosmount '+eos_root)

import sys, os, re
# to be able to import jobSetup using gaudirun
sys.path.append(os.getcwd())

MagString = dict(mu = 'MagUp', md = 'MagDown')
MagnetPolarity = 'mu'
input_file = '../phi2KsKs/Rootuplizer/inputFiles/data/LHCb_Collision12_Beam4000GeVVeloClosed{0}_Real Data_Reco14_Stripping21_90000000_CHARM.MDST.py'.format(MagString[MagnetPolarity])

str_LFNs = open(input_file).read()

LF_dir = re.compile(r'LFN:(/lhcb/.*/000[0-9]{1}/).*dst')
directory=re.search(LF_dir,str_LFNs).group(1)


eos_dir = '/lhcb/grid/prod'
# eos_dir = '/lhcb/grid/user'

print '/eos'+eos_dir+directory

files = [eos_dir+directory+file for file in os.listdir(eos_root+eos_dir+directory)]

files = files[:50]

from GaudiConf import IOHelper
IOHelper().inputFiles(['PFN:root://eoslhcb.cern.ch//eos'+file for file in files], clear=True)

