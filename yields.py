import os, sys
from wzanalysis.plotterconf import *
basepath = os.path.abspath(__file__).rsplit('/xuAnalysis/',1)[0]+'/xuAnalysis/'
sys.path.append(basepath)
from plotter.TopHistoReader import TopHistoReader, Process
from ROOT.TMath import Sqrt as sqrt
from ROOT import kRed, kOrange, kBlue, kTeal, kGreen, kGray, kAzure, kPink, kCyan, kBlack, kSpring, kViolet, kYellow
from framework.functions import GetLumi
from ROOT import TCanvas, gROOT
gROOT.SetBatch(1)

def GetYield(path, files, ch = 'eee', level = 'sr', histopref = '', filepref = '', var = '', isdata = False):
  t = TopHistoReader(path, files)
  t.SetLevel(level)
  t.SetChan(ch)
  t.SetHistoNamePrefix(histopref)
  #t.SetLumi(GetLumi(2018)*1000)
  #t.SetLumi(GetLumi(year)*1000)
  #t.SetLumi(1)
  t.SetFileNamePrefix(filepref)
  t.SetIsData(isdata)
  if var != '':
    pref = histopref + '_' if histopref != '' else ''
    h = t.GetNamedHisto(pref + var + '_' + ch)
    y = h.GetBinError(9)
  else:  
    y = t.GetYield()
  return y

from wzanalysis.wzanalysis import lev, level, ch, chan

#path = '/pool/ciencias/nanoAODv4/5TeV/5TeV_21nov2019/'
path = '/nfs/fanae/user/joanrs/xuAnalysis/tempWZ12/'
#process = ['WZTo3LNU_NNPDF30_TuneCP5_5p20TeV','DYJetsToLL_MLL_50_TuneCP5_5020GeV_amcatnloFXFX','DYJetsToLL_M_10to50_TuneCP5_5020GeV_amcatnloFXFX','ZZTo2L2Nu_5p02TeV','ZZTo4L_5p02TeV','WWTo2L2Nu_NNPDF31_TuneCP5_5p02TeV', 'tW_5f_noFullHad_TuneCP5_PSweights_5p02TeV_py, tW_5f_noFullHad_TuneCP5_5p02TeV', 'tbarW_5f_noFullHad_TuneCP5_PSweights_5p02TeV_powhe, tbarW_5f_noFullHad_TuneCP5_5p02TeV', 'TT_TuneCP5_PSweights_5p02TeV' ]
t = TopHistoReader(path)
t.SetLumi(Lumi)
PR=[];TT=[]; DY=[]; VV=[]; WZ=[]; Da=[]; ZZ=[]; WW=[];
#process  = ['WZTo3LNU']
process = ['WZTo3LNU','DYJetsToLL_MLL50', 'DYJetsToLL_M_10to50','ZZTo2L2Nu','ZZTo4L','WWTo2L2Nu','tW_noFullHad','tbarW_noFullHad','TT', 'HighEGJet','SingleMuon']
name = ['WZ', 'DY_M50','DY_M10to50', 'ZZto2L2Nu', 'ZZto4L', 'WW', 'tW', 'tbarW', 'TT', 'HighEGJet','SingleMuon']
chn = ['All','eee','mee','emm','mmm']
level = {lev.lep:'lep', lev.tight : 'tight', lev.met:'met', lev.wpt:'wpt', lev.zpt:'zpt', lev.m3l:'m3l', lev.htmiss:'htmiss', lev.sr:'sr', lev.tight:'tight', lev.srtight:'srtight'}
#level={lev.tight:'tight'}

for l in level.keys():
 print 
 print level[l]
 TT=[]; DY=[]; VV=[]; WZ=[]; Da=[]; Sig=[]; Back=[]; ZZ=[]; WW=[];
 for pr in process:
  PR.append(pr)
  for c in chan.keys():
   if pr=='WZTo3LNU':
    WZ.append(GetYield(path, pr, chan[c], level=level[l])*Lumi)
   elif pr=='HighEGJet' or pr=='SingleMuon':
    Da.append(GetYield(path, pr, chan[c], level=level[l]))
   elif pr=='DYJetsToLL_MLL50' or pr=='DYJetsToLL_M_10to50':
    DY.append(GetYield(path, pr, chan[c], level=level[l])*Lumi)
   #elif pr=='WWTo2L2Nu' or pr=='ZZTo2L2Nu' or pr=='ZZTo4L':
   # VV.append(GetYield(path, pr, chan[c], level=level[l])*Lumi)
   elif pr=='WWTo2L2Nu':
    WW.append(GetYield(path, pr, chan[c], level=level[l])*Lumi)
   elif pr=='ZZTo2L2Nu' or pr=='ZZTo4L':
    ZZ.append(GetYield(path, pr, chan[c], level=level[l])*Lumi)
   elif pr=='tW_noFullHad' or pr=='tbarW_noFullHad' or pr=='TT':
    TT.append(GetYield(path, pr, chan[c], level=level[l])*Lumi)

 print 'WZ', sum(WZ), WZ
 print 'DY', sum(DY)
 print 'TT', sum(TT)
 print 'ZZ', sum(ZZ)
 print 'WW', sum(WW)
 print 'VV', sum(ZZ+WW)
 #print 'Data', sum(Da)
 print 'Sig/sqrt(Sig+Back)', sum(WZ)/sqrt(sum(WZ+DY+TT+ZZ+WW))
