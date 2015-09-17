#ifndef __CINT__
#include "RooGlobalFunc.h"
#endif
#include "RooWorkspace.h"
#include "RooAbsPdf.h"
#include "RooRealVar.h"
#include "RooDataSet.h"
#include "RooArgSet.h"
#include "RooPlot.h"
#include "TH2.h"
#include "TFile.h"
#include "TTree.h"
#include <iostream>

using namespace RooFit;

int start(){



  ////////////////////////////////////////////////
    // Use times new roman, precision 2 
  Int_t lhcbFont        = 132;  // Old LHCb style: 62;
  // Line thickness
  Double_t lhcbWidth    = 2.00; // Old LHCb style: 3.00;
  // Text size
  Double_t lhcbTSize    = 0.06; 
  
  // use plain black on white colors
  gROOT->SetStyle("Plain"); 
  TStyle *lhcbStyle= new TStyle("lhcbStyle","LHCb plots style");
  
  //lhcbStyle->SetErrorX(0); //  don't suppress the error bar along X

  lhcbStyle->SetFillColor(1);
  lhcbStyle->SetFillStyle(1001);   // solid
  lhcbStyle->SetFrameFillColor(0);
  lhcbStyle->SetFrameBorderMode(0);
  lhcbStyle->SetPadBorderMode(0);
  lhcbStyle->SetPadColor(0);
  lhcbStyle->SetCanvasBorderMode(0);
  lhcbStyle->SetCanvasColor(0);
  lhcbStyle->SetStatColor(0);
  lhcbStyle->SetLegendBorderSize(0);
  lhcbStyle->SetLegendFont(132);

  // If you want the usual gradient palette (blue -> red)
  lhcbStyle->SetPalette(1);
  // // If you want colors that correspond to gray scale in black and white:
  // int colors[8] = {0,5,7,3,6,2,4,1};
  // lhcbStyle->SetPalette(8,colors);

  // set the paper & margin sizes
  lhcbStyle->SetPaperSize(20,26);
  lhcbStyle->SetPadTopMargin(0.09);
  lhcbStyle->SetPadRightMargin(0.05); // increase for colz plots
  lhcbStyle->SetPadBottomMargin(0.15);
  lhcbStyle->SetPadLeftMargin(0.17);
  
  // use large fonts
  lhcbStyle->SetTextFont(lhcbFont);
  lhcbStyle->SetTextSize(lhcbTSize);
  lhcbStyle->SetLabelFont(lhcbFont,"x");
  lhcbStyle->SetLabelFont(lhcbFont,"y");
  lhcbStyle->SetLabelFont(lhcbFont,"z");
  lhcbStyle->SetLabelSize(0.05,"x");
  lhcbStyle->SetLabelSize(0.05,"y");
  lhcbStyle->SetLabelSize(0.05,"z");
  lhcbStyle->SetTitleFont(lhcbFont);
  lhcbStyle->SetTitleFont(lhcbFont,"x");
  lhcbStyle->SetTitleFont(lhcbFont,"y");
  lhcbStyle->SetTitleFont(lhcbFont,"z");
  lhcbStyle->SetTitleSize(0.05,"x");
  lhcbStyle->SetTitleSize(0.05,"y");
  lhcbStyle->SetTitleSize(0.05,"z");


  // use medium bold lines and thick markers
  lhcbStyle->SetLineWidth(lhcbWidth);
  lhcbStyle->SetFrameLineWidth(lhcbWidth);
  lhcbStyle->SetHistLineWidth(lhcbWidth);
  lhcbStyle->SetFuncWidth(lhcbWidth);
  lhcbStyle->SetGridWidth(lhcbWidth);
  lhcbStyle->SetLineStyleString(2,"[12 12]"); // postscript dashes
  lhcbStyle->SetMarkerStyle(20);
  lhcbStyle->SetMarkerSize(1.0);

  // label offsets
  lhcbStyle->SetLabelOffset(0.01,"x");
  lhcbStyle->SetLabelOffset(0.01,"y");

  // by default, do not display histogram decorations:
  lhcbStyle->SetOptStat(0);  
  //lhcbStyle->SetOptStat("emr");  // show only nent -e , mean - m , rms -r
  // full opts at http://root.cern.ch/root/html/TStyle.html#TStyle:SetOptStat
  lhcbStyle->SetStatFormat("6.3g"); // specified as c printf options
  lhcbStyle->SetOptTitle(1);
  lhcbStyle->SetOptFit(0);
  //lhcbStyle->SetOptFit(1011); // order is probability, Chi2, errors, parameters
  //titles
  lhcbStyle->SetTitleOffset(1.5,"X")
  lhcbStyle->SetTitleOffset(1.5,"Y")
  lhcbStyle->SetTitleOffset(1.2,"Z");
  lhcbStyle->SetTitleFillColor(0);
  lhcbStyle->SetTitleStyle(0);
  lhcbStyle->SetTitleBorderSize(0);
  lhcbStyle->SetTitleFont(lhcbFont,"title");
  lhcbStyle->SetTitleX(0.0);
  lhcbStyle->SetTitleY(1.0); 
  lhcbStyle->SetTitleW(1.0);
  lhcbStyle->SetTitleH(0.08);
  
  // look of the statistics box:
  lhcbStyle->SetStatBorderSize(0);
  lhcbStyle->SetStatFont(lhcbFont);
  lhcbStyle->SetStatFontSize(0.05);
  lhcbStyle->SetStatX(0.9);
  lhcbStyle->SetStatY(0.9);
  lhcbStyle->SetStatW(0.25);
  lhcbStyle->SetStatH(0.15);

  // put tick marks on top and RHS of plots
  lhcbStyle->SetPadTickX(1);
  lhcbStyle->SetPadTickY(1);

  // histogram divisions: only 5 in x to avoid label overlaps
  lhcbStyle->SetNdivisions(505,"x");
  lhcbStyle->SetNdivisions(510,"y");
  
  gROOT->SetStyle("lhcbStyle");
  gROOT->ForceStyle();
  //////////////////////////////////////////////////////////

  //lhcbStyle();
  double ratio = 3.51e-2/2.912e4;
  int eventsPerIfb = 29120;
  double lumiInfb = 100.;//3.;
  gStyle->SetOptStat(0);
  gStyle->SetPadRightMargin(0.12);

  RooWorkspace w("w",kTRUE);

  //w.writeToFile("myWorkspace.root");
  w.factory("GammaS[9.61911e+01,0,10000]");//8.57924e+01
  w.factory("GammaL[1.955e-5]");
  w.factory("DeltaM[0.5289e-2]");
  w.factory("Ks1_TAU[0.005,0.1]");
  w.factory("Ks2_TAU[0.005,0.1]");
  w.factory("EXPR::comb('exp(-GammaS*(Ks1_TAU+Ks2_TAU))',GammaS,Ks1_TAU,Ks2_TAU)");
  w.factory("EXPR::cpv('exp(-GammaS*Ks1_TAU-GammaL*Ks2_TAU)+exp(-GammaS*Ks2_TAU-GammaL*Ks1_TAU) + 2*cos(DeltaM*(Ks1_TAU-Ks2_TAU))*exp(-0.5*(Ks1_TAU+Ks2_TAU)*(GammaS+GammaL))',GammaS,GammaL,DeltaM,Ks1_TAU,Ks2_TAU)");
  w.factory("SUM::model(cpvfrac[1.20536e-06]*cpv,comb)"); // had to directly enter the ratio
  // w.factory("EXPR::mom1a('(2*Ks1_PTa)^b*exp(2*c*Ks1_PTa)',Ks1_PTa[0,1.6015e3],b[2.19],c[-1.52e-3])");
  // w.factory("EXPR::mom1b('Ks1_PTb^b*exp(c*Ks1_PTb)',Ks1_PTb[1.6015e3,70000],b[2.19],c[-1.52e-3])");
  // w.factory("SUM::mom1(mom1a,m1frac[.4]*mom1b)");
  // w.factory("EXPR::mom2a('(2*Ks2_PTa)^b*exp(2*c*Ks2_PTa)',Ks2_PTa[0,1.6015e3],b[2.19],c[-1.52e-3])");
  // w.factory("EXPR::mom2b('Ks2_PTb^d*exp(e*Ks2_PTb)',Ks2_PTb[1.6015e3,70000],d[2.19],e[-1.52e-3])");
  // w.factory("SUM::mom2(mom2a,m2frac[.4]*mom2b)");
  w.factory("Ks1_PT[0,70000]");
  w.factory("Ks2_PT[0,70000]");
  w.factory("EXPR::mom1('Ks1_PT^b*exp(c*Ks1_PT)',Ks1_PT,b[1.52],c[-2.19e-3])");
  w.factory("EXPR::mom2('Ks2_PT^e*exp(f*Ks2_PT)',Ks2_PT,e[1.52],f[-2.19e-3])");
  w.factory("PROD::mod(model,mom1,mom2)");
  w::GammaS.Print();

  w.Print();

  w::Ks1_TAU.setBins(4*25);
  w::Ks2_TAU.setBins(4*25);

  std::cout << w::Ks1_TAU.getBins() << endl;

  // RooPlot* frame = w.var("Ks1_TAU")->frame();
  // w.pdf("model")->plotOn(frame);
  // frame->Draw();

  int sizeDataset = lumiInfb*eventsPerIfb;
  sizeDataset = 130000;

  // RooDataSet * data = w::mod.generate(RooArgSet(w::Ks1_TAU,w::Ks2_TAU,w::Ks1_PTa,w::Ks1_PTb,w::Ks2_PTa,w::Ks2_PTb),sizeDataset);
  RooDataSet * data = w::mod.generate(RooArgSet(w::Ks1_TAU,w::Ks2_TAU,w::Ks1_PT,w::Ks2_PT),sizeDataset);

  // w::model.fitTo(*data);

  data->Print();

  // RooDataSet * data2 = data->reduce(Cut("(Ks1_TAU*Ks1_PT*299.792/497.614 < 30 && Ks1_TAU*Ks1_PTb*299.792/497.614 < 40) || (Ks2_TAU*Ks2_PTa*299.792/497.614 < 30&& Ks2_TAU*Ks2_PTb*299.792/497.614 < 40)"));
  RooDataSet * data2 = data->reduce(Cut("(Ks1_TAU*Ks1_PT*299.792/497.614 < 7) || (Ks2_TAU*Ks2_PT*299.792/497.614 < 7)"));

  data2->Print();

  TH2* hh_pdf2 = data2->createHistogram(w::Ks1_TAU,w::Ks2_TAU);
  TCanvas *canv2 = new TCanvas("model_canv","model_canv",2);
  canv2->cd();
  hh_pdf2->GetXaxis()->SetTitle("t_{1}");
  hh_pdf2->GetYaxis()->SetTitle("t_{2}");
  hh_pdf2->GetYaxis()->SetTitleOffset(1.6);
  hh_pdf2->GetXaxis()->SetTitleOffset(1.1);
  hh_pdf2->SetTitle("Model");
  hh_pdf2->Draw("colz");

  TPaveText* lhcbName = new TPaveText(gStyle->GetPadLeftMargin() + 0.30,
                                      0.87 - gStyle->GetPadTopMargin(),
                                      gStyle->GetPadLeftMargin() + 0.65,
                                      0.95 - gStyle->GetPadTopMargin(),
                                      "BRNDC");
  lhcbName->AddText("LHCb Unofficial");
  lhcbName->SetFillColor(0);
  lhcbName->SetTextAlign(12);
  lhcbName->SetBorderSize(0);
  lhcbName->Draw();

  canv2->Print("model.pdf");

  


  // TH2* hh_pdf3 = w::mod.createHistogram("Ks1_PT,Ks2_PT");
  // hh_pdf3->Draw("colz");

  // TFile * data2012_f = new TFile("/afs/cern.ch/work/s/sbartkow/files/Ds_Phi2KsKs_Ds.root");
  // TFile * data2012_f = new TFile("/afs/cern.ch/work/s/sbartkow/files/Ds_Phi2KsKs_2012.root");
  // TFile * data2012_f = new TFile("/afs/cern.ch/work/s/sbartkow/files/Ds_Phi2KsKs_datasmall.root");
  TFile * data2012_f = new TFile("/afs/cern.ch/work/s/sbartkow/files/data2012.root");
  

  TTree * loaddata = (TTree*)data2012_f->Get("TuplePhi2KsKs/DecayTree");

  TFile f2("temp.root","recreate");
  
  TString str = "Ks1_TAU >= 0.000 && Ks2_TAU >= 0.000 && pi1_TRACK_Type ==3 && pi2_TRACK_Type ==3 && pi3_TRACK_Type ==3 && pi4_TRACK_Type ==3 && (sqrt(Ks1_ENDVERTEX_X^2 + Ks1_ENDVERTEX_Y^2) < 7 || sqrt(Ks2_ENDVERTEX_X^2 + Ks2_ENDVERTEX_Y^2) < 7)";
  TTree *tree = loaddata->CopyTree(str);

  RooDataSet ds("ds","ds",RooArgSet(w::Ks1_TAU,w::Ks2_TAU),Import(*tree)) ;
  ds.Print();
  RooDataHist ds_hist = RooDataHist("ds_hist", "ds_hist", RooArgSet(w::Ks1_TAU,w::Ks2_TAU));


  // RooPlot* frame = w::Ks1_TAU.frame();
  // ds.plotOn(frame);
  // frame->Draw();

  TH2* hh_pdf = ds.createHistogram("Ks1_TAU,Ks2_TAU");
  hh_pdf->Write();
  hh_pdf->SetTitle("2012 Data");
  TCanvas *canv = new TCanvas("data_canv","data_canv",2);
  canv->cd();
  hh_pdf->GetXaxis()->SetTitle("t_{1}");
  hh_pdf->GetYaxis()->SetTitle("t_{2}");
  hh_pdf->GetZaxis()->SetTitle("");
  hh_pdf->GetYaxis()->SetTitleOffset(1.6);
  hh_pdf->GetXaxis()->SetTitleOffset(1.1);
  hh_pdf->Draw("colz");
  lhcbName->Draw();
  canv->Print("data.pdf");
  
  w::Ks1_TAU.setConstant(kTRUE);
  w::Ks2_TAU.setConstant(kTRUE);
  w::mod.fitTo(ds);

  TCanvas *canv3 = new TCanvas("data_canv","data_canv",0);
  canv3->cd();
  RooPlot* frame = w::Ks1_TAU.frame(Title("Projection"));
  ds.plotOn(frame);
  w::mod.plotOn(frame);
  frame->Draw();
  canv3->Print("proj.pdf");

  return 0;

}