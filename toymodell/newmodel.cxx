#ifndef __CINT__
#include "RooGlobalFunc.h"
#endif
#include "RooWorkspace.h"
#include "RooAbsPdf.h"
#include "RooRealVar.h"
#include "RooDataSet.h"
#include "RooFormulaVar.h"
#include "RooArgSet.h"
#include "RooPlot.h"
#include "TH2.h"
#include "TFile.h"
#include "TTree.h"
#include "gROOT.h"
#include <iostream>


#include "RooStats/ProfileLikelihoodCalculator.h"
#include "RooStats/ModelConfig.h"


using namespace RooFit;
using namespace RooStats;


int newmodel(){

  double ratio = 8/19680;
  int eventsPerIfb = 4010;
  double lumiInfb = 23.;//3.;8.;23.;

  TString lumi ="";
  lumi += lumiInfb;
  std::cout << lumi << std::endl;

  RooWorkspace w("w",kTRUE);

  //w.writeToFile("myWorkspace.root");
  w.factory("GammaS[1.23097e+02]");
  w.factory("GammaL[1.95-2]");
  w.factory("BkgOffSet[1.51857e-02]");
  w.factory("DeltaM[5.289]");
  w.factory("zeta[0,1]");
  w.factory("Ks1_TAU[0.005,0.1]");
  w.factory("Ks2_TAU[0.005,0.1]");
  w.factory("EXPR::combi('exp(-GammaS*(Ks1_TAU+Ks2_TAU))+BkgOffSet',GammaS,Ks1_TAU,Ks2_TAU,BkgOffSet)");
  w.factory("EXPR::cpv('exp(-GammaS*Ks1_TAU-GammaL*Ks2_TAU)+exp(-GammaS*Ks2_TAU-GammaL*Ks1_TAU) + 2*cos(DeltaM*(Ks1_TAU-Ks2_TAU))*exp(-0.5*(Ks1_TAU+Ks2_TAU)*(GammaS+GammaL))',GammaS,GammaL,DeltaM,Ks1_TAU,Ks2_TAU)");
  w.factory("EXPR::cptv('exp(-GammaS*Ks1_TAU-GammaL*Ks2_TAU)+exp(-GammaS*Ks2_TAU-GammaL*Ks1_TAU) +(1-zeta)*2*cos(DeltaM*(Ks1_TAU-Ks2_TAU))*exp(-0.5*(Ks1_TAU+Ks2_TAU)*(GammaS+GammaL))',GammaS,GammaL,DeltaM,Ks1_TAU,Ks2_TAU,zeta)");
  // w.factory("SUM::mod(cpvfrac[1.287e-4]*cpv,combi)"); // had to directly enter the ratio
  // w.factory("SUM::sig(cpvfrac[1.287e-4]*cptv,combi)"); // had to directly enter the ratio
  w.factory("SUM::mod(cpvfrac[2e-4]*cpv,combi)"); // had to directly enter the ratio
  w.factory("SUM::sig(cpvfrac[2e-4]*cptv,combi)"); // had to directly enter the ratio
  w.factory("Ks1_PT[0,70000]");
  w.factory("Ks2_PT[0,70000]");
  w.factory("EXPR::mom1('Ks1_PT^b*exp(c*Ks1_PT)',Ks1_PT,b[2.19],c[-1.52e-3])");
  w.factory("EXPR::mom2('Ks2_PT^e*exp(f*Ks2_PT)',Ks2_PT,e[2.19],f[-1.52e-3])");
  w.factory("PROD::model(mod,mom1,mom2)");
  w.factory("PROD::comb(combi,mom1,mom2)");
  w.factory("PROD::signal(sig,mom1,mom2)");
  w.factory("DeltaTau[0,0.02]");
  
  RooFormulaVar CalcDeltaTau("DeltaTau","abs(@0-@1)",RooArgList(w::Ks1_TAU,w::Ks2_TAU,w::Ks1_PT,w::Ks2_PT));


  w.Print();
  

  w::Ks1_TAU.setBins(4*25);
  w::Ks2_TAU.setBins(4*25);

  std::cout << w::Ks1_TAU.getBins() << endl;

  // RooPlot* frame = w.var("Ks1_TAU")->frame();
  // w.pdf("model")->plotOn(frame);
  // frame->Draw();

  int sizeDataset = lumiInfb*eventsPerIfb;
  sizeDataset = 21*lumiInfb+42e4*lumiInfb;
  w.Print();
  RooDataSet * data2 = w::model.generate(RooArgSet(w::Ks1_TAU,w::Ks2_TAU,w::Ks1_PT,w::Ks2_PT),sizeDataset);
  w::model.fitTo(*data2);


  data2->Print();

  RooDataSet * data = data2->reduce(Cut("Ks1_TAU*Ks1_PT*299.792/497.614 < 7 || Ks2_TAU*Ks2_PT*299.792/497.614 < 7"));
  data->Print();

  // sizeDataset = sizeDataset-int(sizeDataset*1.287e-4);
  sizeDataset = 42e4*lumiInfb;

  std::cout << sizeDataset << std::endl;

  RooDataSet * combbkg2 = w::comb.generate(RooArgSet(w::Ks1_TAU,w::Ks2_TAU,w::Ks1_PT,w::Ks2_PT),sizeDataset);

  RooDataSet * combbkg = combbkg2->reduce(Cut("Ks1_TAU*Ks1_PT*299.792/497.614 < 7 || Ks2_TAU*Ks2_PT*299.792/497.614 < 7"));  



  // RooDataSet * data2 = data->reduce(Cut("Ks1_TAU*Ks1_PT*300/497.614 < 7 && Ks2_TAU*Ks2_PT*300/497.614 < 7"));

  // data2->Print();

  // TH2* hh_pdf2 = data->createHistogram(w::Ks1_TAU,w::Ks2_TAU);
  // TCanvas *canv2 = new TCanvas("model_canv","model_canv",0);
  // canv2->cd();
  // hh_pdf2->Draw("colz");
  // canv2->Print("model.pdf");


  RooFormulaVar CalcDeltaTau("DeltaTau","abs(@0-@1)",RooArgList(w::Ks1_TAU,w::Ks2_TAU));

  data->addColumn(CalcDeltaTau);
  combbkg->addColumn(CalcDeltaTau);
  data->Print();
  


  // TH2* hh_pdf3 = w::mod.createHistogram("Ks1_PT,Ks2_PT");
  // hh_pdf3->Draw("colz");

  // // TFile * data2012_f = new TFile("/afs/cern.ch/work/s/sbartkow/files/Ds_Phi2KsKs_Ds.root");
  // // TFile * data2012_f = new TFile("/afs/cern.ch/work/s/sbartkow/files/Ds_Phi2KsKs_2012.root");
  // // TFile * data2012_f = new TFile("/afs/cern.ch/work/s/sbartkow/files/Ds_Phi2KsKs_datasmall.root");
  // // TFile * data2012_f = new TFile("/afs/cern.ch/work/s/sbartkow/files/data2012.root");
  // TFile * data2012_f = new TFile("/afs/cern.ch/work/s/sbartkow/files/phi2KsKs_incl.root");
  
  

  // TTree * loaddata = (TTree*)data2012_f->Get("TuplePhi2KsKs/DecayTree");

  // TFile f2("temp.root","recreate");
  
  // TString str = "Ks1_TAU >= 0.000 && Ks2_TAU >= 0.000 && pi1_TRACK_Type ==3 && pi2_TRACK_Type ==3 && pi3_TRACK_Type ==3 && pi4_TRACK_Type ==3 && Ks1_TAU > 0.005 && Ks2_TAU > 0.005 && Ks1_TAU < 0.025 && Ks2_TAU < 0.025";//- cuts 
  // //&& sqrt(Ks1_ENDVERTEX_X^2 + Ks1_ENDVERTEX_Y^2) < 7 && sqrt(Ks2_ENDVERTEX_X^2 + Ks2_ENDVERTEX_Y^2) < 7
  // TTree *tree = loaddata->CopyTree(str);

  // RooDataSet ds("ds","ds",RooArgSet(w::Ks1_TAU,w::Ks2_TAU),Import(*tree)) ;
  // ds.addColumn(CalcDeltaTau);
  // ds.Print();
  // RooDataHist ds_hist = RooDataHist("ds_hist", "ds_hist", RooArgSet(w::Ks1_TAU,w::Ks2_TAU));


  // // RooPlot* frame = Ks1_TAU.frame();
  // // ds.plotOn(frame);
  // // frame->Draw();

  // // TH2* hh_pdf = ds.createHistogram("Ks1_TAU,Ks2_TAU");
  // // hh_pdf->Write();
  // // TCanvas *canv = new TCanvas("data_canv","data_canv",0);
  // // canv->cd();
  // // hh_pdf->Draw("colz");
  // // canv->Print("data.pdf");
  
  // w::Ks1_TAU.setConstant(kTRUE);
  // w::Ks2_TAU.setConstant(kTRUE);
  // w::model.fitTo(ds);

  TCanvas *canv3 = new TCanvas("proj_canv","proj_canv",0);
  canv3->cd();
  RooPlot* dtFrame = w::DeltaTau.frame(Title("Simulation #int L dt = "+lumi+"fb^{-1}"));
  //dtFrame->SetLineStyle(0);
  data->plotOn(dtFrame,DataError(RooAbsData::None));
  combbkg->plotOn(dtFrame,MarkerColor(kBlue),LineColor(kBlue));//,DataError(RooAbsData::None)) ;
  
  dtFrame->Draw() ;
  canv3->Print("DeltaTau.pdf");

  ModelConfig modelConfig(&w);
  modelConfig.Print();
  modelConfig.SetPdf(w::signal);
  modelConfig.SetParametersOfInterest(w::zeta);
  modelConfig.SetNuisanceParameters(RooArgSet(w::cpvfrac,w::BkgOffSet,w::GammaS));
  modelConfig.SetObservables(RooArgSet(w::Ks1_TAU,w::Ks2_TAU));
  // modelConfig.SetGlobalObservables( RooArgSet(*gSigEff,*gSigBkg));
  modelConfig.SetName("ModelConfig");
  w.import(modelConfig);


  std::cout << "Likelihood" << std::endl;

  ProfileLikelihoodCalculator plc(*data, modelConfig);
  plc.SetTestSize(.05);
  ConfInterval* lrint = plc.GetInterval();

  std::cout << "Profile lower limit on zeta = " << ((LikelihoodInterval*) lrint)->LowerLimit(w::zeta) << std::endl;
  std::cout << "Profile upper limit on zeta = " << ((LikelihoodInterval*) lrint)->UpperLimit(w::zeta) << std::endl;


  

  return 0;

}