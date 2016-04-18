#/bin/sh

#Rad 1000
#python generalTreeAnalyzer_v9_pt_expanded.py --pathIn=/eos/uscms/store/group/lpchbb/HeppyNtuples/V14/BulkGravTohhTohbbhbb_narrow_M-1000_13TeV-madgraph/VHBB_HEPPY_V14_BulkGravTohhTohbbhbb_narrow_M-1000_13TeV-madgraph__RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/151024_223151/0000/ --outName=BG_1000_v9_pt_ex --min=0 --max=2 --file=TxtFiles/BG1000.txt &

#Rad 1200
python generalTreeAnalyzer_76X.py --pathIn=/eos/uscms/store/user/lpchbb/HeppyNtuples/V21/BulkGravTohhTohbbhbb_narrow_M-1200_13TeV-madgraph/VHBB_HEPPY_V21_BulkGravTohhTohbbhbb_narrow_M-1200_13TeV-madgraph__fall15MAv2-pu25ns15v1_76r2as_v12-v1/160316_151428/0000/ --outName=BG_1200_76X_boost --trigger=False --jets=True --deta=True --isMC=True --min=0 --max=1 --file=TxtFiles/BG1200.txt &

#Rad 1400
python generalTreeAnalyzer_76X.py --pathIn=/eos/uscms/store/user/lpchbb/HeppyNtuples/V21/BulkGravTohhTohbbhbb_narrow_M-1400_13TeV-madgraph/VHBB_HEPPY_V21_BulkGravTohhTohbbhbb_narrow_M-1400_13TeV-madgraph__fall15MAv2-pu25ns15v1_76r2as_v12-v1/160316_142930/0000/ --outName=BG_1400_76X_boost --trigger=False --jets=True --deta=True --isMC=True --min=0 --max=1 --file=TxtFiles/BG1400.txt &

#Rad 1600
python generalTreeAnalyzer_76X.py --pathIn=/eos/uscms/store/user/lpchbb/HeppyNtuples/V21/BulkGravTohhTohbbhbb_narrow_M-1600_13TeV-madgraph/VHBB_HEPPY_V21_BulkGravTohhTohbbhbb_narrow_M-1600_13TeV-madgraph__fall15MAv2-pu25ns15v1_76r2as_v12-v1/160316_142958/0000/ --outName=BG_1600_76X_boost --trigger=False --jets=True --deta=True --isMC=True --min=0 --max=1 --file=TxtFiles/BG1600.txt &

#Rad 2000
#python generalTreeAnalyzer_v9_pt_expanded.py --pathIn=/eos/uscms/store/group/lpchbb/HeppyNtuples/V14/BulkGravTohhTohbbhbb_narrow_M-2000_13TeV-madgraph/VHBB_HEPPY_V14_BulkGravTohhTohbbhbb_narrow_M-2000_13TeV-madgraph__RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/151025_083027/0000/ --outName=BG_2000_v9_pt_ex --min=0 --max=1 --file=TxtFiles/BG2000.txt &

#Rad 3000
python generalTreeAnalyzer_76X.py --pathIn=/eos/uscms/store/user/lpchbb/HeppyNtuples/V21/BulkGravTohhTohbbhbb_narrow_M-3000_13TeV-madgraph/VHBB_HEPPY_V21_BulkGravTohhTohbbhbb_narrow_M-3000_13TeV-madgraph__fall15MAv2-pu25ns15v1_76r2as_v12-v1/160316_151510/0000/ --outName=BG_3000_76X_boost --trigger=False --jets=True --deta=True --isMC=True --min=0 --max=1 --file=TxtFiles/BG3000.txt &

