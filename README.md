#Doubly Charged Higgs Analysis at 8 TeV

This package is used to perform a search for a Doubly-Charged Higgs boson using
the 8 TeV CMS dataset. It runs on n-tuples produced by `FinalStateAnalysis`
(https://github.com/uwcms/FinalStateAnalysis).

##Producing n-tuples
To produce the FSA n-tuples used by this package, you run

```sh
make_ntuples_cfg.py rerunFSA=1 channels="zz" dblhMode=1
```

within `FinalStateAnalysis/NtupleTools/test`. The `mkntuples.py` script runs on the
FSA n-tuples to produce n-tuples with the preselection and event reconstruction
applied. These n-tuples are stored as HDF5 files.

##Four-Lepton Final State
In this channel, a Z decays to a H++/H-- pair. The Higgs decay to a pair of
same-sign leptons, not necessarily of the same flavor.

###Pre-Selection
 - Triggers
   - Double Muon
   - Double Electron + Triple Electron
   - Muon/Electron
 - Electrons
   - pT > 15 and |&eta;| < 2.5
   - MVA "Non-Triggers" ID
 - Muons
   - pT > 5 and |&eta;| < 2.4
 - pT1 > 20 and pT2 > 10
 - QCD Rejection: require all lepton pairs with m > 12 GeV
 - PF Relative Isolation < 0.4 for all leptons

###tt-bar Control Region
Run with `python mkntuples.py tt [samples,...]`. We make the following modifications to the
pre-selection:

 - Two best isolated leptons < 0.4 and worst > 0.4
 - Z-veto: for all OSSF pairs, require |m(ll) - Mz| > 20.0
 - sT > 150 and MET > 30

Make plots with `python mkplots.py tt`.

###Z Control Region
Run with `python mkntuples.py z [sample,...]`. We make the following modifications to
the pre-selection:

 - Z-flag: Require at least one OSSF pair with |m(ll) - Mz| < 20.0
 - sT > 150

Make plots with `python mkplots.py z`.

##Limits
The branching fractions are not constrained by the model, so we test seven
different branching ratio benchpoints.

 - BP1: tribimaximal neutrino mixing is assumed, no CP violation, normal neutrino mass ordering and the lowest neutrino mass to be vanishing.
 - BP2: same as BP1, but with the assumption of inverted neutrino mass ordering.
 - BP3: same as BP1, but the lightest neutrino mass is assumed to be 0.2 eV which is at the present cosmological limit.
 - BP4: all branching ratios are asummed to be equally 16.7%.
 - 100% to ee
 - 100% to em
 - 100% to mm

Name| ee   | em   | et   | mm    | mt   | tt
----|------|------|------|-------|------|------
BP1 | 0    | 0.01 | 0.01 | 0.3   | 0.38 | 0.3
BP2 | 0.5  | 0    | 0    | 0.125 | 0.25 | 0.125
BP3 | 0.34 | 0    | 0    | 0.33  | 0    | 0.33
BP4 | 1/6  | 1/6  | 1/6  | 1/6   | 1/6  | 1/6

To produce the datacards for a given benchpoint, run `python mklimits.py [BP]`, where `BP = BP1, BP2, BP3, BP4, ee100, em100, mm100`. The datacards must be uploaded to `login02.hep.wisc.edu` to run the limits.
```sh
cd datacards
make upload
```
On `login02.hep.wisc.edu`,
```sh
cd /afs/hep.wisc.edu/home/belknap/DblHLimits_611/src/datacards
cmsenv
sh run_combine.sh [BP]
```
Locally, run `make download` to download the `combine` products. To produce the limit plots, run `python mklimits.py plot [BP]`.
