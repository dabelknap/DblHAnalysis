import sys
import os
import glob

import numpy as np
import tables as tb
import xsec

import matplotlib as mpl

# Use PFG/Tikz backend to generate plots
# Enables Latex, with better performance
mpl.use("pgf")
pgf_with_pdflatex = {
        "pgf.texsystem": "pdflatex",
        "pgf.preamble": [
            r"\usepackage[utf8x]{inputenc}",
            r"\usepackage[T1]{fontenc}",
            r"\usepackage{libertine}",
            r"\usepackage[libertine,cmintegrals,cmbraces]{newtxmath}"
            ]
        }
mpl.rcParams.update(pgf_with_pdflatex)

import matplotlib.pyplot as plt


class Plotter(object):

    def __init__(self, analysis, base_selections, ntuple_dir, out_dir,
            channels=[], lumi=19.7):
        self.base_selections = base_selections
        self.analysis = analysis
        self.out_dir = out_dir
        self.ntuple_dir = ntuple_dir
        self.sample_groups = {}
        self.sample_order = []
        self.channels = channels
        self.lumi = lumi

        os.system("mkdir -p %s" % self.out_dir)

    def add_group(self, group_name, label, *sample_names, **kwargs):
        """
        Create a named group of MC samples, and assign plotting attributes
        """
        samples = []
        for name in sample_names:
            samples += glob.glob("%s/%s" % (self.ntuple_dir, name))

        edgecolor = kwargs.get('edgecolor', 'black')
        facecolor = kwargs.get('facecolor', 'white')
        is_data = kwargs.get('isdata', False)

        self.sample_groups[group_name] = {
                'sample_names': [os.path.splitext(os.path.basename(x))[0]
                                 for x in samples],
                'edgecolor': edgecolor,
                'facecolor': facecolor,
                'label': label,
                'isdata': is_data}

    def stack_order(self, *sample_order):
        """
        Define the order in which mc samples are to be stacked in the plot
        """
        self.sample_order = []
        for sample in sample_order:
            if sample not in self.sample_groups:
                raise ValueError("%s not defined" % sample)
            self.sample_order.append(sample)

    def plot_stack(self, file_name, var, nbins, xmin, xmax, **kwargs):
        """
        Plot a stacked histogram
        """
        values = []
        weights = []
        labels = []

        cuts = kwargs.get('cuts', '(True)')
        legend_loc = kwargs.get('legend_loc', 'best')
        ylab_width = kwargs.get('label_bin_width', False)
        ylab = kwargs.get('ylab', '')
        xlab = kwargs.get('xlab', '')
        title = kwargs.get('title', '')
        log_scale = kwargs.get('log', False)

        hist_style = {'histtype': 'stepfilled',
                      'linewidth': 1.5,
                      'stacked': True,
                      'log': log_scale}

        cut = "%s & %s" % (self.base_selections, cuts)

        for mc in self.sample_order:
            vals = []
            wgts = []

            for sample_name in self.sample_groups[mc]["sample_names"]:
                with tb.open_file("%s/%s.h5" % (self.ntuple_dir, sample_name),
                        'r') as h5file:
                    for chan in self.channels:
                        table = getattr(getattr(h5file.root, self.analysis),
                                        chan)
                        vals += [x[var] for x in table.where(cut)]
                        scale = self.lumi * xsec.xsecs[sample_name] / \
                                xsec.nevents[sample_name]
                        wgts += [x['pu_weight'] * x['lep_scale'] * scale for x in table.where(cut)]

            values.append(vals)
            weights.append(wgts)
            labels += [self.sample_groups[mc]['label']]

        if 'data' in self.sample_groups:
            vals = []
            evt_set = set()
            for sample_name in self.sample_groups['data']['sample_names']:
                with tb.open_file("%s/%s.h5" % (self.ntuple_dir, sample_name),
                        'r') as h5file:
                    for chan in self.channels:
                        table = getattr(getattr(h5file.root, self.analysis), chan)
                        for x in table.where(cut):
                            if (x['evt'], x['run'], x['lumi']) not in evt_set:
                                vals.append(x[var])
                                evt_set.add((x['evt'], x['run'], x['lumi']))

            (n1, bins1, patches1) = plt.hist(vals, nbins, range=(xmin, xmax))
            plt.clf()

        plt.figure(figsize=(5, 4))
        (n, bins, patches) = plt.hist(
                values, nbins, weights=weights, range=(xmin, xmax),
                label=labels, **hist_style)

        if 'data' in self.sample_groups:
            plt.errorbar(0.5*(bins[1:]+bins[:-1]), n1, yerr=np.sqrt(n1),
                         fmt='ko', capsize=0, linewidth=1, ms=5, label="Observed")

        for i, name in enumerate(self.sample_order):
            try:
                for p in patches[i]:
                    p.set_facecolor(self.sample_groups[name]['facecolor'])
                    p.set_edgecolor(self.sample_groups[name]['edgecolor'])
            except TypeError:
                patches[i].set_facecolor(self.sample_groups[name]['facecolor'])
                patches[i].set_edgecolor(self.sample_groups[name]['edgecolor'])

        plt.legend(loc=legend_loc)
        if log_scale:
            plt.ylim(ymin=0.1)
        else:
            plt.ylim(ymin=0)
        if ylab_width:
            plt.ylabel('Events/%.1f GeV' % (bins[1] - bins[0]))
        else:
            plt.ylabel(ylab)
        plt.xlabel(xlab)
        plt.title(title)

        plt.tight_layout(0.5)

        plt.savefig("%s/%s" % (self.out_dir, file_name))


def main():
    plotter = Plotter("DblH4l", "(mass > 80)", "../ntuples", "../plots/test",
                      channels=["mmmm"], lumi=19.7)

    plotter.add_group("hpp", "HPP", "HPlus*110*",
                      facecolor='mediumorchid', edgecolor='indigo')
    plotter.add_group("zz", "ZZ", "ZZTo*",
                      facecolor='lightskyblue', edgecolor='darkblue')

    plotter.stack_order("zz", "hpp")

    plotter.plot_stack('test.pdf', 'h1mass', 10, 10, 210,
            title=r'$\sqrt{s}=$ 8 TeV, 19.7 $\text{fb}^{-1}$',
            xlab=r'$M_{l^+l^+}$ [GeV]',
            label_bin_width=True)


if __name__ == "__main__":
    main()
