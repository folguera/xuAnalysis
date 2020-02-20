import os,sys
sys.path.append(os.path.abspath(__file__).rsplit("/xuAnalysis/",1)[0]+"/xuAnalysis/")
from framework.analysis import analysis
import framework.functions as fun
from ROOT import TLorentzVector

class skim3l(analysis):
  def init(self):
    self.CreateTH1F('Count', 'Count', 1, 0, 1)
    self.CreateTH1F('SumWeights', 'SumWeights', 1, 0, 1)
    self.CreateTTree('EventTree','')
    self.CreateTH1F('SumOfPDFweights','', 33, 0.5, 33.5)
    self.CreateTH1F('SumOfScaleWeights','', 9, 0.5, 9.5)
    self.obj['EventTree'] = self.tchain.CloneTree(0)
    self.isData = True if not hasattr(self.obj['EventTree'], "genWeight") else False

    self.obj['Count'].SetBinContent(1, self.nGenEvents/20)
    self.obj['SumWeights'].SetBinContent(1, self.nSumOfWeights/20)

  def insideLoop(self,t):
    if not self.isData:
      for i in range(t.nLHEPdfWeight):
        self.obj['SumOfPDFweights'].Fill(i+1, t.LHEPdfWeight[i])
      for i in range(t.nLHEScaleWeight):
        self.obj['SumOfScaleWeights'].Fill(i+1, t.LHEScaleWeight[i])
   
    # Three leptons
    looseLeptons = []
    for imu in range(t.nMuon):
      if t.Muon_pt[imu] >= 0:
        l = TLorentzVector()
        l.SetPtEtaPhiM(t.Muon_pt[imu], t.Muon_eta[imu], t.Muon_phi[imu], t.Muon_mass[imu])
        looseLeptons.append(l) 
    for iel in range(t.nElectron):
      if t.Electron_pt >=0: 
        l = TLorentzVector()
        l.SetPtEtaPhiM(t.Electron_pt[iel], t.Electron_eta[iel], t.Electron_phi[iel], t.Electron_mass[iel])
        looseLeptons.append(l)
    
    if len(looseLeptons) < 3: return

    self.obj['EventTree'].Fill()
