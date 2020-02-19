import ROOT
from numpy import sort

file = ROOT.TFile("/pool/ciencias/nanoAODv4/5TeV/nanoAODnoSkim/postProc/WWTo2L2Nu_1.root","READ")
tree = file.Get("Events")

#Nominal is 4, 2 and 6 are unphysical
tree.Draw("1>>hNominal(1,0.5,1.5)","LHEScaleWeight[4]")
tree.Draw("1>>h0(1,0.5,1.5)","LHEScaleWeight[0]")
tree.Draw("1>>h1(1,0.5,1.5)","LHEScaleWeight[1]")
tree.Draw("1>>h3(1,0.5,1.5)","LHEScaleWeight[3]")
tree.Draw("1>>h5(1,0.5,1.5)","LHEScaleWeight[5]")
tree.Draw("1>>h7(1,0.5,1.5)","LHEScaleWeight[7]")
tree.Draw("1>>h8(1,0.5,1.5)","LHEScaleWeight[8]")


hn = ROOT.gDirectory.Get("hNominal")
h0 = ROOT.gDirectory.Get("h0")
h1 = ROOT.gDirectory.Get("h1")
h3 = ROOT.gDirectory.Get("h3")
h5 = ROOT.gDirectory.Get("h5")
h7 = ROOT.gDirectory.Get("h7")
h8 = ROOT.gDirectory.Get("h8")

scalevariations = [h0.GetBinContent(1), h1.GetBinContent(1),h3.GetBinContent(1),h5.GetBinContent(1),h7.GetBinContent(1),h8.GetBinContent(1)]
print "Nominal: ", hn.GetBinContent(1)
print "Scale Vars: ", [h0.GetBinContent(1), h1.GetBinContent(1),h3.GetBinContent(1),h5.GetBinContent(1),h7.GetBinContent(1),h8.GetBinContent(1)]
sortedscalevariations = sort(scalevariations)
print "Envelope (percent): - %1.3f  + %1.3f "%((sortedscalevariations[0]- hn.GetBinContent(1))/hn.GetBinContent(1), (sortedscalevariations[-1]- hn.GetBinContent(1))/hn.GetBinContent(1))
