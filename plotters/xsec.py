PB = 1.0e3
FB = 1.0

BR_WJJ = 0.676
BR_WLNU = 0.324

Z_XSEC = 3503.7 * PB
TT_XSEC = 252.89 * PB

import json

xsecs = {'HPlusPlusHMinusMinusHTo4L_M-110_8TeV-pythia6': 352.49 * FB,
         'HPlusPlusHMinusMinusHTo4L_M-400_8TeV-pythia6': 1.3414 * FB,
         'HPlusPlusHMinusMinusHTo4L_M-450_8TeV-pythia6': 0.71531 * FB,
         'HPlusPlusHMinusMinusHTo4L_M-500_8TeV-pythia6': 0.39604 * FB,

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

         'ZZJetsTo4L_TuneZ2star_8TeV-madgraph-tauola': 0.1296 * PB,

         'T_s-channel_TuneZ2star_8TeV-powheg-tauola':        3.79 * PB,
         'T_t-channel_TuneZ2star_8TeV-powheg-tauola':        56.4 * PB,
         'T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola':    11.1 * PB,
         'Tbar_s-channel_TuneZ2star_8TeV-powheg-tauola':     1.56 * PB,
         'Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola':     30.7 * PB,
         'Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola': 11.1 * PB,

         'WZJetsTo2L2Q_TuneZ2star_8TeV-madgraph-tauola': 2.207 * PB,
         'WZJetsTo3LNu_TuneZ2_8TeV-madgraph-tauola':     1.058 * PB}

nevents = json.load(open("./plotters/mc_events.json", 'r'))
