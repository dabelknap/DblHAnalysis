import tables as tb
import numpy as np
import matplotlib.pyplot as plt
from itertools import chain

NEVENTS = 4807893.0
#LUMI = 19.6e3
LUMI_A = 854.716
LUMI_B = 3828.3217
LUMI_C = 6375.8242
LUMI_D = 6612.6485
LUMI = LUMI_B + LUMI_C + LUMI_D
XSEC = 0.1296

for label in ["B", "C", "D"]:
    mass0 = []
    z1mass0 = []
    z2mass0 = []
    with tb.open_file('ntuples/data_DoubleMuParked_Run2012%s_22Jan2013_v1.h5' % label, 'r') as h5file:
        table   = h5file.root.ZZ4l.mmmm
        mass0 += [x['mass'] for x in table.where('(z1mass > 40)')]
        z1mass0 += [x['z1mass'] for x in table.where('(z1mass > 40)')]
        z2mass0 += [x['z2mass'] for x in table.where('(z1mass > 40)')]

print "Events w/ z1mass > 40:", len(mass0)


with tb.open_file('ntuples/ZZJetsTo4L_TuneZ2star_8TeV-madgraph-tauola.h5', 'r') as h5file:
    table = h5file.root.ZZ4l.mmmm
    mass   = np.fromiter((x['mass'] for x in table.where('(z1mass > 40)')),np.float)
    z1mass = np.fromiter((x['z1mass'] for x in table.where('(z1mass > 40)')),np.float)
    z2mass = np.fromiter((x['z2mass'] for x in table.where('(z1mass > 40)')),np.float)
    weights = np.ones(mass.shape) * LUMI * XSEC / NEVENTS

errbar_settings = {'fmt': 'ko',
                  'capsize': 0,
                  'linewidth': 1,
                  'ms': 5,
                  'label': 'Observed'}

zzstyle = {'facecolor': 'lightskyblue',
           'edgecolor': 'mediumblue',
           'linewidth': 1.5,
           'label': 'ZZJets'}

(n, bins) = np.histogram(mass0, 100, range=(50,300))
plt.hist(mass, bins=bins, weights=weights, histtype='stepfilled', **zzstyle)
plt.errorbar(0.5*(bins[1:]+bins[:-1]), n, yerr=np.sqrt(n), **errbar_settings)
plt.legend(loc='best')
plt.savefig('./plots/test_mass.pdf')

plt.clf()
(n, bins) = np.histogram(z1mass0, 100, range=(60,120))
plt.hist(z1mass, bins=bins, weights=weights, histtype='stepfilled', **zzstyle)
plt.errorbar(0.5*(bins[1:]+bins[:-1]), n, yerr=np.sqrt(n), **errbar_settings)
plt.legend(loc='best')
plt.savefig('./plots/test_z1mass.pdf')

plt.clf()
(n, bins) = np.histogram(z2mass0, 100, range=(40,120))
plt.hist(z2mass, bins=bins, weights=weights, histtype='stepfilled', **zzstyle)
plt.errorbar(0.5*(bins[1:]+bins[:-1]), n, yerr=np.sqrt(n), **errbar_settings)
plt.legend(loc='best')
plt.savefig('./plots/test_z2mass.pdf')
