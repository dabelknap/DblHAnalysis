PB = 1.0e3
FB = 1.0

BR_WJJ = 0.676
BR_WLNU = 0.324

Z_XSEC = 3503.7 * PB
TT_XSEC = 252.89 * PB

import json

xsecs = {'HPlusPlusHMinusMinusHTo4L_M-110_8TeV-pythia6': 352.49 * FB,
         'HPlusPlusHMinusMinusHTo4L_M-130_8TeV-pythia6': 186.21 * FB,
         'HPlusPlusHMinusMinusHTo4L_M-150_8TeV-pythia6': 106.55 * FB,
         'HPlusPlusHMinusMinusHTo4L_M-170_8TeV-pythia6': 64.641 * FB,
         'HPlusPlusHMinusMinusHTo4L_M-200_8TeV-pythia6': 33.209 * FB,
         'HPlusPlusHMinusMinusHTo4L_M-250_8TeV-pythia6': 12.724 * FB,
         'HPlusPlusHMinusMinusHTo4L_M-300_8TeV-pythia6': 5.5458 * FB,
         'HPlusPlusHMinusMinusHTo4L_M-350_8TeV-pythia6': 2.6413 * FB,
         'HPlusPlusHMinusMinusHTo4L_M-400_8TeV-pythia6': 1.3414 * FB,
         'HPlusPlusHMinusMinusHTo4L_M-450_8TeV-pythia6': 0.71531 * FB,
         'HPlusPlusHMinusMinusHTo4L_M-500_8TeV-pythia6': 0.39604 * FB,
         'HPlusPlusHMinusMinusHTo4L_M-600_8TeV-pythia6': 0.13271 * FB,
         'HPlusPlusHMinusMinusHTo4L_M-700_8TeV-pythia6': 0.48382e-1 * FB,

         'GluGluToHToZZTo4L_M-125_8TeV-powheg-pythia6': 19.27 * 2.76e-04 * PB,

         'ggZZ4L': 4.8 * FB,
         'ggZZ2L2L': 12.03 * FB,

         'DYJetsToLL_M-10To50filter_8TeV-madgraph':          915.0 * PB,
         'DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball': 3503.71 * PB,

         'Z1jets_M50':     Z_XSEC * 0.190169492,
         'Z2jets_M50_S10': Z_XSEC * 0.061355932,
         'Z3jets_M50':     Z_XSEC * 0.017322034,
         'Z4jets_M50':     Z_XSEC * 0.007810169,

         'ZZTo4e_8TeV-powheg-pythia6':      0.07691 * PB,
         'ZZTo4mu_8TeV-powheg-pythia6':     0.07691 * PB,
         'ZZTo4tau_8TeV-powheg-pythia6':    0.07691 * PB,
         'ZZTo2e2mu_8TeV-powheg-pythia6':   0.1767 * PB,
         'ZZTo2e2tau_8TeV-powheg-pythia6':  0.1767 * PB,
         'ZZTo2mu2tau_8TeV-powheg-pythia6': 0.1767 * PB,

         'TTJetsFullLepMGDecays': TT_XSEC * BR_WLNU * BR_WLNU,
         'TTJetsSemiLepMGDecays': TT_XSEC * BR_WJJ * BR_WLNU * 2,

         'TTGJets':  2.166 * PB,
         'TTWJets':  0.2057 * PB,
         'TTWWJets': 0.002 * PB,
         'TTZJets':  0.232 * PB,

         'ZZJetsTo4L_TuneZ2star_8TeV-madgraph-tauola': 0.1296 * PB,

         'T_s-channel_TuneZ2star_8TeV-powheg-tauola':        3.79 * PB,
         'T_t-channel_TuneZ2star_8TeV-powheg-tauola':        56.4 * PB,
         'T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola':    11.1 * PB,
         'Tbar_s-channel_TuneZ2star_8TeV-powheg-tauola':     1.56 * PB,
         'Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola':     30.7 * PB,
         'Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola': 11.1 * PB,

         'WZJetsTo2L2Q_TuneZ2star_8TeV-madgraph-tauola': 2.207 * PB,
         'WZJetsTo3LNu_TuneZ2_8TeV-madgraph-tauola':     1.058 * PB,

         'WWJetsTo2L2Nu_TuneZ2star_8TeV-madgraph-tauola': 54.838*(0.1075+0.1057+0.1125)*(0.1075+0.1057+0.1125) * PB,

         'ZZZNoGstarJets': 0.0192 * PB,
         'WWZNoGstarJets': 0.0633 * PB,
         'WWWJets':        0.08217 * PB,
         'WWGJets':        1.44 * PB}

nevents = json.load(open("./plotters/mc_events.json", 'r'))
