#Doubly Charged Higgs Analysis at 8 TeV

This package is used to perform a search for a Doubly-Charged Higgs boson using
the 8 TeV CMS dataset. It runs on n-tuples produced by `FinalStateAnalysis`
(https://github.com/uwcms/FinalStateAnalysis).

##Producing n-tuples
To produce the FSA n-tuples used by this package, you run

```sh
make_ntuples_cfg.py rerunFSA=1 channels="zz" dblhMode=1
```

within `FinalStateAnalysis/NtupleTools/test`. The `run.py` script runs on the
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
Run with `python run.py tt [samples,...]`. We make the following modifications to the
pre-selection:

 - Two best isolated leptons < 0.4 and worst > 0.4
 - Z-veto: for all OSSF pairs, require |m(ll) - Mz| > 20.0
 - sT > 150 and MET > 30

Make plots with `python mkplots.py tt`.

###Z Control Region
Run with `python run.py z [sample,...]`. We make the following modifications to
the pre-selection:

 - Z-flag: Require at least one OSSF pair with |m(ll) - Mz| < 20.0
 - sT > 150

Make plots with `python mkplots.py z`.
