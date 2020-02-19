import os, sys, ROOT
from wzanalysis.plotterconf import *
basepath = os.path.abspath(__file__).rsplit('/xuAnalysis/',1)[0]+'/xuAnalysis/'
sys.path.append(basepath)
from plotter.TopHistoReader import TopHistoReader, Process
from ROOT.TMath import Sqrt as sqrt
from ROOT import kRed, kOrange, kBlue, kTeal, kGreen, kGray, kAzure, kPink, kCyan, kBlack, kSpring, kViolet, kYellow
from framework.functions import GetLumi
from ROOT import TCanvas, gROOT
gROOT.SetBatch(1)
print
#####Calcular el #eventos de la region fiducial y la total
path = '/nfs/fanae/user/joanrs/xuAnalysis/tempWZae/'
process = 'WZTo3LNU'
chn = ['eee','mee','emm','mmm']
f = ROOT.TFile.Open(path+process+'.root',"read")
FR=[]; TR=[];
for i in range(len(chn)):
    h1=f.Get('YieldsFid_'+chn[i])
    FR.append(h1.GetEntries())
    h2=f.Get('YieldsTot_'+chn[i])
    TR.append(h2.GetEntries())
    #print chn[i], FR[i]
print 'Fiducial Region', sum(FR)
print 'Total Region', sum(TR)

####Calculo del #eventos de WZ para el level deseado
def GetYield(path, files, ch = 'eee', level = 'sr', inc = None, histopref = '', filepref = '', var = '', isdata = False):
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
    if inc == None:
     h = t.GetNamedHisto(pref + var + '_' + ch)
    else:
     h = t.GetNamedHisto(pref + var + '_' + ch + '_'+inc)
    y = h.GetBinContent(9)
  else:  
    y = t.GetYield()
  return y

from wzanalysis.wzanalysis import lev, level, ch, chan
path = '/nfs/fanae/user/joanrs/xuAnalysis/tempWZ11/'

t = TopHistoReader(path)
t.SetLumi(Lumi)
WZ=[];
process  = ['WZTo3LNU']
chn = ['All','eee','mee','emm','mmm']
level = {lev.lep:'lep', lev.tight : 'tight', lev.met:'met', lev.wpt:'wpt', lev.zpt:'zpt', lev.m3l:'m3l', lev.htmiss:'htmiss', lev.sr:'sr', lev.tight:'tight', lev.srtight:'srtight'}

for l in level.keys():
 if level[l]=='tight': 
  print level[l]
  WZ=[];
  for pr in process:
   for c in chan.keys():
    if pr=='WZTo3LNU':
     WZ.append(GetYield(path, pr, chan[c], level=level[l], var = 'Yields')*Lumi)
     #print chan[c], WZ[c]
print 'WZ', sum(WZ)

####Calculo de aceptancia y eficiencias
print
A =sum(FR)/sum(TR)
print 'A =',A
#print FR
#print WZ
sigm=1.258
Lum=296.1
LumInc=14.2
LumUp=Lum+LumInc
LumDo=Lum-LumInc
sigmaLumUp=abs(1-Lum/LumUp)*100
sigmaLumDo=abs(1-Lum/LumDo)*100
nGenEvent=500000
print
Ef_All =sum(WZ)*nGenEvent/(sum(FR)*Lum*sigm)
Ef_eee =WZ[0]*nGenEvent/(FR[0]*Lum*sigm)
Ef_mee =WZ[1]*nGenEvent/(FR[1]*Lum*sigm)
Ef_emm =WZ[2]*nGenEvent/(FR[2]*Lum*sigm)
Ef_mmm =WZ[3]*nGenEvent/(FR[3]*Lum*sigm)

print 'Ef_All =', Ef_All
print 'Ef_eee =', Ef_eee
print 'Ef_mee =', Ef_mee
print 'Ef_emm =', Ef_emm
print 'Ef_mmm =', Ef_mmm


#####Calculo de secciones eficaces
def GetYield2(path, files, ch = 'eee', level = 'sr', inc = None, histopref = '', filepref = '', var = '', isdata = False):
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
    if inc == None:
     h = t.GetNamedHisto(pref + var + '_' + ch)
    else:
     h = t.GetNamedHisto(pref + var + '_' + ch +'_'+inc)
    y = h.GetBinContent(9)
  else:  
    y = t.GetYield()
  return y

t = TopHistoReader(path)
t.SetLumi(Lumi)
PR=[];TT=[]; DY=[]; VV=[]; WZ=[]; Da=[]; ZZ=[]; WW=[]; Error=[]; nameinc=[]; Efficiency=[]; Background=[];
#process  = ['WZTo3LNU']
process = ['WZTo3LNU','DYJetsToLL_MLL50', 'DYJetsToLL_M_10to50','ZZTo2L2Nu','ZZTo4L','WWTo2L2Nu','tW_noFullHad','tbarW_noFullHad', 'HighEGJet','SingleMuon']
chn = ['All','eee','mee','emm','mmm']
inc = [None,'MuonEffUp','MuonEffDown','ElecEffUp','ElecEffDown','PUUp','PUDown','PrefireUp','PrefireDo','JESUp','JESDown','JERUp','JERDown']
level = {lev.tight:'tight'}

for l in level.keys():
 for i in range(0,len(inc)):
  Da=[];Back=[]; WZ=[];
  for pr in process:
   PR.append(pr)
   for c in chan.keys():
    if pr=='WZTo3LNU': 
     WZ.append(GetYield2(path, pr, chan[c], level=level[l], inc = inc[i], var = 'Yields')*Lumi)
    elif pr=='HighEGJet' or pr=='SingleMuon':
     Da.append(GetYield2(path, pr, chan[c], level=level[l], inc = inc[i]))
    elif pr=='DYJetsToLL_MLL50' or pr=='DYJetsToLL_M_10to50' or pr=='WWTo2L2Nu' or pr=='ZZTo2L2Nu' or pr=='ZZTo4L' or pr=='tW_noFullHad' or pr=='tbarW_noFullHad' or pr=='TT':
     Back.append(GetYield2(path, pr, chan[c], level=level[l], inc = inc[i], var = 'Yields')*Lumi)
  #print WZ
  Ef_WZ =sum(WZ)*nGenEvent/(sum(FR)*Lum*sigm)
  Efficiency.append(100*(Ef_All-Ef_WZ)/Ef_All)
  #Ndata=sum(Back+WZ)
  Nback=sum(Back)
  if inc[i]==None:
    Ndata = sum(Back+WZ)
    Sigma=(Ndata-Nback)/(Ef_All*A*Lum);
    SigmaLumUp=(Ndata-Nback*LumUp/Lum)/(Ef_All*A*LumUp);
    SigmaLumDo=(Ndata-Nback*LumDo/Lum)/(Ef_All*A*LumDo);
    NB=Nback
  else:
    sigma=(Ndata-Nback)/(Ef_WZ*A*Lum);
    #print '', Sigma, sigma
    Background.append(100*(NB-Nback)/NB)
    nameinc.append(inc[i])
    Error.append((100*(Sigma-sigma)/Sigma))
print
for j in range(0,len(Error)):
 print nameinc[j],'=', Error[j], 'Eff=', Efficiency[j+1], 'Nback=', Background[j]
print 'LumUp', '=', ((1+NB/sum(WZ))*(1-Lum/LumUp))*100, 'Nback=', 100*(NB-NB*LumUp/Lum)/NB
print 'LumDo', '=', ((1+NB/sum(WZ))*(1-Lum/LumDo))*100, 'Nback=', 100*(NB-NB*LumDo/Lum)/NB


def GetYield3(path, files, ch = 'eee', level = 'sr', inc = None, histopref = '', filepref = '', var = '', isdata = False):
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
    if inc == None:
     h = t.GetNamedHisto(pref + var + '_' + ch)
    else:
     h = t.GetNamedHisto(pref + var + '_' + ch +'_'+inc)
    y = h.GetBinContent(9)+h.GetBinError(9)
  else:  
    y = t.GetYield()
  return y

def GetYield4(path, files, ch = 'eee', level = 'sr', inc = None, histopref = '', filepref = '', var = '', isdata = False):
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
    if inc == None:
     h = t.GetNamedHisto(pref + var + '_' + ch)
    else:
     h = t.GetNamedHisto(pref + var + '_' + ch +'_'+inc)
    y = h.GetBinContent(9)-h.GetBinError(9)
  else:  
    y = t.GetYield()
  return y

PR=[];TT=[]; DY=[]; VV=[]; WZ=[]; Da=[]; ZZ=[]; WW=[]; ErrorU=[]; nameinc=[]; EfficiencyU=[]; BackgroundU=[];
#process  = ['WZTo3LNU']
process = ['WZTo3LNU','DYJetsToLL_MLL50', 'DYJetsToLL_M_10to50','ZZTo2L2Nu','ZZTo4L','WWTo2L2Nu','tW_noFullHad','tbarW_noFullHad', 'HighEGJet','SingleMuon']
chn = ['All','eee','mee','emm','mmm']
inc = [None]
level = {lev.tight:'tight'}

for l in level.keys():
 for i in range(0,len(inc)):
  DaU=[];BackU=[]; WZU=[]; DaD=[];BackD=[]; WZD=[];
  for pr in process:
   PR.append(pr)
   for c in chan.keys():
    if pr=='WZTo3LNU': 
     WZU.append(GetYield3(path, pr, chan[c], level=level[l], inc = inc[i], var = 'Yields')*Lumi)
     WZD.append(GetYield4(path, pr, chan[c], level=level[l], inc = inc[i], var = 'Yields')*Lumi)
    elif pr=='HighEGJet' or pr=='SingleMuon':
     DaU.append(GetYield2(path, pr, chan[c], level=level[l], inc = inc[i]))
     DaD.append(GetYield2(path, pr, chan[c], level=level[l], inc = inc[i]))
    elif pr=='DYJetsToLL_MLL50' or pr=='DYJetsToLL_M_10to50' or pr=='WWTo2L2Nu' or pr=='ZZTo2L2Nu' or pr=='ZZTo4L' or pr=='tW_noFullHad' or pr=='tbarW_noFullHad' or pr=='TT':
     BackU.append(GetYield2(path, pr, chan[c], level=level[l], inc = inc[i], var = 'Yields')*Lumi)
     BackD.append(GetYield2(path, pr, chan[c], level=level[l], inc = inc[i], var = 'Yields')*Lumi)
  #print WZ
  Ef_WZU =sum(WZU)*nGenEvent/(sum(FR)*Lum*sigm)
  Ef_WZD =sum(WZD)*nGenEvent/(sum(FR)*Lum*sigm)
  EfficiencyU.append(100*(Ef_All-Ef_WZU)/Ef_All)
  EfficiencyU.append(100*(Ef_All-Ef_WZD)/Ef_All)
  NdataU=sum(WZU+BackU)
  NbackU=sum(BackU)
  NdataD=sum(WZD+BackD)
  NbackD=sum(BackD)
  sigmaU=(Ndata-NbackU)/(Ef_WZU*A*Lum);
  sigmaD=(Ndata-NbackD)/(Ef_WZD*A*Lum);
  BackgroundU.append(100*(NB-NbackU)/NB)
  BackgroundU.append(100*(NB-NbackD)/NB)
  ErrorU.append((100*(Sigma-sigmaU)/Sigma))
  ErrorU.append((100*(Sigma-sigmaD)/Sigma))
print 'MCSigUp','=', ErrorU[0], 'Eff=', EfficiencyU[0], 'Nback=', BackgroundU[0]
print 'MCSigDown','=', ErrorU[1], 'Eff=', EfficiencyU[1], 'Nback=', BackgroundU[1]

PR=[];TT=[]; DY=[]; VV=[]; WZ=[]; Da=[]; ZZ=[]; WW=[]; ErrorU=[]; nameinc=[]; EfficiencyU=[]; BackgroundU=[];
for l in level.keys():
 for i in range(0,len(inc)):
  DaU=[];BackU=[]; WZU=[]; DaD=[];BackD=[]; WZD=[]; DYUp=[]; DYDo=[];
  for pr in process:
   PR.append(pr)
   for c in chan.keys():
    if pr=='WZTo3LNU': 
     WZU.append(GetYield2(path, pr, chan[c], level=level[l], inc = inc[i], var = 'Yields')*Lumi)
     WZD.append(GetYield2(path, pr, chan[c], level=level[l], inc = inc[i], var = 'Yields')*Lumi)
    elif pr=='HighEGJet' or pr=='SingleMuon':
     DaU.append(GetYield2(path, pr, chan[c], level=level[l], inc = inc[i]))
     DaD.append(GetYield2(path, pr, chan[c], level=level[l], inc = inc[i]))
    elif pr=='DYJetsToLL_MLL50' or pr=='DYJetsToLL_M_10to50':
     BackU.append(GetYield3(path, pr, chan[c], level=level[l], inc = inc[i], var = 'Yields')*Lumi)
     BackD.append(GetYield4(path, pr, chan[c], level=level[l], inc = inc[i], var = 'Yields')*Lumi)
     DYUp.append(GetYield3(path, pr, chan[c], level=level[l], inc = inc[i], var = 'Yields')*Lumi)
     DYDo.append(GetYield4(path, pr, chan[c], level=level[l], inc = inc[i], var = 'Yields')*Lumi)
    elif pr=='WWTo2L2Nu' or pr=='ZZTo2L2Nu' or pr=='ZZTo4L' or pr=='tW_noFullHad' or pr=='tbarW_noFullHad' or pr=='TT':
     BackU.append(GetYield2(path, pr, chan[c], level=level[l], inc = inc[i], var = 'Yields')*Lumi)
     BackD.append(GetYield2(path, pr, chan[c], level=level[l], inc = inc[i], var = 'Yields')*Lumi)
  #print WZ
  Ef_WZU =sum(WZU)*nGenEvent/(sum(FR)*Lum*sigm)
  Ef_WZD =sum(WZD)*nGenEvent/(sum(FR)*Lum*sigm)
  EfficiencyU.append(100*(Ef_All-Ef_WZU)/Ef_All)
  EfficiencyU.append(100*(Ef_All-Ef_WZD)/Ef_All)
  NdataU=sum(WZU+BackU)
  NbackU=sum(BackU)
  NdataD=sum(WZD+BackD)
  NbackD=sum(BackD)
  sigmaU=(Ndata-NbackU)/(Ef_WZU*A*Lum);
  sigmaD=(Ndata-NbackD)/(Ef_WZD*A*Lum);
  BackgroundU.append(100*(NB-NbackU)/NB)
  BackgroundU.append(100*(NB-NbackD)/NB)
  ErrorU.append((100*(Sigma-sigmaU)/Sigma))
  ErrorU.append((100*(Sigma-sigmaD)/Sigma))
print 'MCDYUp','=', ErrorU[0], 'Eff=', EfficiencyU[0], 'Nback=', BackgroundU[0]
print 'MCDYDown','=', ErrorU[1], 'Eff=', EfficiencyU[1], 'Nback=', BackgroundU[1]
print sum(DYUp), sum(DYDo)
PR=[];TT=[]; DY=[]; VV=[]; WZ=[]; Da=[]; ZZ=[]; WW=[]; ErrorU=[]; nameinc=[]; EfficiencyU=[]; BackgroundU=[];
for l in level.keys():
 for i in range(0,len(inc)):
  DaU=[];BackU=[]; WZU=[]; DaD=[];BackD=[]; WZD=[];
  for pr in process:
   PR.append(pr)
   for c in chan.keys():
    if pr=='WZTo3LNU': 
     WZU.append(GetYield2(path, pr, chan[c], level=level[l], inc = inc[i], var = 'Yields')*Lumi)
     WZD.append(GetYield2(path, pr, chan[c], level=level[l], inc = inc[i], var = 'Yields')*Lumi)
    elif pr=='HighEGJet' or pr=='SingleMuon':
     DaU.append(GetYield2(path, pr, chan[c], level=level[l], inc = inc[i]))
     DaD.append(GetYield2(path, pr, chan[c], level=level[l], inc = inc[i]))
    elif pr=='ZZTo2L2Nu' or pr=='ZZTo4L':
     BackU.append(GetYield3(path, pr, chan[c], level=level[l], inc = inc[i], var = 'Yields')*Lumi)
     BackD.append(GetYield4(path, pr, chan[c], level=level[l], inc = inc[i], var = 'Yields')*Lumi)
    elif pr=='WWTo2L2Nu' or pr=='DYJetsToLL_MLL50' or pr=='DYJetsToLL_M_10to50' or pr=='tW_noFullHad' or pr=='tbarW_noFullHad' or pr=='TT':
     BackU.append(GetYield2(path, pr, chan[c], level=level[l], inc = inc[i], var = 'Yields')*Lumi)
     BackD.append(GetYield2(path, pr, chan[c], level=level[l], inc = inc[i], var = 'Yields')*Lumi)
  #print WZ
  Ef_WZU =sum(WZU)*nGenEvent/(sum(FR)*Lum*sigm)
  Ef_WZD =sum(WZD)*nGenEvent/(sum(FR)*Lum*sigm)
  EfficiencyU.append(100*(Ef_All-Ef_WZU)/Ef_All)
  EfficiencyU.append(100*(Ef_All-Ef_WZD)/Ef_All)
  NdataU=sum(WZU+BackU)
  NbackU=sum(BackU)
  NdataD=sum(WZD+BackD)
  NbackD=sum(BackD)
  sigmaU=(Ndata-NbackU)/(Ef_WZU*A*Lum);
  sigmaD=(Ndata-NbackD)/(Ef_WZD*A*Lum);
  BackgroundU.append(100*(NB-NbackU)/NB)
  BackgroundU.append(100*(NB-NbackD)/NB)
  ErrorU.append((100*(Sigma-sigmaU)/Sigma))
  ErrorU.append((100*(Sigma-sigmaD)/Sigma))
print 'MCZZUp','=', ErrorU[0], 'Eff=', EfficiencyU[0], 'Nback=', BackgroundU[0]
print 'MCZZDown','=', ErrorU[1], 'Eff=', EfficiencyU[1], 'Nback=', BackgroundU[1]

PR=[];TT=[]; DY=[]; VV=[]; WZ=[]; Da=[]; ZZ=[]; WW=[]; ErrorU=[]; nameinc=[]; EfficiencyU=[]; BackgroundU=[];
for l in level.keys():
 for i in range(0,len(inc)):
  DaU=[];BackU=[]; WZU=[]; DaD=[];BackD=[]; WZD=[];
  for pr in process:
   PR.append(pr)
   for c in chan.keys():
    if pr=='WZTo3LNU': 
     WZU.append(GetYield2(path, pr, chan[c], level=level[l], inc = inc[i], var = 'Yields')*Lumi)
     WZD.append(GetYield2(path, pr, chan[c], level=level[l], inc = inc[i], var = 'Yields')*Lumi)
    elif pr=='HighEGJet' or pr=='SingleMuon':
     DaU.append(GetYield2(path, pr, chan[c], level=level[l], inc = inc[i]))
     DaD.append(GetYield2(path, pr, chan[c], level=level[l], inc = inc[i]))
    elif pr=='WWTo2L2Nu':
     BackU.append(GetYield3(path, pr, chan[c], level=level[l], inc = inc[i], var = 'Yields')*Lumi)
     BackD.append(GetYield4(path, pr, chan[c], level=level[l], inc = inc[i], var = 'Yields')*Lumi)
    elif  pr=='DYJetsToLL_MLL50' or pr=='DYJetsToLL_M_10to50' or pr=='ZZTo2L2Nu' or pr=='ZZTo4L' or pr=='tW_noFullHad' or pr=='tbarW_noFullHad' or pr=='TT':
     BackU.append(GetYield2(path, pr, chan[c], level=level[l], inc = inc[i], var = 'Yields')*Lumi)
     BackD.append(GetYield2(path, pr, chan[c], level=level[l], inc = inc[i], var = 'Yields')*Lumi)
  #print WZ
  Ef_WZU =sum(WZU)*nGenEvent/(sum(FR)*Lum*sigm)
  Ef_WZD =sum(WZD)*nGenEvent/(sum(FR)*Lum*sigm)
  EfficiencyU.append(100*(Ef_All-Ef_WZU)/Ef_All)
  EfficiencyU.append(100*(Ef_All-Ef_WZD)/Ef_All)
  NdataU=sum(WZU+BackU)
  NbackU=sum(BackU)
  NdataD=sum(WZD+BackD)
  NbackD=sum(BackD)
  sigmaU=(Ndata-NbackU)/(Ef_WZU*A*Lum);
  sigmaD=(Ndata-NbackD)/(Ef_WZD*A*Lum);
  BackgroundU.append(100*(NB-NbackU)/NB)
  BackgroundU.append(100*(NB-NbackD)/NB)
  ErrorU.append((100*(Sigma-sigmaU)/Sigma))
  ErrorU.append((100*(Sigma-sigmaD)/Sigma))
print 'MCWWUp','=', ErrorU[0], 'Eff=', EfficiencyU[0], 'Nback=', BackgroundU[0]
print 'MCWWDown','=', ErrorU[1], 'Eff=', EfficiencyU[1], 'Nback=', BackgroundU[1]

PR=[];TT=[]; DY=[]; VV=[]; WZ=[]; Da=[]; ZZ=[]; WW=[]; ErrorU=[]; nameinc=[]; EfficiencyU=[]; BackgroundU=[];
for l in level.keys():
 for i in range(0,len(inc)):
  DaU=[];BackU=[]; WZU=[]; DaD=[];BackD=[]; WZD=[];
  for pr in process:
   PR.append(pr)
   for c in chan.keys():
    if pr=='WZTo3LNU': 
     WZU.append(GetYield2(path, pr, chan[c], level=level[l], inc = inc[i], var = 'Yields')*Lumi)
     WZD.append(GetYield2(path, pr, chan[c], level=level[l], inc = inc[i], var = 'Yields')*Lumi)
    elif pr=='HighEGJet' or pr=='SingleMuon':
     DaU.append(GetYield2(path, pr, chan[c], level=level[l], inc = inc[i]))
     DaD.append(GetYield2(path, pr, chan[c], level=level[l], inc = inc[i]))
    elif pr=='ZZTo4L' or pr=='tW_noFullHad' or pr=='tbarW_noFullHad' or pr=='TT':
     BackU.append(GetYield3(path, pr, chan[c], level=level[l], inc = inc[i], var = 'Yields')*Lumi)
     BackD.append(GetYield4(path, pr, chan[c], level=level[l], inc = inc[i], var = 'Yields')*Lumi)
    elif  pr=='DYJetsToLL_MLL50' or pr=='DYJetsToLL_M_10to50' or pr=='ZZTo2L2Nu' or pr=='WWTo2L2Nu':
     BackU.append(GetYield2(path, pr, chan[c], level=level[l], inc = inc[i], var = 'Yields')*Lumi)
     BackD.append(GetYield2(path, pr, chan[c], level=level[l], inc = inc[i], var = 'Yields')*Lumi)
  #print WZ
  Ef_WZU =sum(WZU)*nGenEvent/(sum(FR)*Lum*sigm)
  Ef_WZD =sum(WZD)*nGenEvent/(sum(FR)*Lum*sigm)
  EfficiencyU.append(100*(Ef_All-Ef_WZU)/Ef_All)
  EfficiencyU.append(100*(Ef_All-Ef_WZD)/Ef_All)
  NdataU=sum(WZU+BackU)
  NbackU=sum(BackU)
  NdataD=sum(WZD+BackD)
  NbackD=sum(BackD)
  sigmaU=(Ndata-NbackU)/(Ef_WZU*A*Lum);
  sigmaD=(Ndata-NbackD)/(Ef_WZD*A*Lum);
  BackgroundU.append(100*(NB-NbackU)/NB)
  BackgroundU.append(100*(NB-NbackD)/NB)
  ErrorU.append((100*(Sigma-sigmaU)/Sigma))
  ErrorU.append((100*(Sigma-sigmaD)/Sigma))
print 'MCTTUp','=', ErrorU[0], 'Eff=', EfficiencyU[0], 'Nback=', BackgroundU[0]
print 'MCTTDown','=', ErrorU[1], 'Eff=', EfficiencyU[1], 'Nback=', BackgroundU[1]
