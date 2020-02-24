import os, sys
from plotterconf import *
basepath = os.path.abspath(__file__).rsplit('/xuAnalysis/',1)[0]+'/xuAnalysis/'
print basepath
sys.path.append(basepath)
from ROOT.TMath import Sqrt as sqrt
from ROOT import kRed, kOrange, kBlue, kTeal, kGreen, kGray, kAzure, kPink, kCyan, kBlack, kSpring, kViolet, kYellow
from ROOT import TCanvas, gROOT
gROOT.SetBatch(1)

######################################################################################
### Plots
hm = HistoManager(processes_2lss, systematics, '', path=path_2lss, processDic=processDic, lumi = Lumi)
doParallel = True

## create outputfolder first: 
for p in [outpath,outpath_2lss]:
  if not os.path.exists(p):
    os.mkdir(p)
    os.system("cp ~folgueras/www/utils/index.php %s/" %p)


def Draw(name = 'Lep0Pt_eee_lep', rebin = 1, xtit = '', ytit = 'Events', doStackOverflow = False, binlabels = '', setLogY = False, maxscale = 2, tag = False):
  if doParallel:
    return "Draw(%s, %i, \'%s\', \'%s\', %s, \'%s\', %s, %i, %s)"%("\'" + name + "\'" if type(name) == str else "[\'"+ "\',\'".join(name) + "\']" , rebin, xtit, ytit, "True" if doStackOverflow else "False", binlabels, "True" if setLogY else "False", maxscale, "False" if not(tag) else tag)

  s = Stack(outpath=outpath_2lss, doRatio = True)
  s.SetColors(colors)
  s.SetProcesses(processes_2lss)
  s.SetLumi(Lumi)
  s.SetHistoPadMargins(top = 0.08, bottom = 0.10, right = 0.06, left = 0.10)
  s.SetRatioPadMargins(top = 0.03, bottom = 0.40, right = 0.06, left = 0.10)
  s.SetTextLumi(texlumi = '%2.1f pb^{-1} (5.02 TeV)', texlumiX = 0.61, texlumiY = 0.96, texlumiS = 0.05)
  s.SetTextCMSmode(y = 0.865, s = 0.052)
  s.SetTextCMS(y = 0.87, s = 0.06)
  hm.SetStackOverflow(doStackOverflow)
  hm.SetHisto(name, rebin)
  hm.IsScaled=False
  s.SetHistosFromMH(hm)
  if tag == False:
    tag = name if type(name) == str else name[0]
    if type(name) == type([]):
      tag = tag.replace("ee","2l").replace("em","2l").replace("mm","2l")
      
  s.SetOutName(tag)
  s.SetBinLabels(binlabels)
  s.SetTextChan('')
  s.SetRatioMin(2-maxscale)
  s.SetRatioMax(maxscale)
  s.SetTextChan('')
  s.SetLogY(setLogY)
  s.SetPlotMaxScale(maxscale)
  s.SetXtitle(size = 0.05, offset = 0.8, nDiv = 510, labSize = 0.04)
  s.SetYtitle(labSize = 0.04)
  s.DrawStack(xtit, ytit)
  return 1

joblist = []

for lev in ['SS2l_LL','SS2l','SR2l']:
  for ch in ['em','ee','mm','2l']:
    if ch == '2l':
      joblist.append(Draw(GetAllCh2l('Yields', ''), 1, 'Yields', 'Events'))
      joblist.append(Draw(GetAllCh2l('HT', lev), 1, 'H_{T} (GeV)', 'Events / 5 GeV'))
      joblist.append(Draw(GetAllCh2l('MET', lev), 2, 'p_{T}^{miss} (GeV)', 'Events'))
      joblist.append(Draw(GetAllCh2l('mtw',lev), 2, 'm_{T}^{W} (GeV)',    'Events'))
      joblist.append(Draw(GetAllCh2l('LepWPt', lev), 2, 'p_{T}(lepW)  (GeV)', 'Events'))
      joblist.append(Draw(GetAllCh2l('LepWEta', lev), 1, '#eta (lepW)', 'Events'))
      joblist.append(Draw(GetAllCh2l('LepWPhi', lev), 1, '#phi (lepW) (rad/#pi)', 'Events'))
      joblist.append(Draw(GetAllCh2l('LepZPt', lev), 2, 'p_{T}(lep0Z)  (GeV)', 'EventsV'))
      joblist.append(Draw(GetAllCh2l('LepZEta', lev), 1, '#eta (lep0Z)', 'Events'))
      joblist.append(Draw(GetAllCh2l('LepZPhi', lev), 1, '#phi (lep0Z) (rad/#pi)', 'Events'))
      joblist.append(Draw(GetAllCh2l('InvMass', lev), 1, 'Invariant Mass', 'Events', True))
      joblist.append(Draw(GetAllCh2l('NJets', lev), 1, 'Jet multiplicity', 'Events', True))
      joblist.append(Draw(GetAllCh2l('Btags', lev), 1, 'Jet B multiplicity', 'Events'))
      joblist.append(Draw(GetAllCh2l('Channel', lev), 1, 'Channel', 'Events'))
      joblist.append(Draw(GetAllCh2l('lW_genFlavor', lev), 1, 'Generator Flavor (lepW)', 'Events'))
      joblist.append(Draw(GetAllCh2l('lZ_genFlavor', lev), 1, 'Generator Flavor (lepZ0)', 'Events'))
      joblist.append(Draw(GetAllCh2l('l0Pt', lev), 1, 'p_{T}(lep0)  (GeV)', 'Events / 40 GeV'))
      joblist.append(Draw(GetAllCh2l('l1Pt', lev), 1, 'p_{T}(lep1)  (GeV)', 'Events / 40 GeV'))
      joblist.append(Draw(GetAllCh2l('l0Eta', lev), 1, '#eta (lep0)', 'Events'))
      joblist.append(Draw(GetAllCh2l('l0Phi', lev), 1, '#phi (lep0) (rad/#pi)', 'Events'))
      joblist.append(Draw(GetAllCh2l('l1Eta', lev), 1, '#eta (lep1)', 'Events'))
      joblist.append(Draw(GetAllCh2l('l1Phi', lev), 1, '#phi (lep1) (rad/#pi)', 'Events'))
    else:                
      joblist.append(Draw(GetName('HT', ch, lev), 1, 'H_{T} (GeV)', 'Events / 5 GeV'))
      joblist.append(Draw(GetName('MET',ch, lev), 1, 'p_{T}^{miss} (GeV)', 'Events / 5 GeV'))
      joblist.append(Draw(GetName('mtw',ch, lev), 1, 'm_{T}^{W} (GeV)',    'Events'))
      joblist.append(Draw(GetName('LepWPt',ch, lev), 1, 'p_{T}(lepW)  (GeV)', 'Events / 40 GeV'))
      joblist.append(Draw(GetName('LepWEta',ch, lev), 1, '#eta (lepW)', 'Events'))
      joblist.append(Draw(GetName('LepWPhi',ch, lev), 1, '#phi (lepW) (rad/#pi)', 'Events'))
      joblist.append(Draw(GetName('LepZPt',ch, lev), 1, 'p_{T}(lep0Z)  (GeV)', 'Events / 40 GeV'))
      joblist.append(Draw(GetName('LepZEta',ch, lev), 1, '#eta (lep0Z)', 'Events'))
      joblist.append(Draw(GetName('LepZPhi',ch, lev), 1, '#phi (lep0Z) (rad/#pi)', 'Events'))
      joblist.append(Draw(GetName('Btags',ch, lev), 1, 'Jet B multiplicity', 'Events', True))
      joblist.append(Draw(GetName('Channel', ch, lev), 1, 'Channel', 'Events'))
      joblist.append(Draw(GetName('NJets',ch, lev), 1, 'Jet multiplicity', 'Events', True))
      joblist.append(Draw(GetName('lW_genFlavor',ch, lev), 1, 'Generator Flavor (lepW)', 'Events'))
      joblist.append(Draw(GetName('lZ_genFlavor',ch, lev), 1, 'Generator Flavor (lepZ0)', 'Events'))
      joblist.append(Draw(GetName('InvMass',ch, lev), 1, 'Invariant Mass', 'Events', True))
    


if doParallel:
  from multiprocessing import Pool
  from contextlib import closing
  import time
  doParallel = False
  def execute(com):
    eval(com)

  with closing(Pool(4)) as p:
    print "Now running " + str(len(joblist)) + " commands using: " + str(4) + " processes. Please wait" 
    retlist1 = p.map_async(execute, joblist, 1)
    while not retlist1.ready():
      print("Plots left: {}".format(retlist1._number_left ))
      time.sleep(.5)
    retlist1 = retlist1.get()
    p.close()
    p.join()
    p.terminate()
