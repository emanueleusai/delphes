from ROOT import TFile,TCanvas,gROOT,gStyle,TLegend,TGraphAsymmErrors,kGreen,kRed,kBlue,kOrange,kSpring,TF1,kAzure,Double, TColor
from os import system
from sys import argv
from os import mkdir
from os.path import exists
from array import array
import math

from utils import compare,hadd,doeff,make_plot,make_ratioplot,make_ratioplot2,make_comp,envelope,make_fitplot
gROOT.SetBatch()

hexcolor=["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"]
intcolor=[TColor.GetColor(i) for i in hexcolor]

file=TFile('Granularity.root')

for i in ['800','1600']:
  for j in ['W','Z']:
    for k in ['SDMass','Mass','Tau32']:
     for l in ['Barrel','HGCAL']:
      print k+'_'+i+'_'+j+'_'+l, ['WZ_M'+i+'_PU0_G0X/h'+k+l+'_'+j,'WZ_M'+i+'_PU0_G1X/h'+k+l+'_'+j,'WZ_M'+i+'_PU0_G2X/h'+k+l+'_'+j,'WZ_M'+i+'_PU0_G6X/h'+k+l+'_'+j]
      fit='gaus'
      fitlow=70
      fithigh=90
      if not ('Mass' in k):
        fit=''
      if j=='Z':
        fitlow=80
        fithigh=100
      rebin=30
      if 'Tau' in k:
        rebin=40

      compare(
      name=k+'_'+i+'_'+j+'_'+l,
      colors=intcolor,
      normalize=True,
      rebin=rebin,

      file_list=[file]*4,
      name_list=['WZ_M'+i+'_PU0_G0X/h'+k+l+'_'+j,'WZ_M'+i+'_PU0_G1X/h'+k+l+'_'+j,'WZ_M'+i+'_PU0_G2X/h'+k+l+'_'+j,'WZ_M'+i+'_PU0_G6X/h'+k+l+'_'+j],
      legend_list=['NoHGCAL','Phase2','Phase2 1/2 tow.','Phase2 1/6 tow.'],
      drawoption='hist c',
      fitlow=[fitlow]*4,
      fithigh=[fithigh]*4,
      fit=fit,
      #ytitle='A.U.',
      #xtitle='SD Mass [GeV]',
      minx=20,maxx=150,
      #miny=0.3,maxy=1.1,rebin=1,
      textsizefactor=0.7)


      compare(
      name=k+'_'+i+'_'+j+'_'+l+'_200',
      colors=intcolor,
      normalize=True,
      rebin=rebin,

      file_list=[file]*3,
      name_list=['WZ_M'+i+'_PU200_G1X/h'+k+l+'_'+j,'WZ_M'+i+'_PU200_G2X/h'+k+l+'_'+j,'WZ_M'+i+'_PU200_G6X/h'+k+l+'_'+j],
      legend_list=['Phase2','Phase2 1/2 tow.','Phase2 1/6 tow.'],
      drawoption='hist c',
      fitlow=[fitlow]*3,
      fithigh=[fithigh]*3,
      fit=fit,
      #ytitle='A.U.',
      #xtitle='SD Mass [GeV]',
      minx=20,maxx=150,
      #miny=0.3,maxy=1.1,rebin=1,
      textsizefactor=0.7)

      compare(
      name='2'+k+'_'+i+'_'+j+'_'+l,
      #colors=intcolor,
      normalize=True,
      rebin=rebin,

      file_list=[file]*6,
      name_list=['WZ_M'+i+'_PU0_G1X/h'+k+l+'_W','WZ_M'+i+'_PU0_G2X/h'+k+l+'_W','WZ_M'+i+'_PU0_G6X/h'+k+l+'_W',
      'WZ_M'+i+'_PU0_G1X/h'+k+l+'_Z','WZ_M'+i+'_PU0_G2X/h'+k+l+'_Z','WZ_M'+i+'_PU0_G6X/h'+k+l+'_Z'],
      legend_list=['Phase2 W','Phase2 1/2 tow. W','Phase2 1/6 tow. W','Phase2 Z','Phase2 1/2 tow. Z','Phase2 1/6 tow. Z'],
      drawoption='hist c',
      colors=[kRed,kBlue,kGreen,kRed+2,kBlue+2,kGreen+2],
      #ytitle='A.U.',
      #xtitle='SD Mass [GeV]',
      minx=20,maxx=150,
      #miny=0.3,maxy=1.1,rebin=1,
      textsizefactor=0.7)

      compare(
      name='2'+k+'_'+i+'_'+j+'_'+l+'_200',
      #colors=intcolor,
      normalize=True,
      rebin=rebin,

      file_list=[file]*6,
      name_list=['WZ_M'+i+'_PU200_G1X/h'+k+l+'_W','WZ_M'+i+'_PU200_G2X/h'+k+l+'_W','WZ_M'+i+'_PU200_G6X/h'+k+l+'_W',
      'WZ_M'+i+'_PU200_G1X/h'+k+l+'_Z','WZ_M'+i+'_PU200_G2X/h'+k+l+'_Z','WZ_M'+i+'_PU200_G6X/h'+k+l+'_Z'],
      legend_list=['Phase2 W','Phase2 1/2 tow. W','Phase2 1/6 tow. W','Phase2 Z','Phase2 1/2 tow. Z','Phase2 1/6 tow. Z'],
      drawoption='hist c',
      colors=[kRed,kBlue,kGreen,kRed+2,kBlue+2,kGreen+2],
      #ytitle='A.U.',
      #xtitle='SD Mass [GeV]',
      minx=20,maxx=150,
      #miny=0.3,maxy=1.1,rebin=1,
      textsizefactor=0.7)


      compare(
      name='PUCompG1X_'+k+'_'+i+'_'+j+'_'+l,
      #colors=intcolor,
      normalize=True,
      rebin=rebin,

      file_list=[file]*4,
      name_list=['WZ_M'+i+'_PU0_G1X/h'+k+l+'_W','WZ_M'+i+'_PU200_G1X/h'+k+l+'_W','WZ_M'+i+'_PU0_G1X/h'+k+l+'_Z','WZ_M'+i+'_PU200_G1X/h'+k+l+'_Z'],
      legend_list=['Phase2 W 0PU','Phase2 W 200PU PUPPI','Phase2 Z 0PU','Phase2 Z 200PU PUPPI'],
      drawoption='hist c',
      colors=[kRed,kBlue,kRed+2,kBlue+2],
      #ytitle='A.U.',
      #xtitle='SD Mass [GeV]',
      minx=20,maxx=150,
      #miny=0.3,maxy=1.1,rebin=1,
      textsizefactor=0.7)

      compare(
      name='PUCompG2X_'+k+'_'+i+'_'+j+'_'+l,
      #colors=intcolor,
      normalize=True,
      rebin=rebin,

      file_list=[file]*4,
      name_list=['WZ_M'+i+'_PU0_G2X/h'+k+l+'_W','WZ_M'+i+'_PU200_G2X/h'+k+l+'_W','WZ_M'+i+'_PU0_G2X/h'+k+l+'_Z','WZ_M'+i+'_PU200_G2X/h'+k+l+'_Z'],
      legend_list=['Phase2 W 0PU','Phase2 W 200PU PUPPI','Phase2 Z 0PU','Phase2 Z 200PU PUPPI'],
      drawoption='hist c',
      colors=[kRed,kBlue,kRed+2,kBlue+2],
      #ytitle='A.U.',
      #xtitle='SD Mass [GeV]',
      minx=20,maxx=150,
      #miny=0.3,maxy=1.1,rebin=1,
      textsizefactor=0.7)

      compare(
      name='PUCompG6X_'+k+'_'+i+'_'+j+'_'+l,
      #colors=intcolor,
      normalize=True,
      rebin=rebin,

      file_list=[file]*4,
      name_list=['WZ_M'+i+'_PU0_G6X/h'+k+l+'_W','WZ_M'+i+'_PU200_G6X/h'+k+l+'_W','WZ_M'+i+'_PU0_G6X/h'+k+l+'_Z','WZ_M'+i+'_PU200_G6X/h'+k+l+'_Z'],
      legend_list=['Phase2 W 0PU','Phase2 W 200PU PUPPI','Phase2 Z 0PU','Phase2 Z 200PU PUPPI'],
      drawoption='hist c',
      colors=[kRed,kBlue,kRed+2,kBlue+2],
      #ytitle='A.U.',
      #xtitle='SD Mass [GeV]',
      minx=20,maxx=150,
      #miny=0.3,maxy=1.1,rebin=1,
      textsizefactor=0.7)

compare(
      name='pt',
      colors=intcolor,
      normalize=True,
      rebin=40,

      file_list=[file]*2,
      name_list=['WZ_M800_PU0_G1X/hPtHGCAL','WZ_M1600_PU0_G1X/hPtHGCAL'],
      legend_list=['M=800 GeV','M=1600 GeV'],
      drawoption='hist c',
      minx=100,maxx=1000,
      textsizefactor=0.7)

compare(
      name='eta',
      colors=intcolor,
      normalize=False,
      rebin=10,

      file_list=[file]*4,
      name_list=['WZ_M800_PU0_G1X/hEtaHGCAL','WZ_M1600_PU0_G1X/hEtaHGCAL','WZ_M800_PU0_G1X/hEtaBarrel','WZ_M1600_PU0_G1X/hEtaBarrel'],
      legend_list=['HGCAL M=800 GeV','HGCAL M=1600 GeV', 'Barrel M=800 GeV','Barrel M=1600 GeV'],
      drawoption='HIST',
      #colors=[kRed,kBlue,kRed+2,kBlue+2],
      ytitle='A.U.',
      xtitle='#eta',
      #minx=1,maxx=1000,
      textsizefactor=0.7)
#pt comparison, eta comparison