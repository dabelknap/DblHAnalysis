import sys
import os
import glob
import logging

import plotters.xsec as xsec
import tables as tb
import numpy as np


class Yields(object):

    def __init__(self, analysis, base_selections, ntuple_dir,
            channels=[], lumi=19.7):
        self.base_selections = base_selections
        self.analysis = analysis
        self.ntuple_dir = ntuple_dir
        self.sample_groups = {}
        self.lumi = lumi
        self.channels = channels

        self.log = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

    def add_group(self, group_name, *sample_names, **kwargs):
        samples = []
        for name in sample_names:
            samples += glob.glob("%s/%s" % (self.ntuple_dir, name))

        is_data = kwargs.get('isData', False)
        is_sig = kwargs.get('isSignal', False)
        scale = kwargs.get('scale', 1.0)

        self.sample_groups[group_name] = {
            'sample_names': [os.path.splitext(os.path.basename(x))[0]
                             for x in samples],
            'scale': scale,
            'isSig': is_sig,
            'isData': is_data}

    def yields(self, group_name, **kwargs):
        values = []
        weights = []

        var = 'mass'

        cuts = kwargs.get('cuts', '(True)')
        cut = "%s & %s" % (self.base_selections, cuts)

        # choose which lepton scale-factor to use
        # e.g. lep_scale, lep_scale_e_up, lep_scale_m_up, ...
        lep_scale = kwargs.get('scale', 'lep_scale')

        is_data = self.sample_groups[group_name]['isData']
        vals = []
        wgts = []

        # Scale the yields globally by the given factor
        # Indented for adjusting yields for different BR scenarios
        scale_factor = self.sample_groups[group_name]['scale']

        if not is_data:
            self.log.info("Processing MC: %s" % group_name)

            for sample_name in self.sample_groups[group_name]["sample_names"]:
                with tb.open_file(
                    "%s/%s.h5" % (self.ntuple_dir, sample_name), 'r') \
                        as h5file:
                    for chan in self.channels:
                        table = getattr(getattr(h5file.root,
                                                self.analysis), chan)
                        vals += [x[var] for x in table.where(cut)]
                        scale = self.lumi * xsec.xsecs[sample_name] * \
                            scale_factor / xsec.nevents[sample_name]
                        wgts += [x['pu_weight'] * \
                                 x['lep_scale'] * \
                                 x['trig_scale'] * \
                                 scale \
                                 for x in table.where(cut)]

            counts = sum(wgts)
            if counts == 0:
                err = 0
            else:
                err = counts / np.sqrt(float(len(wgts)))

        else:
            self.log.info('Processing Data')

            vals = []
            evt_set = set()
            for sample_name in self.sample_groups['data']['sample_names']:
                with tb.open_file(
                    "%s/%s.h5" % (self.ntuple_dir, sample_name), 'r') \
                        as h5file:
                    for chan in self.channels:
                        table = getattr(getattr(h5file.root,
                                                self.analysis), chan)
                        for x in table.where(cut):
                            if (x['evt'], x['run'], x['lumi']) \
                                    not in evt_set:
                                vals.append(x[var])
                                evt_set.add(
                                    (x['evt'], x['run'], x['lumi']))
            counts = len(vals)
            err = np.sqrt(float(counts))

        return (counts, err)
