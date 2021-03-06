import os, sys
from config import *
basepath = os.path.abspath(__file__).rsplit('/xuAnalysis/',1)[0]+'/xuAnalysis/'
sys.path.append(basepath)
from plotter.TopHistoReader import TopHistoReader, HistoManager
from plotter.Plotter import Stack, HistoComp
from framework.looper import looper
from ROOT.TMath import Sqrt as sqrt
from ROOT import kRed, kOrange, kBlue, kTeal, kGreen, kGray, kAzure, kPink, kCyan, kBlack, kSpring, kViolet, kYellow
from ROOT import TCanvas, gROOT, TLegend, TCanvas
from numpy import arange

gROOT.SetBatch(1)
treeName="MiniTree"

# Set signal masses
ms = 275
ml = 100

# Set constants
outpath = './Unc/SR/mass%i_%i/'%(ms, ml)
os.system("mkdir -p %s"%outpath)
model = '/nfs/fanae/user/juanr/CMSSW_10_2_5/src/xuAnalysis/TopPlots/DrawMiniTrees/NNtotal_model2.h5'

# Set year
year = 2018

# Create the looper, set readOutput to true to read previous temporary rootfiles created for each sample
#l = looper(path=path[year], nSlots = 6, treeName = 'MiniTree', options = 'merge', nEvents = 1000, outpath='tempfiles/')
l = looper(path=path[year], nSlots = 5, treeName = 'MiniTree', options = 'merge', outpath = outpath+'tempfiles/', readOutput=True)

# Add processes
processes = processDic[year].keys() #['tt']
for p in processes: l.AddSample(p,  processDic[year][p])

# Systematic uncertainties
syst = 'MuonEff, ElecEff, Trig, JES, JER, MuonES, Uncl, Btag, MisTag, PU, TopPt'
if year != 2018: syst += ', Pref'
systlist = [x+y for x in syst.replace(' ','').split(',') for y in ['Up','Down']]

# Lines below to read the DNN values
l.AddHeader('from framework.mva import ModelPredict\n')
l.AddInit('      self.pd1 = ModelPredict("%s")\n'%model)
l.AddInit("      if self.sampleName in ['tt_hdampUp', 'tt_hdampDown', 'tt_UEUp', 'tt_UEDown', 'data', 'data_obs', 'Data']: self.systematics = ['']\n")
l.AddSyst(systlist)
loopcode = '''
values = [%i,  %i, t.TDilep_Pt, t.TDeltaPhi, t.TDeltaEta, t.TLep0Pt, t.TLep0Eta, t.TLep1Pt, vmet, t.TLep1Eta, vmll, vmt2, vht]
prob1 = self.pd1.GetProb(values)
'''%(ms, ml)
l.AddLoopCode(loopcode)

# Select the signal and add cut in masses (in principle, one signal at a time)
stopcutline = lambda signal, mstop, mlsp : '   if self.outname == "%s"  and not (mStop == %s. and mLSP == %s. ): return\n'%(signal, mstop, mlsp)
massfromsig = lambda signal : signal[4:].split('_')
stopcuts = ''
for sig in ['stop%i_%i'%(ms, ml)]:
  mstop, mlsp = massfromsig(sig)
  stopcuts += stopcutline(sig, mstop, mlsp)
selection = '''
 if self.outname.startswith('stop'):
   mStop = t.Tm_stop; mLSP = t.Tm_LSP%s
'''%('\n'+stopcuts+'\n')
l.AddSelection(selection)

# Define expresions, including varibles with syst variations
l.AddExpr('deltaphi', 'TDeltaPhi', 'abs(TDeltaPhi)/3.141592')
l.AddExpr('deltaeta', 'TDeltaEta', 'abs(TDeltaEta)')
l.AddExpr('weight1', [], '1')
l.AddExpr('exprW', ['TWeight'], 'TWeight')
l.AddExpr('vmet', ['TMET'], 'TMET')
l.AddExpr('vmt2', ['TMT2'], 'TMT2')
l.AddExpr('vht',  ['THT' ], 'THT')
l.AddExpr('vmll', ['TMll'], 'TMll')
l.AddExpr('vpd', '', 'prob1', True)

# Weight and cuts...
l.AddSelection('')
l.AddCut('t.TIsSS == 0', [])
l.AddCut('TPassDilep == 1', 'TPassDilep')
l.AddCut('TMET >= 50', 'TMET')
l.AddCut('TMT2 >= 80', 'TMT2')
l.AddCut('TNJets >= 2', 'TNJets')
l.AddCut('TNBtags >= 1', 'TNBtags')

# Add histograms
cut = ''
weight = 'exprW'
l.AddHisto('vpd',  'dnn',  20, 0, 1,   weight = weight, cut = '')
l.AddHisto('vpd',  'dnn2',  20, 0.5, 1,   weight = weight, cut = 'vpd >= 0.5')
l.AddHisto('TMll', 'mll', 30, 0, 300, weight = weight, cut = '')
l.AddHisto('TMET', 'met', 25, 50, 300, weight = weight, cut = '')
l.AddHisto('TMT2', 'mt2', 8, 80, 160, weight = weight, cut = '')
l.AddHisto('TDilep_Pt', 'dileppt', 30, 0, 300, weight = weight, cut = '')
l.AddHisto('TLep0Pt', 'lep0pt', 15, 0, 150, weight = weight, cut = '')
l.AddHisto('TLep1Pt', 'lep1pt', 30, 0, 300, weight = weight, cut = '')
l.AddHisto('TLep0Eta', 'lep0eta', 30, -2.4, 2.4, weight = weight, cut = '')
l.AddHisto('TLep1Eta', 'lep1eta', 30, -2.4, 2.4, weight = weight, cut = '')
l.AddHisto('deltaphi', 'deltaphi', 30, 0, 1, weight = weight, cut = '')
l.AddHisto('deltaeta', 'deltaeta', 30, 0, 5, weight = weight, cut = '')
l.AddHisto('TJet0Pt', 'jet0pt', 30, 0, 450, weight = weight, cut = '')
l.AddHisto('TJet1Pt', 'jet1pt', 30, 0, 300, weight = weight, cut = '')
l.AddHisto('TJet0Eta', 'jet0eta', 30, -2.4, 2.4, weight = weight, cut = '')
l.AddHisto('TJet1Eta', 'jet1eta', 30, -2.4, 2.4, weight = weight, cut = '')
l.AddHisto('THT', 'ht', 40, 0, 800, weight = weight, cut = '')
l.AddHisto('TNJets', 'njets', 6, 1.5, 7.5, weight = weight, cut = '')
l.AddHisto('TNBtags', 'nbtags', 3, 0.5, 3.5, weight = weight, cut = '')
histos = ['mt2',  'met',  'mll',  'dnn',  'dileppt',  'deltaphi',  'deltaeta',  'ht',  'lep0pt',  'lep1pt',  'lep0eta',  'lep1eta', 'njets', 'nbtags', 'jet0pt', 'jet1pt', 'jet0eta', 'jet1eta'] 
# Scan in MET
for val in arange(50, 300, 10):
  hname = 'metScanstop%i_%i_%1.0f'%(ms,ml,val*100)
  histos.append(hname)
  l.AddHisto('weight1', hname,  1, -1, 20,   weight = weight, cut = 'vmet > %1.2f'%val)
# Scan in DNN
for val in arange(0.5, 1, 0.05):
  hname = 'dnnScanstop%i_%i_%1.0f'%(ms,ml,val*100)
  histos.append(hname)
  l.AddHisto('weight1', hname,  1, -1, 20,   weight = weight, cut = 'vpd > %1.2f'%val)
 
# Let's rock
out = l.Run()

# Create HistoManager with the out dictionary from the looper
hm = HistoManager(processes, path = path[year], processDic = processDic[year], lumi = GetLumi(year)*1000,indic = out)

# Function to save the histograms into combine rootfiles
def save(name):
  hm.SetHisto(name)
  hm.Save(outname = outpath+'/'+name, htag = '')

# Save the histograms
for v in histos: save(v)

