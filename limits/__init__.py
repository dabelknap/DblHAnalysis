from __future__ import absolute_import

import sys
import os
import glob
import logging

from .datacard import Datacard
import plotters.xsec as xsec
import tables as tb
import numpy as np


class Limits(object):

    def __init__(self, analysis, base_selections, ntuple_dir, out_dir,
                 channels=[], lumi=19.7, blinded=True):
        self.base_selections = base_selections
        self.analysis = analysis
        self.out_dir = out_dir
        self.ntuple_dir = ntuple_dir
        self.sample_groups = {}
        self.lumi = lumi
        self.blinded = blinded
        self.sytematic_list = []
        self.datacard = Datacard(self.analysis)
        self.channels = channels

        self.log = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

        os.system("mkdir -p %s" % self.out_dir)

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

    def add_bkg_rate(self, name, rate):
        self.datacard.add_bkg(name, rate)

    def add_systematics(self, syst_name, syst_type, **kwargs):
        self.datacard.add_syst(syst_name, syst_type, **kwargs)

    def gen_card(self, file_name, **kwargs):
        values = []
        weights = []

        var = 'mass'

        cuts = kwargs.get('cuts', '(True)')
        cut = "%s & %s" % (self.base_selections, cuts)

        for key in self.sample_groups:
            is_data = self.sample_groups[key]['isData']
            is_sig = self.sample_groups[key]['isSig']
            vals = []
            wgts = []

            scale_factor = self.sample_groups[key]['scale']

            if not is_data and not is_sig:
                self.log.info("Processing MC: %s" % key)

                for sample_name in self.sample_groups[key]["sample_names"]:
                    with tb.open_file(
                        "%s/%s.h5" % (self.ntuple_dir, sample_name), 'r') \
                            as h5file:
                        for chan in self.channels:
                            table = getattr(getattr(h5file.root,
                                                    self.analysis), chan)
                            vals += [x[var] for x in table.where(cut)]

                            scale = self.lumi * xsec.xsecs[sample_name] * \
                                scale_factor / xsec.nevents[sample_name]
                            wgts += [x['pu_weight'] * x['lep_scale'] * scale
                                     for x in table.where(cut)]

                self.datacard.add_bkg(key, sum(wgts))

            # apply to signal MC only
            elif is_sig and not is_data:
                self.log.info("Processing Signal MC: %s" % key)

                for sample_name in self.sample_groups[key]["sample_names"]:
                    with tb.open_file(
                        "%s/%s.h5" % (self.ntuple_dir, sample_name), 'r') \
                            as h5file:

                        # chan is dblh4l
                        # for-loop is technically not necessary
                        for chan in self.channels:

                            # c is mmmm, emem, eeee, etc.
                            try:
                                for c in scale_factor.keys():
                                    c_cut = "%s & (channel == '%s')" % (cut, c)

                                    table = getattr(getattr(h5file.root,
                                                            self.analysis), chan)
                                    vals += [x[var] for x in table.where(c_cut)]

                                    scl = scale_factor[c]

                                    scale = self.lumi * xsec.xsecs[sample_name] * \
                                        scl / xsec.nevents[sample_name]

                                    wgts += [x['pu_weight'] * x['lep_scale'] * scale
                                             for x in table.where(c_cut)]

                            # if scale_factor is a scalar instead of a dict
                            except AttributeError:
                                table = getattr(getattr(h5file.root,
                                                        self.analysis), chan)
                                vals += [x[var] for x in table.where(cut)]

                                scl = scale_factor

                                scale = self.lumi * xsec.xsecs[sample_name] * \
                                    scl / xsec.nevents[sample_name]

                                wgts += [x['pu_weight'] * x['lep_scale'] * scale
                                         for x in table.where(cut)]

                self.datacard.add_sig(key, sum(wgts))


            elif is_data and not self.blinded:
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

                self.datacard.set_observed(len(vals))

        self.log.info("Saving card to file: %s/%s" % (self.out_dir, file_name))

        with open("%s/%s" % (self.out_dir, file_name), 'w') as outfile:
            outfile.write(self.datacard.dump())
