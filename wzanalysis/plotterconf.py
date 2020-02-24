
import os, sys
basepath = os.path.abspath(__file__).rsplit('/xuAnalysis/',1)[0]+'/xuAnalysis/'
print basepath
sys.path.append(basepath)
from framework.functions import GetLumi
from plotter.TopHistoReader import TopHistoReader, HistoManager
from plotter.Plotter import Stack
from ROOT.TMath import Sqrt as sqrt
from ROOT import kRed, kOrange, kBlue, kTeal, kGreen, kGray, kAzure, kPink, kCyan, kBlack, kSpring, kViolet, kYellow

### Input and output
path_3l   = '/nfs/fanae/user/folgueras/SMP/5TeV/xuAnalysis/Feb20_WZ_3L_noSyst/'
path_2lss = '/nfs/fanae/user/folgueras/SMP/5TeV/xuAnalysis/Feb20_WZ_2LSS_noSyst/'

outpath    = '/nfs/fanae/user/folgueras/www/5TeV/plotsWZ/Feb24/'
outpath_3l = '/nfs/fanae/user/folgueras/www/5TeV/plotsWZ/Feb24/3L/'
outpath_2lss = '/nfs/fanae/user/folgueras/www/5TeV/plotsWZ/Feb24/2LSS/'

### Definition of the processes
processDic_2lss = {
'WZ'  : 'WZTo3LNU',
'WW'  : 'WWTo2L2Nu',
'ZZ'  : 'ZZTo2L2Nu,ZZTo4L',
'DY'  : 'DYJetsToLL_M_10to50,DYJetsToLL_MLL50',
'top'  : 'TT,tW_noFullHad,tbarW_noFullHad',
'W'    : 'WJets',
'data': 'HighEGJet, SingleMuon'}
processes_2lss = ['ZZ', 'WW', 'top', 'DY',  'WZ', 'W']

processDic_3l = {
'WZ'  : 'WZTo3LNU',
'WW'  : 'WWTo2L2Nu',
'ZZ'  : 'ZZTo2L2Nu,ZZTo4L',
'DY'  : 'DYJetsToLL_M_10to50,DYJetsToLL_MLL50',
'top'  : 'TT,tW_noFullHad,tbarW_noFullHad',
'data': 'HighEGJet, SingleMuon'}
processes_3l   = ['ZZ', 'WW', 'top', 'DY',  'WZ']


#process = processDic

### Definition of colors for the processes
colors ={
'WZ'  : kOrange,
'WW'  : kGray+2,
'ZZ'  : kGreen+2,
'DY'  : kCyan+1,
'top' : kRed+1,
'W'   : kAzure-8,
'data': 1}

systematics = '' #'MuonEff, ElecEff'#, TrigEff, Prefire, JES, JER, ISR, FSR'

Lumi = 296.1 #294.24 #296.1

def GetName(var, chan, lev):
  return (var + '_' + chan + '_' + lev) if lev != '' else (var + '_' + chan)

def GetAllCh(var, lev):
  return [GetName(var,'eee',lev), GetName(var,'emm',lev), GetName(var,'mee',lev), GetName(var,'mmm',lev)]

def GetAllCh3l(var, lev):
  return [GetName(var,'eee',lev), GetName(var,'emm',lev), GetName(var,'mee',lev), GetName(var,'mmm',lev)]

def GetAllCh2l(var, lev):
  return [GetName(var,'ee',lev), GetName(var,'em',lev), GetName(var,'mm',lev)]

