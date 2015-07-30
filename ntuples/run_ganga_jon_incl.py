from Ganga.GPI import *

gridProxy.renew()
t = JobTemplate()
t.application="DaVinci"
t.name = "Ds2phipi_incl full trigger"
t.application.optsfile="Dsphi2KsKs.py"
#t.application.extraopts = 'DaVinci().EvtMax = -1'
t.inputdata =  LHCbDataset([
    'LFN:/lhcb/user/j/jrharris/2015_02/99698/99698109/gauss.dst',
    'LFN:/lhcb/user/j/jrharris/2015_02/99698/99698113/gauss.dst',
    'LFN:/lhcb/user/j/jrharris/2015_02/99698/99698121/gauss.dst',
    'LFN:/lhcb/user/j/jrharris/2015_02/99698/99698139/gauss.dst',
    'LFN:/lhcb/user/j/jrharris/2015_02/99698/99698156/gauss.dst',
    'LFN:/lhcb/user/j/jrharris/2015_02/99698/99698168/gauss.dst',
    'LFN:/lhcb/user/j/jrharris/2015_02/99698/99698177/gauss.dst',
    'LFN:/lhcb/user/j/jrharris/2015_02/99698/99698185/gauss.dst',
    'LFN:/lhcb/user/j/jrharris/2015_02/99700/99700724/gauss.dst',
    'LFN:/lhcb/user/j/jrharris/2015_02/99698/99698210/gauss.dst',
    'LFN:/lhcb/user/j/jrharris/2015_02/99698/99698218/gauss.dst',
    'LFN:/lhcb/user/j/jrharris/2015_02/99698/99698229/gauss.dst',
    'LFN:/lhcb/user/j/jrharris/2015_02/99698/99698243/gauss.dst',
    'LFN:/lhcb/user/j/jrharris/2015_02/99698/99698253/gauss.dst',
    'LFN:/lhcb/user/j/jrharris/2015_02/99698/99698267/gauss.dst',
    'LFN:/lhcb/user/j/jrharris/2015_02/99698/99698274/gauss.dst',
    'LFN:/lhcb/user/j/jrharris/2015_02/99698/99698284/gauss.dst',
    'LFN:/lhcb/user/j/jrharris/2015_02/99698/99698296/gauss.dst',
    'LFN:/lhcb/user/j/jrharris/2015_02/99698/99698303/gauss.dst',
    'LFN:/lhcb/user/j/jrharris/2015_02/99698/99698312/gauss.dst',
    'LFN:/lhcb/user/j/jrharris/2015_02/99698/99698319/gauss.dst',
    'LFN:/lhcb/user/j/jrharris/2015_02/99698/99698326/gauss.dst',
    'LFN:/lhcb/user/j/jrharris/2015_02/99698/99698332/gauss.dst',
    'LFN:/lhcb/user/j/jrharris/2015_02/99698/99698341/gauss.dst',
    'LFN:/lhcb/user/j/jrharris/2015_02/99698/99698347/gauss.dst'
    ])
j=Job(t)
j.backend=Dirac()
# j.backend=Interactive()
j.splitter = SplitByFiles(filesPerJob=60)
j.outputfiles = ["*.root"] # puts the files on the grid
#j.outputfiles += [MassStorageFile(outputNtupleName.root)] #send the files directly to eos
j.postprocessors.append(RootMerger(overwrite=True,ignorefailed = True))
j.postprocessors[-1].files = ['Ds2PhiPi_incl.root']
j.submit()

