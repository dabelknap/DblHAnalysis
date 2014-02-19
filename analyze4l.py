import tables as tb
import numpy as np
import os
import sys
from itertools import permutations, combinations
import argparse

from ntuple_defs import Event4l

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




class Analyzer4l(object):

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
        self.h5file = tb.open_file(self.out_file, mode='a')

        try:
            self.h5file.removeNode('/DblH4l/%s' % self.channel)
        except tb.NodeError:
            pass

        try:
            self.group = self.h5file.create_group('/', 'DblH4l', 'DblH to 4l')
        except tb.NodeError:
            self.group = self.h5file.root.DblH4l

        self.table = self.h5file.create_table(
                self.group, self.channel,
                Event4l, "Selected %s Events" % self.channel)

        self.h5row = self.table.row


    def analyze(self):
        event_set = None

        for i, file_name in enumerate(self.file_names):
            if i % 20 == 0:
                print "  Processing %i/%i files" % (i+1, len(self.file_names))
            file_path = os.path.join(self.sample_location, file_name)
            rtFile = rt.TFile(file_path, "READ")
            tree = rtFile.Get("%s/final/Ntuple" % self.channel)

            cnt = 0
            for rtrow in tree:
                cnt += 1
                print "Row: %i" % cnt
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

                if cnt == 10:
                    break

            self.h5row.append()
            self.table.flush()
            rtFile.Close()


    def finish(self):
        self.h5file.close()


    def trigger_threshold(self, rtrow):
        pts = [getattr(rtrow, "%sPt" % l) for l in self.leptons]
        pts.sort(reverse=True)
        return pts[0] > 20.0 and pts[1] > 10.0


    def qcd_rejection(self, rtrow):
        qcd_pass = [getattr(rtrow, "%s_%s_Mass" % (l[0], l[1])) > 12.0
                    for l in combinations(self.leptons, 2)]
        return all(qcd_pass)


    @staticmethod
    def good_to_store(cand1, cand2):
        """Are cand1 masses closer together than cand2?"""
        return abs(cand1[0] - cand1[1]) < abs(cand2[0] - cand2[1])


    def choose_leptons(self, rtrow):
        """
        The leptons should already be ordered the way we wish from
        the n-tuple. Can be overridden for more complicated final states.
        """
        l1, l2, l3, l4 = self.leptons
        mh1 = getattr(rtrow, "%s_%s_Mass" % (l1, l2))
        mh2 = getattr(rtrow, "%s_%s_Mass" % (l3, l4))
        return (mh1, mh2, list(self.leptons))


    def store_row(self, rtrow, h5row, l1, l2, l3, l4):
        h5row["evt"] = rtrow.evt
        h5row["lumi"] = rtrow.lumi
        h5row["run"] = rtrow.run

        h5row["weight"] = 1.0

        h5row["channel"] = self.channel

        h5row["mass"] = rtrow.Mass
        h5row["h1mass"] = getattr(rtrow, "%s_%s_Mass" % (l1, l2))
        h5row["h2mass"] = getattr(rtrow, "%s_%s_Mass" % (l3, l4))

        for i, l in enumerate([l1, l2, l3, l4]):
            j = i + 1
            h5row["l%iPt" % j] = getattr(rtrow, "%sPt" % l)
            h5row["l%iEta" % j] = getattr(rtrow, "%sEta" % l)
            h5row["l%iPhi" % j] = getattr(rtrow, "%sPhi" % l)
            h5row["l%iChg" % j] = getattr(rtrow, "%sCharge" % l)
            h5row["l%sFlv" % j] = l[0]
            h5row["l%sIso" % j] = getattr(rtrow, "%sRelPFIsoDB")



class Analyzer4lEEEE(Analyzer4l):

    def __init__(self, sample_location, out_file):
        self.channel = "eeee"
        self.leptons = ["e1", "e2", "e3", "e4"]

        super(Analyzer4lEEEE, self).__init__(sample_location, out_file)


    def fiducial(self, rtrow):
        pt_cut = 15.0
        eta_cut = 2.5
        pts = [getattr(rtrow, "%sPt" % l) > pt_cut for l in self.leptons]
        etas = [getattr(rtrow, "%sAbsEta" % l) < eta_cut for l in self.leptons]
        return all(pts) and all(etas)


    def eleID(self, rtrow):
        ids = [getattr(rtrow, "%sMVAIDH2TauWP" % l) > 0.5 for l in self.leptons]
        return all(ids)


    def isolation(self, rtrow):
        iso_type = "RelPFIsoDB"
        isos = sorted([getattr(rtrow, "%s%s" % (l, iso_type)) for l in self.leptons], reverse=True)
        return (isos[0] + isos[1]) < 0.35


    def preselection(self, rtrow):
        cuts = CutSequence()
        cuts.add(self.fiducial)
        cuts.add(self.eleID)
        cuts.add(self.trigger_threshold)
        cuts.add(self.qcd_rejection)
        cuts.add(self.isolation)

        return cuts.evaluate(rtrow)




class Analyzer4lMMMM(Analyzer4l):

    def __init__(self, sample_location, out_file):
        self.channel = "mmmm"
        self.leptons = ["m1", "m2", "m3", "m4"]

        super(Analyzer4lMMMM, self).__init__(sample_location, out_file)


    def fiducial(self, rtrow):
        pt_cut = 5.0
        eta_cut = 2.4
        pts = [getattr(rtrow, "%sPt" % l) > pt_cut for l in self.leptons]
        etas = [getattr(rtrow, "%sAbsEta" % l) < eta_cut for l in self.leptons]
        return all(pts) and all(etas)


    def muID(self, rtrow):
        ids = [getattr(rtrow, "%sPFIDTight" % l) > 0.5 for l in self.leptons]
        return all(ids)


    def isolation(self, rtrow):
        iso_type = "RelPFIsoDB"
        isos = sorted([getattr(rtrow, "%s%s" % (l, iso_type)) for l in self.leptons], reverse=True)
        return (isos[0] + isos[1]) < 0.35


    def preselection(self, rtrow):
        cuts = CutSequence()
        cuts.add(self.fiducial)
        cuts.add(self.muID)
        cuts.add(self.trigger_threshold)
        cuts.add(self.qcd_rejection)
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
        with Analyzer4lMMMM(args.in_sample, args.out_file) as MuAnalyzer:
            MuAnalyzer.analyze()

    if chan in ['eeee', 'all']:
        with Analyzer4lEEEE(args.in_sample, args.out_file) as eAnalyzer:
            eAnalyzer.analyze()

    return 0



if __name__ == "__main__":
    status = main()
    sys.exit(status)
