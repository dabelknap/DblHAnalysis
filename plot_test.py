import tables as tb
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as sp_stat
from itertools import chain

#NEVENTS = 4807893.0 # ZZJets
NEVENTS = 1499064.0 # ZZTo4Mu
#LUMI = 19.6e3
#LUMI_A = 854.716 # DoubleMuParked 2012A
LUMI_A = 886.75482
LUMI_B = 3828.3217
LUMI_C = 6375.8242
LUMI_D = 6612.6485
LUMIS = {'A': LUMI_A,
         'B': LUMI_B,
         'C': LUMI_C,
         'D': LUMI_D}
#XSEC = 0.1296 # ZZJets
XSEC = 0.07691 # ZZTo4Mu

datasets = ["A", "B", "C", "D"]

CUT = ('(40 < z1mass) & (z1mass < 120) &'
       '(12 < z2mass) & (z2mass < 120)')

mass0 = []
z1mass0 = []
z2mass0 = []
for label in datasets:
    if label == 'A':
        filename = 'data_DoubleMu_Run2012A_22Jan2013_v1.h5'
    else:
        filename = 'data_DoubleMuParked_Run2012%s_22Jan2013_v1.h5' % label

    with tb.open_file('ntuples/' + filename, 'r') as h5file:
        table   = h5file.root.ZZ4l.mmmm
        mass0.extend([x['mass'] for x in table.where(CUT)])
        z1mass0.extend([x['z1mass'] for x in table.where(CUT)])
        z2mass0.extend([x['z2mass'] for x in table.where(CUT)])

print "Obs:", len(mass0)


#with tb.open_file('ntuples/ZZJetsTo4L_TuneZ2star_8TeV-madgraph-tauola.h5', 'r') as h5file:
with tb.open_file('ntuples/ZZTo4mu_8TeV-powheg-pythia6.h5', 'r') as h5file:
    table = h5file.root.ZZ4l.mmmm
    mass   = np.fromiter((x['mass'] for x in table.where(CUT)),np.float)
    z1mass = np.fromiter((x['z1mass'] for x in table.where(CUT)),np.float)
    z2mass = np.fromiter((x['z2mass'] for x in table.where(CUT)),np.float)
    weights = np.ones(mass.shape) * sum((LUMIS[x] for x in datasets))  * XSEC / NEVENTS

print "Exp: %.2f +/- %.2f" % (sum(weights), np.sqrt(sum(weights)))
print "P-val: %.4f sig" % sp_stat.norm.isf(sp_stat.poisson.sf(len(mass0), sum(weights)))

errbar_settings = {'fmt': 'ko',
                  'capsize': 0,
                  'linewidth': 1,
                  'ms': 5,
                  'label': 'Observed'}

zzstyle = {'facecolor': 'lightskyblue',
           'edgecolor': 'mediumblue',
           'linewidth': 1.5,
           'label': 'ZZJets'}

(n, bins) = np.histogram(mass0, 30, range=(50,300))
plt.hist(mass, bins=bins, weights=weights, histtype='stepfilled', **zzstyle)
plt.errorbar(0.5*(bins[1:]+bins[:-1]), n, yerr=np.sqrt(n), **errbar_settings)
plt.legend(loc='best')
plt.savefig('./plots/test_mass.pdf')

plt.clf()
(n, bins) = np.histogram(z1mass0, 25, range=(60,120))
plt.hist(z1mass, bins=bins, weights=weights, histtype='stepfilled', **zzstyle)
plt.errorbar(0.5*(bins[1:]+bins[:-1]), n, yerr=np.sqrt(n), **errbar_settings)
plt.legend(loc='best')
plt.savefig('./plots/test_z1mass.pdf')

plt.clf()
(n, bins) = np.histogram(z2mass0, 25, range=(40,120))
plt.hist(z2mass, bins=bins, weights=weights, histtype='stepfilled', **zzstyle)
plt.errorbar(0.5*(bins[1:]+bins[:-1]), n, yerr=np.sqrt(n), **errbar_settings)
plt.legend(loc='best')
plt.savefig('./plots/test_z2mass.pdf')
