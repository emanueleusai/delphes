import ROOT
from ROOT import TFile,TCanvas,gROOT,gStyle,TLegend,TGraphAsymmErrors,THStack,TIter,kRed,kYellow,kGray,kBlack,TLatex,kOrange,kAzure,TLine,kWhite,kBlue,kTRUE,kFALSE
from ROOT.TH1 import kPoisson
from os import system
from sys import argv
from os import mkdir
from os.path import exists
import math
import CMS_lumi

def envelope(plots):
  output=[]
  for imtt in range(1,plots[0].GetNbinsX()+1):
    minimium=float('inf')
    maximum=-float('inf')
    values=[]
    for plot in plots:
      values.append(plot.GetBinContent(imtt))
    output.append([min(values),max(values)])
  return output

def compare(name,file_list,name_list,legend_list,normalize=False,drawoption='hE',xtitle='',ytitle='',minx=0,maxx=0,rebin=1,miny=0,maxy=0,textsizefactor=1,logy=False,fit='',fitlow=0,fithigh=0,colors=[]):
  c=TCanvas(name,'',600,600)
  # c.SetLeftMargin(0.15)#
  # c.SetRightMargin(0.05)#
  # # c.SetTopMargin(0.05)#
  # c.SetBottomMargin(0.10)
  # # if not useOutfile:
  # # legend=TLegend(0.7,0.7,0.95,0.95)
  # # else:
  # c.SetTopMargin(0.15)
  # legend=TLegend(0.0,0.85,0.99,0.99)
  # #legend=TLegend(0.35,0.2,0.85,0.5)



  c.SetLeftMargin(0.15)#
  c.SetRightMargin(0.05)#
  c.SetBottomMargin(0.11)
  c.SetTopMargin(0.25)
  legend=TLegend(0.0,0.76,0.99,1.04)


  legend.SetHeader('')
  #legend.SetTextSize(0.03)
  legend.SetBorderSize(0)
  legend.SetTextFont(42)
  legend.SetLineColor(1)
  legend.SetLineStyle(1)
  legend.SetLineWidth(1)
  legend.SetFillColor(0)
  legend.SetFillStyle(0)
  histo_list=[]
  # tfile_list=[]
  the_maxy=0
  widths=[]
  for i in range(len(name_list)):
    # tfile_list.append(TFile(file_list[i],'READ'))
    histo_list.append(file_list[i].Get(name_list[i]).Clone())
    print legend_list[i],histo_list[-1].Integral()
    if normalize:
      histo_list[-1].Scale(1.0/(histo_list[-1].Integral()+0.00000001))
    if not histo_list[-1].ClassName()=='TGraphAsymmErrors':
      histo_list[-1].SetStats(0)
    histo_list[-1].SetLineWidth(3)
    if colors==[]:
      histo_list[-1].SetLineColor(i+1)
      if i>6:
        histo_list[-1].SetLineColor(i+4)
    else:
      histo_list[-1].SetLineColor(colors[i])
    histo_list[-1].SetTitle('')
    
    if rebin!=1:
      histo_list[-1].Rebin(rebin)
    if not histo_list[-1].ClassName()=='TGraphAsymmErrors':
      the_maxy=max(the_maxy,histo_list[-1].GetBinContent(histo_list[-1].GetMaximumBin())*1.05)
    if fit!='':
      if fitlow==0 and fithigh==0:
        histo_list[-1].Fit(fit)
      else:
        histo_list[-1].Fit(fit,'','',fitlow[i],fithigh[i])
      histo_list[-1].GetFunction("gaus").SetLineColor(i+1)
      gaus=histo_list[-1].GetFunction("gaus")
      print i,gaus.GetParameter(0),gaus.GetParameter(1),gaus.GetParameter(2)
      widths.append(gaus.GetParameter(2))
    if fit=='':
      legend.AddEntry(histo_list[-1],legend_list[i],'l')
    else:
      legend.AddEntry(histo_list[-1],legend_list[i]+' FWHM='+ "%.2f [GeV]" % (2.354*widths[i]),'l')
  for i in range(len(name_list)):
    if i==0:
      if not histo_list[-1].ClassName()=='TGraphAsymmErrors':
        if miny!=0 or maxy!=0:
          histo_list[i].SetMaximum(maxy)
          histo_list[i].SetMinimum(miny)
        else:
          histo_list[i].SetMaximum(the_maxy)
          histo_list[i].SetMinimum(0.0001)
      else:
        histo_list[i].SetMaximum(1.05)
        histo_list[i].SetMinimum(0.0001)
      histo_list[i].Draw(drawoption)
      charsize=0.05*textsizefactor
      histo_list[i].GetYaxis().SetLabelSize(charsize)
      histo_list[i].GetYaxis().SetTitleSize(charsize)
      histo_list[i].GetYaxis().SetTitleOffset(1.6)
      histo_list[i].GetXaxis().SetLabelSize(charsize)
      histo_list[i].GetXaxis().SetTitleSize(charsize)
      histo_list[i].GetXaxis().SetTitleOffset(0.95)
      # if useOutfile:
      if xtitle!='':
        histo_list[i].GetXaxis().SetTitle(xtitle)
      if ytitle!='':  
        histo_list[i].GetYaxis().SetTitle(ytitle)
      if maxx!=0 or minx!=0:
        histo_list[i].GetXaxis().SetRangeUser(minx,maxx)
      #   histo_list[i].GetYaxis().SetTitle('Efficiency')
    else:
      if histo_list[-1].ClassName()=='TGraphAsymmErrors':
        drawoption= drawoption.replace("A", "")
      histo_list[i].Draw(drawoption+'SAME')
  if logy:
    c.SetLogy()
  legend.Draw()
  # outfile.cd()
  # c.Write(name)
  c.SaveAs('pdf/'+name+'.pdf')
  #c.SaveAs(folder+name+'.png')

def hadd(path_base,name_base,inputlist,outputname,force=True,merge=True):
  command_list='hadd -f '+path_base+outputname+'.root'#-v 0
  if not force:
    command_list='hadd '+path_base+outputname+'.root'#-v 0
  for i in inputlist:
    command_list+=' '+path_base+name_base+i+'.root'
  if merge:
    system(command_list)
  return path_base+outputname+'.root'

def doeff(filename, histoname_den, histoname_num, histoname_out, outfile,rebin=1):
  numerator=filename.Get(histoname_num)
  denominator=filename.Get(histoname_den)
  if not rebin==1:
    numerator.Rebin(rebin)
    denominator.Rebin(rebin)
  n_num=numerator.Integral()
  n_den=denominator.Integral()
  error_bars=TGraphAsymmErrors()
  error_bars.Divide(numerator,denominator,"cl=0.683 b(1,1) mode")
  outfile.cd()
  error_bars.Write(histoname_out)
  return n_num/n_den

def slice_and_save(sample,histo,outfile):
  outfile.cd()
  histo_stack=THStack(histo,'x','Stack_'+histo.GetName(),'')
  histo_1d=histo_stack.GetHists()
  histo_stack.Write(histo_stack.GetName()+'_'+sample)
  nextinlist=TIter(histo_1d)
  obj=nextinlist()
  while obj:
    obj.Write(obj.GetName()+'_'+sample)
    obj=nextinlist()
  histo.Write(histo.GetName()+'_'+sample)

def domistag(infile,outfile,mistag_den,mistag_num,outname):
  den_histo=infile.Get(mistag_den).Clone('Denominator')
  num_histo=infile.Get(mistag_num).Clone('Numerator')
  mistag_histo=num_histo.Clone('Mistag')
  mistag_histo.Divide(num_histo,den_histo,1,1,'B')
  slice_and_save(outname,mistag_histo,outfile)
  slice_and_save(outname,num_histo,outfile)
  slice_and_save(outname,den_histo,outfile)

def make_fitplot(ratio,ratiomean,ratioup,ratiodown,btag):
  c=TCanvas('fitplot'+btag.replace(' ',''),'',1200,1000)
  margine=0.15
  c.SetRightMargin(0.10)
  c.SetLeftMargin(margine)
  c.SetTopMargin(0.10)
  c.SetBottomMargin(margine)
  ratio.Draw()
  ratio.SetMinimum(0.41)
  ratio.SetMaximum(2.5)
  # if '1' in btag:
  #   ratio.SetMinimum(0.61)
  #   ratio.SetMaximum(1.8)


  sizefactor=1.6
  ratio.SetLineWidth(3)
  ratio.SetLineColor(kBlack)
  ratio.GetXaxis().SetTitle("m_{Z'} [GeV]")
  ratio.GetYaxis().SetTitle("Ratio")
  ratio.GetXaxis().SetTitleSize(sizefactor*ratio.GetXaxis().GetTitleSize())
  ratio.GetYaxis().SetTitleSize(sizefactor*ratio.GetYaxis().GetTitleSize())
  ratio.GetXaxis().SetLabelSize(sizefactor*ratio.GetXaxis().GetLabelSize())
  ratio.GetYaxis().SetLabelSize(sizefactor*ratio.GetYaxis().GetLabelSize())
  offset=1.2
  ratio.GetXaxis().SetTitleOffset(offset*ratio.GetXaxis().GetTitleOffset())
  ratio.GetYaxis().SetTitleOffset(offset*ratio.GetYaxis().GetTitleOffset())
  ratio.SetStats(0)
  ratiomean.SetLineWidth(3)
  ratioup.SetLineWidth(3)
  ratiodown.SetLineWidth(3)
  ratiomean.Draw('SAME')
  ratioup.Draw('SAME')
  ratiodown.Draw('SAME')

  legend=TLegend(0.5,0.65,0.9,0.9)
  legend.SetHeader('')
  legend.SetBorderSize(0)
  legend.SetTextFont(42)
  legend.SetLineColor(1)
  legend.SetLineStyle(1)
  legend.SetLineWidth(1)
  legend.SetFillColor(0)
  legend.SetFillStyle(0)
  legend.AddEntry(0,"",'')
  legend.AddEntry(ratio,'QCD multijet','le')
  legend.AddEntry(ratiomean,'Fit','l')
  legend.AddEntry(ratioup,'#pm 1 std. deviation','l')
  legend.SetTextSize(0.05)
  legend.Draw()

  texheader='2 b-tag category'
  if '1' in btag:
    texheader='1 b-tag category'
  latex=TLatex(0.4,0.85,texheader)
  latex.SetNDC(1)
  latex.SetTextFont(42)
  latex.SetTextSize(0.05)
  latex.Draw()

  CMS_lumi.writeExtraText = True
  CMS_lumi.CMS_lumi(c, 0, 11)
  c.SaveAs('pdf/fitplot'+btag.replace(' ','')+'.pdf')
  CMS_lumi.writeExtraText = False

def make_plot(name, ttbar_file, qcd_file, data_file, signal_files, histo, histo_qcd='',histo_signal='',rebin=1,minx=0,maxx=0,miny=0,maxy=0,logy=False):
  c=TCanvas(name,'',600,600)
  c.SetLeftMargin(0.15)#
  c.SetRightMargin(0.05)#
  c.SetBottomMargin(0.1)
  c.SetTopMargin(0.25)
  latex=TLatex(0.6,0.70,'13 TeV, 2.69 fb^{-1}')
  latex.SetNDC(1)
  latex.SetTextFont(42)
  legend=TLegend(0.0,0.75,0.99,1.04)
  legend.SetHeader('')
  #legend.SetTextSize(0.03)
  legend.SetBorderSize(0)
  legend.SetTextFont(42)
  legend.SetLineColor(1)
  legend.SetLineStyle(1)
  legend.SetLineWidth(1)
  legend.SetFillColor(0)
  legend.SetFillStyle(0)
  stack=THStack(name+'_stack','')
  data_histo=data_file.Get(histo).Clone()
  data_histo.Rebin(rebin)
  ttbar_histo=ttbar_file.Get(histo).Clone()
  ttbar_histo.Rebin(rebin)
  if histo_qcd=='':
    qcd_histo=qcd_file.Get(histo).Clone()
  else:
    qcd_histo=qcd_file.Get(histo_qcd).Clone()
  qcd_histo.Rebin(rebin)
  signal_histos=[]
  colors=[28,9,8,2,3,4,5,6,7]+[i for i in range(30,50)]
  for i in range(len(signal_files)):
    if histo_signal=='':
      signal_histos.append(signal_files[i].Get(histo).Clone())
    else:
      signal_histos.append(signal_files[i].Get(histo_signal).Clone())
    signal_histos[i].SetLineWidth(3)
    signal_histos[i].SetLineStyle(1)
    signal_histos[i].SetLineColor(colors[i])
    signal_histos[i].Rebin(rebin)
  ttbar_histo.SetFillColor(kRed)
  qcd_histo.SetFillColor(kYellow)
  ttbar_histo.SetLineColor(kRed)
  qcd_histo.SetLineColor(kYellow)
  data_histo.SetLineColor(kBlack)
  ttbar_histo.SetMarkerColor(kRed)
  qcd_histo.SetMarkerColor(kYellow)
  data_histo.SetMarkerColor(kBlack)
  data_histo.SetLineWidth(3)
  legend.AddEntry(ttbar_histo,'t#bar{t}','f')
  legend.AddEntry(qcd_histo,'QCD from MC','f')
  legend.AddEntry(signal_histos[0],"Z'(2TeV)#rightarrowT't, T'(1.2TeV)#rightarrowbW 1pb",'l')
  legend.AddEntry(signal_histos[1],"Z'(2TeV)#rightarrowT't, T'(1.2TeV)#rightarrowtZ 1pb",'l')
  #legend.AddEntry(signal_histos[2] ,"Z' 3 TeV 1pb",'l')
  stack.Add(ttbar_histo)
  stack.Add(qcd_histo)
  errors=ttbar_histo.Clone(histo+'tmp')
  errors.Add(qcd_histo)
  err=TGraphAsymmErrors(errors)
  stack.Draw('hist')
  stack.GetXaxis().SetRangeUser(0,4000)
  err.SetFillStyle(3145)
  err.SetFillColor(kGray)
  errors.SetLineColor(kBlack)
  errors.SetFillStyle(0)
  errors.Draw('samehist')
  err.Draw('2')
  #summc.Draw('samehist')
  #stack.SetMinimum(0.1)
  #stack.SetMaximum(stack.GetMaximum()*1.2)
  stack.GetXaxis().SetTitle("m_{tWb} [GeV]")
  stack.GetYaxis().SetTitle('Events')
  charsize=0.05
  stack.GetYaxis().SetLabelSize(charsize)
  stack.GetYaxis().SetTitleSize(charsize)
  stack.GetYaxis().SetTitleOffset(1.6)
  stack.GetXaxis().SetLabelSize(charsize)
  stack.GetXaxis().SetTitleSize(charsize)
  stack.GetXaxis().SetTitleOffset(0.95)
  #stack.SetMinimum(0.001)
  if maxx!=0 or minx!=0:
    stack.GetXaxis().SetRangeUser(minx,maxx)
  if maxy!=0 or miny!=0:
    stack.SetMinimum(miny)
    stack.SetMaximum(maxy)
  else:
    if logy:
      stack.SetMaximum(stack.GetMaximum()*100)
      stack.SetMinimum(0.1)
    else:
      stack.SetMaximum(stack.GetMaximum()*1.5)
  for i in range(len(signal_files)):
    signal_histos[i].Draw('samehist')
  data_histo.Draw('SAME')
  if logy:
    c.SetLogy()
  legend.Draw()
  latex.Draw()
  c.SaveAs('pdf/'+name+'.pdf')
  #c.SaveAs('pdf/'+name+'.png')

us='_'
def make_ratioplot(name, ttbar_file=0, qcd_file=0, data_file=0, signal_files=[], histo=0, histo_qcd='',histo_signal='',histo_ttbar='',rebin=1,minx=0,maxx=0,miny=0,maxy=0,minratio=0,maxratio=0,logy=False,
                    xtitle='',ytitle='',textsizefactor=1,signal_legend=[],outfile=0,signal_colors=[],separate_legend=False,fixratio=False, signal_zoom=1, qcd_zoom=1, ttbar_zoom=1,normalize=False,
                    ttbar_legend='t#bar{t}',qcd_legend='QCD from MC', data_legend='Data',dosys=False,sysdict={},
                    syspath='/afs/desy.de/user/u/usaiem/xxl-af-cms/code/cmssw/CMSSW_7_6_3/src/UHH2/ZprimeAllHadronic/python/data/sys/top_added',bkgup=0,bkgdown=0,blind=False,
                    systtbarpath='/afs/desy.de/user/u/usaiem/xxl-af-cms/code/cmssw/CMSSW_7_6_3/src/UHH2/ZprimeAllHadronic/python/data/sys/uhh2.AnalysisModuleRunner.MC.TTbar',bkgfitup=0,bkgfitdown=0,drawratio=True,qcdnorm=False,docms=True,legendtitle=''):
  
  ###canvas setting up
  canvas=0
  if separate_legend:
    canvas=TCanvas(name,'',0,0,600,600)
  else:
    canvas=TCanvas(name,'',0,0,600,900)
  canvas.Divide(1,2)
  top_pad=canvas.GetPad(1)
  bottom_pad=canvas.GetPad(2)
  top_pad.SetPad( 0.0, 0.30, 1.0, 1.0 )
  bottom_pad.SetPad( 0.0, 0.0, 1.0, 0.30 )
  top_pad.SetLeftMargin(0.17)
  top_pad.SetRightMargin(0.07)
  if separate_legend:
    top_pad.SetTopMargin(0.12)
  else:
    top_pad.SetTopMargin(0.25)
  top_pad.SetBottomMargin(0.0)
  bottom_pad.SetLeftMargin(0.17)
  bottom_pad.SetRightMargin(0.07)
  bottom_pad.SetTopMargin(0.0)
  bottom_pad.SetBottomMargin(0.45)
  if not drawratio:
    top_pad.SetBottomMargin(0.10)
  charsize=0
  offset=0
  if separate_legend:
    charsize=0.07
    offset=1.
  else:
    charsize=0.05
    offset=1.4
  pullcharsize=charsize*0.7/0.3
  pulloffset=offset*0.3/0.7

  ###latex label
  latex=0
  if separate_legend:
    latex=TLatex(0.62,0.83,'13 TeV, 2.69 fb^{-1}')
  else:
    latex=TLatex(0.6,0.7,'13 TeV, 2.69 fb^{-1}')
  latex.SetTextSize(charsize)
  latex.SetNDC(1)
  latex.SetTextFont(42)

  ###legend setting up
  #legend=TLegend(0.0,0.75,0.99,1.04)
  legend=TLegend(0.47,0.43,0.9,0.9)
  legend.SetNColumns(2)
  legend.SetHeader('')
  # if 'parabola' in name and '2' in name:
  #   legend.SetHeader('2 b-tag category')
  # elif 'parabola' in name and '1' in name:
  #   legend.SetHeader('1 b-tag category')
  if 'parabola' in name:
    legend.SetNColumns(1)
    legend.SetTextSize(0.047)
  legend.SetBorderSize(0)
  legend.SetTextFont(42)
  legend.SetLineColor(1)
  legend.SetLineStyle(1)
  legend.SetLineWidth(1)
  legend.SetFillColor(0)
  legend.SetFillStyle(0)

  ###data
  data_histo=data_file.Get(histo).Clone()
  data_histo.Rebin(rebin)
  data_histo.SetMarkerColor(kBlack)
  data_histo.SetLineWidth(3)
  data_histo.SetLineColor(kBlack)
  data_histo.SetMarkerColor(kBlack)
  data_histo.SetMarkerStyle(20)
  if normalize:
      data_histo.Scale(1.0/(data_histo.Integral()+0.00000001))
  legend.AddEntry(data_histo,data_legend,'pe')

  ###mc stack
  stack=THStack(name+'_stack','')
  
  if histo_qcd=='':
    qcd_histo=qcd_file.Get(histo).Clone(name+'_make_plot')
  else:
    qcd_histo=qcd_file.Get(histo_qcd).Clone(name+'_make_plot')
  qcd_histo.Rebin(rebin)
  ttbar_histo=0
  if ttbar_file!=0:
    if histo_ttbar=='':
      ttbar_histo=ttbar_file.Get(histo).Clone()
    else:
      ttbar_histo=ttbar_file.Get(histo_ttbar).Clone()
    ttbar_histo.Rebin(rebin)
    ttbar_histo.SetFillColor(kAzure)
    ttbar_histo.SetLineColor(kAzure)
    ttbar_histo.SetMarkerColor(kAzure)
    if ttbar_zoom!=1:
      ttbar_histo.Scale(ttbar_zoom)
    
    legend.AddEntry(ttbar_histo,ttbar_legend,'f')
  qcd_histo.SetFillColor(kOrange)
  qcd_histo.SetLineColor(kOrange)
  qcd_histo.SetMarkerColor(kOrange)
  if qcd_zoom!=1:
      qcd_histo.Scale(qcd_zoom)
  legend.AddEntry(qcd_histo,qcd_legend,'f')

  if qcdnorm:
    qcd_histo.Scale((data_histo.Integral()-ttbar_histo.Integral())/qcd_histo.Integral())

  sum_mc=qcd_histo.Clone(histo+'tmp')
  #sum_mc.SetLineWidth(3)
  #sum_mc.SetLineColor(kRed)
  #legend.AddEntry(sum_mc,qcd_legend,'l')
  if ttbar_file!=0:
    sum_mc.Add(ttbar_histo)
  if normalize:
    if ttbar_file==0:
      qcd_histo.Scale(1.0/(qcd_histo.Integral()+0.00000001))
      sum_mc.Scale(1.0/(sum_mc.Integral()+0.00000001))
    else:
      qcd_histo.Scale(1.0/(sum_mc.Integral()+0.00000001))
      ttbar_histo.Scale(1.0/(sum_mc.Integral()+0.00000001))
      sum_mc.Scale(1.0/(sum_mc.Integral()+0.00000001))
  if ttbar_file!=0:
    stack.Add(ttbar_histo)
  stack.Add(qcd_histo)
  
  sum_mc.SetLineColor(kBlack)
  sum_mc.SetFillStyle(0)
  err=TGraphAsymmErrors(sum_mc)
  legend.AddEntry(err,'Total uncertainty','f')

  if legendtitle=='':
    legend.AddEntry(0,"",'')
    legend.AddEntry(0,"Z'#rightarrowTt, T#rightarrowbW",'')
  else:
    legend.AddEntry(0,"",'')
    legend.AddEntry(0,legendtitle,'')

  ###signal setting up
  signal_histos=[]
  colors=[30,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60]
  styles=[5,7,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
  if signal_colors!=[]:
    colors=signal_colors
  for i in range(len(signal_files)):
    if histo_signal=='':
      signal_histos.append(signal_files[i].Get(histo).Clone())
    else:
      signal_histos.append(signal_files[i].Get(histo_signal).Clone())
    signal_histos[i].SetLineWidth(3)
    signal_histos[i].SetLineStyle(styles[i])
    signal_histos[i].SetLineColor(colors[i])
    signal_histos[i].SetMarkerColor(colors[i])
    signal_histos[i].Rebin(rebin)
    if signal_zoom!=1:
      signal_histos[i].Scale(signal_zoom)
    if normalize:
      signal_histos[i].Scale(1.0/(signal_histos[i].Integral()+0.00000001))
    legend.AddEntry(signal_histos[i],signal_legend[i],'l')

  ###mc shape line
  ttbar_line=0
  if ttbar_file!=0:
    ttbar_line=ttbar_histo.Clone()
    ttbar_line.SetLineColor(kBlack)
    ttbar_line.SetFillStyle(0)

  ###mc errors
  if dosys:
    #sys_diff=[]
    sys_diff_qcd=[]
    sys_diff_ttbar=[]
    #sys_diff=[]
    for imtt in range(1,ttbar_histo.GetNbinsX()+1):
      sys_diff_qcd.append([])
      sys_diff_ttbar.append([])
    for sys in sysdict:
      if not (sys in ['mur','muf','murmuf','pdf']):
        #tmp=[]
        #for imtt in range(1,ttbar_histo.GetNbinsX()+1):
        #  tmp.append([])
        for side in ['UP','DOWN']:
          ttf=TFile(syspath+sysdict[sys]+side+'.root','READ')
          ttf_mean=TFile(syspath+'UP.root')
          #outfile.cd()
          ttbar_mean=ttf_mean.Get(histo).Clone()
          ttbar_mean.Rebin(rebin)
          ttbar_tmp=ttf.Get(histo).Clone()#'ttbar'+sysdict[sys]+side
          ttbar_tmp.Rebin(rebin)
          ttbar_tmp.Add(ttbar_histo,-1)
          for imtt in range(1,ttbar_histo.GetNbinsX()+1):
            #tmp[imtt-1].append(ttbar_tmp.GetBinContent(imtt))
            sys_diff_ttbar[imtt-1].append(ttbar_tmp.GetBinContent(imtt))
        #print sys,tmp
    #adding pdf
    if ('pdf' in sysdict):
      ttbar_pdf=TFile(systtbarpath+sysdict['pdf']+'UP.root','READ')
      pdfplots=[]
      ttbar_pdf_mean=ttbar_pdf.Get(histo)
      ttbar_pdf_mean.Rebin(rebin)
      for i in range(100):
        pdfplots.append(ttbar_pdf.Get(histo.split('/')[0]+'PDF'+str(i)+'/'+histo.split('/')[1]).Clone())
        pdfplots[-1].Rebin(rebin)
      for imtt in range(1,ttbar_pdf_mean.GetNbinsX()+1):
        rms=0.0
        for i in pdfplots:
          rms=rms+math.pow(i.GetBinContent(imtt)-ttbar_pdf_mean.GetBinContent(imtt),2)
        rms=math.sqrt(rms/100)
        sys_diff_ttbar[imtt-1].append(rms)
        sys_diff_ttbar[imtt-1].append(-rms)
        #print rms

    #adding mu
    if ('mur' in sysdict) and ('muf' in sysdict) and ('murmuf' in sysdict):
      ttbar_MURUP=TFile(syspath+sysdict['mur']+'UP.root','READ')
      ttbar_MURDOWN=TFile(syspath+sysdict['mur']+'DOWN.root','READ')
      ttbar_MUFUP=TFile(syspath+sysdict['muf']+'UP.root','READ')
      ttbar_MUFDOWN=TFile(syspath+sysdict['muf']+'DOWN.root','READ')
      ttbar_MURMUFUP=TFile(syspath+sysdict['murmuf']+'UP.root','READ')
      ttbar_MURMUFDOWN=TFile(syspath+sysdict['murmuf']+'DOWN.root','READ')
      ttf_mean=TFile(syspath+'UP.root')
      plotMean=ttf_mean.Get(histo)
      plotMURUP=ttbar_MURUP.Get(histo)
      plotMURDOWN=ttbar_MURDOWN.Get(histo)
      plotMUFUP=ttbar_MUFUP.Get(histo)
      plotMUFDOWN=ttbar_MUFDOWN.Get(histo)
      plotMURMUFUP=ttbar_MURMUFUP.Get(histo)
      plotMURMUFDOWN=ttbar_MURMUFDOWN.Get(histo)
      plotMean.Rebin(rebin)
      plotMURUP.Rebin(rebin)
      plotMURDOWN.Rebin(rebin)
      plotMUFUP.Rebin(rebin)
      plotMUFDOWN.Rebin(rebin)
      plotMURMUFUP.Rebin(rebin)
      plotMURMUFDOWN.Rebin(rebin)

      envelopesr=envelope([plotMURUP,plotMURDOWN,plotMUFUP,plotMUFDOWN,plotMURMUFUP,plotMURMUFDOWN])
      for imtt in range(1,ttbar_histo.GetNbinsX()+1):
        sys_diff_ttbar[imtt-1].append(envelopesr[imtt-1][0]-plotMean.GetBinContent(imtt))
        sys_diff_ttbar[imtt-1].append(envelopesr[imtt-1][1]-plotMean.GetBinContent(imtt))
        #print envelopesr[imtt-1][0], envelopesr[imtt-1][1]
    #adding bkg uncertainties
    if bkgup!=0 and bkgdown!=0 and bkgfitup!=0 and bkgfitdown!=0:
      bkgupdiff=qcd_file.Get(bkgup).Clone(name+'_bkgupdiff_make_plot')
      bkgdowndiff=qcd_file.Get(bkgdown).Clone(name+'_bkgdowndiff_make_plot')
      bkgfitupdiff=qcd_file.Get(bkgfitup).Clone(name+'_bkgfitupdiff_make_plot')
      bkgfitdowndiff=qcd_file.Get(bkgfitdown).Clone(name+'_bkgfitdowndiff_make_plot')
      bkgupdiff.Rebin(rebin)
      bkgdowndiff.Rebin(rebin)
      bkgfitupdiff.Rebin(rebin)
      bkgfitdowndiff.Rebin(rebin)
      bkgupdiff.Add(qcd_histo,-1)
      bkgdowndiff.Add(qcd_histo,-1)
      bkgfitupdiff.Add(qcd_histo,-1)
      bkgfitdowndiff.Add(qcd_histo,-1)
      for imtt in range(1,qcd_histo.GetNbinsX()+1):
        sys_diff_qcd[imtt-1].append(bkgupdiff.GetBinContent(imtt))
        sys_diff_qcd[imtt-1].append(bkgdowndiff.GetBinContent(imtt))
        sys_diff_qcd[imtt-1].append(bkgfitupdiff.GetBinContent(imtt))
        sys_diff_qcd[imtt-1].append(bkgfitdowndiff.GetBinContent(imtt))
    #adding stat uncertainties
    for imtt in range(1,ttbar_histo.GetNbinsX()+1):
      sys_diff_ttbar[imtt-1].append(ttbar_histo.GetBinError(imtt))
      sys_diff_ttbar[imtt-1].append(-ttbar_histo.GetBinError(imtt))
      sys_diff_qcd[imtt-1].append(qcd_histo.GetBinError(imtt))
      sys_diff_qcd[imtt-1].append(-qcd_histo.GetBinError(imtt))
    #adding flat uncertainties
    for imtt in range(1,ttbar_histo.GetNbinsX()+1):
      #3% trigger
      sys_diff_ttbar[imtt-1].append(0.03*ttbar_histo.GetBinContent(imtt))
      sys_diff_ttbar[imtt-1].append(-0.03*ttbar_histo.GetBinContent(imtt))
      #2.7% lumi
      sys_diff_ttbar[imtt-1].append(0.023*ttbar_histo.GetBinContent(imtt))
      sys_diff_ttbar[imtt-1].append(-0.023*ttbar_histo.GetBinContent(imtt))
      #15% ttbar
      #sys_diff_ttbar[imtt-1].append(0.15*ttbar_histo.GetBinContent(imtt))
      #sys_diff_ttbar[imtt-1].append(-0.15*ttbar_histo.GetBinContent(imtt))
      #2.8% QCD
      sys_diff_qcd[imtt-1].append(0.028*qcd_histo.GetBinContent(imtt))
      sys_diff_qcd[imtt-1].append(-0.028*qcd_histo.GetBinContent(imtt))
    #combining uncertainties
    sys_tot_ttbar=[]
    sys_tot_qcd=[]
    sys_tot=[]
    sys_global_ttbar=[0.0,0.0]
    sys_global_qcd=[0.0,0.0]
    nevt_global=[0.0,0.0,0.0]
    for imtt in range(1,ttbar_histo.GetNbinsX()+1):
      uperr_qcd=0
      downerr_qcd=0
      uperr_ttbar=0
      downerr_ttbar=0
      for error in sys_diff_ttbar[imtt-1]:
        if error<0:
          downerr_ttbar=downerr_ttbar+error*error
        else:
          uperr_ttbar=uperr_ttbar+error*error
      for error in sys_diff_qcd[imtt-1]:
        if error<0:
          downerr_qcd=downerr_qcd+error*error
        else:
          uperr_qcd=uperr_qcd+error*error
      sys_tot_ttbar.append([math.sqrt(downerr_ttbar),math.sqrt(uperr_ttbar)])
      sys_tot_qcd.append([math.sqrt(downerr_qcd),math.sqrt(uperr_qcd)])
      sys_tot.append([math.sqrt(downerr_qcd+downerr_ttbar),math.sqrt(uperr_qcd+uperr_ttbar)])
      sys_global_qcd[0]=sys_global_qcd[0]+downerr_qcd
      sys_global_qcd[1]=sys_global_qcd[1]+uperr_qcd
      sys_global_ttbar[0]=sys_global_ttbar[0]+downerr_ttbar
      sys_global_ttbar[1]=sys_global_ttbar[1]+uperr_ttbar
      nevt_global[0]=nevt_global[0]+data_histo.GetBinContent(imtt)
      nevt_global[1]=nevt_global[1]+qcd_histo.GetBinContent(imtt)
      nevt_global[2]=nevt_global[2]+ttbar_histo.GetBinContent(imtt)
      #print 'ttbar+qcd',math.sqrt(uperr_qcd+uperr_ttbar),math.sqrt(downerr_qcd+downerr_ttbar)
      #print 'qcd',math.sqrt(uperr_qcd),math.sqrt(downerr_qcd)
      #print 'ttbar',math.sqrt(uperr_ttbar),math.sqrt(downerr_ttbar)
      err.SetPointEYhigh(imtt-1,math.sqrt(uperr_qcd+uperr_ttbar))
      err.SetPointEYlow(imtt-1,math.sqrt(downerr_qcd+downerr_ttbar))
    sys_global=[0.0,0.0]
    sys_global[0]=math.sqrt(sys_global_qcd[0]+sys_global_ttbar[0])
    sys_global[1]=math.sqrt(sys_global_qcd[1]+sys_global_ttbar[1])
    sys_global_qcd[0]=math.sqrt(sys_global_qcd[0])
    sys_global_qcd[1]=math.sqrt(sys_global_qcd[1])
    sys_global_ttbar[0]=math.sqrt(sys_global_ttbar[0])
    sys_global_ttbar[1]=math.sqrt(sys_global_ttbar[1])
    print name
    print "\hline"
    print "Multijet QCD & $%.0f^{+%.0f}_{-%.0f}$ \\\\" % (nevt_global[1],sys_global_qcd[1],sys_global_qcd[0])
    print "SM ttbar & $%.0f^{+%.0f}_{-%.0f}$ \\\\" % (nevt_global[2],sys_global_ttbar[1],sys_global_ttbar[0])
    print "\hline"
    print "Total background & $%.0f^{+%.0f}_{-%.0f}$ \\\\" % (nevt_global[1]+nevt_global[2],sys_global[1],sys_global[0])
    print 'DATA & %.0f' %nevt_global[0]


  err.SetFillStyle(3145)
  err.SetFillColor(kGray+1)
  
  ###pull distribution
  pull=data_histo.Clone()
  pull.Add(sum_mc,-1)
  data_histo.Sumw2(kFALSE)
  data_histo.SetBinErrorOption(kPoisson)
  #for i in range(pull.GetNbinsX()+2):
  for imtt in range(1,ttbar_histo.GetNbinsX()+1):
    #print 'eh',data_histo.GetBinErrorLow(imtt), data_histo.GetBinErrorUp(imtt)
    
    if dosys:
      if pull.GetBinContent(imtt)>0:
        pull.SetBinContent(imtt,pull.GetBinContent(imtt)/(math.sqrt(sys_tot[imtt-1][1]*sys_tot[imtt-1][1]+data_histo.GetBinErrorLow(imtt)*data_histo.GetBinErrorLow(imtt)) ) )
      else:
        pull.SetBinContent(imtt,pull.GetBinContent(imtt)/(math.sqrt(sys_tot[imtt-1][0]*sys_tot[imtt-1][0]+data_histo.GetBinErrorUp(imtt)*data_histo.GetBinErrorUp(imtt)) ) )
    else:
      if pull.GetBinErrorUp(imtt)!=0:
        pull.SetBinContent(imtt,pull.GetBinContent(imtt)/pull.GetBinError(imtt))
      else:
        pull.SetBinContent(imtt,0)
  pull.SetFillColor(kOrange+7)

  ###drawing top
  top_pad.cd()
  stack.Draw('hist')
  stack.GetXaxis().SetTitle('')
  stack.GetYaxis().SetTitle(ytitle)
  stack.GetYaxis().SetLabelSize(charsize)
  stack.GetYaxis().SetTitleSize(charsize)
  stack.GetYaxis().SetTitleOffset(offset)
  if drawratio:
    stack.GetXaxis().SetLabelSize(0)
    stack.GetXaxis().SetTitleSize(0)
    stack.GetXaxis().SetTitleOffset(100)
    stack.GetXaxis().SetLabelOffset(100)
  if minx!=0 or maxx!=0:
    stack.GetXaxis().SetRangeUser(minx,maxx)
  #else:
  #  stack.GetXaxis().SetRangeUser(0,4000)
  if miny!=0 or maxy!=0:
    stack.SetMaximum(maxy)
    stack.SetMinimum(miny)
  else:
    if logy:
      stack.SetMaximum(stack.GetMaximum()*10)
      stack.SetMinimum(0.2)
    else:
      stack.SetMaximum(stack.GetMaximum()*2.0)
      stack.SetMinimum(0.001)
  err.Draw('2')
  sum_mc.Draw('samehist')
  if ttbar_file!=0:
    ttbar_line.Draw('samehist')
  for i in signal_histos:
    i.Draw('samehist')
  if not blind:
    # data_histo.Draw('E0 P SAME')
    #data_histo2=data_histo.Clone()
    #for imtt in range(1,ttbar_histo.GetNbinsX()+1):
    #  if sum_mc.GetBinContent(imtt)<0.000001:
    #    data_histo2.SetBinContent(imtt,-100)

    data_histo2=data_histo.Clone()
    data_histo2.SetMarkerStyle(1)
    data_histo2.SetMarkerSize(1)
    data_histo2.Sumw2(kFALSE)
    data_histo2.SetBinErrorOption(kPoisson)
    data_histo2.Draw('E0 X0 SAME')
    data_histo.Draw('P SAME')
  if logy:
    top_pad.SetLogy()
  if not separate_legend:
    legend.Draw()
  legend.Draw()

  latex2text=''
  if 'parabola' in name and '2' in name:
    latex2text='2 b-tag category'
  elif 'parabola' in name and '1' in name:
    latex2text='1 b-tag category'
  latex2=TLatex(0.205,0.7,latex2text)
  latex2.SetTextSize(0.05)
  latex2.SetNDC(1)
  latex2.SetTextFont(42)
  latex2.Draw()

  

  #latex.Draw()





  ###drawing bottom
  if drawratio:
    bottom_pad.cd()
    pull.SetStats(0)
    pull.SetTitle('')
    if blind:
      for imtt in range(1,pull.GetNbinsX()+1):
        pull.SetBinContent(imtt,0)
    pull.Draw('hist')
    if minx!=0 or maxx!=0:
      pull.GetXaxis().SetRangeUser(minx,maxx)
    pull.GetYaxis().SetLabelSize(pullcharsize)
    pull.GetYaxis().SetTitleSize(pullcharsize)
    pull.GetYaxis().SetTitleOffset(pulloffset)
    pull.GetXaxis().SetLabelSize(pullcharsize)
    pull.GetXaxis().SetTitleSize(pullcharsize)
    pull.GetXaxis().SetTitleOffset(1.3)
    pull.GetYaxis().SetTitle('#frac{Data-MC}{#sigma}')#'(Data-MC)/#sigma'
    if xtitle!='':
      pull.GetXaxis().SetTitle(xtitle)
    if fixratio:
      pull.GetYaxis().SetRangeUser(-3.9,3.9)
    pull.GetYaxis().SetNdivisions(4,2,0)
    pull.GetXaxis().SetNdivisions(10,5,0)
    #pull.GetXaxis().SetRangeUser(pull.GetXaxis().GetXmin(),pull.GetXaxis().GetXmax()*zf)
    line1=0
    if minx==0 and maxx==0:
      line1=TLine(pull.GetXaxis().GetXmin(),0.0,pull.GetXaxis().GetXmax(),0.0)
    else:
      line1=TLine(minx,0.0,maxx,0.0)
    line1.SetLineStyle(2)
    line1.SetLineWidth(3)

    line1.Draw()

  if docms:
    CMS_lumi.CMS_lumi(top_pad, 4, 11)

  ###saving
  canvas.SaveAs('pdf/'+name+'.pdf')
  if outfile!=0:
      canvas.Write()



  ###separate legend
  # if separate_legend:
  #   legendcanvas=TCanvas(name+'_legend','',0,0,600,600)
  #   legendcanvas.cd()
  #   legend.SetNColumns(1)
  #   legend.SetX1(0.0)
  #   legend.SetX2(1.0)
  #   legend.SetY1(0.0)
  #   legend.SetY2(1.0)
  #   legend.Draw()
  #   legendcanvas.SaveAs('pdf/'+name+'_legend.pdf')
  #   if outfile!=0:
  #     legendcanvas.Write()
  



def make_ratioplot2(name, ttbar_file=0, qcd_file=0, data_file=0, signal_files=[], histo=0, histo_qcd='',histo_signal='',histo_ttbar='',rebin=1,minx=0,maxx=0,miny=0,maxy=0,minratio=0,maxratio=0,logy=False,
                    xtitle='',ytitle='',textsizefactor=1,signal_legend=[],outfile=0,signal_colors=[],separate_legend=False,fixratio=False, signal_zoom=1, qcd_zoom=1, ttbar_zoom=1,normalize=False,
                    ttbar_legend='t#bar{t}',qcd_legend='QCD from MC', data_legend='Data',rebinlist=0,rebinlen=0):
  
  ###canvas setting up
  canvas=0
  if separate_legend:
    canvas=TCanvas(name,'',0,0,600,600)
  else:
    canvas=TCanvas(name,'',0,0,600,900)
  canvas.Divide(1,2)
  top_pad=canvas.GetPad(1)
  bottom_pad=canvas.GetPad(2)
  top_pad.SetPad( 0.0, 0.30, 1.0, 1.0 )
  bottom_pad.SetPad( 0.0, 0.0, 1.0, 0.30 )
  top_pad.SetLeftMargin(0.15)
  top_pad.SetRightMargin(0.05)
  if separate_legend:
    top_pad.SetTopMargin(0.10)
  else:
    top_pad.SetTopMargin(0.25)
  top_pad.SetBottomMargin(0.0)
  bottom_pad.SetLeftMargin(0.15)
  bottom_pad.SetRightMargin(0.05)
  bottom_pad.SetTopMargin(0.0)
  bottom_pad.SetBottomMargin(0.45)
  charsize=0
  offset=0
  if separate_legend:
    charsize=0.07
    offset=1.
  else:
    charsize=0.05
    offset=1.4
  pullcharsize=charsize*0.7/0.3
  pulloffset=offset*0.3/0.7

  ###latex label
  latex=0
  if separate_legend:
    latex=TLatex(0.62,0.83,'13 TeV, 2.69 fb^{-1}')
  else:
    latex=TLatex(0.6,0.7,'13 TeV, 2.69 fb^{-1}')
  latex.SetTextSize(charsize)
  latex.SetNDC(1)
  latex.SetTextFont(42)

  ###legend setting up
  legend=TLegend(0.0,0.75,0.99,1.04)
  legend.SetNColumns(2)
  legend.SetHeader('')
  #legend.SetTextSize(0.03)
  legend.SetBorderSize(0)
  legend.SetTextFont(42)
  legend.SetLineColor(1)
  legend.SetLineStyle(1)
  legend.SetLineWidth(1)
  legend.SetFillColor(0)
  legend.SetFillStyle(0)

  ###data
  data_histo=data_file.Get(histo).Clone()
  if rebinlist==0:
    data_histo.Rebin(rebin)
  else:
    data_histo=data_histo.Rebin(rebinlen,name+'datarebin',rebinlist)
  data_histo.SetMarkerColor(kBlack)
  data_histo.SetLineWidth(3)
  data_histo.SetLineColor(kBlack)
  data_histo.SetMarkerColor(kBlack)
  data_histo.SetMarkerStyle(20)
  if normalize:
      data_histo.Scale(1.0/(data_histo.Integral()+0.00000001))
  legend.AddEntry(data_histo,data_legend,'l')

  ###mc stack
  stack=THStack(name+'_stack','')
  
  if histo_qcd=='':
    qcd_histo=qcd_file.Get(histo).Clone()
  else:
    qcd_histo=qcd_file.Get(histo_qcd).Clone()
  if rebinlist==0:
    qcd_histo.Rebin(rebin)
  else:
    qcd_histo=qcd_histo.Rebin(rebinlen,name+'qcdrebin',rebinlist)
  ttbar_histo=0
  if ttbar_file!=0:
    if histo_ttbar=='':
      ttbar_histo=ttbar_file.Get(histo).Clone()
    else:
      ttbar_histo=ttbar_file.Get(histo_ttbar).Clone()
    if rebinlist==0:
      ttbar_histo.Rebin(rebin)
    else:
      ttbar_histo=ttbar_histo.Rebin(rebinlen,name+'ttbarrebin',rebinlist)
    ttbar_histo.SetFillColor(kAzure)
    ttbar_histo.SetLineColor(kAzure)
    ttbar_histo.SetMarkerColor(kAzure)
    if ttbar_zoom!=1:
      ttbar_histo.Scale(ttbar_zoom)
    
    legend.AddEntry(ttbar_histo,ttbar_legend,'f')
  qcd_histo.SetFillColor(kOrange)
  qcd_histo.SetLineColor(kOrange)
  qcd_histo.SetMarkerColor(kOrange)
  if qcd_zoom!=1:
      qcd_histo.Scale(qcd_zoom)
  #legend.AddEntry(qcd_histo,qcd_legend,'f')

  sum_mc=qcd_histo.Clone(histo+'tmp')
  sum_mc.SetLineWidth(3)
  sum_mc.SetLineColor(kRed)
  legend.AddEntry(sum_mc,qcd_legend,'l')
  if ttbar_file!=0:
    sum_mc.Add(ttbar_histo)
  if normalize:
    if ttbar_file==0:
      qcd_histo.Scale(1.0/(qcd_histo.Integral()+0.00000001))
      sum_mc.Scale(1.0/(sum_mc.Integral()+0.00000001))
    else:
      qcd_histo.Scale(1.0/(sum_mc.Integral()+0.00000001))
      ttbar_histo.Scale(1.0/(sum_mc.Integral()+0.00000001))
      sum_mc.Scale(1.0/(sum_mc.Integral()+0.00000001))
  if ttbar_file!=0:
    stack.Add(ttbar_histo)
  stack.Add(qcd_histo)
  
  ###signal setting up
  signal_histos=[]
  colors=[30,40,41,42,43,44,45,46,47,48,49]
  if signal_colors!=[]:
    colors=signal_colors
  for i in range(len(signal_files)):
    if histo_signal=='':
      signal_histos.append(signal_files[i].Get(histo).Clone())
    else:
      signal_histos.append(signal_files[i].Get(histo_signal).Clone())
    signal_histos[i].SetLineWidth(3)
    signal_histos[i].SetLineStyle(1)
    signal_histos[i].SetLineColor(colors[i])
    signal_histos[i].SetMarkerColor(colors[i])
    if rebinlist==0:
      signal_histos[i].Rebin(rebin)
    else:
      signal_histos[i]=signal_histos[i].Rebin(rebinlen,name+str(i)+'signalrebin',rebinlist)
    if signal_zoom!=1:
      signal_histos[i].Scale(signal_zoom)
    if normalize:
      signal_histos[i].Scale(1.0/(signal_histos[i].Integral()+0.00000001))
    legend.AddEntry(signal_histos[i],signal_legend[i],'l')

  ###mc shape line
  #sum_mc.SetLineColor(kBlack)
  sum_mc.SetFillStyle(0)
  ttbar_line=0
  if ttbar_file!=0:
    ttbar_line=ttbar_histo.Clone()
    ttbar_line.SetLineColor(kBlack)
    ttbar_line.SetFillStyle(0)

  ###mc errors
  err=TGraphAsymmErrors(sum_mc)
  err.SetFillStyle(3145)
  err.SetFillColor(kGray)
  
  ###pull distribution
  pull=data_histo.Clone()
  pull.Add(sum_mc,-1)
  for i in range(pull.GetNbinsX()+2):
    if pull.GetBinError(i)!=0:
      pull.SetBinContent(i,pull.GetBinContent(i)/pull.GetBinError(i))
    else:
      pull.SetBinContent(i,0)
  pull.SetFillColor(kOrange+7)

  # ###drawing top
  # top_pad.cd()
  # stack.Draw('hist')
  # stack.GetXaxis().SetTitle('')
  # stack.GetYaxis().SetTitle(ytitle)
  # stack.GetYaxis().SetLabelSize(charsize)
  # stack.GetYaxis().SetTitleSize(charsize)
  # stack.GetYaxis().SetTitleOffset(offset)
  # stack.GetXaxis().SetLabelSize(0)
  # stack.GetXaxis().SetTitleSize(0)
  # stack.GetXaxis().SetTitleOffset(100)
  # stack.GetXaxis().SetLabelOffset(100)
  # if minx!=0 or maxx!=0:
  #   stack.GetXaxis().SetRangeUser(minx,maxx)
  # #else:
  # #  stack.GetXaxis().SetRangeUser(0,4000)
  # if miny!=0 or maxy!=0:
  #   stack.SetMaximum(maxy)
  #   stack.SetMinimum(miny)
  # else:
  #   if logy:
  #     stack.SetMaximum(stack.GetMaximum()*10)
  #     stack.SetMinimum(0.2)
  #   else:
  #     stack.SetMaximum(stack.GetMaximum()*1.5)
  #     stack.SetMinimum(0.001)
  # err.Draw('2')
  # sum_mc.Draw('samehist')
  # if ttbar_file!=0:
  #   ttbar_line.Draw('samehist')
  # for i in signal_histos:
  #   i.Draw('samehist')
  # data_histo.Draw('p ex0 SAME')
  # if logy:
  #   top_pad.SetLogy()
  # if not separate_legend:
  #   legend.Draw()
  # latex.Draw()



  ###drawing top
  top_pad.cd()
  sum_mc2=sum_mc.Clone()
  sum_mc.SetFillColorAlpha(kRed,0.5)
  sum_mc.SetFillStyle(1001)
  sum_mc.Draw('E2')
  sum_mc2.Draw('hist same')
  sum_mc.SetStats(0)
  sum_mc.GetXaxis().SetTitle('')
  sum_mc.GetYaxis().SetTitle(ytitle)
  sum_mc.GetYaxis().SetLabelSize(charsize)
  sum_mc.GetYaxis().SetTitleSize(charsize)
  sum_mc.GetYaxis().SetTitleOffset(offset)
  sum_mc.GetXaxis().SetLabelSize(0)
  sum_mc.GetXaxis().SetTitleSize(0)
  sum_mc.GetXaxis().SetTitleOffset(100)
  sum_mc.GetXaxis().SetLabelOffset(100)
  if minx!=0 or maxx!=0:
    sum_mc.GetXaxis().SetRangeUser(minx,maxx)
  #else:
  #  sum_mc.GetXaxis().SetRangeUser(0,4000)
  if miny!=0 or maxy!=0:
    sum_mc.SetMaximum(maxy)
    sum_mc.SetMinimum(miny)
  else:
    if logy:
      sum_mc.SetMaximum(sum_mc.GetMaximum()*10)
      sum_mc.SetMinimum(0.2)
    else:
      sum_mc.SetMaximum(sum_mc.GetMaximum()*1.5)
      sum_mc.SetMinimum(0.001)
  #err.Draw('2')
  #sum_mc.Draw('samehist')
  #if ttbar_file!=0:
  #  ttbar_line.Draw('samehist')
  #for i in signal_histos:
  #  i.Draw('samehist')
  data_histo2=data_histo.Clone()
  data_histo.SetFillColorAlpha(kBlack,0.5)
  data_histo.Draw('E2 SAME')
  data_histo2.Draw('histo same')
  if logy:
    top_pad.SetLogy()
  if not separate_legend:
    legend.Draw()
  latex.Draw()

  ###drawing bottom
  bottom_pad.cd()
  pull.SetStats(0)
  pull.SetTitle('')
  pull.Draw('hist')
  if minx!=0 or maxx!=0:
    pull.GetXaxis().SetRangeUser(minx,maxx)
  pull.GetYaxis().SetLabelSize(pullcharsize)
  pull.GetYaxis().SetTitleSize(pullcharsize)
  pull.GetYaxis().SetTitleOffset(pulloffset)
  pull.GetXaxis().SetLabelSize(pullcharsize)
  pull.GetXaxis().SetTitleSize(pullcharsize)
  pull.GetXaxis().SetTitleOffset(1.3)
  pull.GetYaxis().SetTitle('#frac{Data-MC}{#sigma}')#'(Data-MC)/#sigma'
  if xtitle!='':
    pull.GetXaxis().SetTitle(xtitle)
  if fixratio:
    pull.GetYaxis().SetRangeUser(-3.9,3.9)
  pull.GetYaxis().SetNdivisions(4,2,0)
  pull.GetXaxis().SetNdivisions(10,5,0)
  #pull.GetXaxis().SetRangeUser(pull.GetXaxis().GetXmin(),pull.GetXaxis().GetXmax()*zf)
  line1=0
  if minx==0 and maxx==0:
    line1=TLine(pull.GetXaxis().GetXmin(),0.0,pull.GetXaxis().GetXmax(),0.0)
  else:
    line1=TLine(minx,0.0,maxx,0.0)
  line1.SetLineStyle(2)
  line1.SetLineWidth(3)

  line1.Draw()


  ###saving
  canvas.SaveAs('pdf/'+name+'.pdf')
  if outfile!=0:
      canvas.Write()



  ###separate legend
  if separate_legend:
    legendcanvas=TCanvas(name+'_legend','',0,0,600,600)
    legendcanvas.cd()
    legend.SetNColumns(1)
    legend.SetX1(0.0)
    legend.SetX2(1.0)
    legend.SetY1(0.0)
    legend.SetY2(1.0)
    legend.Draw()
    legendcanvas.SaveAs('pdf/'+name+'_legend.pdf')
    if outfile!=0:
      legendcanvas.Write()




def make_comp(mean_histo_orig,up_histo_orig,down_histo_orig,cname,rebin=1):
    mean_histo=mean_histo_orig.Clone()
    up_histo=up_histo_orig.Clone()
    down_histo=down_histo_orig.Clone()
    legend=TLegend(0.65,0.5,0.945,0.895,cname)
    legend.SetFillColor(kWhite)
    legend.SetBorderSize(0)
    legend.SetFillStyle(0)
    canvas=TCanvas(cname+us+'canvas','',0,0,600,600)#,'',100,100)
    canvas.Divide(1,2)
    top_pad=canvas.GetPad(1)
    bottom_pad=canvas.GetPad(2)
    top_pad.SetPad( 0.0, 0.30, 1.0, 1.0 )
    bottom_pad.SetPad( 0.0, 0.0, 1.0, 0.30 )
    #top_pad.SetLeftMargin(0.18)#0.15
    #top_pad.SetRightMargin(0.05)#0.01
    #top_pad.SetTopMargin(0.13)#0.10
    #top_pad.SetBottomMargin(0.15)#0.0
    top_pad.SetLeftMargin(0.15)#
    top_pad.SetRightMargin(0.05)#
    top_pad.SetTopMargin(0.10)#
    top_pad.SetBottomMargin(0.0)#
    bottom_pad.SetLeftMargin(0.15)
    bottom_pad.SetRightMargin(0.05)
    bottom_pad.SetTopMargin(0.0)
    bottom_pad.SetBottomMargin(0.45)
    top_pad.cd()
    up_histo.SetLineWidth(3)
    down_histo.SetLineWidth(3)
    mean_histo.SetLineWidth(3)
    mean_histo.SetLineColor(kBlack)
    mean_histo.SetFillColor(0)
    up_histo.SetLineColor(kRed)
    down_histo.SetLineColor(kBlue)
    up_histo.GetYaxis().SetTitle('Events / 100 GeV')
    up_histo.GetYaxis().SetLabelSize(0.07)
    up_histo.GetYaxis().SetTitleSize(0.07)
    up_histo.GetYaxis().SetTitleOffset(1.15)
    up_histo.GetXaxis().SetLabelSize(0.07)
    up_histo.GetXaxis().SetTitleSize(0.07)
    up_histo.GetXaxis().SetTitleOffset(1.0)
    up_histo.SetStats(0)
    up_histo.SetMinimum(0.1)
    down_histo.SetStats(0)
    mean_histo.SetStats(0)
    mean_histo.Rebin(rebin)
    up_histo.Rebin(rebin)
    down_histo.Rebin(rebin)
    up_histo.SetMaximum(max(up_histo.GetMaximum(),down_histo.GetMaximum(),mean_histo.GetMaximum())*1.2)
    up_histo.Draw('histo')
    mean_histo.Draw('histoSAME')
    down_histo.Draw('histoSAME')
    legend.AddEntry(mean_histo,'normal','l')
    legend.AddEntry(up_histo,'up','l')
    legend.AddEntry(down_histo,'down','l')
    legend.Draw()
    bottom_pad.cd()
    upratio_histo=up_histo.Clone(up_histo.GetName()+'ratio')
    downratio_histo=down_histo.Clone(down_histo.GetName()+'ratio')
    upratio_histo.Divide(mean_histo)
    downratio_histo.Divide(mean_histo)
    upratio_histo.SetStats(0)
    downratio_histo.SetStats(0)
    line1=TLine(upratio_histo.GetXaxis().GetXmin(),1.0,upratio_histo.GetXaxis().GetXmax(),1.0)
    upratio_histo.GetYaxis().SetRangeUser(0.4,1.65)
    upratio_histo.GetYaxis().SetNdivisions(3,2,0)
    #downratio_histo.GetYaxis().SetRangeUser(-0.25,2.25)
    #downratio_histo.GetYaxis().SetNdivisions(3,2,0)
    upratio_histo.SetTitle('') 
    upratio_histo.GetYaxis().SetLabelSize(0.16333)
    upratio_histo.GetYaxis().SetTitleSize(0.16333)
    upratio_histo.GetYaxis().SetTitleOffset(0.4928)
    upratio_histo.GetXaxis().SetLabelSize(0.16333)
    upratio_histo.GetXaxis().SetTitleSize(0.16333)
    upratio_histo.GetXaxis().SetTitleOffset(1.3)
    upratio_histo.GetYaxis().SetTitle('Var/Nor')
    upratio_histo.Draw('histo')
    downratio_histo.Draw('histoSAME')
    line1.SetLineStyle(2)
    line1.Draw()
    canvas.SaveAs('pdf/'+cname+'_comp.pdf')


#   def make_plot_old(histo_name,folder=htfolder,override=False,ttbar1=0,ttbar2=0,bkg1=0,bkg2=0,data1=0,data2=0,err1=0,err2=0): 
#     zf=1
#     legendstring="HEPTopTagger HT>800 GeV"
#     if folder==mjfolder:
#       legendstring="HEPTopTagger HT<800 GeV"
#     if override:
#       legendstring="HEPTopTagger"
#     larghezza=0.7
#     if histo_name in ['Mtt0','Mtt1','Mtt2','Mtt012']:
#       larghezza=0.5
#     legend=TLegend(larghezza,0.5,0.945,0.895,legendstring)
#     legend.SetFillColor(kWhite)
#     legend.SetBorderSize(0)
#     legend.SetFillStyle(0)
#     if histo_name in ['Mtt0','Mtt1','Mtt2','Mtt012']:
#       legend.SetTextSize(0.05)
#     stack=THStack(histo_name+us+'stack','')
#     #ttbar_histo=ttbar_file.Get(cut_name+'/'+histo_name).Clone('ttbar'+us+histo_name+us+cut_name)
#     #qcd_histo=qcd_file.Get(cut_name+'/'+histo_name).Clone('qcd'+us+histo_name+us+cut_name)
#     #data_histo=data_file.Get(cut_name+'/'+histo_name).Clone('data'+us+histo_name+us+cut_name)
#     bkg_histo_name=histo_name
#     measured_histo_name='Measured'+histo_name
#     #if '_0btag_' in cut_name:
#       #bkg_histo_name='Mtt0'
#       #measured_histo_name='MeasuredMtt0'
#     #elif '_1btag_' in cut_name:
#       #bkg_histo_name='Mtt1'
#       #measured_histo_name='MeasuredMtt1'
#     #elif '_2btag_' in cut_name:
#       #bkg_histo_name='Mtt2'
#       #measured_histo_name='MeasuredMtt2'
#     #elif '_012btag_' in cut_name:
#       #bkg_histo_name='Mtt012'
#       #measured_histo_name='MeasuredMtt012'
#     if folder==mjfolder:
#       data_file=mjdata_file
#     else:
#       data_file=htdata_file
#     data_histo=data_file.Get(folder+measured_histo_name).Clone('data'+us+histo_name)
#     bkg_histo=data_file.Get(folder+bkg_histo_name).Clone('bkg'+us+histo_name)#background_file.Get(folder+bkg_histo_name).Clone('bkg'+us+histo_name+us+cut_name)
#     bkg_histo_up=bkg_histo.Clone('bkg'+us+histo_name+'_up')
#     bkg_histo_down=bkg_histo.Clone('bkg'+us+histo_name+'_down')
#     ttbar_histo=ttbar_file.Get(folder+measured_histo_name).Clone('ttbar'+us+histo_name)
#     ttbkg_histo=ttbar_file.Get(folder+bkg_histo_name)
#     qcd_histo=bkg_histo.Clone("aa")#qcd_file.Get(folder+measured_histo_name).Clone('qcd'+us+histo_name)
#     ###mistag error propagation
#     sys_diff=[]
#     for imtt in range(1,ttbar_histo.GetNbinsX()+1):
#       sys_diff.append([])
#     for isys in range(1,len(systematics)):
#       ttf=TFile(path_base+cyclename+'TTbar'+systematics[isys]+'.root','READ')
#       outfile.cd()
#       ttbar_tmp=ttf.Get(folder+measured_histo_name).Clone('ttbar'+theta_sys[isys])
#       ttbar_tmp.Add(ttbar_histo,-1)
#       for imtt in range(1,ttbar_histo.GetNbinsX()+1):
#         sys_diff[imtt-1].append(ttbar_tmp.GetBinContent(imtt))
    
#     doaverageq2=True
#     ttbar_q2up=ttbar_histo.Clone('ttbar_q2up')
#     ttbar_q2down=ttbar_histo.Clone('ttbar_q2down')
#     if doaverageq2:
#       ttf_up=TFile(path_base+cyclename+'TTbar'+'_scaleup'+'.root','READ')
#       ttf_down=TFile(path_base+cyclename+'TTbar'+'_scaledown'+'.root','READ')
#       tt_up=ttf_up.Get(folder+measured_histo_name).Clone('ttbar_q2up')
#       tt_down=ttf_down.Get(folder+measured_histo_name).Clone('ttbar_q2down')
#       tt_updiff=ttbar_histo.Clone('tt_updiff')
#       tt_downdiff=ttbar_histo.Clone('tt_downdiff')
#       tt_updiff.Add(tt_up,-1)
#       tt_downdiff.Add(tt_down,-1)
#       for imtt in range(1,ttbar_histo.GetNbinsX()+1):
#         diff=max(abs(tt_updiff.GetBinContent(imtt)),abs(tt_downdiff.GetBinContent(imtt)))
#         sys_diff[imtt-1].append(diff)
#         sys_diff[imtt-1].append(-diff)
#         ttbar_q2up.SetBinContent(imtt,ttbar_q2up.GetBinContent(imtt)+diff)
#         ttbar_q2down.SetBinContent(imtt,ttbar_q2down.GetBinContent(imtt)-diff)

#     if histo_name=='Mtt0' or histo_name=='Mtt1' or histo_name=='Mtt2':
#       #for imtt in range(1,ttbar_histo.GetNbinsX()+1):
#       #  sys_diff.append([])
#       #for isys in range(1,len(systematics)):
#       #  ttf=TFile(path_base+cyclename+'TTbar'+systematics[isys]+'.root','READ')
#       #  outfile.cd()
#       #  ttbar_tmp=ttf.Get(folder+measured_histo_name).Clone('ttbar'+theta_sys[isys])
#       #  ttbar_tmp.Add(ttbar_histo,-1)
#       #  for imtt in range(1,ttbar_histo.GetNbinsX()+1):
#       #    sys_diff[imtt-1].append(ttbar_tmp.GetBinContent(imtt))
      
#       the_pdfsysfilename='thetapdf.root'
#       if folder==mjfolder:
#         the_pdfsysfilename='mjthetapdf.root'
#       pdffile=TFile(the_pdfsysfilename,"READ")
#       the_namebase='httbtag'
#       if folder==mjfolder:
#         the_namebase='mjhttbtag'
#       uu='__'
#       pdfttbarup=pdffile.Get(the_namebase+histo_name[3]+uu+'ttbar'+uu+'pdf__plus').Clone('pdfup'+the_namebase+histo_name[3])
#       pdfttbardown=pdffile.Get(the_namebase+histo_name[3]+uu+'ttbar'+uu+'pdf__minus').Clone('pdfdown'+the_namebase+histo_name[3])
#       pdfttbarup.Add(ttbar_histo,-1)
#       pdfttbardown.Add(ttbar_histo,-1)
#       for imtt in range(1,ttbar_histo.GetNbinsX()+1):
#         sys_diff[imtt-1].append(pdfttbarup.GetBinContent(imtt))
#         sys_diff[imtt-1].append(pdfttbardown.GetBinContent(imtt))
#       #print sys_diff
#       mistag_matrix=bkg_file.Get(folder+"Mistag/data_htt/Mistag_data_htt")
#       errmtt=data_file.Get(folder+'Err'+histo_name)
#       for mtt_bin in range(1,errmtt.GetNbinsX()+1):
#         a1 = 0.0
#         a2 = 0.0
#         den = 0.0
#         for pt_bin in range(1,errmtt.GetNbinsY()+1):
#           for csv_bin in range(1,errmtt.GetNbinsZ()+1):
#             #print errmtt.GetBinContent(mtt_bin,pt_bin,csv_bin)
#             a1 += mistag_matrix.GetBinContent(pt_bin,csv_bin) * sqrt(errmtt.GetBinContent(mtt_bin,pt_bin,csv_bin))
#             a2 += mistag_matrix.GetBinError(pt_bin,csv_bin) * errmtt.GetBinContent(mtt_bin,pt_bin,csv_bin)
#             den += mistag_matrix.GetBinContent(pt_bin,csv_bin) * errmtt.GetBinContent(mtt_bin,pt_bin,csv_bin)
#             dx=0.0
#             if  den>0.0:
#               dx = sqrt(a1*a1+a2*a2)/ den
#                 #print mtt_bin,dx
#         bkg_histo.SetBinError(mtt_bin, dx * bkg_histo.GetBinContent(mtt_bin))
#         bkg_histo_up.SetBinContent(mtt_bin, bkg_histo.GetBinContent(mtt_bin) + dx * bkg_histo.GetBinContent(mtt_bin))
#         bkg_histo_down.SetBinContent(mtt_bin, bkg_histo.GetBinContent(mtt_bin) - dx * bkg_histo.GetBinContent(mtt_bin))
#     ###
    
#     #ttbkg_histo.Scale(0.92*0.95*0.95*0.92)
#     bkg_histo.Add(ttbkg_histo,-1.0)######################################## ttbar subtraction
#     bkg_histo_up.Add(ttbkg_histo,-1.0)########################################
#     bkg_histo_down.Add(ttbkg_histo,-1.0)########################################
#     sum_mc=ttbar_histo.Clone('sum_mc'+us+histo_name)
#     sum_mc.Add(bkg_histo)
#     err=TGraphAsymmErrors(sum_mc)
#     sysup=[]
#     relsysup=[]
#     sysdown=[]
#     if True:#histo_name=='Mtt0' or histo_name=='Mtt1' or histo_name=='Mtt2':
#       for ierr in range(1,err.GetN()+1):
#         eup=0.
#         edown=0.
#         for i in sys_diff[ierr-1]:
#           #print i
#           if i<0:
#             edown=edown+i*i
#           else:
#             eup=eup+i*i
#         sysup.append(sqrt(eup))
#         relsysup.append(sqrt(eup)/(ttbar_histo.GetBinContent(ierr)+0.00000001))
#         sysdown.append(sqrt(edown))
#         #print eup,err.GetErrorYhigh(ierr)
#         lumierr=0.0263*ttbar_histo.GetBinContent(ierr)
#         trigerr=0#0.0202*ttbar_histo.GetBinContent(ierr)
#         xserr=0.1618*ttbar_histo.GetBinContent(ierr)
#         err.SetPointEYhigh(ierr-1,sqrt(lumierr*lumierr+trigerr*trigerr+xserr*xserr+err.GetErrorYhigh(ierr-1)*err.GetErrorYhigh(ierr-1)+eup))
#         err.SetPointEYlow(ierr-1,sqrt(lumierr*lumierr+trigerr*trigerr+xserr*xserr+err.GetErrorYlow(ierr-1)*err.GetErrorYlow(ierr-1)+edown))
#     #print relsysup
#     if override:
#       ttbarm=ttbar1.Clone()
#       ttbarm.Add(ttbar2)
#       bkgm=bkg1.Clone()
#       bkgm.Add(bkg2)
#       datam=data1.Clone()
#       datam.Add(data2)
#       errm=err1.Clone()
#       sum_mcm=ttbarm.Clone()
#       sum_mcm.Add(bkgm)
#       errm=TGraphAsymmErrors(sum_mcm)
#       for ierr in range(1,err1.GetN()+1):
#         errm.SetPointEYhigh(ierr-1,sqrt(err1.GetErrorYhigh(ierr-1)*err1.GetErrorYhigh(ierr-1)+err2.GetErrorYhigh(ierr-1)*err2.GetErrorYhigh(ierr-1)))
#         errm.SetPointEYlow(ierr-1,sqrt(err1.GetErrorYlow(ierr-1)*err1.GetErrorYlow(ierr-1)+err2.GetErrorYlow(ierr-1)*err2.GetErrorYlow(ierr-1)))
#       sum_mc=sum_mcm
#       data_histo=datam
#       ttbar_histo=ttbarm
#       bkg_histo=bkgm
#       err=errm

#     sum_mc_noerr=sum_mc.Clone('sum_mc_noerr'+us+histo_name)
#     for i in range(1,sum_mc_noerr.GetNbinsX()+1):
#       sum_mc_noerr.SetBinError(i,0)
    
#     data_histo_noerr=data_histo.Clone('data_noerr'+us+histo_name)
#     for i in range(1,data_histo_noerr.GetNbinsX()+1):
#       data_histo_noerr.SetBinError(i,0)
#     ratio_histo_nodataerr=data_histo_noerr.Clone('ratio_nodataerr'+us+histo_name)
#     ratio_histo_nodataerr.Divide(sum_mc)
#     ratio_histo_nodataerr2=ratio_histo_nodataerr.Clone('ratio_nodataerr2'+us+histo_name)
#     for i in range(1,ratio_histo_nodataerr.GetNbinsX()+1):
#       ratio_histo_nodataerr.SetBinContent(i,1)
#       #if ratio_histo_nodataerr.GetBinError(i)==0:
#   #ratio_histo_nodataerr.SetBinError(i,1.25)
#     err_ratio=TGraphAsymmErrors(ratio_histo_nodataerr)
#     if True:#histo_name=='Mtt0' or histo_name=='Mtt1' or histo_name=='Mtt2':
#       for ierr in range(1,err.GetN()+1):
#         if sum_mc.GetBinContent(ierr)>0:
#           val=sum_mc.GetBinContent(ierr)
#           staterr=sum_mc.GetBinError(ierr)
#           #err_ratio.SetPointEYhigh(ierr,sqrt(staterr*staterr/(val*val)+sysup[ierr-1]*sysup[ierr-1]/(val*val)))
#           #err_ratio.SetPointEYlow(ierr,sqrt(staterr*staterr/(val*val)+sysdown[ierr-1]*sysdown[ierr-1]/(val*val)))
#           #print err.GetErrorYhigh(ierr-1),sqrt(staterr*staterr+sysup[ierr-1]*sysup[ierr-1])
#           if data_histo.GetBinContent(ierr)>0:
#             err_ratio.SetPointEYhigh(ierr-1,err.GetErrorYhigh(ierr-1)/val)
#             err_ratio.SetPointEYlow(ierr-1,err.GetErrorYlow(ierr-1)/val)
#           else:
#             err_ratio.SetPointEYhigh(ierr-1,0)
#             err_ratio.SetPointEYlow(ierr-1,0)

    
#     summc=sum_mc.Clone('summc')
#     summc.SetLineColor(kBlack)
#     ratio_histo=data_histo.Clone('ratio'+us+histo_name)
#     ratio_histo.Divide(sum_mc_noerr)
#     ratio_histo.SetLineColor(1)
#     ratio_histo.SetLineStyle(1)
#     ratio_histo.SetLineWidth(1)
#     ratio_histo.SetMarkerColor(1)
#     ratio_histo.SetMarkerStyle(8)
#     ratio_histo.SetMarkerSize(1)
#     ratio_histo.SetStats(0)
#     ratio_histo.SetTitle('') 
#     ratio_histo.GetYaxis().SetLabelSize(0.16333)
#     ratio_histo.GetYaxis().SetTitleSize(0.16333)
#     ratio_histo.GetYaxis().SetTitleOffset(0.4928)
#     ratio_histo.GetXaxis().SetLabelSize(0.16333)
#     ratio_histo.GetXaxis().SetTitleSize(0.16333)
#     ratio_histo.GetXaxis().SetTitleOffset(1.3)
#     ratio_histo.GetYaxis().SetTitle('Data/Bkg')
#     #ratio_histo.GetXaxis().SetTitle('m_{t#bar{t}} [GeV]')
#     ratio_histo.GetYaxis().SetRangeUser(-0.25,2.25)
#     ratio_histo.GetYaxis().SetNdivisions(3,2,0)
#     #ratio_histo.GetXaxis().SetRangeUser(ratio_histo.GetXaxis().GetXmin(),ratio_histo.GetXaxis().GetXmax()*zf)
#     line1=TLine(ratio_histo.GetXaxis().GetXmin(),1.0,ratio_histo.GetXaxis().GetXmax(),1.0)#*zf
#     line1.SetLineStyle(2)
#     ttbar_histo.SetFillColor(kRed)
#     qcd_histo.SetFillColor(kYellow)
#     bkg_histo.SetFillColor(kYellow)
#     ttbar_histo.SetLineColor(kRed)
#     qcd_histo.SetLineColor(kYellow)
#     bkg_histo.SetLineColor(kYellow)
#     ttbar_histo.SetMarkerColor(kRed)
#     qcd_histo.SetMarkerColor(kYellow)
#     bkg_histo.SetMarkerColor(kYellow)
#     data_histo.SetLineColor(1)
#     data_histo.SetLineStyle(1)
#     data_histo.SetLineWidth(1)
#     data_histo.SetMarkerColor(1)
#     data_histo.SetMarkerStyle(8)
#     data_histo.SetMarkerSize(1)
#     #data_histo.GetXaxis().SetRangeUser(data_histo.GetXaxis().GetXmin(),data_histo.GetXaxis().GetXmax()*zf)
#     legend.AddEntry(data_histo,'Data','pEX0')
#     legend.AddEntry(ttbar_histo,'t#bar{t}','f')
#     #legend.AddEntry(qcd_histo,'QCD MC','f')
#     legend.AddEntry(bkg_histo,'NTMJ','f')
#     stack.Add(ttbar_histo)
#     #stack.Add(qcd_histo)
#     stack.Add(bkg_histo)
#     cmslabelstring="CMS Preliminary #sqrt{s} = 8TeV  19.7 fb^{-1}"
#     if folder==mjfolder:
#       cmslabelstring="CMS Preliminary #sqrt{s} = 8TeV  18.3 fb^{-1}"
#     if override:
#       cmslabelstring="CMS Preliminary #sqrt{s} = 8TeV  18.3-19.7 fb^{-1}"
#     cmslabel=TLatex(0.15,0.925,cmslabelstring)
#     #cmslabel=TLatex(0.15,0.925,"Private work")
#     cmslabel.SetTextSize(0.07)
#     cmslabel.SetNDC()
#     cmslabel.SetTextFont(42)
#     #cmslabel.SetLineWidth(5)
    
#     signal1000=signal_files[process_names_signal_narrow.index('750')].Get(folder+measured_histo_name).Clone('ZP1000'+us+histo_name)
#     signal2000=signal_files[process_names_signal_narrow.index('1000')].Get(folder+measured_histo_name).Clone('ZP2000'+us+histo_name)
#     signal3000=signal_files[process_names_signal_narrow.index('1250')].Get(folder+measured_histo_name).Clone('ZP3000'+us+histo_name)
#     if override:
#       signal1000.Add(signal_files[process_names_signal_narrow.index('750')].Get(mjfolder+measured_histo_name).Clone('ZP1000'+us+histo_name))
#       signal2000.Add(signal_files[process_names_signal_narrow.index('1000')].Get(mjfolder+measured_histo_name).Clone('ZP2000'+us+histo_name))
#       signal3000.Add(signal_files[process_names_signal_narrow.index('1250')].Get(mjfolder+measured_histo_name).Clone('ZP3000'+us+histo_name))
#     signal1000.SetLineWidth(3)
#     signal1000.SetLineStyle(1)
#     signal2000.SetLineWidth(3)
#     signal2000.SetLineStyle(1)
#     signal3000.SetLineWidth(3)
#     signal3000.SetLineStyle(1)
#     signal1000.SetLineColor(28)
#     signal2000.SetLineColor(9)
#     signal3000.SetLineColor(8)
#     signal1000.Scale(3.0)
#     signal2000.Scale(3.0)
#     signal3000.Scale(3.0)
#     legend.AddEntry(signal1000,"Z' 750 GeV 3pb",'l')
#     legend.AddEntry(signal2000,"Z' 1.0 TeV 3pb",'l')
#     legend.AddEntry(signal3000,"Z' 1.25 TeV 3pb",'l')
    
#     mjpostfix=''
#     if folder==mjfolder:
#       mjpostfix='mj'
#     canvas=TCanvas(histo_name+mjpostfix+us+'canvas','',0,0,600,600)#,'',100,100)
#     canvas.Divide(1,2)
#     top_pad=canvas.GetPad(1)
#     bottom_pad=canvas.GetPad(2)
#     top_pad.SetPad( 0.0, 0.30, 1.0, 1.0 )
#     bottom_pad.SetPad( 0.0, 0.0, 1.0, 0.30 )
#     #top_pad.SetLeftMargin(0.18)#0.15
#     #top_pad.SetRightMargin(0.05)#0.01
#     #top_pad.SetTopMargin(0.13)#0.10
#     #top_pad.SetBottomMargin(0.15)#0.0
#     top_pad.SetLeftMargin(0.15)#
#     top_pad.SetRightMargin(0.05)#
#     top_pad.SetTopMargin(0.10)#
#     top_pad.SetBottomMargin(0.0)#
#     bottom_pad.SetLeftMargin(0.15)
#     bottom_pad.SetRightMargin(0.05)
#     bottom_pad.SetTopMargin(0.0)
#     bottom_pad.SetBottomMargin(0.45)
#     top_pad.cd()
#     stack.Draw('hist')
#     err.SetFillStyle(3145)
#     err.SetFillColor(kGray)
#     err.Draw('2')
#     data_histo.Draw("sameEX0")
#     #if histo_name not in ['Mtt0','Mtt1','Mtt2','Mtt012']:
#     summc.Draw('samehist')
#     stack.SetMinimum(0.1)
#     stack.SetMaximum(stack.GetMaximum()*1.2)
#     stack.GetXaxis().SetTitle("a")#ttbar_histo.GetXaxis().GetTitle())
#     stack.GetYaxis().SetTitle('Events')
#     stack.GetYaxis().SetLabelSize(0.07)
#     stack.GetYaxis().SetTitleSize(0.07)
#     stack.GetYaxis().SetTitleOffset(1.15)
#     stack.GetXaxis().SetLabelSize(0.07)
#     stack.GetXaxis().SetTitleSize(0.07)
#     stack.GetXaxis().SetTitleOffset(1.0)
# #stack.GetYaxis().SetRangeUser(stack.GetYaxis().GetXmin(),stack.GetYaxis().GetXmax()*1.5)
    
#     #stack.GetYaxis().SetLabelSize(0.045)
#     #stack.GetYaxis().SetTitleSize(0.045)
#     #stack.GetYaxis().SetTitleOffset(1.9)
#     #stack.GetXaxis().SetLabelSize(0.045)
#     #stack.GetXaxis().SetTitleSize(0.045)
#     #stack.GetXaxis().SetTitleOffset(1.5)
    
#     #stack.GetXaxis().SetRangeUser(stack.GetXaxis().GetXmin(),stack.GetXaxis().GetXmax()*zf)
#     signal1000.Draw('samehist')
#     signal2000.Draw('samehist')
#     signal3000.Draw('samehist')
#     legend.Draw()
#     cmslabel.Draw()
#     bottom_pad.cd()
#     err_ratio.SetFillStyle(1001)
#     err_ratio.SetFillColor(kGray)
#     ratio_histo.Draw('EX0')
#     err_ratio.Draw('same2')
#     ratio_histo.Draw('sameEX0')
#     line1.Draw()
#     #outfile.cd(cut_name)
#     outfile.cd()
#     canvas.Write()
#     overridepostfix=''
#     if override:
#       overridepostfix='merge'
#     canvas.SaveAs('pdf/'+folder+canvas.GetName()+overridepostfix+'.pdf')
#     if histo_name in ['Mtt0','Mtt1','Mtt2','Mtt012']:
#       canvas.SaveAs('pdf/'+folder+canvas.GetName()+overridepostfix+'.png')
#     bkg_histo.Write()
#     bkg_histo_up.Write()
#     bkg_histo_down.Write()
#     return [bkg_histo,bkg_histo_up,bkg_histo_down,ttbar_q2up,ttbar_q2down,ttbar_histo,data_histo,err]
    
#   #for i in range(len(histo_name_list)):
#   #  for j in range(len(histo_folder_list)):