from Ganga.GPI import *

gridProxy.renew()
t = JobTemplate()
t.application="DaVinci"
t.name = "phi2ksks"
t.application.optsfile="Rootuplizer.py"
bk_down = BKQuery(r'/LHCb/Collision12/Beam4000GeV-VeloClosed-MagDown/Real Data/Reco14/Stripping21/90000000/CHARM.MDST')
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

