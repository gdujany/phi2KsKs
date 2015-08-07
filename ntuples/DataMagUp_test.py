#-- GAUDI jobOptions generated on Fri Aug  7 12:00:35 2015
#-- Contains event types : 
#--   90000000 - 1 files - 59699 events - 3.99 GBytes


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
IOHelper('ROOT').inputFiles(['LFN:/lhcb/LHCb/Collision12/CHARMCOMPLETEEVENT.DST/00041834/0000/00041834_00000527_1.charmcompleteevent.dst'
], clear=True)
FileCatalog().Catalogs += [ 'xmlcatalog_file:DataMagUp_test.xml' ]
