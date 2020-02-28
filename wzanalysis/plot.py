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
hm_3l   = HistoManager(processes_3l  , systematics, '', path=path_3l  , processDic=processDic, lumi = Lumi)
hm_2lss = HistoManager(processes_2lss, systematics, '', path=path_2lss, processDic=processDic, lumi = Lumi)
doParallel = False

## create outputfolder first: 
for path in [path_3l,path_2lss]:
  if not os.path.exists(path):
    os.mkdir(path)
    os.system("cp ~folgueras/www/utils/index.php %s/" %path)


def Draw2lss(name = 'Lep0Pt_eee_lep', rebin = 1, xtit = '', ytit = 'Events', doStackOverflow = False, binlabels = '', setLogY = False, maxscale = 2, tag = False):
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
  hm_2lss.SetStackOverflow(doStackOverflow)
  hm_2lss.SetHisto(name, rebin)
  hm_2lss.IsScaled=False
  s.SetHistosFromMH(hm_2lss)
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

def Draw3l(name = 'Lep0Pt_eee_lep', rebin = 1, xtit = '', ytit = 'Events', doStackOverflow = False, binlabels = '', setLogY = False, maxscale = 2, tag = False):
  if doParallel:
    return "Draw(%s, %i, \'%s\', \'%s\', %s, \'%s\', %s, %i, %s)"%("\'" + name + "\'" if type(name) == str else "[\'"+ "\',\'".join(name) + "\']" , rebin, xtit, ytit, "True" if doStackOverflow else "False", binlabels, "True" if setLogY else "False", maxscale, "False" if not(tag) else tag)

  s = Stack(outpath=outpath_3l, doRatio = True)
  s.SetColors(colors)
  s.SetProcesses(processes_3l)
  s.SetLumi(Lumi)
  s.SetHistoPadMargins(top = 0.08, bottom = 0.10, right = 0.06, left = 0.10)
  s.SetRatioPadMargins(top = 0.03, bottom = 0.40, right = 0.06, left = 0.10)
  s.SetTextLumi(texlumi = '%2.1f pb^{-1} (5.02 TeV)', texlumiX = 0.61, texlumiY = 0.96, texlumiS = 0.05)
  s.SetTextCMSmode(y = 0.865, s = 0.052)
  s.SetTextCMS(y = 0.87, s = 0.06)
  hm_3l.SetStackOverflow(doStackOverflow)
  hm_3l.SetHisto(name, rebin)
  hm_3l.IsScaled=False
  s.SetHistosFromMH(hm_3l)
  if tag == False:
    tag = name if type(name) == str else name[0]
    if type(name) == type([]):
      tag = tag.replace("eee","3l").replace("emm","3l").replace("mee","3l").replace("mmm","3l")
      
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

for lev in ['BR3L','lepWtight','SStight','m3l','SR3l','SR3l_LT','CR3l'] :
  for ch in ['eee','mee','emm','mmm','3l']:
    if ch == '3l':
      joblist.append(Draw3l(GetAllCh3l('Yields', ''), 1, 'Yields', 'Events'))
      joblist.append(Draw3l(GetAllCh3l('HT', lev), 1, 'H_{T} (GeV)', 'Events / 5 GeV'))
      joblist.append(Draw3l(GetAllCh3l('TrilepPt', lev), 2, 'p_{T}^{lll} (GeV)', 'Events / 5 GeV'))
      joblist.append(Draw3l(GetAllCh3l('ZPt', lev), 1, 'p_{T}^{Z} (GeV)', 'Events / 5 GeV'))
      joblist.append(Draw3l(GetAllCh3l('MET', lev), 2, 'p_{T}^{miss} (GeV)', 'Events'))
      joblist.append(Draw3l(GetAllCh3l('m3l', lev), 1, 'm_{3l} (GeV)',      'Events'))
      joblist.append(Draw3l(GetAllCh3l('mtw',lev), 2, 'm_{T}^{W} (GeV)',    'Events'))
      joblist.append(Draw3l(GetAllCh3l('mz', lev), 2, 'm_{Z} (GeV)',        'Events'))
      joblist.append(Draw3l(GetAllCh3l('LepWPt', lev), 2, 'p_{T}(lepW)  (GeV)', 'Events'))
      joblist.append(Draw3l(GetAllCh3l('LepWEta', lev), 1, '#eta (lepW)', 'Events'))
      joblist.append(Draw3l(GetAllCh3l('LepWPhi', lev), 1, '#phi (lepW) (rad/#pi)', 'Events'))
      joblist.append(Draw3l(GetAllCh3l('LepZ0Pt', lev), 2, 'p_{T}(lep0Z)  (GeV)', 'EventsV'))
      joblist.append(Draw3l(GetAllCh3l('LepZ0Eta', lev), 1, '#eta (lep0Z)', 'Events'))
      joblist.append(Draw3l(GetAllCh3l('LepZ0Phi', lev), 1, '#phi (lep0Z) (rad/#pi)', 'Events'))
      joblist.append(Draw3l(GetAllCh3l('LepZ1Pt', lev), 2, 'p_{T}(lep1Z)  (GeV)', 'Events'))
      joblist.append(Draw3l(GetAllCh3l('LepZ1Eta', lev), 1, '#eta (lep1Z)', 'Events'))
      joblist.append(Draw3l(GetAllCh3l('LepZ1Phi', lev), 1, '#phi (lep1Z) (rad/#pi)', 'Events'))
      joblist.append(Draw3l(GetAllCh3l('TrilepPt', lev), 1, 'Trilep p_{T} (GeV)', 'Events'))
      joblist.append(Draw3l(GetAllCh3l('ZPt', lev),  1, 'Z p_{T} (GeV)', 'Events'))
      joblist.append(Draw3l(GetAllCh3l('MaxDeltaPhi', lev), 1, 'max(#Delta#phi (ll)) (rad/#pi)', 'Events'))
      joblist.append(Draw3l(GetAllCh3l('InvMass01', lev), 1, 'Invariant Mass 01', 'Events', True))
      joblist.append(Draw3l(GetAllCh3l('InvMass02', lev), 1, 'Invariant Mass 02', 'Events', True))
      joblist.append(Draw3l(GetAllCh3l('InvMass12', lev), 1, 'Invariant Mass 12', 'Events', True))
      joblist.append(Draw3l(GetAllCh3l('NJets', lev), 1, 'Jet multiplicity', 'Events', True))
      joblist.append(Draw3l(GetAllCh3l('Btags', lev), 1, 'Jet B multiplicity', 'Events'))
      joblist.append(Draw3l(GetAllCh3l('Channel', lev), 1, 'Channel', 'Events'))
      joblist.append(Draw3l(GetAllCh3l('lW_genFlavor', lev), 1, 'Generator Flavor (lepW)', 'Events'))
      joblist.append(Draw3l(GetAllCh3l('lZ0_genFlavor', lev), 1, 'Generator Flavor (lepZ0)', 'Events'))
      joblist.append(Draw3l(GetAllCh3l('lZ1_genFlavor', lev), 1, 'Generator Flavor (lepZ1)', 'Events'))
      joblist.append(Draw3l(GetAllCh3l('l0Pt', lev), 1, 'p_{T}(lep0)  (GeV)', 'Events / 40 GeV'))
      joblist.append(Draw3l(GetAllCh3l('l1Pt', lev), 1, 'p_{T}(lep1)  (GeV)', 'Events / 40 GeV'))
      joblist.append(Draw3l(GetAllCh3l('l2Pt', lev), 1, 'p_{T}(lep2)  (GeV)', 'Events / 40 GeV'))
      joblist.append(Draw3l(GetAllCh3l('l0Eta', lev), 1, '#eta (lep0)', 'Events'))
      joblist.append(Draw3l(GetAllCh3l('l0Phi', lev), 1, '#phi (lep0) (rad/#pi)', 'Events'))
      joblist.append(Draw3l(GetAllCh3l('l1Eta', lev), 1, '#eta (lep1)', 'Events'))
      joblist.append(Draw3l(GetAllCh3l('l1Phi', lev), 1, '#phi (lep1) (rad/#pi)', 'Events'))
      joblist.append(Draw3l(GetAllCh3l('l2Eta', lev), 1, '#eta (lep2)', 'Events'))
      joblist.append(Draw3l(GetAllCh3l('l2Phi', lev), 1, '#phi (lep2) (rad/#pi)', 'Events'))
    else:               
      joblist.append(Draw3l(GetName('HT',ch , lev ), 1, 'H_{T} (GeV)', 'Events / 5 GeV'))
      joblist.append(Draw3l(GetName('TrilepPt',ch , lev ), 2, 'p_{T}^{lll} (GeV)', 'Events / 5 GeV'))
      joblist.append(Draw3l(GetName('ZPt',ch , lev ), 1, 'p_{T}^{Z} (GeV)', 'Events / 5 GeV'))
      joblist.append(Draw3l(GetName('MET',ch , lev ), 2, 'p_{T}^{miss} (GeV)', 'Events'))
      joblist.append(Draw3l(GetName('m3l',ch , lev ), 1, 'm_{3l} (GeV)',      'Events'))
      joblist.append(Draw3l(GetName('mtw',ch, lev), 2, 'm_{T}^{W} (GeV)',    'Events'))
      joblist.append(Draw3l(GetName('mz',ch , lev ), 2, 'm_{Z} (GeV)',        'Events'))
      joblist.append(Draw3l(GetName('LepWPt',ch , lev ), 2, 'p_{T}(lepW)  (GeV)', 'Events'))
      joblist.append(Draw3l(GetName('LepWEta',ch , lev ), 1, '#eta (lepW)', 'Events'))
      joblist.append(Draw3l(GetName('LepWPhi',ch , lev ), 1, '#phi (lepW) (rad/#pi)', 'Events'))
      joblist.append(Draw3l(GetName('LepZ0Pt',ch , lev ), 2, 'p_{T}(lep0Z)  (GeV)', 'EventsV'))
      joblist.append(Draw3l(GetName('LepZ0Eta',ch , lev ), 1, '#eta (lep0Z)', 'Events'))
      joblist.append(Draw3l(GetName('LepZ0Phi',ch , lev ), 1, '#phi (lep0Z) (rad/#pi)', 'Events'))
      joblist.append(Draw3l(GetName('LepZ1Pt',ch , lev ), 2, 'p_{T}(lep1Z)  (GeV)', 'Events'))
      joblist.append(Draw3l(GetName('LepZ1Eta',ch , lev ), 1, '#eta (lep1Z)', 'Events'))
      joblist.append(Draw3l(GetName('LepZ1Phi',ch , lev ), 1, '#phi (lep1Z) (rad/#pi)', 'Events'))
      joblist.append(Draw3l(GetName('TrilepPt',ch , lev ), 1, 'Trilep p_{T} (GeV)', 'Events'))
      joblist.append(Draw3l(GetName('ZPt',ch , lev ),  1, 'Z p_{T} (GeV)', 'Events'))
      joblist.append(Draw3l(GetName('MaxDeltaPhi',ch , lev ), 1, 'max(#Delta#phi (ll)) (rad/#pi)', 'Events'))
      joblist.append(Draw3l(GetName('InvMass01',ch , lev ), 1, 'Invariant Mass 01', 'Events', True))
      joblist.append(Draw3l(GetName('InvMass02',ch , lev ), 1, 'Invariant Mass 02', 'Events', True))
      joblist.append(Draw3l(GetName('InvMass12',ch , lev ), 1, 'Invariant Mass 12', 'Events', True))
      joblist.append(Draw3l(GetName('NJets',ch , lev ), 1, 'Jet multiplicity', 'Events', True))
      joblist.append(Draw3l(GetName('Btags',ch , lev ), 1, 'Jet B multiplicity', 'Events'))
      joblist.append(Draw3l(GetName('Channel',ch , lev ), 1, 'Channel', 'Events'))
      joblist.append(Draw3l(GetName('lW_genFlavor',ch , lev ), 1, 'Generator Flavor (lepW)', 'Events'))
      joblist.append(Draw3l(GetName('lZ0_genFlavor',ch , lev ), 1, 'Generator Flavor (lepZ0)', 'Events'))
      joblist.append(Draw3l(GetName('lZ1_genFlavor',ch , lev ), 1, 'Generator Flavor (lepZ1)', 'Events'))
      joblist.append(Draw3l(GetName('l0Pt',ch , lev ), 1, 'p_{T}(lep0)  (GeV)', 'Events / 40 GeV'))
      joblist.append(Draw3l(GetName('l1Pt',ch , lev ), 1, 'p_{T}(lep1)  (GeV)', 'Events / 40 GeV'))
      joblist.append(Draw3l(GetName('l2Pt',ch , lev ), 1, 'p_{T}(lep2)  (GeV)', 'Events / 40 GeV'))
      joblist.append(Draw3l(GetName('l0Eta',ch , lev ), 1, '#eta (lep0)', 'Events'))
      joblist.append(Draw3l(GetName('l0Phi',ch , lev ), 1, '#phi (lep0) (rad/#pi)', 'Events'))
      joblist.append(Draw3l(GetName('l1Eta',ch , lev ), 1, '#eta (lep1)', 'Events'))
      joblist.append(Draw3l(GetName('l1Phi',ch , lev ), 1, '#phi (lep1) (rad/#pi)', 'Events'))
      joblist.append(Draw3l(GetName('l2Eta',ch , lev ), 1, '#eta (lep2)', 'Events'))
      joblist.append(Draw3l(GetName('l2Phi',ch , lev ), 1, '#phi (lep2) (rad/#pi)', 'Events'))


for lev in ['SS2l_LL','SS2l','SR2l']:
  for ch in ['em','ee','mm','2l']:
    if ch == '2l':
      joblist.append(Draw2lss(GetAllCh2l('Yields', ''), 1, 'Yields', 'Events'))
      joblist.append(Draw2lss(GetAllCh2l('HT', lev), 1, 'H_{T} (GeV)', 'Events / 5 GeV'))
      joblist.append(Draw2lss(GetAllCh2l('HTmiss', lev), 1, 'H_{T}^{miss} (GeV)', 'Events / 5 GeV'))
      joblist.append(Draw2lss(GetAllCh2l('ZPt', lev), 1, 'p_{T}^{Z} (GeV)', 'Events / 5 GeV'))
      joblist.append(Draw2lss(GetAllCh2l('MET', lev), 2, 'p_{T}^{miss} (GeV)', 'Events'))
      joblist.append(Draw2lss(GetAllCh2l('mtw',lev), 2, 'm_{T}^{W} (GeV)',    'Events'))
      joblist.append(Draw2lss(GetAllCh2l('LepWPt', lev), 2, 'p_{T}(lepW)  (GeV)', 'Events'))
      joblist.append(Draw2lss(GetAllCh2l('LepWEta', lev), 1, '#eta (lepW)', 'Events'))
      joblist.append(Draw2lss(GetAllCh2l('LepWPhi', lev), 1, '#phi (lepW) (rad/#pi)', 'Events'))
      joblist.append(Draw2lss(GetAllCh2l('LepZ0Pt', lev), 2, 'p_{T}(lep0Z)  (GeV)', 'EventsV'))
      joblist.append(Draw2lss(GetAllCh2l('LepZ0Eta', lev), 1, '#eta (lep0Z)', 'Events'))
      joblist.append(Draw2lss(GetAllCh2l('LepZ0Phi', lev), 1, '#phi (lep0Z) (rad/#pi)', 'Events'))
      joblist.append(Draw2lss(GetAllCh2l('InvMass01', lev), 1, 'Invariant Mass 01', 'Events', True))
      joblist.append(Draw2lss(GetAllCh2l('InvMass02', lev), 1, 'Invariant Mass 02', 'Events', True))
      joblist.append(Draw2lss(GetAllCh2l('InvMass12', lev), 1, 'Invariant Mass 12', 'Events', True))
      joblist.append(Draw2lss(GetAllCh2l('NJets', lev), 1, 'Jet multiplicity', 'Events', True))
      joblist.append(Draw2lss(GetAllCh2l('Btags', lev), 1, 'Jet B multiplicity', 'Events'))
      joblist.append(Draw2lss(GetAllCh2l('Channel', lev), 1, 'Channel', 'Events'))
      joblist.append(Draw2lss(GetAllCh2l('lW_genFlavor', lev), 1, 'Generator Flavor (lepW)', 'Events'))
      joblist.append(Draw2lss(GetAllCh2l('lZ0_genFlavor', lev), 1, 'Generator Flavor (lepZ0)', 'Events'))
      joblist.append(Draw2lss(GetAllCh2l('l0Pt', lev), 1, 'p_{T}(lep0)  (GeV)', 'Events / 40 GeV'))
      joblist.append(Draw2lss(GetAllCh2l('l1Pt', lev), 1, 'p_{T}(lep1)  (GeV)', 'Events / 40 GeV'))
      joblist.append(Draw2lss(GetAllCh2l('l0Eta', lev), 1, '#eta (lep0)', 'Events'))
      joblist.append(Draw2lss(GetAllCh2l('l0Phi', lev), 1, '#phi (lep0) (rad/#pi)', 'Events'))
      joblist.append(Draw2lss(GetAllCh2l('l1Eta', lev), 1, '#eta (lep1)', 'Events'))
      joblist.append(Draw2lss(GetAllCh2l('l1Phi', lev), 1, '#phi (lep1) (rad/#pi)', 'Events'))
    else:                
      joblist.append(Draw2lss(GetName('HT', ch, lev), 1, 'H_{T} (GeV)', 'Events / 5 GeV'))
      joblist.append(Draw2lss(GetName('HTmiss', ch, lev), 1, 'H_{T}^{miss} (GeV)', 'Events / 5 GeV'))
      joblist.append(Draw2lss(GetName('ZPt', ch, lev), 1, 'p_{T}^{Z} (GeV)', 'Events / 5 GeV'))
      joblist.append(Draw2lss(GetName('MET',ch, lev), 1, 'p_{T}^{miss} (GeV)', 'Events / 5 GeV'))
      joblist.append(Draw2lss(GetName('mtw',ch, lev), 1, 'm_{T}^{W} (GeV)',    'Events'))
      joblist.append(Draw2lss(GetName('LepWPt',ch, lev), 1, 'p_{T}(lepW)  (GeV)', 'Events / 40 GeV'))
      joblist.append(Draw2lss(GetName('LepWEta',ch, lev), 1, '#eta (lepW)', 'Events'))
      joblist.append(Draw2lss(GetName('LepWPhi',ch, lev), 1, '#phi (lepW) (rad/#pi)', 'Events'))
      joblist.append(Draw2lss(GetName('LepZ0Pt',ch, lev), 1, 'p_{T}(lep0Z)  (GeV)', 'Events / 40 GeV'))
      joblist.append(Draw2lss(GetName('LepZ0Eta',ch, lev), 1, '#eta (lep0Z)', 'Events'))
      joblist.append(Draw2lss(GetName('LepZ0Phi',ch, lev), 1, '#phi (lep0Z) (rad/#pi)', 'Events'))
      joblist.append(Draw2lss(GetName('Btags',ch, lev), 1, 'Jet B multiplicity', 'Events', True))
      joblist.append(Draw2lss(GetName('Channel', ch, lev), 1, 'Channel', 'Events'))
      joblist.append(Draw2lss(GetName('NJets',ch, lev), 1, 'Jet multiplicity', 'Events', True))
      joblist.append(Draw2lss(GetName('lW_genFlavor',ch, lev), 1, 'Generator Flavor (lepW)', 'Events'))
      joblist.append(Draw2lss(GetName('lZ0_genFlavor',ch, lev), 1, 'Generator Flavor (lepZ0)', 'Events'))
      joblist.append(Draw2lss(GetName('InvMass01',ch, lev), 1, 'Invariant Mass 01', 'Events', True))
      joblist.append(Draw2lss(GetName('InvMass02',ch, lev), 1, 'Invariant Mass 02', 'Events', True))
      joblist.append(Draw2lss(GetName('InvMass12',ch, lev), 1, 'Invariant Mass 12', 'Events', True))
    


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
