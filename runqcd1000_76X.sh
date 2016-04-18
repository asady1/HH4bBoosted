#!/bin/sh

for i in `seq 0 20 40`
do
python generalTreeAnalyzer_76X.py --pathIn=/eos/uscms/store/user/lpchbb/HeppyNtuples/V21/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/VHBB_HEPPY_V21_QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-Py8__fall15MAv2-pu25ns15v1_76r2as_v12-v1/160316_151306/0000/ --outName=QCD_HT1000_76X_boost --trigger=False --jets=True --deta=True --isMC=True --min=$i --max=$((i+20)) --file=TxtFiles/QCDHT1000_76X.txt &
done

python generalTreeAnalyzer_76X.py --pathIn=/eos/uscms/store/user/lpchbb/HeppyNtuples/V21/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/VHBB_HEPPY_V21_QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-Py8__fall15MAv2-pu25ns15v1_76r2as_v12-v1/160316_151306/0000/ --outName=QCD_HT1000_76X_boost --trigger=False --jets=True --deta=True --isMC=True --min=60 --max=63 --file=TxtFiles/QCDHT1000_76X.txt &

for i in `seq 0 20 20`
do
python generalTreeAnalyzer_76X.py --pathIn=/eos/uscms/store/user/lpchbb/HeppyNtuples/V21/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/VHBB_HEPPY_V21_QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-Py8__fall15MAv2-pu25ns15v1_76r2as_v12-v1/160316_144454/0000/ --outName=QCD_HT1500_76X_boost --trigger=False --jets=True --deta=True --isMC=True --min=$i --max=$((i+20)) --file=TxtFiles/QCDHT1500_76X.txt &
done

python generalTreeAnalyzer_76X.py --pathIn=/eos/uscms/store/user/lpchbb/HeppyNtuples/V21/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/VHBB_HEPPY_V21_QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-Py8__fall15MAv2-pu25ns15v1_76r2as_v12-v1/160316_144454/0000/ --outName=QCD_HT1500_76X_boost --trigger=False --jets=True --deta=True --isMC=True --min=40 --max=49 --file=TxtFiles/QCDHT1500_76X.txt &

python generalTreeAnalyzer_76X.py --pathIn=/eos/uscms/store/user/lpchbb/HeppyNtuples/V21/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/VHBB_HEPPY_V21_QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-Py8__fall15MAv2-pu25ns15v1_76r2as_v12-v1/160316_144521/0000/ --outName=QCD_HT2000_76X_boost --trigger=False --jets=True --deta=True --isMC=True  --min=0 --max=28 --file=TxtFiles/QCDHT2000_76X.txt &

