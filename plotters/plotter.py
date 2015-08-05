import sys
import os
import glob
import logging

import numpy as np
import tables as tb
import xsec

import matplotlib as mpl

# Use PFG/Tikz backend to generate plots
# Enables Latex, with better performance
# mpl.use("pgf")
# pgf_with_pdflatex = {
#         "pgf.texsystem": "pdflatex",
#         "pgf.preamble": [
#             r"\usepackage[utf8x]{inputenc}",
#             r"\usepackage[T1]{fontenc}",
#             r"\usepackage{cmbright}",
#             r"\usepackage{amsmath}",
#             #r"\usepackage{arev}",
#             r"\usepackage{libertine}",
#             r"\usepackage[libertine,cmintegrals,cmbraces]{newtxmath}"
#             ]
#         }
# mpl.rcParams.update(pgf_with_pdflatex)

import matplotlib.pyplot as plt
import matplotlib


plt.rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
plt.rc('text', usetex=True)
plt.rcParams['text.latex.preamble']=[r'\usepackage[helvet]{sfmath}']
#plt.rc('font', family='sans-serif')


class Plotter(object):

    def __init__(self, analysis, base_selections, ntuple_dir, out_dir,
            channels=[], lumi=19.7, partial_blind=False):
        self.base_selections = base_selections
        self.analysis = analysis
        self.out_dir = out_dir
        self.ntuple_dir = ntuple_dir
        self.sample_groups = {}
        self.sample_order = []
        self.channels = channels
        self.lumi = lumi
        self.partial_blind = partial_blind

        self.log = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

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

    def cut_flow(self, file_name, cuts, labels, **kwargs):
        log_scale = kwargs.get('log', False)
        title = kwargs.get('title', '')
        ylab = kwargs.get('ylab', '')
        legend_loc = kwargs.get('legend_loc', 'best')

        ind = np.arange(len(cuts))
        counts = np.zeros((len(cuts),))

        plots = []
        leg_labs = []
        plt.figure(figsize=(6, 5))

        for mc in self.sample_order:
            self.log.info('Processing MC: %s' % mc)

            tmp = np.zeros((len(cuts),))
            for sample_name in self.sample_groups[mc]["sample_names"]:
                with tb.open_file("%s/%s.h5" % (self.ntuple_dir, sample_name), 'r') as h5file:
                    for chan in self.channels:
                        table = getattr(getattr(h5file.root, self.analysis), chan)

                        for i, ct in enumerate(cuts):
                            cut = '%s & %s' % (self.base_selections, ct)
                            scale = self.lumi * xsec.xsecs[sample_name] / \
                                    xsec.nevents[sample_name]
                            cnts = sum([x['pu_weight'] * x['lep_scale'] * scale for x in table.where(cut)])

                            tmp[i] += cnts

            plots.append(plt.bar(ind, tmp, 1, bottom=counts, color=self.sample_groups[mc]['facecolor'], log=log_scale))
            leg_labs.append(self.sample_groups[mc]['label'])
            counts += tmp


        plt.legend( [p[0] for p in plots], leg_labs, loc=legend_loc )
        #plt.legend(loc=legend_loc)
        #if log_scale:
        #    plt.ylim(ymin=0.1)
        #    self.log.info('Applying log scale')
        #else:
        #    plt.ylim(ymin=0)

        plt.title(title)
        plt.xticks(ind+1/2., labels, size='large')
        plt.ylabel("Events", size='large', ha='right', position=(0,1))

        plt.tight_layout(0.5)

        self.log.info("Generating Histogram: cut flow, %s/%s" % (self.out_dir,
            file_name))

        plt.savefig("%s/%s" % (self.out_dir, file_name))

    def plot_stack(self, file_name, var, nbins, xmin, xmax, **kwargs):
        """
        Plot a stacked histogram
        shade=[(xmin1,xmax1,color1), (xmin2,xmax2,color2), ...]
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
        shade = kwargs.get('shade', None)
        legend_size = kwargs.get('legend_size', None)
        mc_err = kwargs.get('mc_err', False)

        hist_style = {'histtype': 'stepfilled',
                      'linewidth': 1.5,
                      'stacked': True,
                      'log': log_scale}

        cut = "%s & %s" % (self.base_selections, cuts)

        for mc in self.sample_order:
            vals = []
            wgts = []

            self.log.info("Processing MC: %s" % mc)

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

            if self.partial_blind:
                data_cut = cut + "& (h1mass < 120) & (h2mass < 120)"
            else:
                data_cut = cut

            self.log.info("Processing Data")

            vals = []
            evt_set = set()
            for sample_name in self.sample_groups['data']['sample_names']:
                with tb.open_file("%s/%s.h5" % (self.ntuple_dir, sample_name),
                        'r') as h5file:
                    for chan in self.channels:
                        table = getattr(getattr(h5file.root, self.analysis), chan)
                        for x in table.where(data_cut):
                            if (x['evt'], x['run'], x['lumi']) not in evt_set:
                                vals.append(x[var])
                                evt_set.add((x['evt'], x['run'], x['lumi']))

            (n1, bins1, patches1) = plt.hist(vals, nbins, range=(xmin, xmax))
            plt.clf()

        self.log.info("Generating Histogram: %s, %s/%s" % (var, self.out_dir, file_name))

        # Plot stacked MC
        plt.figure(figsize=(6, 5))
        (n, bins, patches) = plt.hist(
                values, nbins, weights=weights, range=(xmin, xmax),
                label=labels, **hist_style)

        if mc_err:
            n_total = n
            N = np.histogram(values, bins=bins)[0]
            plt.plot(0.5*(bins[1:] + bins[:-1]), n_total + n_total/np.sqrt(N) + 0.05*n_total,
                color='k', alpha=0.5, drawstyle='steps-mid')
            plt.plot(0.5*(bins[1:] + bins[:-1]), n_total - n_total/np.sqrt(N) - 0.05*n_total,
                color='k', alpha=0.5, drawstyle='steps-mid')

        if log_scale:
            plt.yscale('log')

        if 'data' in self.sample_groups:
            plt.errorbar(0.5*(bins[1:]+bins[:-1]), n1, yerr=[np.sqrt(n1)*0.99,np.sqrt(n1)],
                         fmt='ko', capsize=0, linewidth=1, ms=5, label="Observed")

        for i, name in enumerate(self.sample_order):
            try:
                for p in patches[i]:
                    p.set_facecolor(self.sample_groups[name]['facecolor'])
                    p.set_edgecolor(self.sample_groups[name]['edgecolor'])
            except TypeError:
                patches[i].set_facecolor(self.sample_groups[name]['facecolor'])
                patches[i].set_edgecolor(self.sample_groups[name]['edgecolor'])

        if legend_size:
            plt.legend(loc=legend_loc, prop={'size': legend_size})
        else:
            plt.legend(loc=legend_loc)

        if log_scale:
            plt.ylim(ymin=0.1)
        else:
            plt.ylim(ymin=0)
        if ylab_width:
            plt.ylabel('Events / %.1f GeV' % (bins[1] - bins[0]), ha='right', position=(0,1), size='larger')
        else:
            plt.ylabel(ylab, ha='right', position=(0,1), size='larger')
        plt.xlabel(xlab, ha='right', position=(1,0), size='larger')
        plt.title(title)

        if shade:
            for specs in shade:
                xmin, xmax, color = specs
                plt.axvspan(xmin, xmax, facecolor=color, alpha=0.2)

        plt.tight_layout(0.5)

        plt.savefig("%s/%s" % (self.out_dir, file_name))


    def plot_compare(self, file_name, var, nbins, xmin, xmax, **kwargs):
        """
        Plot a stacked histogram
        shade=[(xmin1,xmax1,color1), (xmin2,xmax2,color2), ...]
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
        shade = kwargs.get('shade', None)
        legend_size = kwargs.get('legend_size', None)

        hist_style = {'histtype': 'step',
                      'linewidth': 1.5,
                      'normed': True,
                      'log': log_scale}

        cut = "%s & %s" % (self.base_selections, cuts)

        for mc in self.sample_order:
            vals = []
            wgts = []

            self.log.info("Processing MC: %s" % mc)

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
            self.log.info("Processing Data")

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

        self.log.info("Generating Histogram: %s, %s/%s" % (var, self.out_dir, file_name))

        plt.figure(figsize=(6, 5))
        (n, bins, patches) = plt.hist(
                values, nbins, weights=weights, range=(xmin, xmax),
                label=labels, **hist_style)

        if log_scale:
            plt.yscale('log')

        if 'data' in self.sample_groups:
            plt.errorbar(0.5*(bins[1:]+bins[:-1]), n1, yerr=[np.sqrt(n1)*0.99,np.sqrt(n1)],
                         fmt='ko', capsize=0, linewidth=1, ms=5, label="Observed")

        for i, name in enumerate(self.sample_order):
            try:
                for p in patches[i]:
                    p.set_facecolor(self.sample_groups[name]['facecolor'])
                    p.set_edgecolor(self.sample_groups[name]['edgecolor'])
            except TypeError:
                patches[i].set_facecolor(self.sample_groups[name]['facecolor'])
                patches[i].set_edgecolor(self.sample_groups[name]['edgecolor'])

        if legend_size:
            plt.legend(loc=legend_loc, prop={'size': legend_size})
        else:
            plt.legend(loc=legend_loc)

        if log_scale:
            plt.ylim(ymin=0.1)
        else:
            plt.ylim(ymin=0)
        if ylab_width:
            plt.ylabel('Events/%.1f GeV' % (bins[1] - bins[0]), ha='right', position=(0,1), size='larger')
        else:
            plt.ylabel(ylab, ha='right', position=(0,1), size='larger')
        plt.xlabel(xlab, ha='right', position=(1,0), size='larger')
        plt.title(title)

        if shade:
            for specs in shade:
                xmin, xmax, color = specs
                plt.axvspan(xmin, xmax, facecolor=color, alpha=0.2)

        plt.tight_layout(0.5)

        plt.savefig("%s/%s" % (self.out_dir, file_name), dpi=300)

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
