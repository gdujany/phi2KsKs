#-- GAUDI jobOptions generated on Mon Jul 13 17:31:04 2015
#-- Contains event types : 
#--   90000000 - 20 files - 3437856 events - 27.62 GBytes


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
IOHelper('ROOT').inputFiles(['LFN:/lhcb/LHCb/Collision12/CHARM.MDST/00041834/0000/00041834_00000004_1.charm.mdst',
'LFN:/lhcb/LHCb/Collision12/CHARM.MDST/00041834/0000/00041834_00000018_1.charm.mdst',
'LFN:/lhcb/LHCb/Collision12/CHARM.MDST/00041834/0000/00041834_00000032_1.charm.mdst',
'LFN:/lhcb/LHCb/Collision12/CHARM.MDST/00041834/0000/00041834_00000046_1.charm.mdst',
'LFN:/lhcb/LHCb/Collision12/CHARM.MDST/00041834/0000/00041834_00000060_1.charm.mdst',
'LFN:/lhcb/LHCb/Collision12/CHARM.MDST/00041834/0000/00041834_00000092_1.charm.mdst',
'LFN:/lhcb/LHCb/Collision12/CHARM.MDST/00041834/0000/00041834_00000106_1.charm.mdst',
'LFN:/lhcb/LHCb/Collision12/CHARM.MDST/00041834/0000/00041834_00000123_1.charm.mdst',
'LFN:/lhcb/LHCb/Collision12/CHARM.MDST/00041834/0000/00041834_00000152_1.charm.mdst',
'LFN:/lhcb/LHCb/Collision12/CHARM.MDST/00041834/0000/00041834_00000176_1.charm.mdst',
'LFN:/lhcb/LHCb/Collision12/CHARM.MDST/00041834/0000/00041834_00000202_1.charm.mdst',
'LFN:/lhcb/LHCb/Collision12/CHARM.MDST/00041834/0000/00041834_00000219_1.charm.mdst',
'LFN:/lhcb/LHCb/Collision12/CHARM.MDST/00041834/0000/00041834_00000252_1.charm.mdst',
'LFN:/lhcb/LHCb/Collision12/CHARM.MDST/00041834/0000/00041834_00000261_1.charm.mdst',
'LFN:/lhcb/LHCb/Collision12/CHARM.MDST/00041834/0000/00041834_00000268_1.charm.mdst',
'LFN:/lhcb/LHCb/Collision12/CHARM.MDST/00041834/0000/00041834_00000269_1.charm.mdst',
'LFN:/lhcb/LHCb/Collision12/CHARM.MDST/00041834/0000/00041834_00000274_1.charm.mdst',
'LFN:/lhcb/LHCb/Collision12/CHARM.MDST/00041834/0000/00041834_00000279_1.charm.mdst',
'LFN:/lhcb/LHCb/Collision12/CHARM.MDST/00041834/0000/00041834_00000296_1.charm.mdst',
'LFN:/lhcb/LHCb/Collision12/CHARM.MDST/00041834/0000/00041834_00000322_1.charm.mdst'
], clear=True)
FileCatalog().Catalogs += [ 'xmlcatalog_file:data_magup20.xml' ]
