#-- GAUDI jobOptions generated on Tue Aug 18 15:56:07 2015
#-- Contains event types : 
#--   90000000 - 16 files - 7836648 events - 62.61 GBytes


#--  Extra information about the data processing phases:


#--  Processing Pass Step-127012 

#--  StepId : 127012 
#--  StepName : Stripping21-Merging-DV-v36r1 
#--  ApplicationName : DaVinci 
#--  ApplicationVersion : v36r1 
#--  OptionFiles : $APPCONFIGOPTS/Merging/DV-Stripping-Merging.py 
#--  DDDB : dddb-20130929-1 
#--  CONDDB : cond-20141107 
#--  ExtraPackages : AppConfig.v3r203;SQLDDDB.v7r10 
#--  Visible : N 

from Gaudi.Configuration import * 
from GaudiConf import IOHelper
IOHelper('ROOT').inputFiles(['LFN:/lhcb/LHCb/Collision12/CHARM.MDST/00041834/0000/00041834_00000123_1.charm.mdst',
'LFN:/lhcb/LHCb/Collision12/CHARM.MDST/00041834/0000/00041834_00000252_1.charm.mdst',
'LFN:/lhcb/LHCb/Collision12/CHARM.MDST/00041834/0000/00041834_00000261_1.charm.mdst',
'LFN:/lhcb/LHCb/Collision12/CHARM.MDST/00041834/0000/00041834_00000268_1.charm.mdst',
'LFN:/lhcb/LHCb/Collision12/CHARM.MDST/00041834/0000/00041834_00000269_1.charm.mdst',
'LFN:/lhcb/LHCb/Collision12/CHARM.MDST/00041834/0000/00041834_00000274_1.charm.mdst',
'LFN:/lhcb/LHCb/Collision12/CHARM.MDST/00041834/0000/00041834_00000368_1.charm.mdst',
'LFN:/lhcb/LHCb/Collision12/CHARM.MDST/00041834/0000/00041834_00000370_1.charm.mdst',
'LFN:/lhcb/LHCb/Collision12/CHARM.MDST/00041834/0000/00041834_00000476_1.charm.mdst',
'LFN:/lhcb/LHCb/Collision12/CHARM.MDST/00041834/0000/00041834_00000482_1.charm.mdst',
'LFN:/lhcb/LHCb/Collision12/CHARM.MDST/00041834/0000/00041834_00000516_1.charm.mdst',
'LFN:/lhcb/LHCb/Collision12/CHARM.MDST/00041834/0000/00041834_00000533_1.charm.mdst',
'LFN:/lhcb/LHCb/Collision12/CHARM.MDST/00041834/0000/00041834_00000564_1.charm.mdst',
'LFN:/lhcb/LHCb/Collision12/CHARM.MDST/00041834/0000/00041834_00000579_1.charm.mdst',
'LFN:/lhcb/LHCb/Collision12/CHARM.MDST/00041834/0000/00041834_00000607_1.charm.mdst',
'LFN:/lhcb/LHCb/Collision12/CHARM.MDST/00041834/0000/00041834_00000616_1.charm.mdst'
], clear=True)
FileCatalog().Catalogs += [ 'xmlcatalog_file:charm_test_magup2.xml' ]
