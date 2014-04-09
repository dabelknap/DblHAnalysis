import tables as tb
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as sp_stat
from itertools import chain

madgraph = False

subdir = '2014-03-31'

chan = 'eeee'

if madgraph:
    NEVENTS = 4807893.0 # ZZJets
    XSEC = 0.1296 # ZZJets
    MC_NAME = 'ntuples/ZZJetsTo4L_TuneZ2star_8TeV-madgraph-tauola.h5'
else:
    if chan == 'mmmm':
        MC_NAME = 'ntuples/ZZTo4mu_8TeV-powheg-pythia6.h5'
        XSEC = 0.07691 # ZZTo4Mu
        NEVENTS = 1499064.0 # ZZTo4Mu
    if chan == 'eeee':
        XSEC = 0.07691 # ZZTo4e
        NEVENTS = 1476608.0 # ZZTo4e
        MC_NAME = 'ntuples/ZZTo4e_8TeV-powheg-pythia6.h5'

if chan == 'mmmm':
    data_name = 'DoubleMu'
    LUMI_A = 886.75482
    LUMI_B = 3828.3217
    LUMI_C = 6375.8242
    LUMI_D = 6612.6485
elif chan == 'eeee':
    data_name = 'DoubleElectron'
    LUMI_A = 887.7079
    LUMI_B = 4402.9805
    LUMI_C = 7147.8159
    LUMI_D = 7317.7986

LUMIS = {'A': LUMI_A,
         'B': LUMI_B,
         'C': LUMI_C,
         'D': LUMI_D}

datasets = ["A", "B", "C", "D"]

CUT = ('(40 < z1mass) & (z1mass < 120) &'
       '(12 < z2mass) & (z2mass < 120)')

mass0 = []
z1mass0 = []
z2mass0 = []
l1Pt0 = []
l2Pt0 = []
l3Pt0 = []
l4Pt0 = []

for label in datasets:
    if label != 'A' and chan == 'mmmm':
        filename = 'data_DoubleMuParked_Run2012%s_22Jan2013_v1.h5' % label
    else:
        filename = 'data_%s_Run2012%s_22Jan2013_v1.h5' % (data_name, label)

    with tb.open_file('ntuples/' + filename, 'r') as h5file:
        table   = getattr(h5file.root.ZZ4l, chan)
        mass0.extend([x['mass'] for x in table.where(CUT)])
        z1mass0.extend([x['z1mass'] for x in table.where(CUT)])
        z2mass0.extend([x['z2mass'] for x in table.where(CUT)])
        l1Pt0.extend([x['l1Pt'] for x in table.where(CUT)])
        l2Pt0.extend([x['l2Pt'] for x in table.where(CUT)])
        l3Pt0.extend([x['l3Pt'] for x in table.where(CUT)])
        l4Pt0.extend([x['l4Pt'] for x in table.where(CUT)])


print "Obs:", len(mass0)


with tb.open_file(MC_NAME, 'r') as h5file:
    table = getattr(h5file.root.ZZ4l, chan)
    mass   = np.fromiter((x['mass'] for x in table.where(CUT)),np.float)
    z1mass = np.fromiter((x['z1mass'] for x in table.where(CUT)),np.float)
    z2mass = np.fromiter((x['z2mass'] for x in table.where(CUT)),np.float)
    l1Pt   = np.fromiter((x['l1Pt'] for x in table.where(CUT)),np.float)
    l2Pt   = np.fromiter((x['l2Pt'] for x in table.where(CUT)),np.float)
    l3Pt   = np.fromiter((x['l3Pt'] for x in table.where(CUT)),np.float)
    l4Pt   = np.fromiter((x['l4Pt'] for x in table.where(CUT)),np.float)
    weights = np.fromiter((x['lep_scale'] * x['pu_weight'] for x in table.where(CUT)),np.float)
    weights *= sum((LUMIS[x] for x in datasets)) * XSEC / NEVENTS
    #weights = np.ones(mass.shape) * sum((LUMIS[x] for x in datasets))  * XSEC / NEVENTS
    #weights = np.ones(mass.shape) * 19.6e3  * XSEC / NEVENTS

print "Lumi: %.2f ifb" % (sum((LUMIS[x] for x in datasets)) / 1000.0)
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
plt.ylim(ymin=0)
plt.title('%s, 8 TeV, 19.6 ifb' % chan)
plt.xlabel('4l Mass [GeV]')
plt.ylabel('Events/%.1f GeV' % (bins[1] - bins[0]))
plt.savefig('./plots/%s/%s_mass.pdf' % (subdir, chan))

plt.clf()
(n, bins) = np.histogram(z1mass0, 25, range=(60,120))
plt.hist(z1mass, bins=bins, weights=weights, histtype='stepfilled', **zzstyle)
plt.errorbar(0.5*(bins[1:]+bins[:-1]), n, yerr=np.sqrt(n), **errbar_settings)
plt.legend(loc='best')
plt.ylim(ymin=0)
plt.title('%s, 8 TeV, 19.6 ifb' % chan)
plt.xlabel('Z1 Mass [GeV]')
plt.ylabel('Events/%.1f GeV' % (bins[1] - bins[0]))
plt.savefig('./plots/%s/%s_z1mass.pdf' % (subdir, chan))

plt.clf()
(n, bins) = np.histogram(z2mass0, 25, range=(40,120))
plt.hist(z2mass, bins=bins, weights=weights, histtype='stepfilled', **zzstyle)
plt.errorbar(0.5*(bins[1:]+bins[:-1]), n, yerr=np.sqrt(n), **errbar_settings)
plt.legend(loc='best')
plt.ylim(ymin=0)
plt.title('%s, 8 TeV, 19.6 ifb' % chan)
plt.xlabel('Z2 Mass [GeV]')
plt.ylabel('Events/%.1f GeV' % (bins[1] - bins[0]))
plt.savefig('./plots/%s/%s_z2mass.pdf' % (subdir, chan))

"""Lepton Pt Plots"""

nbins = 25
xlow = 0
xhigh = 200

plt.clf()
(n, bins) = np.histogram(l1Pt0, nbins, range=(xlow, xhigh))
plt.hist(l1Pt, bins=bins, weights=weights, histtype='stepfilled', **zzstyle)
plt.errorbar(0.5*(bins[1:]+bins[:-1]), n, yerr=np.sqrt(n), **errbar_settings)
plt.legend(loc='best')
plt.ylim(ymin=0)
plt.title('%s, 8 TeV, 19.6 ifb' % chan)
plt.xlabel('l1 pT [GeV]')
plt.ylabel('Events/%.1f GeV' % (bins[1] - bins[0]))
plt.savefig('./plots/%s/%s_l1Pt.pdf' % (subdir, chan))

plt.clf()
(n, bins) = np.histogram(l2Pt0, nbins, range=(xlow, xhigh))
plt.hist(l2Pt, bins=bins, weights=weights, histtype='stepfilled', **zzstyle)
plt.errorbar(0.5*(bins[1:]+bins[:-1]), n, yerr=np.sqrt(n), **errbar_settings)
plt.legend(loc='best')
plt.ylim(ymin=0)
plt.title('%s, 8 TeV, 19.6 ifb' % chan)
plt.xlabel('l2 pT [GeV]')
plt.ylabel('Events/%.1f GeV' % (bins[1] - bins[0]))
plt.savefig('./plots/%s/%s_l2Pt.pdf' % (subdir, chan))

plt.clf()
(n, bins) = np.histogram(l3Pt0, nbins, range=(xlow, xhigh))
plt.hist(l3Pt, bins=bins, weights=weights, histtype='stepfilled', **zzstyle)
plt.errorbar(0.5*(bins[1:]+bins[:-1]), n, yerr=np.sqrt(n), **errbar_settings)
plt.legend(loc='best')
plt.ylim(ymin=0)
plt.title('%s, 8 TeV, 19.6 ifb' % chan)
plt.xlabel('l3 pT [GeV]')
plt.ylabel('Events/%.1f GeV' % (bins[1] - bins[0]))
plt.savefig('./plots/%s/%s_l3Pt.pdf' % (subdir, chan))

plt.clf()
(n, bins) = np.histogram(l4Pt0, nbins, range=(xlow, xhigh))
plt.hist(l4Pt, bins=bins, weights=weights, histtype='stepfilled', **zzstyle)
plt.errorbar(0.5*(bins[1:]+bins[:-1]), n, yerr=np.sqrt(n), **errbar_settings)
plt.legend(loc='best')
plt.ylim(ymin=0)
plt.title('%s, 8 TeV, 19.6 ifb' % chan)
plt.xlabel('l4 pT [GeV]')
plt.ylabel('Events/%.1f GeV' % (bins[1] - bins[0]))
plt.savefig('./plots/%s/%s_l4Pt.pdf' % (subdir, chan))
