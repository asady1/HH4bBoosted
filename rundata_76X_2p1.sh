#!/bin/sh

python generalTreeAnalyzer_2p1_jv.py --pathIn=/eos/uscms/store/user/lpchbb/HeppyNtuples/V21/JetHT/VHBB_HEPPY_V21_JetHT__Run2015C_25ns-16Dec2015-v1/160318_132855/0000/ --outName=Jet_HT_C_2p1 --trigger="True" --jets="True" --isMC="False" --xsec=1. --min=0 --max=31 --file=TxtFiles/76XRunC.txt --syst=None&

for i in `seq 0 20 780`
do
nohup python generalTreeAnalyzer_2p1_jv.py --pathIn=/eos/uscms/store/user/lpchbb/HeppyNtuples/V21/JetHT/VHBB_HEPPY_V21_JetHT__Run2015D-16Dec2015-v1/160317_130618/0000/ --outName=Jet_HT_D_2p1 --trigger="True" --jets="True" --isMC="False" --xsec=1. --min=$i --max=$((i+20)) --file=TxtFiles/76XRunD.txt --syst=None&
done

#python generalTreeAnalyzer_2p1_jv.py --pathIn=/eos/uscms/store/user/lpchbb/HeppyNtuples/V21/JetHT/VHBB_HEPPY_V21_JetHT__Run2015D-16Dec2015-v1/160317_130618/0000/ --outName=Jet_HT_D_2p1 --trigger="True" --jets="True" --isMC="False" --xsec=1.0 --min=800 --max=804 --file=TxtFiles/76XRunD.txt --syst=None&

