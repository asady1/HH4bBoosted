#!/bin/sh

for i in `seq 0 20 100`
do
python generalTreeAnalyzer_76X_vh.py --pathIn=/eos/uscms/store/user/lpchbb/HeppyNtuples/V21/TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/VHBB_HEPPY_V21_TTJets_TuneCUETP8M1_13TeV-madgraphMLM-Py8__fall15MAv2-pu25ns15v1_76r2as_v12-v1/160316_145733/0000/ --outName=TTBar_76X_vh --trigger=False --jets=True --deta=True --isMC=True --xsec=831.76 --min=$i --max=$((i+20)) --file=TxtFiles/ttbar.txt --syst=None&
done

python generalTreeAnalyzer_76X_vh.py --pathIn=/eos/uscms/store/user/lpchbb/HeppyNtuples/V21/TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/VHBB_HEPPY_V21_TTJets_TuneCUETP8M1_13TeV-madgraphMLM-Py8__fall15MAv2-pu25ns15v1_76r2as_v12-v1/160316_145733/0000/ --outName=TTBar_76X_vh --trigger=False --jets=True --deta=True --isMC=True --xsec=831.76 --min=120 --max=136 --file=TxtFiles/ttbar.txt --syst=None

