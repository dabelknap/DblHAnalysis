import tables as tb
import numpy as np
import os
import sys
from itertools import permutations, combinations
import argparse

from ntuple_defs import Event4l
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


class Analyzer(object):

    def __init__(self, sample_location, outfile):
        self.sample_name = os.path.basename(sample_location)
        self.filenames = os.listdir(sample_location)
        self.outfile = outfile
        self.sample_location = sample_location

    def __enter__(self):
        self.begin()
        return self

    def __exit__(self, type, value, traceback):
        self.finish()

    def begin(self):
        self.lepscaler = LeptonScaleFactors()
        self.pu_weights = PileupWeights()

        self.h5file = tb.open_file(self.outfile, mode='a')

        try:
            self.h5file.removeNode('/DblH/%s' % self.channel)
        except tb.NodeError:
            pass

        try:
            self.group = self.h5file.create_group('/', 'DblH', 'Doubly-Charged Higgs Analysis')
        except tb.NodeError:
            self.group = self.h5file.root.DblH

        self.table = self.h5file.create_table(
                self.group, self.channel,
                Event4l, "Selected %s Events" % self.channel)

        self.h5row = self.table.row

    def finish(self):
        self.lepscaler.close()
        self.h5file.close()

    def analyze(self):
        event_set = None

        for i, filename in enumerate(self.filenames):
            if len(self.filenames) > 20:
                if i % (len(self.filenames)/20) == 0:
                    print "Processing %i/%i files" % (i+1, len(self.filenames))
            else:
                print "Processing %i/%i files" % (i+1, len(self.filenames))

            file_path = os.path.join(self.sample_location, filename)
            rtFile = rt.TFile(file_path, "READ")

            for fs in self.final_states:
                tree = rtFile.Get("%s/final/Ntuple" % fs)

                self.leptons = self.enumerate_leps(fs)

                for rtrow in tree:

                    if event_set:
                        if (rtrow.evt, rtrow.lumi, rtrow.run) not in event_set and best_cand[0]:
                            self.h5row.append()
                            best_cand = (0, float('inf'), [])
                    else:
                        best_cand = (0, float('inf'), [])
                        event_set = set()

                    if not self.preselection(rtrow):
                        continue

                    event_set.add((rtrow.evt, rtrow.lumi, rtrow.run))

                    candidate = self.choose_leptons(rtrow)

                    if self.good_to_store(candidate, best_cand):
                        self.store_row(rtrow, self.h5row, *candidate[2])
                        best_cand = tuple(candidate)

                if best_cand[0]:
                    self.h5row.append()

            self.table.flush()
            rtFile.Close()

    def choose_leptons(self, rtrow):

        def lep_order(a, b):
            a_index = int(a[1])
            b_index = int(b[1])
            return a_index > b_index or a[0] > b[0]

        cands = [(0, float('inf'), [])]
        for l in permutations(self.leptons):
            if lep_order(l[0], l[1]) or lep_order(l[2], l[3]):
                continue

            mh1 = getattr(rtrow, "%s_%s_Mass" % (l[0], l[1]))
            mh2 = getattr(rtrow, "%s_%s_Mass" % (l[2], l[3]))

            C1 = getattr(rtrow, "%sCharge" % l[0])
            C2 = getattr(rtrow, "%sCharge" % l[2])

            SS1 = getattr(rtrow, "%s_%s_SS" % (l[0], l[1])) > 0.5
            SS2 = getattr(rtrow, "%s_%s_SS" % (l[2], l[3])) > 0.5

            if SS1 and SS2 and C1 > 0 and C2 < 0:
                cands.append((mh1, mh2, list(l)))

        cands.sort(key=lambda x: abs(x[0] - x[1]))

        mh1, mh2, leps = cands[0]

        return (mh1, mh2, leps)

    @staticmethod
    def enumerate_leps(final_state):
        out = []
        for i in ['e', 'm', 't']:
            N = final_state.count(i)
            out += ['%s%i' % (i, n) for n in xrange(1,N+1)]
        return out

    @staticmethod
    def good_to_store(cand1, cand2):
        return abs(cand1[0] - cand1[1]) < abs(cand2[0] - cand2[1])

    def store_row(self, rtrow, h5row, l1, l2, l3, l4):
        h5row["evt"] = rtrow.evt
        h5row["lumi"] = rtrow.lumi
        h5row["run"] = rtrow.run

        h5row["lep_scale"] = self.lepscaler.scale_factor(rtrow, l1, l2, l3, l4)
        h5row["pu_weight"] = self.pu_weights.weight(rtrow)

        h5row["channel"] = "%s%s%s%s" % (l1[0], l2[0], l3[0], l4[0])

        h5row["mass"] = rtrow.Mass

        h5row["h1mass"] = getattr(rtrow, "%s_%s_Mass" % (l1, l2))
        h5row["h2mass"] = getattr(rtrow, "%s_%s_Mass" % (l3, l4))

        h5row["sT1"] = getattr(rtrow, "%sPt" % l1) + getattr(rtrow, "%sPt" % l2)
        h5row["sT2"] = getattr(rtrow, "%sPt" % l3) + getattr(rtrow, "%sPt" % l4)

        h5row["dPhi1"] = getattr(rtrow, "%s_%s_DPhi" % (l1, l2))
        h5row["dPhi2"] = getattr(rtrow, "%s_%s_DPhi" % (l3, l4))

        for i, l in enumerate([l1, l2, l3, l4]):
            j = i + 1
            h5row["l%iPt" % j] = getattr(rtrow, "%sPt" % l)
            h5row["l%iEta" % j] = getattr(rtrow, "%sEta" % l)
            h5row["l%iPhi" % j] = getattr(rtrow, "%sPhi" % l)
            h5row["l%iChg" % j] = getattr(rtrow, "%sCharge" % l)
            h5row["l%sFlv" % j] = l[0]
            if l[0] == 'm':
                h5row["l%sIso" % j] = getattr(rtrow, "%sRelPFIsoDB" % l)
            elif l[0] == 'e':
                h5row["l%sIso" % j] = getattr(rtrow, "%sRelPFIsoRho" % l)


class Analyzer4l(Analyzer):

    def __init__(self, sample_location, outfile):
        self.channel = "dblh4l"
        self.final_states = ["mmmm", "eeee", "eemm"]
        super(Analyzer4l, self).__init__(sample_location, outfile)

    def fiducial(self, rtrow):
        e_pt_cut = 15.0
        e_eta_cut = 2.5

        m_pt_cut = 5.0
        m_eta_cut = 2.4

        e_pts = [getattr(rtrow, "%sPt" % l) > e_pt_cut
                 for l in self.leptons if l[0] == 'e']
        e_eta = [getattr(rtrow, "%sAbsEta" % l) < e_eta_cut
                for l in self.leptons if l[0] == 'e']

        m_pts = [getattr(rtrow, "%sPt" % l) > m_pt_cut
                 for l in self.leptons if l[0] == 'm']
        m_eta = [getattr(rtrow, "%sAbsEta" % l) < m_eta_cut
                for l in self.leptons if l[0] == 'm']

        return all(e_pts) and all(m_pts) and all(e_eta) and all(m_eta)

    def ID(self, rtrow):
        return lepId.lep_id(rtrow, *self.leptons)

    def isolation(self, rtrow):
        e_iso_type = "RelPFIsoRho"
        m_iso_type = "RelPFIsoDB"
        e_isos = [getattr(rtrow, "%s%s" % (l, e_iso_type)) < 0.4
                  for l in self.leptons if l[0] == 'e']
        m_isos = [getattr(rtrow, "%s%s" % (l, m_iso_type)) < 0.4
                  for l in self.leptons if l[0] == 'm']

        return all(e_isos + m_isos)

    def trigger_threshold(self, rtrow):
        pts = [getattr(rtrow, "%sPt" % l) for l in self.leptons]
        pts.sort(reverse=True)
        return pts[0] > 20.0 and pts[1] > 10.0

    def qcd_rejection(self, rtrow):
        qcd_pass = [getattr(rtrow, "%s_%s_Mass" % (l[0], l[1])) > 12.0
                    for l in combinations(self.leptons, 2)]
        return all(qcd_pass)

    def preselection(self, rtrow):
        cuts = CutSequence()
        cuts.add(self.fiducial)
        cuts.add(self.ID)
        cuts.add(self.trigger_threshold)
        cuts.add(self.qcd_rejection)
        cuts.add(self.isolation)

        return cuts.evaluate(rtrow)


class Control4l(Analyzer4l):

    def __init__(self, sample_location, outfile):
        self.channel = "dblh4l_control"
        self.final_states = ["mmmm", "eeee", "eemm"]
        super(Control4l, self).__init__(sample_location, outfile)

    def ID(self, rtrow):
        return lepId.lep_id(rtrow, *self.leptons, control=True)

    def isolation(self, rtrow):
        e_iso_type = "RelPFIsoRho"
        m_iso_type = "RelPFIsoDB"
        e_isos = [getattr(rtrow, "%s%s" % (l, e_iso_type)) > 0.4
                  for l in self.leptons if l[0] == 'e']
        m_isos = [getattr(rtrow, "%s%s" % (l, m_iso_type)) > 0.4
                  for l in self.leptons if l[0] == 'm']

        return all(e_isos + m_isos)



def main():
    with Control4l("./root_files/HPlusPlusHMinusMinusHTo4L_M-450_8TeV-pythia6",
                    "test.h5") as analyzer4l:
        analyzer4l.analyze()

    return 0


if __name__ == "__main__":
    main()
