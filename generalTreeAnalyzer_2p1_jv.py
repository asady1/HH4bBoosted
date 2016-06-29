import os, numpy
import glob
import math
import ROOT
from ROOT import *

#ROOT.gROOT.Macro("rootlogon.C")

import FWCore.ParameterSet.Config as cms

import sys
from DataFormats.FWLite import Events, Handle

from array import *


from optparse import OptionParser
parser = OptionParser()

parser.add_option("-f", "--pathIn", dest="inputFile",
                  help="inputFile path")

parser.add_option("-o", "--outName", dest="outName",
                  help="output file name")

parser.add_option("-i", "--min", dest="min", 
		  help="input index low end")

parser.add_option("-j", "--max", dest="max", 
		  help="input index high end")

parser.add_option("-l", "--file", dest="txt", 
		  help="input txt file")

parser.add_option("-t", "--trigger", dest="trigger",
		  help="bool for trigger cut")

parser.add_option("-k", "--jets", dest="jets",
		  help="bool for jet cuts")

parser.add_option("-m", "--isMC", dest="isMC", 
                    help="bool for is MC")

parser.add_option("-x", "--xsec", dest="xsec", 
                    help="cross section")

parser.add_option("-S", "--syst", dest="syst",
                  help="Systematic")


(options, args) = parser.parse_args()

inputfile = options.txt 

ff_n = 1000

num1 = int(options.min)
num2 = int(options.max)

d1 = options.outName 
d2 = '_'
outputfilename = d1 + d2 + options.min + '.root'

print outputfilename

import copy
#File_tr=ROOT.TFile.Open("trigger_objects.root", "R")
#histo_efficiency=copy.copy(File_tr.Get("histo_efficiency"))
#File_tr.Close()


def trigger_function(histo_efficiency,htJet30=700):
    result = histo_efficiency.GetBinContent(htJet30)
    return result


#defining functions
def ClosestJet(jets, fourvec): #returns the index of the jet (from a collection "jets") closest to the given four-vector
	DR = 9999.
	index = -1
	for j in range(0,len(jets)):
	    if jets[j].Pt() > 0 :
		dR = fourvec.DeltaR(jets[j])
		if dR < DR :
			DR = fourvec.DeltaR(jets[j])
			index = j
	return index

def MatchCollection(Col, jet): #matches a jet to a jet in a different collection
	j = -1
        dr = 0.4
	for i in range(len(Col)):
		C = ROOT.TLorentzVector()
                C.SetPtEtaPhiM( Col[i].Pt(), Col[i].Eta(), Col[i].Phi(), Col[i].M() )
		dr = abs(jet.DeltaR(C))
		if dr < 0.4 :
			#print "WOOHOO MATCH with index " + str(j) + " with dr " + str(dr)
			j = i
                        break
        if dr > 0.4:
	#	print "No Match :( for dr: " + str(dr)
#		print "index " + str(j)
		return -1
	return j

def MatchCollection2(Col, jet, index): #matches a jet to a jet in a different collection
    j = -1
    dr = 0.4
    for i in range(len(Col)):
        if i != index:
            C = ROOT.TLorentzVector()
            C.SetPtEtaPhiM( Col[i].Pt(), Col[i].Eta(), Col[i].Phi(), Col[i].M() )
            dr = abs(jet.DeltaR(C))
            if dr < 0.4 :
    #print "WOOHOO MATCH with index " + str(j) + " with dr " + str(dr)
                j = i
                break
    if dr > 0.4:
            #print "No Match :( for dr: " + str(dr)
            #print "index " + str(j)
            return -1
    return j

def MatchCollection3(Col, jet, index1, index2): #matches a jet to a jet in a different collection
    j = -1
    dr = 0.4
    for i in range(len(Col)):
        if i != index1 and i != index2:
            C = ROOT.TLorentzVector()
            C.SetPtEtaPhiM( Col[i].Pt(), Col[i].Eta(), Col[i].Phi(), Col[i].M() )
            dr = abs(jet.DeltaR(C))
            if dr < 0.4 :
    #print "WOOHOO MATCH with index " + str(j) + " with dr " + str(dr)
                j = i
                break
    if dr > 0.4:
            #print "No Match :( for dr: " + str(dr)
            #print "index " + str(j)
            return -1
    return j

def MatchCollection4(Col, jet, index1, index2, index3): #matches a jet to a jet in a different collection
    j = -1
    dr = 0.4
    for i in range(len(Col)):
        if i != index1 and i != index2 and i != index3:
            C = ROOT.TLorentzVector()
            C.SetPtEtaPhiM( Col[i].Pt(), Col[i].Eta(), Col[i].Phi(), Col[i].M() )
            dr = abs(jet.DeltaR(C))
            if dr < 0.4 :
    #print "WOOHOO MATCH with index " + str(j) + " with dr " + str(dr)
                j = i
                break
    if dr > 0.4:
            #print "No Match :( for dr: " + str(dr)
            #print "index " + str(j)
            return -1
    return j

def open_files(file_name) : #opens files to run on

    g = open(file_name)
    list_file = []
    final_list = []
    for i in range(ff_n):  # this is the length of the file
        list_file.append(g.readline().split())
    s = options.inputFile

    for i in range(len(list_file)):
        for j in range(len(list_file[i])) :
            final_list.append(s + list_file[i][j])
  #  print final_list
    return final_list


def deltaR( particle, jet ) : #gives deltaR between two particles
    DeltaPhiHere = math.fabs( particle.phi() - jet.phi() )
    if DeltaPhiHere > math.pi :
        DeltaPhiHere = 2*math.pi - DeltaPhiHere

    deltaRHere = math.sqrt( (particle.eta() - jet.eta() )**2 + ( DeltaPhiHere )**2  )
    return deltaRHere

print sys.argv[1]

f =  ROOT.TFile(outputfilename, 'recreate')

f.cd()


myTree =  ROOT.TTree('myTree', 'myTree')

#second tree variables (2+1 case)
jet1Array = array('f', [-1.0, -100, -100, -1.0])
jet2Array = array('f', [-1.0, -100, -100, -1.0])
jet1ID = array('f', [-100.0])
jet2ID = array('f', [-100.0])
jet1tau21 = array('f', [-100.0])
jet2tau21 = array('f', [-100.0])
jet1pmass = array('f', [-100.0])
jet2pmass = array('f', [-100.0])
jet1pmassunc = array('f', [-100.0])
jet2pmassunc = array('f', [-100.0])
jet1bbtag = array('f', [-100.0])
jet2bbtag = array('f', [-100.0])
jet1s1csv = array('f', [-100.0])
jet1s2csv = array('f', [-100.0])
jet2s1csv = array('f', [-100.0])
jet2s2csv = array('f', [-100.0])
triggerpass = array('f', [-100.0])
triggerHT800pass = array('f', [-100.0])
trigger1= array('f', [-100.])
trigger2= array('f', [-100.])
trigger3= array('f', [-100.])
trigger_pre= array('f', [-100.])
trigger_muon= array('f', [-100.])
nHiggsTags = array('f', [-100.0])
nTrueInt = array('f', [-100])
#sPUWeight  = array('f', [-100.0])
vtype = array('f', [-100.0])
isData = array('f', [-100.0])
jet1nbHadron = array('f', [-100.0])
jet2nbHadron = array('f', [-100.0])
jet1flavor = array('f', [-100.0])
jet2flavor = array('f', [-100.0])
jet1ncHadron = array('f', [-100.0])
jet2ncHadron = array('f', [-100.0])
genJet1Pt = array('f', [-100.0])
genJet1Phi = array('f', [-100.0])
genJet1Eta = array('f', [-100.0])
genJet1Mass = array('f', [-100.0])
genJet1ID = array('f', [-100.0])
genJet2Pt = array('f', [-100.0])
genJet2Phi = array('f', [-100.0])
genJet2Eta = array('f', [-100.0])
genJet2Mass = array('f', [-100.0])
genJet2ID = array('f', [-100.0])
jet1l1l2l3 = array('f', [-100.0])
jet2l1l2l3 = array('f', [-100.0])
jet1l2l3 = array('f', [-100.0])
jet2l2l3 = array('f', [-100.0])
jet1JER = array('f', [-100.0])
jet2JER = array('f', [-100.0])
puWeights = array('f', [-100.0])
puWeightsUp = array('f', [-100.0])
puWeightsDown = array('f', [-100.0])
bbtag1SF = array('f', [-100.0])
bbtag2SF = array('f', [-100.0])
bbtag1SFUp = array('f', [-100.0])
bbtag2SFUp = array('f', [-100.0])
bbtag1SFDown = array('f', [-100.0])
bbtag2SFDown = array('f', [-100.0])
passesBoosted = array('f', [-100.0])
passesResolved = array('f', [-100.0])
json = array('f', [-100.0])
norm = array('f', [-100.0])
evt = array('f', [-100.0])
ht = array('f', [-100.0])
xsec = array('f', [-100.0])
tPtSum = array('f', [-100.0])
ak4jet_pt = vector('double')()
ak4jet_eta = vector('double')()
ak4jet_phi = vector('double')()
ak4jet_mass = vector('double')()
ak4jetID = vector('double')()
ak4jetHeppyFlavour = vector('double')()
ak4jetMCFlavour = vector('double')()
ak4jetPartonFlavour = vector('double')() 
ak4jetHadronFlavour = vector('double')()
ak4jetCSVLSF = vector('double')()
ak4jetCSVLSF_Up = vector('double')()
ak4jetCSVLSF_Down = vector('double')()
ak4jetCSVMSF = vector('double')()
ak4jetCSVMSF_Up = vector('double')()
ak4jetCSVMSF_Down = vector('double')()
ak4jetCSVTSF = vector('double')()
ak4jetCSVTSF_Up = vector('double')()
ak4jetCSVTSF_Down = vector('double')()
ak4jetCMVALSF = vector('double')()
ak4jetCMVALSF_Up = vector('double')()
ak4jetCMVALSF_Down = vector('double')()
ak4jetCMVAMSF = vector('double')()
ak4jetCMVAMSF_Up = vector('double')()
ak4jetCMVAMSF_Down = vector('double')()
ak4jetCMVATSF = vector('double')()
ak4jetCMVATSF_Up = vector('double')()
ak4jetCMVATSF_Down = vector('double')()
ak4jetCSV = vector('double')()
ak4jetCMVA = vector('double')()
ak4jetCorr = vector('double')()
ak4jetCorrJECUp = vector('double')()
ak4jetCorrJECDown = vector('double')()
ak4jetCorrJER = vector('double')()
ak4jetCorrJERUp = vector('double')()
ak4jetCorrJERDown = vector('double')()
ak4genJetPt = vector('double')()
ak4genJetPhi = vector('double')()
ak4genJetEta = vector('double')()
ak4genJetMass = vector('double')()
ak4genJetID = vector('double')()

#creating the tree branches we need
myTree.Branch('jet1', jet1Array, 'pt/F:eta/F:phi/F:mass/F')
myTree.Branch('jet2', jet2Array, 'pt/F:eta/F:phi/F:mass/F')
myTree.Branch('jet1tau21', jet1tau21, 'jet1tau21/F')
myTree.Branch('jet2tau21', jet2tau21, 'jet2tau21/F')
myTree.Branch('jet1pmass', jet1pmass, 'jet1pmass/F')
myTree.Branch('jet2pmass', jet2pmass, 'jet2pmass/F')
myTree.Branch('jet1pmassunc', jet1pmassunc, 'jet1pmassunc/F')
myTree.Branch('jet2pmassunc', jet2pmassunc, 'jet2pmassunc/F')
myTree.Branch('jet1bbtag', jet1bbtag, 'jet1bbtag/F')
myTree.Branch('jet2bbtag', jet2bbtag, 'jet2bbtag/F')
myTree.Branch('jet1s1csv', jet1s1csv, 'jet1s1csv/F')
myTree.Branch('jet1s2csv', jet1s2csv, 'jet1s2csv/F')
myTree.Branch('jet2s1csv', jet2s1csv, 'jet2s1csv/F')
myTree.Branch('jet2s2csv', jet2s2csv, 'jet2s2csv/F')
myTree.Branch('nHiggsTags', nHiggsTags, 'nHiggsTags/F')
myTree.Branch('triggerpass', triggerpass, 'triggerpass/F')
myTree.Branch('triggerHT800pass', triggerHT800pass, 'triggerHT800pass/F')
myTree.Branch("HLT_ht800", trigger1, "HLT_ht800")
myTree.Branch("HLT_AK08", trigger2, "HLT_AK08")
myTree.Branch("HLT_HH4b", trigger3, "HLT_HH4b")
myTree.Branch("HLT_ht350", trigger_pre, "HLT_ht350")
myTree.Branch("HLT_mu20", trigger_muon, "HLT_mu20")
myTree.Branch('nTrueInt',nTrueInt,'nTrueInt/F')
#myTree.Branch('PUWeight',PUWeight,'PUWeight/F')
myTree.Branch('jet1ID', jet1ID, 'jet1ID/F')
myTree.Branch('jet2ID', jet2ID, 'jet2ID/F')
myTree.Branch('vtype', vtype, 'vtype/F') 
myTree.Branch('isData', isData, 'isData/F') 
myTree.Branch('jet1nbHadron', jet1nbHadron, 'jet1nbHadron/F')
myTree.Branch('jet2nbHadron', jet2nbHadron, 'jet2nbHadron/F')
myTree.Branch('jet1flavor', jet1flavor, 'jet1flavor/F') 
myTree.Branch('jet2flavor', jet2flavor, 'jet2flavor/F') 
myTree.Branch('jet1ncHadron', jet1ncHadron, 'jet1ncHadron/F')
myTree.Branch('jet2ncHadron', jet2ncHadron, 'jet2ncHadron/F')
myTree.Branch('genJet1Pt', genJet1Pt, 'genJet1Pt/F')
myTree.Branch('genJet1Phi', genJet1Phi, 'genJet1Phi/F')
myTree.Branch('genJet1Eta', genJet1Eta, 'genJet1Eta/F')
myTree.Branch('genJet1Mass', genJet1Mass, 'genJet1Mass/F')
myTree.Branch('genJet1ID', genJet1ID, 'genJet1ID/F')
myTree.Branch('genJet2Pt', genJet2Pt, 'genJet2Pt/F')
myTree.Branch('genJet2Phi', genJet2Phi, 'genJet2Phi/F')
myTree.Branch('genJet2Eta', genJet2Eta, 'genJet2Eta/F')
myTree.Branch('genJet2Mass', genJet2Mass, 'genJet2Mass/F')
myTree.Branch('genJet2ID', genJet2ID, 'genJet2ID/F')
myTree.Branch('jet1l1l2l3', jet1l1l2l3, 'jet1l1l2l3/F') 
myTree.Branch('jet2l1l2l3', jet2l1l2l3, 'jet2l1l2l3/F') 
myTree.Branch('jet1l2l3', jet1l2l3, 'jet1l2l3/F')
myTree.Branch('jet2l2l3', jet2l2l3, 'jet2l2l3/F')
myTree.Branch('jet1JER', jet1JER, 'jet1JER/F') 
myTree.Branch('jet2JER', jet2JER, 'jet2JER/F') 
myTree.Branch('puWeights', puWeights, 'puWeights/F')
myTree.Branch('puWeightsUp', puWeightsUp, 'puWeightsUp/F')
myTree.Branch('puWeightsDown', puWeightsDown, 'puWeightsDown/F')
myTree.Branch('bbtag1SF', bbtag1SF, 'bbtag1SF/F')
myTree.Branch('bbtag2SF', bbtag2SF, 'bbtag2SF/F')
myTree.Branch('bbtag1SFUp', bbtag1SFUp, 'bbtag1SFUp/F')
myTree.Branch('bbtag2SFUp', bbtag2SFUp, 'bbtag2SFUp/F')
myTree.Branch('bbtag1SFDown', bbtag1SFDown, 'bbtag1SFDown/F')
myTree.Branch('bbtag2SFDown', bbtag2SFDown, 'bbtag2SFDown/F')
myTree.Branch('json', json, 'json/F')
myTree.Branch('norm', norm, 'norm/F')
myTree.Branch('evt', evt, 'evt/F')
myTree.Branch('ht', ht, 'ht/F')
myTree.Branch('xsec', xsec, 'xsec/F')
myTree.Branch('passesBoosted', passesBoosted, 'passesBoosted/F')
myTree.Branch('passesResolved', passesResolved, 'passesResolved/F')
myTree.Branch('tPtSum', tPtSum, 'tPtSum/F')
myTree.Branch('ak4jet_pt',ak4jet_pt)
myTree.Branch('ak4jet_eta',ak4jet_eta)
myTree.Branch('ak4jet_phi',ak4jet_phi)
myTree.Branch('ak4jet_mass',ak4jet_mass)
myTree.Branch('ak4jetID',ak4jetID)
myTree.Branch('ak4jetHeppyFlavour', ak4jetHeppyFlavour)
myTree.Branch('ak4jetMCFlavour', ak4jetMCFlavour)
myTree.Branch('ak4jetPartonFlavour', ak4jetPartonFlavour)
myTree.Branch('ak4jetHadronFlavour', ak4jetHadronFlavour)
myTree.Branch('ak4jetCSVLSF', ak4jetCSVLSF)
myTree.Branch('ak4jetCSVLSF_Up', ak4jetCSVLSF_Up)
myTree.Branch('ak4jetCSVLSF_Down', ak4jetCSVLSF_Down)
myTree.Branch('ak4jetCSVMSF', ak4jetCSVMSF)
myTree.Branch('ak4jetCSVMSF_Up', ak4jetCSVMSF_Up)
myTree.Branch('ak4jetCSVMSF_Down', ak4jetCSVMSF_Down)
myTree.Branch('ak4jetCSVTSF', ak4jetCSVTSF)
myTree.Branch('ak4jetCSVTSF_Up', ak4jetCSVTSF_Up)
myTree.Branch('ak4jetCSVTSF_Down', ak4jetCSVTSF_Down) 
myTree.Branch('ak4jetCMVALSF', ak4jetCMVALSF)
myTree.Branch('ak4jetCMVALSF_Up', ak4jetCMVALSF_Up)
myTree.Branch('ak4jetCMVALSF_Down', ak4jetCMVALSF_Down) 
myTree.Branch('ak4jetCMVAMSF', ak4jetCMVAMSF)
myTree.Branch('ak4jetCMVAMSF_Up', ak4jetCMVAMSF_Up)
myTree.Branch('ak4jetCMVAMSF_Down', ak4jetCMVAMSF_Down)
myTree.Branch('ak4jetCMVATSF', ak4jetCMVATSF)
myTree.Branch('ak4jetCMVATSF_Up', ak4jetCMVATSF_Up)
myTree.Branch('ak4jetCMVATSF_Down', ak4jetCMVATSF_Down)
myTree.Branch('ak4jetCSV', ak4jetCSV)
myTree.Branch('ak4jetCMVA', ak4jetCMVA)
myTree.Branch('ak4jetCorr', ak4jetCorr)
myTree.Branch('ak4jetCorrJECUp', ak4jetCorrJECUp)
myTree.Branch('ak4jetCorrJECDown', ak4jetCorrJECDown)
myTree.Branch('ak4jetCorrJER', ak4jetCorrJER)
myTree.Branch('ak4jetCorrJERUp', ak4jetCorrJERUp)
myTree.Branch('ak4jetCorrJERDown', ak4jetCorrJERDown)
myTree.Branch('ak4genJetPt', ak4genJetPt) 
myTree.Branch('ak4genJetPhi', ak4genJetPhi)
myTree.Branch('ak4genJetEta', ak4genJetEta)
myTree.Branch('ak4genJetMass', ak4genJetMass)
myTree.Branch('ak4genJetID', ak4genJetID)

files_list	= open_files( inputfile )
#nevent = treeMine.GetEntries();

#list of histograms that may be useful
tpoj = ROOT.TH1F("tpoj", "Before any cuts", 6, -0.5, 5.5)
tpo0 = ROOT.TH1F("tpo0", "After Json", 6, -0.5, 5.5)
tpo1 = ROOT.TH1F("tpo1", "After Trigger", 6, -0.5, 5.5)
tpo2 = ROOT.TH1F("tpo2", "After jet cuts", 6, -0.5, 5.5)
weight = ROOT.TH1F("tpo2", "After jet cuts", 6, -0.5, 5.5)

gSystem.Load("DrawFunctions_h.so")

count = 0
weights = 0
#loop over files
for i in range(num1, num2):
    files = files_list[i]
    print files
    f1 = ROOT.TFile(files, "READ")
    treeMine  = f1.Get('tree')
    nevent = treeMine.GetEntries();
    histo_weight=f1.Get("CountWeighted")
    weights+=histo_weight.GetBinContent(1)

    #loop over events in file
    print "Start looping"
    for j in range(0,nevent):
        treeMine.GetEntry(j)
	count = count + 1
 	if count % 1000 == 0 :
	    print "processing events", count
        #variables we need from the heppy ntuple
	genJetPt = treeMine.GenJet_pt
        genJetEta = treeMine.GenJet_eta
        genJetPhi = treeMine.GenJet_phi
        genJetMass = treeMine.GenJet_mass
        if options.isMC == 'True':
            genBH = treeMine.GenJet_numBHadrons 
            genCH = treeMine.GenJet_numCHadrons
        fNJets = treeMine.nJet
        fJetPt  = treeMine.Jet_pt
	fJetEta  = treeMine.Jet_eta
        fJetPhi = treeMine.Jet_phi
        fJetMass = treeMine.Jet_mass
        fJetID = treeMine.Jet_id
        if options.isMC == 'True':
            fJetHeppyFlavour = treeMine.Jet_heppyFlavour
            fJetMCFlavour = treeMine.Jet_mcFlavour
            fJetPartonFlavour = treeMine.Jet_partonFlavour
            fJetHadronFlavour = treeMine.Jet_hadronFlavour
            fJetCSVLSF = treeMine.Jet_btagCSVLSF
            fJetCSVLSF_Up = treeMine.Jet_btagCSVLSF_Up
            fJetCSVLSF_Down = treeMine.Jet_btagCSVLSF_Down
            fJetCSVMSF = treeMine.Jet_btagCSVMSF
            fJetCSVMSF_Up = treeMine.Jet_btagCSVMSF_Up
            fJetCSVMSF_Down = treeMine.Jet_btagCSVMSF_Down
            fJetCSVTSF = treeMine.Jet_btagCSVTSF
            fJetCSVTSF_Up = treeMine.Jet_btagCSVTSF_Up
            fJetCSVTSF_Down = treeMine.Jet_btagCSVTSF_Down
            fJetCMVALSF = treeMine.Jet_btagCMVAV2LSF
            fJetCMVALSF_Up = treeMine.Jet_btagCMVAV2LSF_Up
            fJetCMVALSF_Down = treeMine.Jet_btagCMVAV2LSF_Down
            fJetCMVAMSF = treeMine.Jet_btagCMVAV2MSF
            fJetCMVAMSF_Up = treeMine.Jet_btagCMVAV2MSF_Up
            fJetCMVAMSF_Down = treeMine.Jet_btagCMVAV2MSF_Down
            fJetCMVATSF = treeMine.Jet_btagCMVAV2TSF
            fJetCMVATSF_Up = treeMine.Jet_btagCMVAV2TSF_Up
            fJetCMVATSF_Down = treeMine.Jet_btagCMVAV2TSF_Down
        fJetCSV = treeMine.Jet_btagCSVV0
        fJetCMVA = treeMine.Jet_btagCMVAV2
        fJetCorr = treeMine.Jet_corr
        fJetCorrJECUp = treeMine.Jet_corr_JECUp
        fJetCorrJECDown = treeMine.Jet_corr_JECDown
        if options.isMC == 'True':
            fJetCorrJER = treeMine.Jet_corr_JER
            fJetCorrJERUp = treeMine.Jet_corr_JERUp
            fJetCorrJERDown = treeMine.Jet_corr_JERDown
        fNJets = treeMine.nJet
	fjUngroomedN = treeMine.nFatjetAK08ungroomed
        fjUngroomedPt = treeMine.FatjetAK08ungroomed_pt
	fjUngroomedEta = treeMine.FatjetAK08ungroomed_eta
	fjUngroomedPhi = treeMine.FatjetAK08ungroomed_phi
	fjUngroomedMass = treeMine.FatjetAK08ungroomed_mass
	fjUngroomedSDMass = treeMine.FatjetAK08ungroomed_msoftdrop
	fjUngroomedTau1 = treeMine.FatjetAK08ungroomed_tau1
	fjUngroomedTau2 = treeMine.FatjetAK08ungroomed_tau2
	fjUngroomedBbTag = treeMine.FatjetAK08ungroomed_bbtag
	fjUngroomedJetID = treeMine.FatjetAK08ungroomed_id_Tight
	fjUngroomedPrunedMass = treeMine.FatjetAK08ungroomed_mprunedcorr
        fjUngroomedPrunedMass_Unc = treeMine.FatjetAK08ungroomed_mpruned
        if options.isMC == 'True':
            fjUngroomedFlavour = treeMine.FatjetAK08ungroomed_Flavour
            fjUngroomedBHadron = treeMine.FatjetAK08ungroomed_BhadronFlavour
            fjUngroomedCHadron = treeMine.FatjetAK08ungroomed_ChadronFlavour
            fjUngroomedJER = treeMine.FatjetAK08ungroomed_GenPt
        fjL2L3 = treeMine.FatjetAK08ungroomed_JEC_L2L3
        fjL1L2L3 = treeMine.FatjetAK08ungroomed_JEC_L1L2L3
        if options.isMC == 'True':
            puweight = treeMine.puWeight 
            puweightUp = treeMine.puWeightUp
            puweightDown = treeMine.puWeightDown
	sjPrunedPt = treeMine.SubjetAK08softdrop_pt
	sjPrunedEta = treeMine.SubjetAK08softdrop_eta
	sjPrunedPhi = treeMine.SubjetAK08softdrop_phi
	sjPrunedMass = treeMine.SubjetAK08softdrop_mass
	sjPrunedBtag = treeMine.SubjetAK08softdrop_btag
	if options.isMC == 'True':
            hPt = treeMine.GenHiggsBoson_pt
            hEta = treeMine.GenHiggsBoson_eta
            hPhi = treeMine.GenHiggsBoson_phi
            hMass = treeMine.GenHiggsBoson_mass
	hltHT800 = treeMine.HLT_BIT_HLT_PFHT800_v
        hltAK8 = treeMine.HLT_BIT_HLT_AK8DiPFJet250_200_TrimMass30_BTagCSV0p45_v
        hltHH4b = treeMine.HLT_HH4bHighLumi
#        hltDouble = treeMine.HLT_BIT_HLT_DoubleJet90_Double30_TripleBTagCSV0p67_v
#        hltQuad = treeMine.HLT_BIT_HLT_QuadJet45_TripleBTagCSV0p67_v
        Data = treeMine.isData
        vType = treeMine.Vtype
        EVT = treeMine.evt 
        if options.isMC == 'True':
            nTInt = treeMine.nTrueInt
        genTopPts = treeMine.GenTop_pt
        JSON = treeMine.json
       	#saving whether an event passes desired trigger
        matched = 0  
        matched800 = 0
	if hltAK8 > 0:
            matched += 1
        if hltHT800 > 0:
            matched800 += 1
#        if hltDouble > 0:
#            matched += 1
#        if hltQuad > 0:
#            matched += 1
        if hltHH4b > 0:
            matched += 1
        triggerpass[0] = matched + matched800
        triggerHT800pass[0] = matched800
        trigger1[0]=hltHT800
        trigger2[0]=hltAK8
        trigger3[0]=hltHH4b
        trigger_pre[0]=treeMine.HLT_BIT_HLT_PFHT350_v
        trigger_muon[0]=treeMine.HLT_BIT_HLT_Mu20_v
        if options.isMC == 'True':
            nTrueInt[0]=nTInt

        #json for data
        tpoj.Fill(triggerpass[0])
        if Data > 0 and treeMine.json_silver < 1:
            print "rejected"
        if Data > 0 and treeMine.json_silver < 1:
            continue		
		
        tpo0.Fill(triggerpass[0])

        #requiring event pass trigger
        if options.trigger == 'True' and triggerpass[0] < 1:
            continue

        tpo1.Fill(triggerpass[0])

        hT =0
        for i in range(0,fNJets):
                if abs(fJetEta[i])<3 and fJetPt[i] >40 :
                        hT=hT+fJetPt[i]

        ht[0] = hT
        
	#filling an array with jet 4-vectors for jets pt > 30 and |eta| < 2.5, an array of tau21s, and an array of bbtag values, pmass, id, nbhadrons, nchadrons, flavor, l1l2l3 corr, l2l3 corr, JER
        jets = []
	jet_tau = []
	jet_bbtag = []
        jet_pmass = []
        jet_pmassunc = []
        jet_id = []
        jet_nb = []
        jet_nc = []
        jet_flav = []
        jet_123 = []
        jet_23 = []
        jet_JER = []
        for j in range(len(fjUngroomedPt)):
            jettemp = ROOT.TLorentzVector()
            jettemp.SetPtEtaPhiM(fjUngroomedPt[j], fjUngroomedEta[j], fjUngroomedPhi[j], fjUngroomedMass[j])
            if (options.syst=="FJEC_Up"):
                            correction_factor=1+(treeMine.FatjetAK08ungroomed_JEC_UP[j]-treeMine.FatjetAK08ungroomed_JEC_L1L2L3[j])
                            jettemp*=correction_factor
            if (options.syst=="FJEC_Down"):
                            correction_factor=1-(treeMine.FatjetAK08ungroomed_JEC_UP[j]-treeMine.FatjetAK08ungroomed_JEC_L1L2L3[j])
                            jettemp*=correction_factor
            if (options.syst=="FJER_Up"):
                            correction_factor=div_except(treeMine.FatjetAK08ungroomed_JER_UP_PT[j],treeMine.FatjetAK08ungroomed_pt[j])
                            jettemp*=correction_factor
            if (options.syst=="FJER_Down"):
                            pJERDown=2*treeMine.FatjetAK08ungroomed_pt[j]-treeMine.FatjetAK08ungroomed_JER_UP_PT[j]
                            correction_factor=div_except((pJERDown),treeMine.FatjetAK08ungroomed_pt[j])
                            jettemp*=correction_factor

	    if jettemp.Pt() > 30. and abs(jettemp.Eta()) < 2.4: 	
                    jets.append(jettemp)
		    if fjUngroomedTau1[j] > 0:
			    jet_tau.append(fjUngroomedTau2[j]/fjUngroomedTau1[j])
		    else:
			    jet_tau.append(100)
                    mpruned_syst=fjUngroomedPrunedMass[j]
                    if (options.syst=="MJEC_Down"):
                            sigma=treeMine.FatjetAK08ungroomed_JEC_L2L3_UP[j]-treeMine.FatjetAK08ungroomed_JEC_L2L3[j]
                            mpruned_syst=treeMine.FatjetAK08ungroomed_mpruned[j]*(treeMine.FatjetAK08ungroomed_JEC_L2L3[j]-sigma)
                    if (options.syst=="MJEC_Up"): 
                        mpruned_syst=treeMine.FatjetAK08ungroomed_mpruned[j]*treeMine.FatjetAK08ungroomed_JEC_L2L3_UP[j]

		    jet_bbtag.append(fjUngroomedBbTag[j])	
                    jet_pmass.append(fjUngroomedPrunedMass[j])
                    jet_pmassunc.append(fjUngroomedPrunedMass_Unc[j])
                    jet_id.append(fjUngroomedJetID[j])
                    if options.isMC == 'True':
                        jet_nb.append(fjUngroomedBHadron[j])
                        jet_nc.append(fjUngroomedCHadron[j])
                        jet_flav.append(fjUngroomedFlavour[j])
                        jet_JER.append(fjUngroomedJER[j])
                    jet_123.append(fjL1L2L3[j])
                    jet_23.append(fjL2L3[j])


	if options.jets == 'True' and len(jets) < 1: # two jets with pt > 30 and |eta| < 2.5
		continue
        
        jet1Array[0] = jets[0].Pt()
        jet1Array[1] = jets[0].Eta()
        jet1Array[2] = jets[0].Phi()
        jet1Array[3] = jets[0].M()
        if len(jets) > 1:
            jet2Array[0] = jets[1].Pt()
            jet2Array[1] = jets[1].Eta()
            jet2Array[2] = jets[1].Phi()
            jet2Array[3] = jets[1].M()
        
        
        idxH1 = 0
        idxH2 = 1
        
	#higgs tagging - matching higgs gen jet to the 1 and 2 pt jet
	if options.isMC == 'True':
            hjets = []
            for j in range(len(hPt)):
		jettemp = ROOT.TLorentzVector()
		jettemp.SetPtEtaPhiM(hPt[j], hEta[j], hPhi[j], hMass[j])
		hjets.append(jettemp)

                h1 = MatchCollection(hjets, jets[idxH1])

                if len(jets) > 1: 
                    h2 = MatchCollection(hjets, jets[idxH2])

                nHiggsTags[0] = 0
                if h1 > -1:
                    nHiggsTags[0] += 1
                if len(jets) > 1:
                    if h2 > -1:
                        nHiggsTags[0] += 1

        jet1pmass[0] = jet_pmass[idxH1]
        jet1pmassunc[0] = jet_pmassunc[idxH1]
        if len(jets) > 1: 
            jet2pmass[0] = jet_pmass[idxH2]
            jet2pmassunc[0] = jet_pmassunc[idxH2]
	jet1ID[0] = jet_id[idxH1]
        if len(jets) > 1: 
            jet2ID[0] = jet_id[idxH2]
	jet1tau21[0] = jet_tau[idxH1]# fjUngroomedTau2[j1]/fjUngroomedTau1[j1]
        if len(jets) > 1: 
            jet2tau21[0] = jet_tau[idxH2]# fjUngroomedTau2[j2]/fjUngroomedTau1[j2]
        if options.isMC == 'True':
            jet1nbHadron[0] = jet_nb[idxH1]
            if len(jets) > 1: 
                jet2nbHadron[0] = jet_nb[idxH2]
            jet1ncHadron[0] = jet_nc[idxH1]
            if len(jets) > 1: 
                jet2ncHadron[0] = jet_nc[idxH2]
            jet1flavor[0] = jet_flav[idxH1]
            if len(jets) > 1: 
                jet2flavor[0] = jet_flav[idxH2]
            jet1JER[0] = jet_JER[idxH1]
            if len(jets) > 1: 
                jet2JER[0] = jet_JER[idxH2]
        jet1l1l2l3[0] = jet_123[idxH1]
        if len(jets) > 1: 
            jet2l1l2l3[0] = jet_123[idxH2]
        jet1l2l3[0] = jet_23[idxH1]
        if len(jets) > 1: 
            jet2l2l3[0] = jet_23[idxH2]

	#filling min subjet csv
	subjets = []
	jet1sj = []
	jet1sjcsv = []
	jet2sj = []
	jet2sjcsv = []
	samesj = 0
        samesj = 0
        for j in range(len(sjPrunedPt)):
            jettemp = ROOT.TLorentzVector()
            jettemp.SetPtEtaPhiM(sjPrunedPt[j], sjPrunedEta[j], sjPrunedPhi[j], sjPrunedMass[j])
            subjets.append(jettemp)

        if len(jets) == 1:
            for j in range(len(subjets)):
                dR1 = subjets[j].DeltaR(jets[idxH1])
                if dR1 < 0.4:
                    jet1sj.append(subjets[j])
                    jet1sjcsv.append(sjPrunedBtag[j])
                n1sj = len(jet1sj)

            jet1s1csv[0] = -1.
            jet2s1csv[0] = -1.
        
        if len(jets) > 1:
            for j in range(len(subjets)):
                dR1 = subjets[j].DeltaR(jets[idxH1])
                dR2 = subjets[j].DeltaR(jets[idxH2])
                if dR1 < 0.4 and dR2 < 0.4:
                    samesj += 1
                elif dR1 < 0.4:
                    jet1sj.append(subjets[j])
                    jet1sjcsv.append(sjPrunedBtag[j])
                elif dR2 < 0.4:
                    jet2sj.append(subjets[j])
                    jet2sjcsv.append(sjPrunedBtag[j])
                n1sj = len(jet1sj)
                n2sj = len(jet2sj)

            #Finding the subjet csvs
            jet1s1csv[0] = -1.
            jet2s1csv[0] = -1.
            jet1s2csv[0] = -1.
            jet2s2csv[0] = -1.
        
            if len(jet1sjcsv) > 1:
                jet1s1csv[0] = jet1sjcsv[0]
                jet1s2csv[0] = jet1sjcsv[1]
            elif len(jet1sjcsv) == 1:
                jet1s1csv[0] = jet1sjcsv[0]

            if len(jet2sjcsv) > 1:
                jet2s1csv[0] = jet2sjcsv[0]
                jet2s2csv[0] = jet2sjcsv[1]
            elif len(jet2sjcsv) == 1:
                jet2s1csv[0] = jet2sjcsv[0]
        
        #finding gen jets to match higgs jets
        if options.isMC == 'True':
            ujets = []
            ujetsCH = []
            ujetsBH = []
            for j in range(len(genJetPt)):
                jettemp = ROOT.TLorentzVector()
                jettemp.SetPtEtaPhiM(genJetPt[j], genJetEta[j], genJetPhi[j], genJetMass[j])
                ujets.append(jettemp)
                ujetsCH.append(genCH[j])
                ujetsBH.append(genBH[j])

            j1 = MatchCollection(ujets, jets[idxH1])
            if len(jets) > 1: 
                j2 = MatchCollection2(ujets, jets[idxH2],j1)

        #filling gen jet info
            genJet1Pt[0] = ujets[j1].Pt()
            genJet1Phi[0] = ujets[j1].Phi()
            genJet1Eta[0] = ujets[j1].Eta()
            genJet1Mass[0] = ujets[j1].M()
            genJet1ID[0] = j1
            if len(jets) > 1: 
                genJet2Pt[0] = ujets[j2].Pt()
                genJet2Phi[0] = ujets[j2].Phi()
                genJet2Eta[0] = ujets[j2].Eta()
                genJet2Mass[0] = ujets[j2].M()
                genJet2ID[0] = j2
        
        #getting total gen top pts
        tPtSums = 0
        if options.isMC == 'True':
            for pt in treeMine.GenTop_pt:
                tPtSums = tPtSums + pt
        tPtSum[0] = tPtSums

	#filling bbtag
	jet1bbtag[0] = jet_bbtag[idxH1] #fjUngroomedBbTag[j1]
	if len(jets) > 1: 
            jet2bbtag[0] = jet_bbtag[idxH2] # fjUngroomedBbTag[j2]
	
        #writing variables to the tree    
        #jet1pt[0] = jets[idxH1].Pt()
	#jet2pt[0] = jets[idxH2].Pt()
	#jet1eta[0] = jets[idxH1].Eta()
	#jet2eta[0] = jets[idxH2].Eta()
	#etadiff[0] = abs(jets[idxH1].Eta() - jets[idxH2].Eta())
	#dijetmass[0] = (jets[idxH1] + jets[idxH2]).M()
	#dijetmass_corr[0] = (jets[idxH1] + jets[idxH2]).M() - (jet1pmass[0]-125)-(jet2pmass[0]-125)
#        PUWeight[0]=weight2(nTInt)
        if options.isMC == 'True':
            puWeights[0]= puweight
            puWeightsUp[0] = puweightUp
            puWeightsDown[0] = puweightDown
            nTrueInt[0] = nTInt 
            xsec[0] = float(options.xsec)
        json[0] = JSON
        evt[0] = EVT
        vtype[0] = vType
        if Data:
            isData[0] = 1
            norm[0] = 1
        else:
            isData[0] = 0

        #hbb tagger SFs
                #handling hbb tagger SFs
        sf1 = -1
        sf2 = -1
        sf1change = 1000000
        sf2change = 1000000
        
        if jets[0].Pt() < 400:
            sf1 = 0.929
            sf1change = 0.078
        elif jets[0].Pt() >= 400 and jets[0].Pt() < 500:
            sf1 = 0.999
            sf1change = 0.126
        elif jets[0].Pt() >= 500 and jets[0].Pt() < 600:
            sf1 = 0.933
            sf1change = 0.195
        elif jets[0].Pt() >= 600:
            sf1 = 1.048
            sf1change = 0.215
        
        bbtag1SF[0] = sf1
        bbtag1SFUp[0] = sf1*(1+sf1change)
        bbtag1SFDown[0] = sf1*(1-sf1change)

        if len(jets) > 1:
            if jets[1].Pt() < 400:
                sf2 = 0.929
                sf2change = 0.078
            elif jets[1].Pt() >= 400 and jets[1].Pt() < 500:
                sf2 = 0.999
                sf2change = 0.126
            elif jets[1].Pt() >= 500 and jets[1].Pt() < 600:
                sf2 = 0.933
                sf2change = 0.195
            elif jets[1].Pt() >= 600:
                sf2 = 1.048
                sf2change = 0.215

            bbtag2SF[0] = sf2
            bbtag2SFUp[0] = sf2*(1+sf2change)
            bbtag2SFDown[0] = sf2*(1-sf2change)


        if len(jets) > 1 and triggerHT800pass[0] > 0 and jets[0].Pt() > 300 and jets[1].Pt() > 300 and abs(jets[0].Eta() - jets[1].Eta()) < 1.3 and ((jets[idxH1] + jets[idxH2]).M() - (jet1pmass[0]-125)-(jet2pmass[0]-125)) > 800 and jet1tau21[0] < 0.6 and jet2tau21[0] < 0.6 and jet1pmass[0] > 105 and jet1pmass[0] < 135 and jet2pmass[0] > 105 and jet2pmass[0] < 135 and jet1bbtag[0] > 0.6 and jet2bbtag[0] > 0.6:
            passesBoosted[0] = 1
        else:
            passesBoosted[0] = 0

        ak4jet_pt.clear()
        ak4jet_eta.clear()
        ak4jet_phi.clear()
        ak4jet_mass.clear()
        ak4jetID.clear()
        ak4jetHeppyFlavour.clear()
        ak4jetMCFlavour.clear()
        ak4jetPartonFlavour.clear() 
        ak4jetHadronFlavour.clear()
        ak4jetCSVLSF.clear()
        ak4jetCSVLSF_Up.clear()
        ak4jetCSVLSF_Down.clear()
        ak4jetCSVMSF.clear()
        ak4jetCSVMSF_Up.clear()
        ak4jetCSVMSF_Down.clear()
        ak4jetCSVTSF.clear()
        ak4jetCSVTSF_Up.clear()
        ak4jetCSVTSF_Down.clear()
        ak4jetCMVALSF.clear()
        ak4jetCMVALSF_Up.clear()
        ak4jetCMVALSF_Down.clear()
        ak4jetCMVAMSF.clear()
        ak4jetCMVAMSF_Up.clear()
        ak4jetCMVAMSF_Down.clear()
        ak4jetCMVATSF.clear()
        ak4jetCMVATSF_Up.clear()
        ak4jetCMVATSF_Down.clear()
        ak4jetCSV.clear()
        ak4jetCMVA.clear()
        ak4jetCorr.clear()
        ak4jetCorrJECUp.clear()
        ak4jetCorrJECDown.clear()
        ak4jetCorrJER.clear()
        ak4jetCorrJERUp.clear()
        ak4jetCorrJERDown.clear()
        ak4genJetPt.clear()
        ak4genJetPhi.clear()
        ak4genJetEta.clear()
        ak4genJetMass.clear()
        ak4genJetID.clear()
           
        #ak4 jets
        akjets = [] 
        for j in range(len(fJetPt)):
            if (options.syst=="JEC_Up"): jet_pT = treeMine.Jet_pt[j]*treeMine.Jet_corr_JECUp[j]/treeMine.Jet_corr[j]
            elif (options.syst=="JEC_Down"): jet_pT = treeMine.Jet_pt[j]*treeMine.Jet_corr_JECDown[j]/treeMine.Jet_corr[j]
            elif (options.syst=="JER_Up"): jet_pT = treeMine.Jet_pt[j]*treeMine.Jet_corr_JERUp[j]*treeMine.Jet_corr_JER[j]
            elif (options.syst=="JER_Down"): jet_pT = treeMine.Jet_pt[j]*treeMine.Jet_corr_JERDown[j]*treeMine.Jet_corr_JER[j]
            else: jet_pT = treeMine.Jet_pt[j]
            jettemp = ROOT.TLorentzVector()
            jettemp.SetPtEtaPhiM(jet_pT, fJetEta[j], fJetPhi[j], fJetMass[j])
 	    if abs(jettemp.Eta()) < 2.4 and jet_pT > 30:     
                akjets.append(jettemp)
                ak4jet_pt.push_back(jet_pT)
                ak4jet_eta.push_back(fJetEta[j])
                ak4jet_phi.push_back(fJetPhi[j])
                ak4jet_mass.push_back(fJetMass[j])
                ak4jetID.push_back(fJetID[j])
                if options.isMC == 'True':
                    ak4jetHeppyFlavour.push_back(fJetHeppyFlavour[j])
                    ak4jetMCFlavour.push_back(fJetMCFlavour[j])
                    ak4jetPartonFlavour.push_back(fJetPartonFlavour[j]) 
                    ak4jetHadronFlavour.push_back(fJetHadronFlavour[j])
                    ak4jetCSVLSF.push_back(fJetCSVLSF[j])
                    ak4jetCSVLSF_Up.push_back(fJetCSVLSF_Up[j])
                    ak4jetCSVLSF_Down.push_back(fJetCSVLSF_Down[j])
                    ak4jetCSVMSF.push_back(fJetCSVMSF[j])
                    ak4jetCSVMSF_Up.push_back(fJetCSVMSF_Up[j])
                    ak4jetCSVMSF_Down.push_back(fJetCSVMSF_Down[j])
                    ak4jetCSVTSF.push_back(fJetCSVTSF[j])
                    ak4jetCSVTSF_Up.push_back(fJetCSVTSF_Up[j])
                    ak4jetCSVTSF_Down.push_back(fJetCSVTSF_Down[j])
                    ak4jetCMVALSF.push_back(fJetCMVALSF[j])
                    ak4jetCMVALSF_Up.push_back(fJetCMVALSF_Up[j])
                    ak4jetCMVALSF_Down.push_back(fJetCMVALSF_Down[j])
                    ak4jetCMVAMSF.push_back(fJetCMVAMSF[j])
                    ak4jetCMVAMSF_Up.push_back(fJetCMVAMSF_Up[j])
                    ak4jetCMVAMSF_Down.push_back(fJetCMVAMSF_Down[j])
                    ak4jetCMVATSF.push_back(fJetCMVATSF[j])
                    ak4jetCMVATSF_Up.push_back(fJetCMVATSF_Up[j])
                    ak4jetCMVATSF_Down.push_back(fJetCMVATSF_Down[j])
                    ak4jetCorr.push_back(fJetCorr[j])
                    ak4jetCorrJECUp.push_back(fJetCorrJECUp[j])
                    ak4jetCorrJECDown.push_back(fJetCorrJECDown[j])
                    ak4jetCorrJER.push_back(fJetCorrJER[j])
                    ak4jetCorrJERUp.push_back(fJetCorrJERUp[j])
                    ak4jetCorrJERDown.push_back(fJetCorrJERDown[j])
                ak4jetCSV.push_back(fJetCSV[j])
                ak4jetCMVA.push_back(fJetCMVA[j])

                if options.isMC == 'True':
                    akj = MatchCollection(ujets, jettemp)
                    ak4genJetPt.push_back(ujets[akj].Pt())
                    ak4genJetEta.push_back(ujets[akj].Eta())
                    ak4genJetPhi.push_back(ujets[akj].Phi())
                    ak4genJetMass.push_back(ujets[akj].M())
                    ak4genJetID.push_back(akj)
        
        if options.jets == 'True' and len(ak4jet_pt) < 2:        
            continue


        #resolved
        ak4res = []
        chi2_old=200
        foundRes = False
        passesResolved[0] = 0
        for j in range(len(akjets)):
            if ak4jetCMVA[j] > 0.185:
                ak4res.append(akjets[j])
        if len(ak4res) > 3:
            jet1=TLorentzVector()
            jet2=TLorentzVector()
            jet3=TLorentzVector()    
            jet4=TLorentzVector()
            for l in range(len(ak4res)):
                jet1.SetPtEtaPhiM(ak4res[l].Pt(), ak4res[l].Eta(), ak4res[l].Phi(), ak4res[l].M())
                for m in range(len(ak4res)):
                    if m!=l:
                        jet2.SetPtEtaPhiM(ak4res[m].Pt(), ak4res[m].Eta(), ak4res[m].Phi(),ak4res[m].M())
                        for n in range(len(ak4res)):
                            if (n!=l and n!=m):
                                jet3.SetPtEtaPhiM(ak4res[n].Pt(), ak4res[n].Eta(), ak4res[n].Phi(),ak4res[n].M())
                                for k in range(len(ak4res)):
                                    if (k!=l and k!=m and k!=n):
                                        jet4.SetPtEtaPhiM(ak4res[k].Pt(), ak4res[k].Eta(), ak4res[k].Phi(),ak4res[k].M())

                                        dijet1=jet1+jet2
                                        dijet2=jet3+jet4
                                        
                                        deltar1=jet1.DeltaR(jet2)
                                        deltar2=jet3.DeltaR(jet4)
                                        
                                        mH1=dijet1.M()
                                        mH2=dijet2.M()
                                        
                                        chi2=((mH1-115)/23)**2+((mH2-115)/23)**2
                                        
                                        if (chi2<chi2_old and deltar1<1.5 and deltar2<1.5):
                                            chi2_old=chi2
                                            foundRes=True

        if foundRes:
            chi=chi2_old**0.5
            if chi<=1:
                passesResolved[0] = 1

        tpo2.Fill(triggerpass[0])

	#filling the tree
        myTree.Fill()

	#filling error values for each object
	#jet1pt[0] = -100.0
	#jet2pt[0] = -100.0
	#jet1eta[0] = -100.0
	#jet2eta[0] = -100.0
	#etadiff[0] = -100.0
	#dijetmass[0] = -100.0
	#dijetmass_corr[0]=-100.0
	jet1pmass[0] = -100.0
	jet2pmass[0] = -100.0
	jet1tau21[0] = -100.0
	jet2tau21[0] = -100.0
	jet1bbtag[0] = -100.0
	jet2bbtag[0] = -100.0
	triggerpass[0] = -100.0
#	PUWeight[0]= -100.0
	
    
    f1.Close()

print "OK"

f.cd()
f.Write()
f.Close()




