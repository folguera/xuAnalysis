import os, sys
basepath = os.path.abspath(__file__).rsplit('/xuAnalysis/',1)[0]+'/xuAnalysis/'
sys.path.append(basepath)
from framework.functions import GetLumi
from plotter.TopHistoReader import TopHistoReader, HistoManager
from plotter.Plotter import Stack
from ROOT.TMath import Sqrt as sqrt
from ROOT import kRed, kOrange, kBlue, kTeal, kGreen, kGray, kAzure, kPink, kCyan, kBlack, kSpring, kViolet, kYellow

### Input and output
#path = '../temp5TeV/sep17/'
path = '../tempWZ12/'
outpath = '/nfs/fanae/user/joanrs/www/5TeV/plotsWZ/m3l100/cuts/'

### Definition of the processes
processDic = {
'WZ'  : 'WZTo3LNU',
'WW'  : 'WWTo2L2Nu',
'ZZ'  : 'ZZTo2L2Nu,ZZTo4L',
'DY'  : 'DYJetsToLL_M_10to50,DYJetsToLL_MLL50',
'top'  : 'TT,tW_noFullHad,tbarW_noFullHad',
'data': 'HighEGJet, SingleMuon'}##SingleMuon
processes = ['ZZ', 'WW', 'top', 'DY',  'WZ']

process = processDic
### Definition of colors for the processes
colors ={
'WZ'  : kOrange,
'WW'  : kGray+2,
'ZZ'  : kGreen+2,
'DY'  : kCyan+1,
'top' : kRed+1,
'data': 1}
#'WZ'  : kYellow-4,
#'VV'  : kGray+2,
#'DY'  : kAzure-8,
#'top' : kRed+1,
#'data': 1}

systematics = 'MuonEff, ElecEff'#, TrigEff, Prefire, JES, JER, ISR, FSR'

Lumi = 296.1 #294.24 #296.1

def GetName(var, chan, lev):
  return (var + '_' + chan + '_' + lev) if lev != '' else (var + '_' + chan)

def GetAllCh(var, lev):
  return [GetName(var,'eee',lev), GetName(var,'emm',lev), GetName(var,'mee',lev), GetName(var,'mmm',lev)]

