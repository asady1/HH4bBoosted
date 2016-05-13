simport os
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

parser.add_option("-d", "--deta", dest="deta", 
		  help="bool for delta eta cut")

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
bbtag2SFUP = array('f', [-100.0])
bbtag1SFDown = array('f', [-100.0])
bbtag2SFDown = array('f', [-100.0])
passesBoosted = array('f', [-100.0])
json = array('f', [-100.0])
norm = array('f', [-100.0])
evt = array('f', [-100.0])
ht = array('f', [-100.0])
xsec = array('f', [-100.0])
tPtSum = array('f', [-100.0])
ak4jet1Array = array('f', [-1.0, -100, -100, -1.0])
ak4jet2Array = array('f', [-1.0, -100, -100, -1.0])
ak4jet3Array = array('f', [-1.0, -100, -100, -1.0])
ak4jet1ID = array('f', [-100.0])
ak4jet2ID = array('f', [-100.0])
ak4jet3ID = array('f', [-100.0])
ak4jet1HeppyFlavour = array('f', [-100.0])
ak4jet1MCFlavour = array('f', [-100.0])
ak4jet1PartonFlavour = array('f', [-100.0])
ak4jet1HadronFlavour = array('f', [-100.0])
ak4jet2HeppyFlavour = array('f', [-100.0])
ak4jet2MCFlavour = array('f', [-100.0])
ak4jet2PartonFlavour = array('f', [-100.0])
ak4jet2HadronFlavour = array('f', [-100.0])
ak4jet3HeppyFlavour = array('f', [-100.0])
ak4jet3MCFlavour = array('f', [-100.0])
ak4jet3PartonFlavour = array('f', [-100.0])
ak4jet3HadronFlavour = array('f', [-100.0])
ak4jet1CSVLSF = array('f', [-100.0])
ak4jet1CSVLSF_Up = array('f', [-100.0])
ak4jet1CSVLSF_Down = array('f', [-100.0])
ak4jet1CSVMSF = array('f', [-100.0])
ak4jet1CSVMSF_Up = array('f', [-100.0])
ak4jet1CSVMSF_Down = array('f', [-100.0])
ak4jet1CSVTSF = array('f', [-100.0])
ak4jet1CSVTSF_Up = array('f', [-100.0])
ak4jet1CSVTSF_Down = array('f', [-100.0])
ak4jet1CMVALSF = array('f', [-100.0])
ak4jet1CMVALSF_Up = array('f', [-100.0])
ak4jet1CMVALSF_Down = array('f', [-100.0])
ak4jet1CMVAMSF = array('f', [-100.0])
ak4jet1CMVAMSF_Up = array('f', [-100.0])
ak4jet1CMVAMSF_Down = array('f', [-100.0])
ak4jet1CMVATSF = array('f', [-100.0])
ak4jet1CMVATSF_Up = array('f', [-100.0])
ak4jet1CMVATSF_Down = array('f', [-100.0])
ak4jet2CSVLSF = array('f', [-100.0])
ak4jet2CSVLSF_Up = array('f', [-100.0])
ak4jet2CSVLSF_Down = array('f', [-100.0])
ak4jet2CSVMSF = array('f', [-100.0])
ak4jet2CSVMSF_Up = array('f', [-100.0])
ak4jet2CSVMSF_Down = array('f', [-100.0])
ak4jet2CSVTSF = array('f', [-100.0])
ak4jet2CSVTSF_Up = array('f', [-100.0])
ak4jet2CSVTSF_Down = array('f', [-100.0])
ak4jet2CMVALSF = array('f', [-100.0])
ak4jet2CMVALSF_Up = array('f', [-100.0])
ak4jet2CMVALSF_Down = array('f', [-100.0])
ak4jet2CMVAMSF = array('f', [-100.0])
ak4jet2CMVAMSF_Up = array('f', [-100.0])
ak4jet2CMVAMSF_Down = array('f', [-100.0])
ak4jet2CMVATSF = array('f', [-100.0])
ak4jet2CMVATSF_Up = array('f', [-100.0])
ak4jet2CMVATSF_Down = array('f', [-100.0])
ak4jet3CSVLSF = array('f', [-100.0])
ak4jet3CSVLSF_Up = array('f', [-100.0])
ak4jet3CSVLSF_Down = array('f', [-100.0])
ak4jet3CSVMSF = array('f', [-100.0])
ak4jet3CSVMSF_Up = array('f', [-100.0])
ak4jet3CSVMSF_Down = array('f', [-100.0])
ak4jet3CSVTSF = array('f', [-100.0])
ak4jet3CSVTSF_Up = array('f', [-100.0])
ak4jet3CSVTSF_Down = array('f', [-100.0])
ak4jet3CMVALSF = array('f', [-100.0])
ak4jet3CMVALSF_Up = array('f', [-100.0])
ak4jet3CMVALSF_Down = array('f', [-100.0])
ak4jet3CMVAMSF = array('f', [-100.0])
ak4jet3CMVAMSF_Up = array('f', [-100.0])
ak4jet3CMVAMSF_Down = array('f', [-100.0])
ak4jet3CMVATSF = array('f', [-100.0])
ak4jet3CMVATSF_Up = array('f', [-100.0])
ak4jet3CMVATSF_Down = array('f', [-100.0])
ak4jet1CSV = array('f', [-100.0])
ak4jet1CMVA = array('f', [-100.0])
ak4jet1Corr = array('f', [-100.0])
ak4jet1CorrJECUp = array('f', [-100.0])
ak4jet1CorrJECDown = array('f', [-100.0])
ak4jet1CorrJER = array('f', [-100.0])
ak4jet1CorrJERUp = array('f', [-100.0])
ak4jet1CorrJERDown = array('f', [-100.0])
ak4jet2CSV = array('f', [-100.0])
ak4jet2CMVA = array('f', [-100.0])
ak4jet2Corr = array('f', [-100.0])
ak4jet2CorrJECUp = array('f', [-100.0])
ak4jet2CorrJECDown = array('f', [-100.0])
ak4jet2CorrJER = array('f', [-100.0])
ak4jet2CorrJERUp = array('f', [-100.0])
ak4jet2CorrJERDown = array('f', [-100.0])
ak4jet3CSV = array('f', [-100.0])
ak4jet3CMVA = array('f', [-100.0])
ak4jet3Corr = array('f', [-100.0])
ak4jet3CorrJECUp = array('f', [-100.0])
ak4jet3CorrJECDown = array('f', [-100.0])
ak4jet3CorrJER = array('f', [-100.0])
ak4jet3CorrJERUp = array('f', [-100.0])
ak4jet3CorrJERDown = array('f', [-100.0])
ak4genJet1Pt = array('f', [-100.0])
ak4genJet1Phi = array('f', [-100.0])
ak4genJet1Eta = array('f', [-100.0])
ak4genJet1Mass = array('f', [-100.0])
ak4genJet1ID = array('f', [-100.0])
ak4genJet2Pt = array('f', [-100.0])
ak4genJet2Phi = array('f', [-100.0])
ak4genJet2Eta = array('f', [-100.0])
ak4genJet2Mass = array('f', [-100.0])
ak4genJet2ID = array('f', [-100.0])
ak4genJet3Pt = array('f', [-100.0])
ak4genJet3Phi = array('f', [-100.0])
ak4genJet3Eta = array('f', [-100.0])
ak4genJet3Mass = array('f', [-100.0])
ak4genJet3ID = array('f', [-100.0])

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
myTree.Branch('tPtSum', tPtSum, 'tPtSum/F')
myTree.Branch('ak4jet1',ak4jet1Array,'pt/F:eta/F:phi/F:mass/F')
myTree.Branch('ak4jet2',ak4jet2Array,'pt/F:eta/F:phi/F:mass/F')
myTree.Branch('ak4jet3',ak4jet3Array,'pt/F:eta/F:phi/F:mass/F')
myTree.Branch('ak4jet1ID',ak4jet1ID, 'ak4jet1ID/F')
myTree.Branch('ak4jet2ID', ak4jet2ID, 'ak4jet2ID/F')
myTree.Branch('ak4jet3ID', ak4jet3ID, 'ak4jet3ID/F')
myTree.Branch('ak4jet1HeppyFlavour', ak4jet1HeppyFlavour, 'ak4jet1HeppyFlavour/F')
myTree.Branch('ak4jet1MCFlavour', ak4jet1MCFlavour, 'ak4jet1MCFlavour/F')
myTree.Branch('ak4jet1PartonFlavour', ak4jet1PartonFlavour, 'ak4jet1PartonFlavour/F')
myTree.Branch('ak4jet1HadronFlavour', ak4jet1HadronFlavour, 'ak4jet1HadronFlavour/F')
myTree.Branch('ak4jet1HeppyFlavour', ak4jet1HeppyFlavour, 'ak4jet1HeppyFlavour/F') 
myTree.Branch('ak4jet2MCFlavour', ak4jet2MCFlavour, 'ak4jet2MCFlavour/F')
myTree.Branch('ak4jet2PartonFlavour', ak4jet2PartonFlavour, 'ak4jet2PartonFlavour/F')
myTree.Branch('ak4jet2HadronFlavour', ak4jet2HadronFlavour, 'ak4jet2HadronFlavour/F')
myTree.Branch('ak4jet2HeppyFlavour', ak4jet2HeppyFlavour, 'ak4jet2HeppyFlavour/F')
myTree.Branch('ak4jet3MCFlavour', ak4jet3MCFlavour, 'ak4jet3MCFlavour/F')
myTree.Branch('ak4jet3PartonFlavour', ak4jet3PartonFlavour, 'ak4jet3PartonFlavour/F')
myTree.Branch('ak4jet3HadronFlavour', ak4jet3HadronFlavour, 'ak4jet3HadronFlavour/F')
myTree.Branch('ak4jet1CSVLSF', ak4jet1CSVLSF, 'ak4jet1CSVLSF/F')
myTree.Branch('ak4jet1CSVLSF_Up', ak4jet1CSVLSF_Up, 'ak4jet1CSVLSF_Up/F')
myTree.Branch('ak4jet1CSVLSF_Down', ak4jet1CSVLSF_Down, 'ak4jet1CSVLSF_Down/F')
myTree.Branch('ak4jet1CSVMSF', ak4jet1CSVMSF, 'ak4jet1CSVMSF/F')
myTree.Branch('ak4jet1CSVMSF_Up', ak4jet1CSVMSF_Up, 'ak4jet1CSVMSF_Up/F')
myTree.Branch('ak4jet1CSVMSF_Down', ak4jet1CSVMSF_Down, 'ak4jet1CSVMSF_Down/F')
myTree.Branch('ak4jet1CSVTSF', ak4jet1CSVTSF, 'ak4jet1CSVTSF/F')
myTree.Branch('ak4jet1CSVTSF_Up', ak4jet1CSVTSF_Up, 'ak4jet1CSVTSF_Up/F')
myTree.Branch('ak4jet1CSVTSF_Down', ak4jet1CSVTSF_Down, 'ak4jet1CSVTSF_Down/F') 
myTree.Branch('ak4jet1CMVALSF', ak4jet1CMVALSF, 'ak4jet1CMVALSF/F')
myTree.Branch('ak4jet1CMVALSF_Up', ak4jet1CMVALSF_Up, 'ak4jet1CMVALSF_Up/F')
myTree.Branch('ak4jet1CMVALSF_Down', ak4jet1CMVALSF_Down, 'ak4jet1CMVALSF_Down/F') 
myTree.Branch('ak4jet1CMVAMSF', ak4jet1CMVAMSF, 'ak4jet1CMVAMSF/F')
myTree.Branch('ak4jet1CMVAMSF_Up', ak4jet1CMVAMSF_Up, 'ak4jet1CMVAMSF_Up/F')
myTree.Branch('ak4jet1CMVAMSF_Down', ak4jet1CMVAMSF_Down, 'ak4jet1CMVAMSF_Down/F')
myTree.Branch('ak4jet1CMVATSF', ak4jet1CMVATSF, 'ak4jet1CMVATSF/F')
myTree.Branch('ak4jet1CMVATSF_Up', ak4jet1CMVATSF_Up, 'ak4jet1CMVATSF_Up/F')
myTree.Branch('ak4jet1CMVATSF_Down', ak4jet1CMVATSF_Down, 'ak4jet1CMVATSF_Down/F')
myTree.Branch('ak4jet2CSVLSF', ak4jet2CSVLSF, 'ak4jet2CSVLSF/F')
myTree.Branch('ak4jet2CSVLSF_Up', ak4jet2CSVLSF_Up, 'ak4jet2CSVLSF_Up/F')
myTree.Branch('ak4jet2CSVLSF_Down', ak4jet2CSVLSF_Down, 'ak4jet2CSVLSF_Down/F')
myTree.Branch('ak4jet2CSVMSF', ak4jet2CSVMSF, 'ak4jet2CSVMSF/F') 
myTree.Branch('ak4jet2CSVMSF_Up', ak4jet2CSVMSF_Up, 'ak4jet2CSVMSF_Up/F')
myTree.Branch('ak4jet2CSVMSF_Down', ak4jet2CSVMSF_Down, 'ak4jet2CSVMSF_Down/F')
myTree.Branch('ak4jet2CSVTSF', ak4jet2CSVTSF, 'ak4jet2CSVTSF/F')
myTree.Branch('ak4jet2CSVTSF_Up', ak4jet2CSVTSF_Up, 'ak4jet2CSVTSF_Up/F')
myTree.Branch('ak4jet2CSVTSF_Down', ak4jet2CSVTSF_Down, 'ak4jet2CSVTSF_Down/F')
myTree.Branch('ak4jet2CMVALSF', ak4jet2CMVALSF, 'ak4jet2CMVALSF/F')
myTree.Branch('ak4jet2CMVALSF_Up', ak4jet2CMVALSF_Up, 'ak4jet2CMVALSF_Up/F')
myTree.Branch('ak4jet2CMVALSF_Down', ak4jet2CMVALSF_Down, 'ak4jet2CMVALSF_Down/F')
myTree.Branch('ak4jet2CMVAMSF', ak4jet2CMVAMSF, 'ak4jet2CMVAMSF/F')
myTree.Branch('ak4jet2CMVAMSF_Up', ak4jet2CMVAMSF_Up, 'ak4jet2CMVAMSF_Up/F')
myTree.Branch('ak4jet2CMVAMSF_Down', ak4jet2CMVAMSF_Down, 'ak4jet2CMVAMSF_Down/F')
myTree.Branch('ak4jet2CMVATSF', ak4jet2CMVATSF, 'ak4jet2CMVATSF/F')
myTree.Branch('ak4jet2CMVATSF_Up', ak4jet2CMVATSF_Up, 'ak4jet2CMVATSF_Up/F')
myTree.Branch('ak4jet2CMVATSF_Down', ak4jet2CMVATSF_Down, 'ak4jet2CMVATSF_Down/F')
myTree.Branch('ak4jet3CSVLSF', ak4jet3CSVLSF, 'ak4jet3CSVLSF/F')
myTree.Branch('ak4jet3CSVLSF_Up', ak4jet3CSVLSF_Up, 'ak4jet3CSVLSF_Up/F')
myTree.Branch('ak4jet3CSVLSF_Down', ak4jet3CSVLSF_Down, 'ak4jet3CSVLSF_Down/F')
myTree.Branch('ak4jet3CSVMSF', ak4jet3CSVMSF, 'ak4jet3CSVMSF/F')
myTree.Branch('ak4jet3CSVMSF_Up', ak4jet3CSVMSF_Up, 'ak4jet3CSVMSF_Up/F')
myTree.Branch('ak4jet3CSVMSF_Down', ak4jet3CSVMSF_Down, 'ak4jet3CSVMSF_Down/F')
myTree.Branch('ak4jet3CSVTSF', ak4jet3CSVTSF, 'ak4jet3CSVTSF/F')
myTree.Branch('ak4jet3CSVTSF_Up', ak4jet3CSVTSF_Up, 'ak4jet3CSVTSF_Up/F')
myTree.Branch('ak4jet3CSVTSF_Down', ak4jet3CSVTSF_Down, 'ak4jet3CSVTSF_Down/F')
myTree.Branch('ak4jet3CMVALSF', ak4jet3CMVALSF, 'ak4jet3CMVALSF/F')
myTree.Branch('ak4jet3CMVALSF_Up', ak4jet3CMVALSF_Up, 'ak4jet3CMVALSF_Up/F')
myTree.Branch('ak4jet3CMVALSF_Down', ak4jet3CMVALSF_Down, 'ak4jet3CMVALSF_Down/F')
myTree.Branch('ak4jet3CMVAMSF', ak4jet3CMVAMSF, 'ak4jet3CMVAMSF/F')
myTree.Branch('ak4jet3CMVAMSF_Up', ak4jet3CMVAMSF_Up, 'ak4jet3CMVAMSF_Up/F')
myTree.Branch('ak4jet3CMVAMSF_Down', ak4jet3CMVAMSF_Down, 'ak4jet3CMVAMSF_Down/F')
myTree.Branch('ak4jet3CMVATSF', ak4jet3CMVATSF, 'ak4jet3CMVATSF/F')
myTree.Branch('ak4jet3CMVATSF_Up', ak4jet3CMVATSF_Up, 'ak4jet3CMVATSF_Up/F')
myTree.Branch('ak4jet3CMVATSF_Down', ak4jet3CMVATSF_Down, 'ak4jet3CMVATSF_Down/F')
myTree.Branch('ak4jet1CSV', ak4jet1CSV, 'ak4jet1CSV/F')
myTree.Branch('ak4jet1CMVA', ak4jet1CMVA, 'ak4jet1CMVA/F')
myTree.Branch('ak4jet1Corr', ak4jet1Corr, 'ak4jet1Corr/F')
myTree.Branch('ak4jet1CorrJECUp', ak4jet1CorrJECUp, 'ak4jet1CorrJECUp/F')
myTree.Branch('ak4jet1CorrJECDown', ak4jet1CorrJECDown, 'ak4jet1CorrJECDown/F')
myTree.Branch('ak4jet1CorrJER', ak4jet1CorrJER, 'ak4jet1CorrJER/F')
myTree.Branch('ak4jet1CorrJERUp', ak4jet1CorrJERUp, 'ak4jet1CorrJERUp/F')
myTree.Branch('ak4jet1CorrJERDown', ak4jet1CorrJERDown, 'ak4jet1CorrJERDown/F')
myTree.Branch('ak4jet2CSV', ak4jet2CSV, 'ak4jet2CSV/F')
myTree.Branch('ak4jet2CMVA', ak4jet2CMVA, 'ak4jet2CMVA/F')
myTree.Branch('ak4jet2Corr', ak4jet2Corr, 'ak4jet2Corr/F')
myTree.Branch('ak4jet2CorrJECUp', ak4jet2CorrJECUp, 'ak4jet2CorrJECUp/F')
myTree.Branch('ak4jet2CorrJECDown', ak4jet2CorrJECDown, 'ak4jet2CorrJECDown/F')
myTree.Branch('ak4jet2CorrJER', ak4jet2CorrJER, 'ak4jet2CorrJER/F')
myTree.Branch('ak4jet2CorrJERUp', ak4jet2CorrJERUp, 'ak4jet2CorrJERUp/F')
myTree.Branch('ak4jet2CorrJERDown', ak4jet2CorrJERDown, 'ak4jet2CorrJERDown/F')
myTree.Branch('ak4jet3CSV', ak4jet3CSV, 'ak4jet3CSV/F')
myTree.Branch('ak4jet3CMVA', ak4jet3CMVA, 'ak4jet3CMVA/F')
myTree.Branch('ak4jet3Corr', ak4jet3Corr, 'ak4jet3Corr/F')
myTree.Branch('ak4jet3CorrJECUp', ak4jet3CorrJECUp, 'ak4jet3CorrJECUp/F')
myTree.Branch('ak4jet3CorrJECDown', ak4jet3CorrJECDown, 'ak4jet3CorrJECDown/F')
myTree.Branch('ak4jet3CorrJER', ak4jet3CorrJER, 'ak4jet3CorrJER/F')
myTree.Branch('ak4jet3CorrJERUp', ak4jet3CorrJERUp, 'ak4jet3CorrJERUp/F')
myTree.Branch('ak4jet3CorrJERDown', ak4jet3CorrJERDown, 'ak4jet3CorrJERDown/F')
myTree.Branch('ak4genJet1Pt', ak4genJet1Pt, 'ak4genJet1Pt/F') 
myTree.Branch('ak4genJet1Phi', ak4genJet1Phi, 'ak4genJet1Phi/F')
myTree.Branch('ak4genJet1Eta', ak4genJet1Eta, 'ak4genJet1Eta/F')
myTree.Branch('ak4genJet1Mass', ak4genJet1Mass, 'ak4genJet1Mass/F')
myTree.Branch('ak4genJet1ID', ak4genJet1ID, 'ak4genJet1ID/F')
myTree.Branch('ak4genJet2Pt', ak4genJet2Pt, 'ak4genJet2Pt/F')
myTree.Branch('ak4genJet2Phi', ak4genJet2Phi, 'ak4genJet2Phi/F')
myTree.Branch('ak4genJet2Eta', ak4genJet2Eta, 'ak4genJet2Eta/F')
myTree.Branch('ak4genJet2Mass', ak4genJet2Mass, 'ak4genJet2Mass/F')
myTree.Branch('ak4genJet2ID', ak4genJet2ID, 'ak4genJet2ID/F')
myTree.Branch('ak4genJet3Pt', ak4genJet3Pt, 'ak4genJet3Pt/F')
myTree.Branch('ak4genJet3Phi', ak4genJet3Phi, 'ak4genJet3Phi/F')
myTree.Branch('ak4genJet3Eta', ak4genJet3Eta, 'ak4genJet3Eta/F')
myTree.Branch('ak4genJet3Mass', ak4genJet3Mass, 'ak4genJet3Mass/F')
myTree.Branch('ak4genJet3ID', ak4genJet3ID, 'ak4genJet3ID/F')

files_list	= open_files( inputfile )
#nevent = treeMine.GetEntries();

#list of histograms that may be useful
tpoj = ROOT.TH1F("tpoj", "Before any cuts", 3, -0.5, 1.5)
tpo0 = ROOT.TH1F("tpo0", "After Json", 3, -0.5, 1.5)
tpo1 = ROOT.TH1F("tpo1", "After Trigger", 3, -0.5, 1.5)
tpo2 = ROOT.TH1F("tpo2", "After jet cuts", 3, -0.5, 1.5)

gSystem.Load("DrawFunctions_h.so")

count = 0
#loop over files
for i in range(num1, num2):
    files = files_list[i]
    print files
    f1 = ROOT.TFile(files, "READ")
    treeMine  = f1.Get('tree')
    nevent = treeMine.GetEntries();

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
        if options.isMC:
            genBH = treeMine.GenJet_numBHadrons 
            genCH = treeMine.GenJet_numCHadrons
        fNJets = treeMine.nJet
        fJetPt  = treeMine.Jet_pt
	fJetEta  = treeMine.Jet_eta
        fJetPhi = treeMine.Jet_phi
        fJetMass = treeMine.Jet_mass
        fJetID = treeMine.Jet_id
        if options.isMC:
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
        if options.isMC:
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
        if options.isMC:
            fjUngroomedFlavour = treeMine.FatjetAK08ungroomed_Flavour
            fjUngroomedBHadron = treeMine.FatjetAK08ungroomed_BhadronFlavour
            fjUngroomedCHadron = treeMine.FatjetAK08ungroomed_ChadronFlavour
            fjUngroomedJER = treeMine.FatjetAK08ungroomed_GenPt
        fjL2L3 = treeMine.FatjetAK08ungroomed_JEC_L2L3
        fjL1L2L3 = treeMine.FatjetAK08ungroomed_JEC_L1L2L3
        if options.isMC:
            puweight = treeMine.puWeight 
            puweightUp = treeMine.puWeightUp
            puweightDown = treeMine.puWeightDown
	sjPrunedPt = treeMine.SubjetAK08softdrop_pt
	sjPrunedEta = treeMine.SubjetAK08softdrop_eta
	sjPrunedPhi = treeMine.SubjetAK08softdrop_phi
	sjPrunedMass = treeMine.SubjetAK08softdrop_mass
	sjPrunedBtag = treeMine.SubjetAK08softdrop_btag
	if options.MC:
            hPt = treeMine.GenHiggsBoson_pt
            hEta = treeMine.GenHiggsBoson_eta
            hPhi = treeMine.GenHiggsBoson_phi
            hMass = treeMine.GenHiggsBoson_mass
	hltHT800 = treeMine.HLT_BIT_HLT_PFHT800_v
        hltAK8 = treeMine.HLT_BIT_HLT_AK8DiPFJet250_200_TrimMass30_BTagCSV0p45_v
        hltDouble = treeMine.HLT_BIT_HLT_DoubleJet90_Double30_TripleBTagCSV0p67_v
        hltQuad = treeMine.HLT_BIT_HLT_QuadJet45_TripleBTagCSV0p67_v
        Data = treeMine.isData
        vType = treeMine.Vtype
        EVT = treeMine.evt 
        if options.isMC:
            nTInt = treeMine.nTrueInt
        genTopPts = treeMine.GenTop_pt
        JSON = treeMine.json
      
	#saving whether an event passes desired trigger
        matched = 0    
	if hltAK8 > 0:
            matched += 1
        if hltHT800 > 0:
            matched800 += 1
        if hltDouble > 0:
            matched += 1
        if hltQuad > 0:
            matched += 1
        triggerpass[0] = matched + matched800
        triggerHT800pass[0] = matched800

	nTrueInt[0]=nTInt

        #json for data
        tpoj.Fill(triggerpass[0])
        if Data and treeMine.json_silver < 1:
            continue		
		
        tpo0.Fill(triggerpass[0])

        #requiring event pass trigger
        if options.trigger and triggerpass[0] < 1:
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
                            correction_factor=1+(tree.FatjetAK08ungroomed_JEC_UP[j]-tree.FatjetAK08ungroomed_JEC_L1L2L3[j])
                            jettemp*=correction_factor
             if (options.syst=="FJEC_Down"):
                            correction_factor=1-(tree.FatjetAK08ungroomed_JEC_UP[j]-tree.FatjetAK08ungroomed_JEC_L1L2L3[j])
                            jettemp*=correction_factor
             if (options.syst=="FJER_Up"):
                            correction_factor=div_except(tree.FatjetAK08ungroomed_JER_UP_PT[j],tree.FatjetAK08ungroomed_pt[j])
                            jettemp*=correction_factor
             if (options.syst=="FJER_Down"):
                            pJERDown=2*tree.FatjetAK08ungroomed_pt[j]-tree.FatjetAK08ungroomed_JER_UP_PT[j]
                            correction_factor=div_except((pJERDown),tree.FatjetAK08ungroomed_pt[j])
                            jettemp*=correction_factor

	    if jettemp.Pt() > 300. and abs(jettemp.Eta()) < 2.4: 	
                    jets.append(jettemp)
		    if fjUngroomedTau1[j] > 0:
			    jet_tau.append(fjUngroomedTau2[j]/fjUngroomedTau1[j])
		    else:
			    jet_tau.append(100)
                    mpruned_syst=fjUngroomedPrunedMass[j]
                    if (options.syst=="MJEC_Down"):
                            sigma=tree.FatjetAK08ungroomed_JEC_L2L3_UP[j]-tree.FatjetAK08ungroomed_JEC_L2L3[j]
                            mpruned_syst=tree.FatjetAK08ungroomed_mpruned[j]*(tree.FatjetAK08ungroomed_JEC_L2L3[j]-sigma)
                    if (options.syst=="MJEC_Up"): 
                        mpruned_syst=tree.FatjetAK08ungroomed_mpruned[j]*tree.FatjetAK08ungroomed_JEC_L2L3_UP[j]

		    jet_bbtag.append(fjUngroomedBbTag[j])	
                    jet_pmass.append(fjUngroomedPrunedMass[j])
                    jet_pmassunc.append(fjUngroomedPrunedMass_Unc[j])
                    jet_id.append(fjUngroomedJetID[j])
                    if options.isMC:
                        jet_nb.append(fjUngroomedBHadron[j])
                        jet_nc.append(fjUngroomedCHadron[j])
                        jet_flav.append(fjUngroomedFlavour[j])
                        jet_JER.append(fjUngroomedJER[j])
                    jet_123.append(fjL1L2L3[j])
                    jet_23.append(fjL2L3[j])


	if options.jets and len(jets) < 1: # two jets with pt > 30 and |eta| < 2.5
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
	if options.isMC:
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
        if options.isMC:
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
            
            for i in range(0,4):
                  jetSJfla[i] =-1
                  jetSJpt[i]  =-1
                  jetSJcsv[i] =-1
                  jetSJeta[i] =-1

        if len(jet1sjcsv) > 1:
            jet1s1csv[0] = jet1sjcsv[0]
            jet1s2csv[0] = jet1sjcsv[1]
        elif len(jet1sjcsv) == 1:
            jet1s1csv[0] = jet1sjcsv[0]

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
        
            for i in range(0,4):
                jetSJfla[i] =-1
                jetSJpt[i]  =-1
                jetSJcsv[i] =-1
                jetSJeta[i] =-1

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
        if options.isMC:
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
        if options.isMC:
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
        else:
            isData[0] = 0

        #hbb tagger SFs
                #handling hbb tagger SFs
        sf1 = -1
        sf2 = -1
        sf1change = 1000000
        sf2change = 1000000

        if jet1pt[0] < 400:
            sf1 = 0.929
            sf1change = 0.078
        elif jet1pt[0] >= 400 and jet1pt[0] < 500:
            sf1 = 0.999
            sf1change = 0.126
        elif jet1pt[0] >= 500 and jet1pt[0] < 600:
            sf1 = 0.933
            sf1change = 0.195
        elif jet1pt[0] >= 600:
            sf1 = 1.048
            sf1change = 0.215
        
        bbtag1SF[0] = sf1
        bbtag1SFUp[0] = sf1*(1+sf1change)
        bbtag1SFDown[0] = sf1*(1-sf1change)

        if len(jets) > 1:
            if jet2pt[0] < 400:
                sf2 = 0.929
                sf2change = 0.078
            elif jet2pt[0] >= 400 and jet2pt[0] < 500:
                sf2 = 0.999
                sf2change = 0.126
            elif jet2pt[0] >= 500 and jet2pt[0] < 600:
                sf2 = 0.933
                sf2change = 0.195
            elif jet2pt[0] >= 600:
                sf2 = 1.048
                sf2change = 0.215

            bbtag2SF[0] = sf2
            bbtag2SFUp[0] = sf2*(1+sf2change)
            bbtag2SFDown[0] = sf2*(1-sf2change)


        #ak4 jets

        akjets = []
        akjet_id = []
        akjet_heppyf = []
        akjet_mcf = []
        akjet_partonf = []
        akjet_hadronf = []
        akjet_CSVLSF = []
        akjet_CSVLSF_Up = []
        akjet_CSVLSF_Down = []
        akjet_CSVMSF = []
        akjet_CSVMSF_Up = []
        akjet_CSVMSF_Down = []
        akjet_CSVTSF = []
        akjet_CSVTSF_Up = []
        akjet_CSVTSF_Down = []
        akjet_CMVALSF = []
        akjet_CMVALSF_Up = [] 
        akjet_CMVALSF_Down = [] 
        akjet_CMVAMSF = []
        akjet_CMVAMSF_Up = [] 
        akjet_CMVAMSF_Down = [] 
        akjet_CMVATSF = []
        akjet_CMVATSF_Up = [] 
        akjet_CMVATSF_Down = []
        akjet_CSV = []
        akjet_CMVA = []
        akjet_corr = []
        akjet_JECUp = []
        akjet_JECDown = []
        akjet_JER = []
        akjet_JERUp = []
        akjet_JERDown = []
        for j in range(len(fJetPt)):
            jettemp = ROOT.TLorentzVector()
            jettemp.SetPtEtaPhiM(fJetPt[j], fJetEta[j], fJetPhi[j], fJetMass[j])
 	    if abs(jettemp.Eta()) < 2.4: 	
                    akjets.append(jettemp)
		    akjet_id.append(fJetID[j])
                    akjet_heppyf.append(fJetHeppyFlavour[j])
                    akjet_mcf.append(fJetMCFlavour[j])
                    akjet_partonf.append(fJetPartonFlavour[j])
                    akjet_hadronf.append(fJetHadronFlavour[j])
                    akjet_CSVLSF.append(fJetCSVLSF[j])
                    akjet_CSVLSF_Up.append(fJetCSVLSF_Up[j])
                    akjet_CSVLSF_Down.append(fJetCSVLSF_Down[j])
                    akjet_CSVMSF.append(fJetCSVMSF[j])
                    akjet_CSVMSF_Up.append(fJetCSVMSF_Up[j])
                    akjet_CSVMSF_Down.append(fJetCSVMSF_Down[j])
                    akjet_CSVTSF.append(fJetCSVTSF[j])
                    akjet_CSVTSF_Up.append(fJetCSVTSF_Up[j])
                    akjet_CSVTSF_Down.append(fJetCSVTSF_Down[j])
                    akjet_CMVALSF.append(fJetCMVALSF[j])
                    akjet_CMVALSF_Up.append(fJetCMVALSF_Up[j]) 
                    akjet_CMVALSF_Down.append(fJetCMVALSF_Down[j]) 
                    akjet_CMVAMSF.append(fJetCMVAMSF[j])
                    akjet_CMVAMSF_Up.append(fJetCMVAMSF_Up[j]) 
                    akjet_CMVAMSF_Down.append(fJetCMVAMSF_Down[j]) 
                    akjet_CMVATSF.append(fJetCMVATSF[j])
                    akjet_CMVATSF_Up.append(fJetCMVATSF_Up[j]) 
                    akjet_CMVATSF_Down.append(fJetCMVATSF_Down[j]) 
                    akjet_CSV.append(fJetCSV[j])
                    akjet_CMVA.append(fJetCMVA[j])
                    akjet_corr.append(fJetCorr[j])
                    akjet_JECUp.append(fJetCorrJECUp[j])
                    akjet_JECDown.append(fJetCorrJECDown[j])
                    akjet_JER.append(fJetCorrJER[j])
                    akjet_JERUp.append(fJetCorrJERUp[j])
                    akjet_JERDown.append(fJetCorrJERDown[j])

        if options.jets and len(akjets) < 2:        
            continue

        tpo2.Fill(triggerpass[0])
	
        ak4jet1Array[0] = akjets[0].Pt()
        ak4jet1Array[1] = akjets[0].Eta()
        ak4jet1Array[2] = akjets[0].Phi()
        ak4jet1Array[3] = akjets[0].M()        
        ak4jet2Array[0] = akjets[1].Pt()
        ak4jet2Array[1] = akjets[1].Eta()
        ak4jet2Array[2] = akjets[1].Phi()
        ak4jet2Array[3] = akjets[1].M()        
        ak4jet1ID[0] = akjet_id[0]
        ak4jet2ID[0] = akjet_id[1]
        ak4jet1HeppyFlavour[0] = akjet_heppyf[0]
        ak4jet2HeppyFlavour[0] = akjet_heppyf[1]
        ak4jet1MCFlavour[0] = akjet_mcf[0]
        ak4jet2MCFlavour[0] = akjet_mcf[1]
        ak4jet1PartonFlavour[0] = akjet_partonf[0]
        ak4jet2PartonFlavour[0] = akjet_partonf[1]
        ak4jet1HadronFlavour[0] = akjet_hadronf[0]
        ak4jet2HadronFlavour[0] = akjet_hadronf[1]
        ak4jet1CSVLSF[0] = akjet_CSVLSF[0]
        ak4jet2CSVLSF[0] = akjet_CSVLSF[1]
        ak4jet1CSVLSF_Up[0] = akjet_CMVALSF_Up[0]
        ak4jet2CSVLSF_Up[0] = akjet_CMVALSF_Up[1]
        ak4jet1CSVLSF_Down[0] = akjet_CMVALSF_Down[0]
        ak4jet2CSVLSF_Down[0] = akjet_CMVALSF_Down[1]
        ak4jet1CSVMSF[0] = akjet_CSVMSF[0]
        ak4jet2CSVMSF[0] = akjet_CSVMSF[1]
        ak4jet1CSVMSF_Up[0] = akjet_CSVMSF_Up[0]
        ak4jet2CSVMSF_Up[0] = akjet_CSVMSF_Up[1]
        ak4jet1CSVMSF_Down[0] = akjet_CSVMSF_Down[0]
        ak4jet2CSVMSF_Down[0] = akjet_CSVMSF_Down[1]
        ak4jet1CSVTSF[0] = akjet_CSVTSF[0]
        ak4jet2CSVTSF[0] = akjet_CSVTSF[1]
        ak4jet1CSVTSF_Up[0] = akjet_CSVTSF_Up[0]
        ak4jet2CSVTSF_Up[0] = akjet_CSVTSF_Up[1]
        ak4jet1CSVTSF_Down[0] = akjet_CSVTSF_Down[0]
        ak4jet2CSVTSF_Down[0] = akjet_CSVTSF_Down[1]
        ak4jet1CMVALSF[0] = akjet_CMVALSF[0]
        ak4jet2CMVALSF[0] = akjet_CMVALSF[1]
        ak4jet1CMVALSF_Up[0] = akjet_CMVALSF_Up[0]
        ak4jet2CMVALSF_Up[0] = akjet_CMVALSF_Up[1]
        ak4jet1CMVALSF_Down[0] = akjet_CMVALSF_Down[0]
        ak4jet2CMVALSF_Down[0] = akjet_CMVALSF_Down[1]
        ak4jet1CMVAMSF[0] = akjet_CMVAMSF[0]
        ak4jet2CMVAMSF[0] = akjet_CMVAMSF[1]
        ak4jet1CMVAMSF_Up[0] = akjet_CMVAMSF_Up[0]
        ak4jet2CMVAMSF_Up[0] = akjet_CMVAMSF_Up[1]
        ak4jet1CMVAMSF_Down[0] = akjet_CMVAMSF_Down[0]
        ak4jet2CMVAMSF_Down[0] = akjet_CMVAMSF_Down[1]
        ak4jet1CMVATSF[0] = akjet_CMVATSF[0]
        ak4jet2CMVATSF[0] = akjet_CMVATSF[1]
        ak4jet1CMVATSF_Up[0] = akjet_CMVATSF_Up[0]
        ak4jet2CMVATSF_Up[0] = akjet_CMVATSF_Up[1]
        ak4jet1CMVATSF_Down[0] = akjet_CMVATSF_Down[0]
        ak4jet2CMVATSF_Down[0] = akjet_CMVATSF_Down[1]
        ak4jet1CSV[0] = akjet_CSV[0]
        ak4jet1CMVA[0] = akjet_CMVA[0]
        ak4jet1Corr[0] = akjet_corr[0]
        ak4jet1CorrJECUp[0] = akjet_JECUp[0]
        ak4jet1CorrJECDown[0] = akjet_JECDown[0]
        ak4jet1CorrJER[0] = akjet_JER[0]
        ak4jet1CorrJERUp[0] = akjet_JERUp[0]
        ak4jet1CorrJERDown[0] = akjet_JERDown[0]
        ak4jet2CSV[0] = akjet_CSV[1]
        ak4jet2CMVA[0] = akjet_CMVA[1]
        ak4jet2Corr[0] = akjet_corr[1]
        ak4jet2CorrJECUp[0] = akjet_JECUp[1]
        ak4jet2CorrJECDown[0] = akjet_JECDown[1]
        ak4jet2CorrJER[0] = akjet_JER[1]
        ak4jet2CorrJERUp[0] = akjet_JERUp[1]
        ak4jet2CorrJERDown[0] = akjet_JERDown[1]
        
        if len(akjets) > 2:
            ak4jet3Array[0] = akjets[2].Pt()
            ak4jet3Array[1] = akjets[2].Eta()
            ak4jet3Array[2] = akjets[2].Phi()
            ak4jet3Array[3] = akjets[2].M()        
            ak4jet3ID[0] = akjet_id[2]
            ak4jet3HeppyFlavour[0] = akjet_heppyf[2] 
            ak4jet3MCFlavour[0] = akjet_mcf[2] 
            ak4jet3PartonFlavour[0] = akjet_partonf[2]
            ak4jet3HadronFlavour[0] = akjet_hadronf[2]
            ak4jet3CSVLSF[0] = akjet_CSVLSF[2]
            ak4jet3CSVLSF_Up[0] = akjet_CMVALSF_Up[2]
            ak4jet3CSVLSF_Down[0] = akjet_CMVALSF_Down[2]
            ak4jet3CSVMSF[0] = akjet_CSVMSF[2]
            ak4jet3CSVMSF_Up[0] = akjet_CSVMSF_Up[2]
            ak4jet3CSVMSF_Down[0] = akjet_CSVMSF_Down[2]
            ak4jet3CSVTSF[0] = akjet_CSVTSF[2]
            ak4jet3CSVTSF_Up[0] = akjet_CSVTSF_Up[2]
            ak4jet3CSVTSF_Down[0] = akjet_CSVTSF_Down[2]
            ak4jet3CMVALSF[0] = akjet_CMVALSF[2]
            ak4jet3CMVALSF_Up[0] = akjet_CMVALSF_Up[2]
            ak4jet3CMVALSF_Down[0] = akjet_CMVALSF_Down[2]
            ak4jet3CMVAMSF[0] = akjet_CMVAMSF[2]
            ak4jet3CMVAMSF_Up[0] = akjet_CMVAMSF_Up[2]
            ak4jet3CMVAMSF_Down[0] = akjet_CMVAMSF_Down[2]
            ak4jet3CMVATSF[0] = akjet_CMVATSF[2]
            ak4jet3CMVATSF_Up[0] = akjet_CMVATSF_Up[2]
            ak4jet3CMVATSF_Down[0] = akjet_CMVATSF_Down[2]
            ak4jet3CSV[0] = akjet_CSV[2]
            ak4jet3CMVA[0] = akjet_CMVA[2]
            ak4jet3Corr[0] = akjet_corr[2]
            ak4jet3CorrJECUp[0] = akjet_JECUp[2]
            ak4jet3CorrJECDown[0] = akjet_JECDown[2]
            ak4jet3CorrJER[0] = akjet_JER[2]
            ak4jet3CorrJERUp[0] = akjet_JERUp[2]
            ak4jet3CorrJERDown[0] = akjet_JERDown[2]
            if len(akjets) > 3:
                ak4jet4Array[0] = akjets[3].Pt()
                ak4jet4Array[1] = akjets[3].Eta()
                ak4jet4Array[2] = akjets[3].Phi()
                ak4jet4Array[3] = akjets[3].M()        
                ak4jet4ID[0] = akjet_id[3]
                ak4jet4HeppyFlavour[0] = akjet_heppyf[3] 
                ak4jet4MCFlavour[0] = akjet_mcf[3] 
                ak4jet4PartonFlavour[0] = akjet_partonf[3]
                ak4jet4HadronFlavour[0] = akjet_hadronf[3]
                ak4jet4CSVLSF[0] = akjet_CSVLSF[3]
                ak4jet4CSVLSF_Up[0] = akjet_CMVALSF_Up[3]
                ak4jet4CSVLSF_Down[0] = akjet_CMVALSF_Down[3]
                ak4jet4CSVMSF[0] = akjet_CSVMSF[3]
                ak4jet4CSVMSF_Up[0] = akjet_CSVMSF_Up[3]
                ak4jet4CSVMSF_Down[0] = akjet_CSVMSF_Down[3]
                ak4jet4CSVTSF[0] = akjet_CSVTSF[3]
                ak4jet4CSVTSF_Up[0] = akjet_CSVTSF_Up[3]
                ak4jet4CSVTSF_Down[0] = akjet_CSVTSF_Down[3]
                ak4jet4CMVALSF[0] = akjet_CMVALSF[3]
                ak4jet4CMVALSF_Up[0] = akjet_CMVALSF_Up[3]
                ak4jet4CMVALSF_Down[0] = akjet_CMVALSF_Down[3]
                ak4jet4CMVAMSF[0] = akjet_CMVAMSF[3]
                ak4jet4CMVAMSF_Up[0] = akjet_CMVAMSF_Up[3]
                ak4jet4CMVAMSF_Down[0] = akjet_CMVAMSF_Down[3]
                ak4jet4CMVATSF[0] = akjet_CMVATSF[3]
                ak4jet4CMVATSF_Up[0] = akjet_CMVATSF_Up[3]
                ak4jet4CMVATSF_Down[0] = akjet_CMVATSF_Down[3]
                ak4jet4CSV[0] = akjet_CSV[3]
                ak4jet4CMVA[0] = akjet_CMVA[3]
                ak4jet4Corr[0] = akjet_corr[3]
                ak4jet4CorrJECUp[0] = akjet_JECUp[3]
                ak4jet4CorrJECDown[0] = akjet_JECDown[3]
                ak4jet4CorrJER[0] = akjet_JER[3]
                ak4jet4CorrJERUp[0] = akjet_JERUp[3]
                ak4jet4CorrJERDown[0] = akjet_JERDown[3]
                
        akj1 = MatchCollection(ujets, akjets[0])
        akj2 = MatchCollection(ujets, akjets[1])
        ak4genJet1Pt[0] = ujets[akj1].Pt()
        ak4genJet1Eta[0] = ujets[akj1].Eta()
        ak4genJet1Phi[0] = ujets[akj1].Phi()
        ak4genJet1Mass[0] = ujets[akj1].M()
        ak4genJet1ID[0] = akj1
        ak4genJet2Pt[0] = ujets[akj2].Pt()
        ak4genJet2Eta[0] = ujets[akj2].Eta()
        ak4genJet2Phi[0] = ujets[akj2].Phi()
        ak4genJet2Mass[0] = ujets[akj2].M()
        ak4genJet2ID[0] = akj2
        if len(akjets) > 2:
            akj3 = MatchCollection(ujets, akjets[2])
            ak4genJet3Pt[0] = ujets[akj3].Pt()
            ak4genJet3Eta[0] = ujets[akj3].Eta()
            ak4genJet3Phi[0] = ujets[akj3].Phi()
            ak4genJet3Mass[0] = ujets[akj3].M()
            ak4genJet3ID[0] = akj3
            if len(akjets) > 3:
                akj4 = MatchCollection(ujets, akjets[3])
                ak4genJet4Pt[0] = ujets[akj4].Pt()
                ak4genJet4Eta[0] = ujets[akj4].Eta()
                ak4genJet4Phi[0] = ujets[akj4].Phi()
                ak4genJet4Mass[0] = ujets[akj4].M()
                ak4genJet4ID[0] = akj4

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
	jet1mscsv[0] = -100.0
	jet2mscsv[0] = -100.0
	jet1bbtag[0] = -100.0
	jet2bbtag[0] = -100.0
	triggerpass[0] = -100.0
#	PUWeight[0]= -100.0
	
    
    f1.Close()

print "OK"

f.cd()
f.Write()
f.Close()




