 ############################################################
##  JOB OPTIONS ##
#
# works with ganga v600r19 (later versions can have troubles with splitting data because too many files)

# Class container with various options

decNumbers = dict(
    Bs2ppKK = 13104061,
    B2ppKPi = 11104072, #11104071 is the same but without gen cuts 
    )

simVersion = dict(
    Bs2ppKK = 'Sim08c',
    B2ppKPi = 'Sim08e',
    )

MagString = dict(mu = 'MagUp', md = 'MagDown')
    

class VariousOptions:
    def __init__(self, name, MagnetPolarity='mu', CondDBtag=None, DDDBtag=None, input_file=None, input_path=None, isMC=True, isPrescaled=False, isNormalization=False, outputNtupleName=None,dataType='2012'):
        self.name = name
        self.MagnetPolarity = MagnetPolarity
        self.DDDBtag = DDDBtag
        self.CondDBtag = CondDBtag if CondDBtag else ('sim-20121025-vc-'+MagnetPolarity+'100' if isMC else 'cond-20121016')
        self.input_file = input_file
        self.input_path = input_path
        self.outputNtupleName = name+'.root' if not outputNtupleName else outputNtupleName
        self.isPrescaled = isPrescaled
        self.isNormalization = isNormalization
        self.isMC = isMC
        self.dataType = dataType


class VariousOptionsMC(VariousOptions):
    def __init__(self, input_file=None,**argd):
        """
        MagnetPolarity in ('mu', 'md')
        """
        VariousOptions.__init__(self, input_file=input_file, isMC=True, isPrescaled=False, DDDBtag='dddb-20130929-1',CondDBtag='sim-20130522-1-vc-mu100',**argd)
        self.decNumber = decNumbers[self.name[:-3]]
        if not self.input_file:
            self.input_file = 'inputFiles/MC/BK_MC_{dataType}_{decNumber}_Beam4000GeV-{dataType}-{MagStr}-Nu2.5-Pythia8_{SimVer}_Digi13_Trig0x409f0045_Reco14a_Stripping20NoPrescalingFlagged_ALLSTREAMS.DST.py'.format(MagStr=MagString[self.MagnetPolarity],SimVer=simVersion[self.name[:-3]],**self.__dict__)

############################################################
# Options for various datasets
dataSamples = {}

MC_list = [
    'Bs2ppKK',
    'B2ppKPi',
    ]

for mc_type in MC_list:
    for MagnetPolarity in ('mu', 'md'):
        dataSamples[mc_type+'_'+MagnetPolarity] = VariousOptionsMC(name = mc_type+'_'+MagnetPolarity, MagnetPolarity = MagnetPolarity)



for MagnetPolarity in ('mu', 'md'):
    dataSamples['data2012_'+MagnetPolarity] = VariousOptions(
        name = 'data2012_'+MagnetPolarity, MagnetPolarity = MagnetPolarity, isMC=False, isPrescaled=False,
        CondDBtag=None, DDDBtag=None,
        input_file = 'inputFiles/data/LHCb_Collision12_Beam4000GeVVeloClosedMagDown_Real Data_Reco14_Stripping21_90000000_CHARM.MDST.py'.format(MagString[MagnetPolarity]),
        input_path = '/LHCb/Collision12/Beam4000GeV-VeloClosed-{}/Real Data/Reco14/Stripping21/90000000/CHARM.MDST'.format(MagString[MagnetPolarity]),
        )


# list of datasamples to be analized
toAnalize = []
# toAnalize += [dataSample for key, dataSample in dataSamples.items() if key[:-3] in MC_list]
toAnalize += [dataSamples['data2012_mu']]#, dataSamples['data2012_md'], dataSamples['data2011_mu'], dataSamples['data2011_md']]
# toAnalize = toAnalize[:]

# For test

dataSample = dataSamples['data2012_mu']


# General options
isGrid = True
isStoreInEOS = True
getDataSet = False# True 
nEvents = -1

#toAnalize = dataSamples.values()


 


############################################################

# Ganga options

if __name__ == '__main__':

    from subprocess import call
    import re

    def submitJob(dataSample):

        with open('dataSample.txt','w') as dsFile:
            dsFile.write(dataSample.name)

        filesPerJob = 5 if dataSample.isMC else 60

        # Get dataset
        if getDataSet:
            if dataSample.input_path:
                bk = BKQuery(dataSample.input_path)
            else:
                raise IOError('input_path not defined')
        else:
            str_LFNs = open(dataSample.input_file).read()
            fileList = re.findall(r'/lhcb/.*/000[0-9]{1}/.*mdst', str_LFNs)
            fileList = fileList[:200]
            

        # Configure job
        j = Job( application = DaVinci(version = 'v36r3p1') )
        j.application.optsfile += [File('Rootuplizer.py')]
        #j.inputdata = DaVinci().readInputData(dataSample.input_file)
        #j.application.optsfile += [File(dataSample.input_file)]
        #j.inputdata = j.application.readInputData(dataSample.input_file)
        j.inputsandbox += ['dataSample.txt']
        j.name = dataSample.name
        j.comment = dataSample.name
        if isGrid:
            j.backend = Dirac()
            isBulksubmit = False if '2012' in dataSample.name else True
            j.splitter = SplitByFiles(filesPerJob = filesPerJob, bulksubmit=isBulksubmit )
            #j.backend.settings['BannedSites']  = ['LCG.IN2P3.fr', 'LCG.GRIDKA.de', 'LCG.PIC.es']
            if getDataSet:
                print 'Getting dataSet '+bk.path
                j.inputdata = bk.getDataset()
            else:
                j.inputdata = LHCbDataset(['LFN:'+fl for fl in fileList])
            if isStoreInEOS:
                j.outputfiles += [MassStorageFile(dataSample.outputNtupleName)] #Like this it will ends up in my eos area $EOSHOME/ganga/<job#>/<subjob#>/
            else:
                j.outputfiles += [LocalFile(dataSample.outputNtupleName)]
                # rm = RootMerger()
                # rm.files = [dataSample.outputNtupleName]
                # rm.overwrite = True #False by default
                # rm.args = '-f2' #pass arguments to hadd
                # j.merger = rm
            j.do_auto_resubmit = True

        else:
            j.backend = Local()#Interactive()
            j.outputfiles += [LocalFile(dataSample.outputNtupleName)] #Like this it will ends up in my working-dir
            if getDataSet:
                print 'Getting dataSet '+bk.path
                ds = bk.getDataset()
                fileList = [f.name for f in ds.files]
            j.inputdata = LHCbDataset(['PFN:root://eoslhcb.cern.ch//eos/lhcb/grid/prod'+fl for fl in fileList])
            #j.outputfiles += [MassStorageFile(output_Ntuple)] #Like this it will ends up in my castor area $CASTORHOME/ganga/<job#>/<subjob#>/
        #return j
        j.submit()
        print 'submitted job: ', j.name
        call(['rm','dataSample.txt'])


    for dataSample in toAnalize[:]:
        submitJob(dataSample)

    # submitJob(dataSamples['data2012_md'])
        
        
    # #     #call(['ls', dataSample.input_file])
  
