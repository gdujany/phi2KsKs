from Gaudi.Configuration import *

eos_root = os.path.expanduser('~/eos/')

eos_dir = '/lhcb/grid/user'
file_list = [
	'/lhcb/user/j/jrharris/2015_02/100022/100022208/gauss.dst',
	'/lhcb/user/j/jrharris/2015_02/100022/100022219/gauss.dst',
	'/lhcb/user/j/jrharris/2015_02/100022/100022234/gauss.dst',
	'/lhcb/user/j/jrharris/2015_02/100022/100022242/gauss.dst',
	'/lhcb/user/j/jrharris/2015_02/100022/100022246/gauss.dst',
	'/lhcb/user/j/jrharris/2015_02/100022/100022253/gauss.dst',
    ]
files = [eos_dir+file for file in file_list]

from GaudiConf import IOHelper
IOHelper().inputFiles(['PFN:root://eoslhcb.cern.ch//eos'+file for file in files], clear=True)
