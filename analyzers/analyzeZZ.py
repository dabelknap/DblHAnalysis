import tables as tb
import numpy as np
import os
import sys
from itertools import permutations
import argparse

from ntuple_defs import EventZZ
from scale_factors import LeptonScaleFactors
from pu_weights import PileupWeights
import leptonId as lepId

sys.argv.append('-b')
import ROOT as rt
sys.argv.pop()


ZMASS = 91.2


class CutSequence(object):

    def __init__(self):
        self.cut_sequence = []

    def add(self, fun):
        self.cut_sequence.append(fun)

    def evaluate(self, rtrow):
        cut_results = [f(rtrow) for f in self.cut_sequence]
        return all(cut_results)


class ZZAnalyzer(object):

    def __init__(self, sample_location, out_file):
        self.sample_name = os.path.basename(sample_location)
        self.file_names = os.listdir(sample_location)
        self.out_file = out_file
        self.sample_location = sample_location

    def __enter__(self):
        self.begin()
        return self

    def __exit__(self, type, value, traceback):
        self.finish()

    def begin(self):
        self.lepscaler = LeptonScaleFactors()
        self.pu_weights = PileupWeights()

        self.h5file = tb.open_file(self.out_file, mode='a')

        try:
            self.h5file.removeNode('/ZZ4l/%s' % self.channel)
        except tb.NodeError:
            pass

        try:
            self.zz_group = self.h5file.create_group('/', 'ZZ4l', 'ZZ to 4l')
        except tb.NodeError:
            self.zz_group = self.h5file.root.ZZ4l

        self.table = self.h5file.create_table(
            self.zz_group, self.channel,
            EventZZ, "Selected %s Events" % self.channel)

        self.h5row = self.table.row

    def analyze(self):
        event_set = None

        for i, file_name in enumerate(self.file_names):
            if i % 20 == 0:
                print "  Processing %i/%i files" % (i+1, len(self.file_names))
            file_path = os.path.join(self.sample_location, file_name)
            rtFile = rt.TFile(file_path, "READ")
            tree = rtFile.Get("%s/final/Ntuple" % self.channel)

            for rtrow in tree:
                if event_set:
                    if rtrow.evt not in event_set:
                        self.h5row.append()
                        best_cand = (0, 0, [])
                else:
                    best_cand = (0, 0, [])
                    event_set = set()

                if not self.preselection(rtrow):
                    continue

                event_set.add(rtrow.evt)

                candidate = self.choose_leptons(rtrow)

                if self.good_to_store(candidate, best_cand):
                    self.store_row(rtrow, self.h5row, *candidate[2])
                    best_cand = tuple(candidate)

            self.h5row.append()
            self.table.flush()
            rtFile.Close()

    def finish(self):
        self.lepscaler.close()
        self.h5file.close()

    def trigger_threshold(self, rtrow):
        pts = [getattr(rtrow, "%sPt" % l) for l in self.leptons]
        pts.sort(reverse=True)
        return pts[0] > 20.0 and pts[1] > 10.0

    def choose_leptons(self, rtrow):
        """
        Choose the arrangement of the leptons that best satisfies
        ZZ selection
        """
        def lep_order(a, b):
            a_index = int(a[1])
            b_index = int(b[1])
            return a_index > b_index

        cands = []
        for l in permutations(self.leptons):
            if lep_order(l[0], l[1]) or lep_order(l[2], l[3]):
                continue

            z1mass = getattr(rtrow, "%s_%s_Mass" % (l[0], l[1]))
            z2Pt = getattr(rtrow, "%sPt" % l[2]) + \
                getattr(rtrow, "%sPt" % l[3])
            OS1 = getattr(rtrow, "%s_%s_SS" % (l[0], l[1])) < 0.5
            OS2 = getattr(rtrow, "%s_%s_SS" % (l[2], l[3])) < 0.5

            if OS1 and OS2:
                cands.append((z1mass, z2Pt, list(l)))

        # Sort by Z2 Pt scalar sum
        cands.sort(key=lambda x: x[1], reverse=True)
        # Sort by Z1 mass closest to nominal
        cands.sort(key=lambda x: abs(x[0] - ZMASS))

        z1mass, z2Pt, leps = cands[0]

        return (z1mass, z2Pt, leps)

    @staticmethod
    def good_to_store(cand1, cand2):
        """Is cand1 better than cand2 for ZZ?"""
        if abs(cand1[0] - ZMASS) < abs(cand2[0] - ZMASS):
            if cand1[1] > cand2[1]:
                return True
        return False

    def store_row(self, rtrow, h5row, l1, l2, l3, l4):
        h5row["evt"] = rtrow.evt
        h5row["lumi"] = rtrow.lumi
        h5row["run"] = rtrow.run

        h5row["lep_scale"] = self.lepscaler.scale_factor(rtrow, l1, l2, l3, l4)
        h5row["pu_weight"] = self.pu_weights.weight(rtrow)

        h5row["channel"] = self.channel

        h5row["mass"] = rtrow.Mass
        h5row["z1mass"] = getattr(rtrow, "%s_%s_Mass" % (l1, l2))
        h5row["z2mass"] = getattr(rtrow, "%s_%s_Mass" % (l3, l4))

        for i, l in enumerate([l1, l2, l3, l4]):
            j = i + 1
            h5row["l%iPt" % j] = getattr(rtrow, "%sPt" % l)
            h5row["l%iEta" % j] = getattr(rtrow, "%sEta" % l)
            h5row["l%iPhi" % j] = getattr(rtrow, "%sPhi" % l)
            h5row["l%iChg" % j] = getattr(rtrow, "%sCharge" % l)
            h5row["l%iIso" % j] = getattr(rtrow, "%sRelPFIsoDB" % l)


class ZZAnalyzerEEEE(ZZAnalyzer):

    def __init__(self, sample_location, out_file):
        self.channel = "eeee"
        self.leptons = ["e1", "e2", "e3", "e4"]

        super(ZZAnalyzerEEEE, self).__init__(sample_location, out_file)

    def fiducial(self, rtrow):
        pt_cut = 5.0
        eta_cut = 2.4
        pts = [getattr(rtrow, "%sPt" % l) > pt_cut for l in self.leptons]
        etas = [getattr(rtrow, "%sAbsEta" % l) < eta_cut for l in self.leptons]
        return all(pts) and all(etas)

    def eleID(self, rtrow):
        return lepId.elec_id(rtrow, 1, 2, 3, 4)

    def isolation(self, rtrow):
        iso_type = "RelPFIsoRho"
        isos = [getattr(rtrow, "%s%s" % (l, iso_type)) < 0.4
                for l in self.leptons]
        return all(isos)

    def preselection(self, rtrow):
        cuts = CutSequence()
        cuts.add(self.fiducial)
        cuts.add(self.trigger_threshold)
        cuts.add(self.eleID)
        cuts.add(self.isolation)

        return cuts.evaluate(rtrow)


class ZZAnalyzerMMMM(ZZAnalyzer):

    def __init__(self, sample_location, out_file):
        self.channel = "mmmm"
        self.leptons = ["m1", "m2", "m3", "m4"]

        super(ZZAnalyzerMMMM, self).__init__(sample_location, out_file)

    def fiducial(self, rtrow):
        pt_cut = 5.0
        eta_cut = 2.4
        pts = [getattr(rtrow, "%sPt" % l) > pt_cut for l in self.leptons]
        etas = [getattr(rtrow, "%sAbsEta" % l) < eta_cut for l in self.leptons]
        return all(pts) and all(etas)

    def muID(self, rtrow):
        return lepId.muon_id(rtrow, 1, 2, 3, 4)

    def isolation(self, rtrow):
        iso_type = "RelPFIsoDB"
        isos = [getattr(rtrow, "%s%s" % (l, iso_type)) < 0.2
                for l in self.leptons]
        return all(isos)

    def preselection(self, rtrow):
        cuts = CutSequence()
        cuts.add(self.fiducial)
        cuts.add(self.trigger_threshold)
        cuts.add(self.muID)
        cuts.add(self.isolation)

        return cuts.evaluate(rtrow)


def parse_command_line(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('in_sample', type=str)
    parser.add_argument('out_file', type=str)
    parser.add_argument('channels', type=str, default='all')

    args = parser.parse_args(argv)
    return args


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    args = parse_command_line(argv)

    chan = args.channels

    if chan in ['mmmm', 'all']:
        with ZZAnalyzerMMMM(args.in_sample, args.out_file) as MuAnalyzer:
            MuAnalyzer.analyze()

    if chan in ['eeee', 'all']:
        with ZZAnalyzerEEEE(args.in_sample, args.out_file) as eAnalyzer:
            eAnalyzer.analyze()

    return 0


if __name__ == "__main__":
    status = main()
    sys.exit(status)
