import ROOT as r

w = r.RooWorkspace("w");

w.factory("GammaS[1.1165e-2]")
w.factory("GammaL[1.955e-5]")
w.factory("DeltaM[0.5293e-2]")
w.factory("t1[0,25]")
w.factory("t2[0,25]")
w.factory("exp::comb('exp(-GammaS*(t1+t2))')");
w.factory("EXPR::cpv('exp(-GammaS*t1-GammaL*t2)+exp(-GammaS*t2-GammaL*t1) + 2*cos(DeltaM*(t1-t2))*exp(-0.5*(t1+t2)*(GammaS+GammaL))')");
w.Print()
w.var("GammaS").Print()
w.var("t1").Print()
w.var("DeltaM").Print()

frame = r.RooPlot(w.var("t1"),0,25,50)
frame.Print()
comb=RooGenericPdf
w.pdf("comb")->plotOn(frame)
frame.Draw()