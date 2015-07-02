from Gaudi.Configuration import *

eos_root = '/afs/cern.ch/user/g/gdujany/eos'

eos_dir = '/lhcb/grid/user'
file_list = [
    '/lhcb/user/j/jrharris/2015_02/99684/99684163/gauss.dst',
    '/lhcb/user/j/jrharris/2015_02/99698/99698267/gauss.dst',
    '/lhcb/user/j/jrharris/2015_02/99698/99698274/gauss.dst',
    '/lhcb/user/j/jrharris/2015_02/99698/99698284/gauss.dst',
    '/lhcb/user/j/jrharris/2015_02/99698/99698296/gauss.dst',
    '/lhcb/user/j/jrharris/2015_02/99698/99698303/gauss.dst',
    ]
files = [eos_dir+file for file in file_list]

from GaudiConf import IOHelper
IOHelper().inputFiles(['PFN:root://eoslhcb.cern.ch//eos'+file for file in files], clear=True)
