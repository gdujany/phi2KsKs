def rootStyle(batchMode=False):
    from ROOT import gROOT, gStyle, kWhite, kBlack,TPaveText
    
    # No info messages
    gROOT.ProcessLine("gErrorIgnoreLevel = kWarning;")

    # Batch mode (no TCanvas)
    gROOT.SetBatch(batchMode)

    # Start from a plain default
    # gROOT.SetStyle("Plain")

    lhcbMarkerType    = 1
    lhcbMarkerSize    = 0.8
    lhcbFont          = 132
    lhcbStatFontSize  = 0.06
    lhcbStatBoxWidth  = 0.15
    lhcbStatBoxHeight = 0.05
    lhcbWidth         = 1
    lhcbTextSize      = 0.02
    lhcbLabelSize     = 0.05
    lhcbAxisLabelSize = 0.05
    lhcbForeColour = kBlack

    gStyle.SetFrameBorderMode(0)
    gStyle.SetPadBorderMode(0)

    gStyle . SetPaperSize( 21 , 30 )
    # canvas options
    gStyle.SetCanvasBorderSize(0)
    gStyle.SetCanvasBorderMode(0)

    # fonts
    gStyle.SetTextFont(lhcbFont)
    gStyle.SetTextSize(lhcbTextSize)
    gStyle.SetLabelFont(lhcbFont,"x")
    gStyle.SetLabelFont(lhcbFont,"y")
    gStyle.SetLabelFont(lhcbFont,"z")
    gStyle.SetLabelSize(lhcbLabelSize,"x")
    gStyle.SetLabelSize(lhcbLabelSize,"y")
    gStyle.SetLabelSize(lhcbLabelSize,"z")
    gStyle.SetTitleFont(lhcbFont,"x")
    gStyle.SetTitleFont(lhcbFont,"y")
    gStyle.SetTitleSize(lhcbAxisLabelSize,"x")
    gStyle.SetTitleSize(lhcbAxisLabelSize,"y")
    # gStyle.SetTitleSize(lhcbAxisLabelSize,"x")
    # gStyle.SetTitleSize(lhcbAxisLabelSize,"y")
    # gStyle.SetTitleSize(lhcbAxisLabelSize,"z")
    gStyle.SetTitleColor(kWhite)
    gStyle.SetTitleFillColor(kWhite)
    gStyle.SetTitleColor(kBlack)
    gStyle.SetTitleBorderSize(0)
    gStyle.SetTitleTextColor(kBlack)

    gStyle.SetPadRightMargin    ( 0.05    ) ## increase for colz plots
    gStyle.SetPadBottomMargin   ( 0.16    )
    gStyle.SetPadLeftMargin     ( 0.14    )


    gStyle.SetLabelFont(lhcbFont,"y")
    gStyle.SetLabelFont(lhcbFont,"z")
    gStyle.SetLabelSize(lhcbLabelSize,"x")
    gStyle.SetLabelSize(lhcbLabelSize,"y")
    gStyle.SetLabelSize(lhcbLabelSize,"z")

    # set title position
    # gStyle.SetTitleX(0.15)
    # gStyle.SetTitleY(0.97)
    # turn off Title box
    gStyle.SetTitleBorderSize(0)
    gStyle.SetTitleTextColor(lhcbForeColour)
    gStyle.SetTitleColor(lhcbForeColour)

    # use bold lines and markers
    gStyle.SetLineWidth(lhcbWidth)
    gStyle.SetFrameLineWidth(lhcbWidth)
    gStyle.SetHistLineWidth(lhcbWidth)
    gStyle.SetFuncWidth(lhcbWidth)
    gStyle.SetGridWidth(lhcbWidth)
    gStyle.SetLineStyleString(2,"[12 12]")
    gStyle.SetMarkerStyle(lhcbMarkerType)
    gStyle.SetMarkerSize(lhcbMarkerSize)
    gStyle.SetLegendBorderSize(0)
    gStyle.SetLegendFont(lhcbFont)

    # # label offsets
    gStyle.SetLabelOffset(0.01,"y")
    gStyle.SetLabelOffset(0.01,"x")
    gStyle.SetTitleOffset(1.1,"y")
    

    # by default, do not display histogram decorations:
    gStyle.SetOptStat("")#1111)
    # show probability, parameters and errors
    # gStyle.SetOptFit(1011)

    # look of the statistics box:
    gStyle.SetStatBorderSize(1)
    gStyle.SetStatFont(lhcbFont)
    gStyle.SetStatFontSize(lhcbStatFontSize)
    gStyle.SetStatX(.92)
    gStyle.SetStatY(.86)
    gStyle.SetStatW(lhcbStatBoxWidth)
    gStyle.SetStatH(lhcbStatBoxHeight)
    gStyle.SetStatFormat ("6.2g") 

    # # put tick marks on top and RHS of plots
    gStyle.SetPadTickX(1)
    gStyle.SetPadTickY(1)

    # # histogram divisions
    gStyle.SetNdivisions(505,"x")
    gStyle.SetNdivisions(510,"y")

    # Force the style
    gROOT.ForceStyle()

    return gStyle

def printLHCb (x = 0.75, y = 0.90) :
    from ROOT import gROOT, TPaveText


    lhcbStyle = rootStyle()
    
    global lhcbName
    lhcbName = TPaveText ( x - 0.1 - lhcbStyle . GetPadRightMargin (),
                                    y-0.05 - lhcbStyle . GetPadTopMargin   (),
                                    x+0.2  - lhcbStyle . GetPadRightMargin (),
                                    y+0.05 - lhcbStyle . GetPadTopMargin   (),
                                    "BRNDC" )
        


    lhcbName.AddText ("LHCb Unofficial")
    
    # lhcbName . SetFillColor(0);
    lhcbName . SetFillColor(4000);
    lhcbName . SetTextAlign(12);
    lhcbName . SetBorderSize(0);
    lhcbName . Draw() 
 
    return lhcbName