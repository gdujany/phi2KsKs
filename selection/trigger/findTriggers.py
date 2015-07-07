#!/usr/bin/env python

import os

lineName = 'PhiToKSKS_PhiToKsKsLine'

eos_root = os.path.expanduser('~/eos')
if not os.listdir(eos_root):
    raise OSError('EOS not mounted, please type:\n eosmount '+eos_root)


    
eos_root += '/lhcb/grid/prod'

directory = eos_root+'/lhcb/LHCb/Collision12/CHARM.MDST/00041836/0000/' #Data md
#directory = eos_root+'/lhcb/LHCb/Collision12/CHARM.MDST/00041834/0000/' #Data mu

line = "/Event/Charm/Phys/"+lineName+"/Particles"
files = [directory+name for name in os.listdir(directory) if '.mdst' in name]

#os.system('python CheckTrg.py -n 100000 '+line+' '+' '.join([file for file in files]))

