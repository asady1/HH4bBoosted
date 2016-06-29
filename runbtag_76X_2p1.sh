#!/bin/sh

nohup python generalTreeAnalyzer_2p1_jv.py --pathIn=/eos/uscms/store/user/lpchbb/HeppyNtuples/V21/BTagCSV/VHBB_HEPPY_V21_BTagCSV__Run2015C_25ns-16Dec2015-v1/160318_133752/0000/ --outName=BTag_C_2p1 --trigger="True" --jets="True" --isMC="False" --xsec=1. --min=0 --max=3 --file=TxtFiles/btagC.txt --syst=None&

for i in `seq 0 20 180`
do
nohup python generalTreeAnalyzer_2p1_jv.py --pathIn=/eos/uscms/store/user/lpchbb/HeppyNtuples/V21/BTagCSV/VHBB_HEPPY_V21_BTagCSV__Run2015D-16Dec2015-v1/160317_132347/0000/ --outName=BTag_D_2p1 --trigger="True" --jets="True" --isMC="False" --xsec=1. --min=$i --max=$((i+20)) --file=TxtFiles/btagD.txt --syst=None&
done

nohup python generalTreeAnalyzer_2p1_jv.py --pathIn=/eos/uscms/store/user/lpchbb/HeppyNtuples/V21/BTagCSV/VHBB_HEPPY_V21_BTagCSV__Run2015D-16Dec2015-v1/160317_132347/0000/ --outName=BTag_D_2p1 --trigger="True" --jets="True" --isMC="False" --xsec=1. --min=200 --max=208 --file=TxtFiles/btagD.txt --syst=None&

