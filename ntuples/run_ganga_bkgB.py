from Ganga.GPI import *

gridProxy.renew()
t = JobTemplate()
t.application="DaVinci"
t.name = "ds2phipi bkgB"
t.application.optsfile="Dsphi2KsKs_stripping.py"
bk_down = BKQuery(r'/MC/2012/Beam4000GeV-2012-MagDown-Nu2.5-Pythia8/Sim08a/Digi13/Trig0x409f0045/Reco14a/Stripping20NoPrescalingFlagged/10000000/ALLSTREAMS.DST')
ds = bk_down.getDataset() 
bk_up = BKQuery(bk_down.path.replace('Down','Up'))
ds.extend(bk_up.getDataset()) 
t.inputdata = ds
j=Job(t)
j.backend=Dirac()
#j.backend=Interactive()
j.splitter = SplitByFiles(filesPerJob=60)
j.outputfiles = ["*.root"] # puts the files on the grid
#j.outputfiles += [MassStorageFile(outputNtupleName.root)] #send the files directly to eos
j.postprocessors.append(RootMerger(overwrite=True,ignorefailed = True))
j.postprocessors[-1].files = ['Phi2KsKs.root']
j.submit()

