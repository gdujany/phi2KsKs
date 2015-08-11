#!/usr/bin/env python

import sys, os
from CompareTreeVars import getHisto, CompareTreeVars
import ROOT as r
from ROOT import TTree
import numpy as np

r.gROOT.SetBatch(True)

# Get trees

eos_root = os.path.expanduser('~/eos/')
if not os.listdir(eos_root):
    raise OSError('EOS not mounted, please type:\n eosmount '+eos_root)

store_dir_g = os.path.join(eos_root, 'lhcb/user/g/gdujany/phi2KsKs/')
store_dir_s = '~/phi2KsKs/files/'

inFiles = {}
inFiles['data2012_Ds'] = r.TFile(os.path.join(store_dir_s, 'Ds_Phi2KsKs_2012.root'))
inFiles['data2012_incl'] = r.TFile(os.path.join(store_dir_g, '../phi2KsKs_noTrigger/data2012.root'))
inFiles['phi2KsKs_incl'] = r.TFile(os.path.join(store_dir_g, 'phi2KsKs_incl.root'))
inFiles['phi2KsKs_Ds'] = r.TFile(os.path.join(store_dir_s, 'Ds_Phi2KsKs_Ds_fulltrigger.root'))# 'Ds_Phi2KsKs_Ds.root'))
inFiles['minbias_incl'] = r.TFile(os.path.join(store_dir_s, 'Phi2KsKs_MBcomb.root'))
inFiles['minbias_Ds'] = r.TFile(os.path.join(store_dir_s, 'Ds_Phi2KsKs_MBcomb.root'))

trees = {}
treesMC = {}


xsec_incl = 3516
xsec_Ds = 388
BR_incl = .342
BR_Ds_Ds = .045
BR_Ds = BR_Ds_Ds*BR_incl
GenCut_incl = .025
GenCut_Ds = .070
PropKsKl_bp1 = 5.8515935540744706e-07
PropKsKl_bp2 = 8.1997422729700727e-10
PropKsKs_bp1 = 5.8509591199106381e-07
PropKsKs_bp2 = 8.103242056933593e-10



def format_e(n):
    a = '{:.2e}'.format(n)
    if(not '+00' in a.split('e')[1]):
        x = a.split('e')[1]
        if(x.startswith('+')):
            x = x.replace('x','')
        while(x.startswith('0')):
            x = x.replace('0','')
        while(x.startswith('-0')):
            x = x.replace('-0','-')
        return a.split('e')[0].rstrip('0').rstrip('.') + '\cdot 10^{' + x + '}'
    else:
        return a.split('e')[0].rstrip('0').rstrip('.')

def isint(b):
    if(b>2.):
        return int(round(b,0))
    else:
        return format_e(b)



effi_Reco_incl = [0.0,0.0] #[1bp,2bp]
effi_Reco_Ds = [0.0,0.0] #[1bp,2bp]

effi_L0_incl = [(0.0,0.0,0.0),(0.0,0.0,0.0)] #[(1bp,1bp_TIS,1bp_TOS),(2bp,2bp_TIS,2bp_TOS)]
effi_L0_Ds = [(0.0,0.0,0.0),(0.0,0.0,0.0)] #[(1bp,1bp_TIS,1bp_TOS),(2bp,2bp_TIS,2bp_TOS)]

effi_Hlt1_incl = [(0.0,0.0,0.0),(0.0,0.0,0.0)] #[(1bp,1bp_TIS,1bp_TOS),(2bp,2bp_TIS,2bp_TOS)]
effi_Hlt1_Ds = [(0.0,0.0,0.0),(0.0,0.0,0.0)] #[(1bp,1bp_TIS,1bp_TOS),(2bp,2bp_TIS,2bp_TOS)]

retention_incl = [0.0,0.0] #[1bp,2bp]
retention_Ds = [0.0,0.0] #[1bp,2bp]

exp_combbkg_incl = [0.0,0.0] #[1bp,2bp]
exp_combbkg_Ds = [0.0,0.0] #[1bp,2bp]
exp_SMbkg_incl = [0.0,0.0] #[1bp,2bp]
exp_SMbkg_Ds = [0.0,0.0] #[1bp,2bp]


for key, inFile in inFiles.items():
    # print('********************'+key+'********************')
    trees[key] = inFile.Get('TuplePhi2KsKs/DecayTree')
    if(key=='phi2KsKs_incl' and not 'data2012' in key):
        treesMC[key] = inFile.Get('MCTuplephi2KsKs/MCDecayTree')
    elif(not 'data2012' in key or not 'minbias' in key ):
        treesMC[key] = inFile.Get('MCTuplePhi2KsKs/MCDecayTree')

    #Figuring out the cuts

    names = [b.GetName() for b in trees[key].GetListOfBranches()]

    truthmatch = 'phi_BKGCAT==0'
    L0trigger = 'phi_L0Global_Dec'
    L0trigger_TIS = 'phi_L0Global_TIS'
    L0trigger_TOS = 'phi_L0Global_TOS'
    Hlt1trigger = '('
    Hlt1trigger_TIS = '('
    Hlt1trigger_TOS = '('

    for i in names:
        if('Hlt1' in i and not 'Global' in i and not 'Phys' in i and not 'Hlt1LumiDecision' in i):
            if '_Dec' in i:
                if Hlt1trigger == '(':
                    Hlt1trigger+=i
                else: 
                    Hlt1trigger += '||'+i
            elif '_TIS' in i:
                if Hlt1trigger_TIS == '(':
                    Hlt1trigger_TIS+=i
                else:
                    Hlt1trigger_TIS += '||'+i
            elif '_TOS' in i:
                if Hlt1trigger_TOS == '(':
                    Hlt1trigger_TOS+=i
                else:
                    Hlt1trigger_TOS += '||'+i
                    
                
    Hlt1trigger += ')'
    Hlt1trigger_TOS += ')'
    Hlt1trigger_TIS += ')'

    beampipe1 = '((sqrt(Ks1_ENDVERTEX_X*Ks1_ENDVERTEX_X+Ks1_ENDVERTEX_Y*Ks1_ENDVERTEX_Y)<7&&sqrt(Ks2_ENDVERTEX_X*Ks2_ENDVERTEX_X+Ks2_ENDVERTEX_Y*Ks2_ENDVERTEX_Y)>7)||(sqrt(Ks1_ENDVERTEX_X*Ks1_ENDVERTEX_X+Ks1_ENDVERTEX_Y*Ks1_ENDVERTEX_Y)>7&&sqrt(Ks2_ENDVERTEX_X*Ks2_ENDVERTEX_X+Ks2_ENDVERTEX_Y*Ks2_ENDVERTEX_Y)<7))'
    beampipe2 = '((sqrt(Ks1_ENDVERTEX_X*Ks1_ENDVERTEX_X+Ks1_ENDVERTEX_Y*Ks1_ENDVERTEX_Y)<7&&sqrt(Ks2_ENDVERTEX_X*Ks2_ENDVERTEX_X+Ks2_ENDVERTEX_Y*Ks2_ENDVERTEX_Y)<7))' 
    

    
    selection = ''
    selection +='phi_M>1010&&phi_M<1030' 
    if(not 'incl' in key):
        selection += ' && Ds_M > 1955 && Ds_M < 1985'
        selection += '&& phi_IPCHI2_OWNPV >=50'
        if('data' in key):
            print 'Selection: ', selection
    # print '*************************************************************************************************************'


    ###########################################################################################

    if('data2012' in key):
        if 'Ds' in key:
            exp_combbkg_Ds[0] = trees[key].GetEntries(selection+'&&'+beampipe1)/2.03
            exp_combbkg_Ds[1] = trees[key].GetEntries(selection+'&&'+beampipe2)/2.03
        if 'incl' in key:
            exp_combbkg_incl[0] = trees[key].GetEntries(selection+'&&'+beampipe1)*2.66
            exp_combbkg_incl[1] = trees[key].GetEntries(selection+'&&'+beampipe2)*2.66
    elif('minbias' in key):
        MC = 42122929.
        Reco = trees[key].GetEntries(selection)
        Reco1 = trees[key].GetEntries(selection+'&&'+beampipe1)
        Reco2 = trees[key].GetEntries(selection+'&&'+beampipe2)
        # RecoL0 = trees[key].GetEntries(selection+'&&'+L0trigger)
        #RecoL0Hlt1 = trees[key].GetEntries(selection+'&&'+L0trigger+'&&'+Hlt1trigger)
        RecoL0Hlt1BP1 = trees[key].GetEntries(selection+'&&'+L0trigger+'&&'+Hlt1trigger+'&&'+beampipe1)
        RecoL0Hlt1BP2 = trees[key].GetEntries(selection+'&&'+L0trigger+'&&'+Hlt1trigger+'&&'+beampipe2)
        if(Reco-Reco2 > 0):
            ret1 = float(RecoL0Hlt1BP1*Reco)/float(MC*(Reco-Reco2))
        else:
            ret1 = 0.0
        if(Reco-Reco1 > 0):
            ret2 = float(RecoL0Hlt1BP2*Reco)/float(MC*(Reco-Reco1))
        else:
            ret2 = 0.0
        if 'Ds' in key:
            retention_Ds = [ret1,ret2] #[1bp,2bp]
        if 'incl' in key:
            retention_incl = [ret1,ret2] #[1bp,2bp]
    elif('phi2KsKs' in key):
        if(key=='phi2KsKs_incl'):
            MC1 = treesMC[key].GetEntries('(sqrt(KS0_TRUEENDVERTEX_X*KS0_TRUEENDVERTEX_X+KS0_TRUEENDVERTEX_Y*KS0_TRUEENDVERTEX_Y)<7&&sqrt(KS00_TRUEENDVERTEX_X*KS00_TRUEENDVERTEX_X+KS00_TRUEENDVERTEX_Y*KS00_TRUEENDVERTEX_Y)>7)||(sqrt(KS0_TRUEENDVERTEX_X*KS0_TRUEENDVERTEX_X+KS0_TRUEENDVERTEX_Y*KS0_TRUEENDVERTEX_Y)>7&&sqrt(KS00_TRUEENDVERTEX_X*KS00_TRUEENDVERTEX_X+KS00_TRUEENDVERTEX_Y*KS00_TRUEENDVERTEX_Y)<7)')
            MC2 = treesMC[key].GetEntries('(sqrt(KS0_TRUEENDVERTEX_X*KS0_TRUEENDVERTEX_X+KS0_TRUEENDVERTEX_Y*KS0_TRUEENDVERTEX_Y)<7&&sqrt(KS00_TRUEENDVERTEX_X*KS00_TRUEENDVERTEX_X+KS00_TRUEENDVERTEX_Y*KS00_TRUEENDVERTEX_Y)<7)' )
        else:
            MC1 = treesMC[key].GetEntries('(sqrt(Ks1_TRUEENDVERTEX_X*Ks1_TRUEENDVERTEX_X+Ks1_TRUEENDVERTEX_Y*Ks1_TRUEENDVERTEX_Y)<7&&sqrt(Ks2_TRUEENDVERTEX_X*Ks2_TRUEENDVERTEX_X+Ks2_TRUEENDVERTEX_Y*Ks2_TRUEENDVERTEX_Y)>7)||(sqrt(Ks1_TRUEENDVERTEX_X*Ks1_TRUEENDVERTEX_X+Ks1_TRUEENDVERTEX_Y*Ks1_TRUEENDVERTEX_Y)>7&&sqrt(Ks2_TRUEENDVERTEX_X*Ks2_TRUEENDVERTEX_X+Ks2_TRUEENDVERTEX_Y*Ks2_TRUEENDVERTEX_Y)<7)')
            MC2 = treesMC[key].GetEntries('(sqrt(Ks1_TRUEENDVERTEX_X*Ks1_TRUEENDVERTEX_X+Ks1_TRUEENDVERTEX_Y*Ks1_TRUEENDVERTEX_Y)<7&&sqrt(Ks2_TRUEENDVERTEX_X*Ks2_TRUEENDVERTEX_X+Ks2_TRUEENDVERTEX_Y*Ks2_TRUEENDVERTEX_Y)<7)' )
        Reco1 = trees[key].GetEntries(selection+'&&'+truthmatch+'&&'+beampipe1)
        Reco2 = trees[key].GetEntries(selection+'&&'+truthmatch+'&&'+beampipe2)
        RecoL01 = trees[key].GetEntries(selection+'&&'+truthmatch+'&&'+L0trigger+'&&'+beampipe1)
        RecoL01_TIS = trees[key].GetEntries(selection+'&&'+truthmatch+'&&'+L0trigger_TIS+'&&'+beampipe1)
        RecoL01_TOS = trees[key].GetEntries(selection+'&&'+truthmatch+'&&'+L0trigger_TOS+'&&'+beampipe1)
        RecoL02 = trees[key].GetEntries(selection+'&&'+truthmatch+'&&'+L0trigger+'&&'+beampipe2)
        RecoL02_TIS = trees[key].GetEntries(selection+'&&'+truthmatch+'&&'+L0trigger_TIS+'&&'+beampipe2)
        RecoL02_TOS = trees[key].GetEntries(selection+'&&'+truthmatch+'&&'+L0trigger_TOS+'&&'+beampipe2)
        RecoL0Hlt11 = trees[key].GetEntries(selection+'&&'+truthmatch+'&&'+L0trigger+'&&'+Hlt1trigger+'&&'+beampipe1)
        RecoL0Hlt11_TIS = trees[key].GetEntries(selection+'&&'+truthmatch+'&&'+L0trigger+'&&'+Hlt1trigger_TIS+'&&'+beampipe1)
        RecoL0Hlt11_TOS = trees[key].GetEntries(selection+'&&'+truthmatch+'&&'+L0trigger+'&&'+Hlt1trigger_TOS+'&&'+beampipe1)
        RecoL0Hlt12 = trees[key].GetEntries(selection+'&&'+truthmatch+'&&'+L0trigger+'&&'+Hlt1trigger+'&&'+beampipe2)
        RecoL0Hlt12_TIS = trees[key].GetEntries(selection+'&&'+truthmatch+'&&'+L0trigger+'&&'+Hlt1trigger_TIS+'&&'+beampipe2)
        RecoL0Hlt12_TOS = trees[key].GetEntries(selection+'&&'+truthmatch+'&&'+L0trigger+'&&'+Hlt1trigger_TOS+'&&'+beampipe2)

        if('Ds' in key):
            effi_Reco_Ds = [float(Reco1)/float(MC1),float(Reco2)/float(MC2)] #[1bp,2bp]
            effi_L0_Ds = [(float(RecoL01)/float(Reco1),float(RecoL01_TIS)/float(RecoL01),float(RecoL01_TOS)/float(RecoL01)),(float(RecoL02)/float(Reco2),float(RecoL02_TIS)/float(RecoL02),float(RecoL02_TOS)/float(RecoL02))] #[(1bp,1bp_TIS,1bp_TOS),(2bp,2bp_TIS,2bp_TOS)]
            effi_Hlt1_Ds = [(float(RecoL0Hlt11)/float(RecoL01),float(RecoL0Hlt11_TIS)/float(RecoL0Hlt11),float(RecoL0Hlt11_TOS)/float(RecoL0Hlt11)),(float(RecoL0Hlt12)/float(RecoL02),float(RecoL0Hlt12_TIS)/float(RecoL0Hlt12),float(RecoL0Hlt12_TOS)/float(RecoL0Hlt12))] #[(1bp,1bp_TIS,1bp_TOS),(2bp,2bp_TIS,2bp_TOS)]
        elif('incl' in key):
            effi_Reco_incl = [float(Reco1)/float(MC1),float(Reco2)/float(MC2)] #[1bp,2bp]
            if(RecoL01 > 0 and RecoL02 > 0):
                effi_L0_incl = [(float(RecoL01)/float(Reco1),float(RecoL01_TIS)/float(RecoL01),float(RecoL01_TOS)/float(RecoL01)),(float(RecoL02)/float(Reco),float(RecoL02_TIS)/float(RecoL02),float(RecoL02_TOS)/float(RecoL02))] #[(1bp,1bp_TIS,1bp_TOS),(2bp,2bp_TIS,2bp_TOS)]
            elif(RecoL01 > 0):
                effi_L0_incl = [(float(RecoL01)/float(Reco1),0.0,0.0),(float(RecoL02)/float(Reco),float(RecoL02_TIS)/float(RecoL02),float(RecoL02_TOS)/float(RecoL02))] #[(1bp,1bp_TIS,1bp_TOS),(2bp,2bp_TIS,2bp_TOS)]
            elif(RecoL02 > 0):
                effi_L0_incl = [(float(RecoL01)/float(Reco1),float(RecoL01_TIS)/float(RecoL01),float(RecoL01_TOS)/float(RecoL01)),(float(RecoL02)/float(Reco),0.0,0.0)] #[(1bp,1bp_TIS,1bp_TOS),(2bp,2bp_TIS,2bp_TOS)]
            else:
                effi_L0_incl = [(0.0,0.0,0.0),(0.0,0.0,0.0)]
            effi_Hlt1_incl = [(0.0 if RecoL01 == 0 else float(RecoL0Hlt11)/float(RecoL01), 0.0 if RecoL0Hlt11 == 0 else float(RecoL0Hlt11_TIS)/float(RecoL0Hlt11), 0.0 if RecoL0Hlt11 == 0 else float(RecoL0Hlt11_TOS)/float(RecoL0Hlt11)),(0.0 if RecoL02 == 0 else float(RecoL0Hlt12)/float(RecoL02), 0.0 if RecoL0Hlt12 == 0 else float(RecoL0Hlt12_TIS)/float(RecoL0Hlt12), 0.0 if RecoL0Hlt12 == 0 else float(RecoL0Hlt12_TOS)/float(RecoL0Hlt12))] #[(1bp,1bp_TIS,1bp_TOS),(2bp,2bp_TIS,2bp_TOS)]
        






#output
##################################################################################


print '************************************************'



print '\\begin{tabular}{ccc}'
print '&Inclusive $\phi$ & $D_s \\rightarrow \phi \pi$ \\\\' 
print '\hline '
print 'Cross section (\SI{14}{TeV}), LHCb acceptance & \SI{',xsec_incl,'}{\micro\\barn} & \SI{',xsec_Ds,'}{\micro\\barn} \\\\' 
print 'Branching fractions &',BR_incl*100,'\% &',BR_Ds_Ds*100,' \% $\cdot$ ',BR_incl*100,'\% \\\\'
print 'Generator cut efficiency &',GenCut_incl*100,'\% &', GenCut_Ds*100 ,'\%\\\\'
print 'Propability of $K_sK_L \\rightarrow 4\pi$ with exactly 1 (2) decays in the beam pipe &\multicolumn{2}{c}{$',format_e(PropKsKl_bp1),'$($',format_e(PropKsKl_bp2),'$)} \\\\'
print '(Propability of $K_sK_s \\rightarrow 4\pi$ with exactly 1 (2) decays in the beam pipe &\multicolumn{2}{c}{17.6\%(2.8\%))} \\\\'
print 'Reconstruction \& selection efficiency & ',round(effi_Reco_incl[0]*100,1),'\%(',round(effi_Reco_incl[1]*100,1),'\%)  &',round(effi_Reco_Ds[0]*100,1),'\%(',round(effi_Reco_Ds[1]*100,1),'\%)\\\\'
print 'L0 efficiency& ',round(effi_L0_incl[0][0]*100,1),'\%(',round(effi_L0_incl[1][0]*100,1),'\%)& ',round(effi_L0_Ds[0][0]*100,1),'\%(',round(effi_L0_Ds[1][0]*100,1),'\%)\\\\'
print 'HLT1 efficiency& ',round(effi_Hlt1_incl[0][0]*100,1),'\%(',round(effi_Hlt1_incl[1][0]*100,1),'\%)&',round(effi_Hlt1_Ds[0][0]*100,1),'\%(',round(effi_Hlt1_Ds[1][0]*100,1),'\%)\\\\'
print '\hline'
print 'Total efficiency SM background &$',format_e(GenCut_incl*effi_Reco_incl[0]*effi_L0_incl[0][0]*effi_Hlt1_incl[0][0]),'$($',format_e(GenCut_incl*effi_Reco_incl[1]*effi_L0_incl[1][0]*effi_Hlt1_incl[1][0]),'$)&$',format_e(GenCut_Ds*effi_Reco_Ds[0]*effi_L0_Ds[0][0]*effi_Hlt1_Ds[0][0]),'$($',format_e(GenCut_Ds*effi_Reco_Ds[1]*effi_L0_Ds[1][0]*effi_Hlt1_Ds[1][0]),'$)\\\\'
print 'Expected events SM background / fb$^{-1}$ &$', isint(1e9*xsec_incl*BR_incl*GenCut_incl*PropKsKl_bp1*effi_Reco_incl[0]*effi_L0_incl[0][0]*effi_Hlt1_incl[0][0]) ,'$($', isint(1e9*xsec_incl*BR_incl*GenCut_incl*PropKsKl_bp2*effi_Reco_incl[1]*effi_L0_incl[1][0]*effi_Hlt1_incl[1][0]),'$)&$',isint(1e9*xsec_Ds*BR_Ds*GenCut_Ds*PropKsKl_bp1*effi_Reco_Ds[0]*effi_L0_Ds[0][0]*effi_Hlt1_Ds[0][0]),'$($',isint(1e9*xsec_Ds*BR_Ds*GenCut_Ds*PropKsKl_bp2*effi_Reco_Ds[1]*effi_L0_Ds[1][0]*effi_Hlt1_Ds[1][0]),'$)\\\\'
print 'Upper limit for signal (KLOE) &$', isint(1e9*xsec_incl*BR_incl*GenCut_incl*PropKsKs_bp1*effi_Reco_incl[0]*effi_L0_incl[0][0]*effi_Hlt1_incl[0][0]) ,'$($', isint(1e9*xsec_incl*BR_incl*GenCut_incl*PropKsKs_bp2*effi_Reco_incl[1]*effi_L0_incl[1][0]*effi_Hlt1_incl[1][0]),'$)&$',isint(1e9*xsec_Ds*BR_Ds*GenCut_Ds*PropKsKs_bp1*effi_Reco_Ds[0]*effi_L0_Ds[0][0]*effi_Hlt1_Ds[0][0]),'$($',isint(1e9*xsec_Ds*BR_Ds*GenCut_Ds*PropKsKs_bp2*effi_Reco_Ds[1]*effi_L0_Ds[1][0]*effi_Hlt1_Ds[1][0]),'$)\\\\'
print 'Total background retention & $',format_e(retention_incl[0]),'$($',format_e(retention_incl[1]),'$) &$', format_e(retention_Ds[0]),'$($',retention_Ds[1],'$)\\\\'
print 'Expected background ($\SI{1000}{MeV} < m_\phi < \SI{1040}{MeV}$) / fb$^{-1}$ &', int(round(exp_combbkg_incl[0],-1)) ,'(',int(round(exp_combbkg_incl[1],-1)),') & ',int(round(exp_combbkg_Ds[0],-1)),'(',int(round(exp_combbkg_Ds[1],-1)),')\\\\'
print '\end{tabular}' 





print '**************************************************************************'
print '\\begin{tabular}{c|c|c|c|c|c|c|c|c}'
print '& \multicolumn{4}{c|}{Inclusive $\phi$} & \multicolumn{4}{c}{$D_s\\rightarrow \phi\pi$} \\\\ '
print '& \multicolumn{2}{c|}{1 decay in beampipe} & \multicolumn{2}{c|}{2 decays in beampipe} & \multicolumn{2}{c|}{1 decay in beampipe} & \multicolumn{2}{c}{2 decays in beampipe}\\\\ '
print '& TIS & TOS & TIS & TOS & TIS & TOS & TIS & TOS\\\\' 
print '\hline '
print 'L0 efficiency & ',round(effi_L0_incl[0][1],2),' & ',round(effi_L0_incl[0][2],2),' & ',round(effi_L0_incl[1][1],2),' & ',round(effi_L0_incl[1][2],2),' & ',round(effi_L0_Ds[0][1],2),' & ',round(effi_L0_Ds[0][2],2),' & ',round(effi_L0_Ds[1][1],2),' & ',round(effi_L0_Ds[1][2],2),' \\\\ '
print 'HLT1 efficiency & ',round(effi_Hlt1_incl[0][1],2),' & ',round(effi_Hlt1_incl[0][2],2),' & ', round(effi_Hlt1_incl[1][1],2),' & ',round(effi_Hlt1_incl[1][2],2),' & ',round(effi_Hlt1_Ds[0][1],2),' & ',round(effi_Hlt1_Ds[0][2],2),' & ',round(effi_Hlt1_Ds[1][1],2),' & ',round(effi_Hlt1_Ds[1][2],2),' \\\\ '
print '\end{tabular}' 

