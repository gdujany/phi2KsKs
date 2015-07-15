 ############################################################
##  JOB OPTIONS ##
#
# works with ganga v600r19 (later versions can have troubles with splitting data because too many files)

# Class container with various options

decNumbers = dict(
    inclb = 10000000,
    minbias = 30000000,
    minbias2 = 30000000,
    )

simVersion = dict(
    inclb = 'Sim08a',
    minbias = 'Sim08a',
    minbias2 = 'Sim08c',
    )

MagString = dict(mu = 'MagUp', md = 'MagDown')
    

class VariousOptions:
    def __init__(self, name, MagnetPolarity='mu', CondDBtag=None, DDDBtag=None, input_file=None, input_path=None, isMC=True, isPrescaled=False, outputNtupleName=None,dataType='2012'):
        self.name = name
        self.MagnetPolarity = MagnetPolarity
        self.DDDBtag = DDDBtag
        self.CondDBtag = CondDBtag if CondDBtag else ('sim-20121025-vc-'+MagnetPolarity+'100' if isMC else 'cond-20121016')
        self.input_file = input_file
        self.input_path = input_path
        self.outputNtupleName = name+'.root' if not outputNtupleName else outputNtupleName
        self.isPrescaled = isPrescaled
        self.isMC = isMC
        self.dataType = dataType


class VariousOptionsMC(VariousOptions):
    def __init__(self, input_file=None,**argd):
        """
        MagnetPolarity in ('mu', 'md')
        """
        VariousOptions.__init__(self, input_file=input_file, isMC=True, isPrescaled=False, **argd)
        self.decNumber = decNumbers.get(self.name[:-3], 0)
        if not self.input_file:
            self.input_file = 'inputFiles/MC/MC_{dataType}_{decNumber}_Beam4000GeV{dataType}{MagStr}Nu2.5Pythia8_{SimVer}_Digi13_Trig0x409f0045_Reco14a_Stripping20NoPrescalingFlagged_ALLSTREAMS.DST.py'.format(MagStr=MagString[self.MagnetPolarity],SimVer=simVersion[self.name[:-3]],**self.__dict__)

           
############################################################
# Options for various datasets
dataSamples = {}

MC_list = [
    # 'inclb',
    'minbias',
    ]

for mc_type in MC_list:
    for MagnetPolarity in ('mu', 'md'):
        dataSamples[mc_type+'_'+MagnetPolarity] = VariousOptionsMC(name = mc_type+'_'+MagnetPolarity, MagnetPolarity = MagnetPolarity, DDDBtag='Sim08-20130503-1',CondDBtag='Sim08-20130503-1-vc-md100')



for MagnetPolarity in ('mu', 'md'):
    dataSamples['data2012_'+MagnetPolarity] = VariousOptions(
        name = 'data2012_'+MagnetPolarity, MagnetPolarity = MagnetPolarity, isMC=False, isPrescaled=0.2,
        input_file = 'inputFiles/data/LHCb_Collision12_Beam4000GeVVeloClosedMagDown_Real Data_Reco14_Stripping21_90000000_CHARM.MDST.py'.format(MagString[MagnetPolarity]),
        input_path = '/LHCb/Collision12/Beam4000GeV-VeloClosed-{}/Real Data/Reco14/Stripping21/90000000/CHARM.MDST'.format(MagString[MagnetPolarity]),
        )

    
dataSamples['phi2KsKs_incl'] = VariousOptionsMC(
        name = 'phi2KsKs_incl', MagnetPolarity = 'mu',
        CondDBtag="sim-20130222-1-vc-md100", DDDBtag="dddb-20130312-1",
        input_file = 'inputFiles/MC/brunel_LFNs_inclusive.py',
        )

dataSamples['phi2KsKs_Ds'] = VariousOptionsMC(
        name = 'phi2KsKs_Ds', MagnetPolarity = 'mu',
        CondDBtag="sim-20130222-1-vc-md100", DDDBtag="dddb-20130312-1",
        input_file = 'inputFiles/MC/brunel_LFNs_Ds.py',
        )

for MagnetPolarity in ('mu', 'md'):
    dataSamples['minbias2_'+MagnetPolarity] = VariousOptionsMC(
        name = 'minbias2_'+MagnetPolarity, MagnetPolarity = MagnetPolarity,
        DDDBtag='dddb-20120831',CondDBtag='sim-20121025-vc-{0}100'.format(MagnetPolarity),
        input_file = 'inputFiles/MC/MC_2012_30000000_Beam4000GeV2012{0}Nu2.5Pythia8_Sim08c_Digi13_Trig0x409f0045_Reco14a_Stripping20NoPrescalingFlagged_ALLSTREAMS.DST.py'.format(MagString[MagnetPolarity]),
        )


for MagnetPolarity in ('mu', 'md'):
    dataSamples['minbias3_'+MagnetPolarity] = VariousOptionsMC(
        name = 'minbias3_'+MagnetPolarity, MagnetPolarity = MagnetPolarity,
        DDDBtag='dddb-20130929-1',CondDBtag='sim-20130522-1-vc-{0}10'.format(MagnetPolarity),
        input_file = 'inputFiles/MC/MC_2012_30000030_Beam4000GeVMayJune2012{0}Nu2.5EmNoCuts_Sim06b_Trig0x4097003dFlagged_Reco14_Stripping20NoPrescalingFlagged_ALLSTREAMS.DST.py'.format(MagString[MagnetPolarity]),
        )



# list of datasamples to be analized
# toAnalize = []
# toAnalize += [dataSamples['phi2KsKs_incl'], dataSamples['phi2KsKs_Ds']]
# toAnalize += [i for i in dataSamples.values() if 'minbias' in i.name]
# #toAnalize += [dataSample for key, dataSample in dataSamples.items() if key[:-3] in MC_list]
# toAnalize += [dataSamples['data2012_mu'], dataSamples['data2012_md']]#, dataSamples['data2011_mu'], dataSamples['data2011_md']]

toAnalize = [dataSamples['minbias2_mu'], dataSamples['minbias2_md'], dataSamples['minbias3_mu'], dataSamples['minbias3_md']]

# toAnalize = toAnalize[:]

# toAnalize = [dataSamples['minbias_mu'], dataSamples['minbias_md']]

# For test

# dataSample = dataSamples['data2012_mu']
#dataSample = dataSamples['minbias_md']
dataSample = dataSamples['phi2KsKs_incl']


# General options
isGrid = True
isStoreInEOS = True
getDataSet = False# True 
nEvents = 5000 # will be overwritten to -1 during grid submissions

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
            fileList = re.findall(r'/lhcb/.*?/.*?/.*dst', str_LFNs)
            # fileList = fileList[:200]
            

        # Configure job
        j = Job( application = DaVinci(version = 'v36r3p1') )
        j.application.optsfile += [File('Rootuplizer.py')]
        #j.inputdata = DaVinci().readInputData(dataSample.input_file)
        #j.application.optsfile += [File(dataSample.input_file)]
        #j.inputdata = j.application.readInputData(dataSample.input_file)
        j.inputfiles += ['dataSample.txt']
        j.name = dataSample.name
        j.comment = dataSample.name
        if isGrid:
            j.backend = Dirac()
            j.application.extraopts = '''DaVinci().EvtMax = {0}'''.format(-1)
            isBulksubmit = False if '2012' in dataSample.name else True
            j.splitter = SplitByFiles(filesPerJob = filesPerJob, bulksubmit=isBulksubmit )
            #j.backend.settings['BannedSites']  = ['LCG.IN2P3.fr', 'LCG.GRIDKA.de', 'LCG.PIC.es']
            if getDataSet:
                print 'Getting dataSet '+bk.path
                j.inputdata = bk.getDataset()
            else:
                j.inputdata = LHCbDataset(['LFN:'+fl for fl in fileList])
            if isStoreInEOS:
                j.outputfiles += [MassStorageFile(dataSample.outputNtupleName)] # Like this it will ends up in my eos area $EOSHOME/ganga/<job#>/<subjob#>/
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
            j.outputfiles += [LocalFile(dataSample.outputNtupleName)] # Like this it will ends up in my working-dir
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
  
