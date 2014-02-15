import tables as tb
import numpy as np
import os
import sys
import glob
from itertools import permutations

from ntuple_defs import EventZZ

sys.argv.append('-b')
import ROOT as rt
sys.argv.pop()



def preselection(row):
    passed = True

    passed = passed and row.doubleMuPass == 1

    for i in xrange(1,5):
        passed = passed and getattr(row, "m%iPFIDTight" % i) > 0.0
        passed = passed and getattr(row, "m%iPt" % i) > 5.0
        passed = passed and getattr(row, "m%iAbsEta" % i) < 2.4
        passed = passed and getattr(row, "m%iRelPFIsoDB" % i) < 0.2

    pts = sorted([getattr(row, 'm%iPt' % i) for i in xrange(1,5)], reverse=True)
    passed = passed and pts[0] > 20.0 and pts[1] > 10.0

    return passed


def store_row(rtrow, h5row, l1, l2, l3, l4):
    h5row["evt"] = rtrow.evt
    h5row["lumi"] = rtrow.lumi
    h5row["run"] = rtrow.run

    h5row["weight"] = 1.0

    h5row["channel"] = "mmmm"

    h5row["mass"] = rtrow.Mass
    h5row["z1mass"] = getattr(rtrow, "m%i_m%i_Mass" % (l1, l2))
    h5row["z2mass"] = getattr(rtrow, "m%i_m%i_Mass" % (l3, l4))



def choose_leptons(row):
    cands = []
    for l in permutations([1,2,3,4]):
        if l[0] > l[1] or l[2] > l[3]:
            continue

        z1mass = getattr(row, "m%i_m%i_Mass" % (l[0], l[1]))
        z2Pt   = getattr(row, "m%iPt" % l[2]) + getattr(row, "m%iPt" % l[3])
        SS1    = getattr(row, "m%i_m%i_SS" % (l[0], l[1])) > 0.5
        SS2    = getattr(row, "m%i_m%i_SS" % (l[2], l[3])) > 0.5

        if not SS1 and not SS2:
            cands.append((z1mass, z2Pt, list(l)))

    # Sort by Z2 scalar pT sum
    cands.sort(key=lambda x: x[1], reverse=True)
    # Sort by Z1 mass closest to nominal
    cands.sort(key=lambda x: abs(x[0] - 91.2))

    z1mass, z2Pt, leps = cands[0]

    return (z1mass, z2Pt, leps)


def good_to_store(cand1, cand2):
    """Is cand1 better than cand2?"""
    if abs(cand1[0] - 91.2) < abs(cand2[0] - 91.2):
        if cand1[1] > cand2[1]:
            return True
    return False


def main(sample):
    sample_name_list = glob.glob("./root_files/" + sample)
    for name in sample_name_list:
        print "Processing: ", name
        sample_name = os.path.basename(name)
        file_names = os.listdir(os.path.join('root_files', sample_name))

        h5file = tb.open_file('./ntuples/' + sample_name + '.h5', mode='w')
        zz_group = h5file.create_group('/', 'ZZ4l', 'ZZ to 4l')
        mmmm_table = h5file.create_table(zz_group, 'mmmm', EventZZ, "Selected 4mu Events")

        mmmm_row = mmmm_table.row

        event_set = None
        for i, file_name in enumerate(file_names):
            if i % 20 == 0:
                print "Processing %i/%i Files" % (i+1, len(file_names))
            file_path = os.path.join('root_files', sample_name, file_name)
            rtFile = rt.TFile(file_path, "READ")
            tree = rtFile.Get("mmmm/final/Ntuple")

            for row in tree:
                if event_set:
                    # Once we move to the next event, capture the info from the previous event
                    if row.evt not in event_set:
                        mmmm_row.append()
                        best_cand = (0, 0, [1,2,3,4])
                else:
                    best_cand = (0, 0, [1,2,3,4])
                    event_set = set()

                if not preselection(row):
                    continue

                event_set.add(row.evt)

                candidate = choose_leptons(row)

                if good_to_store(candidate, best_cand):
                    store_row(row, mmmm_row, *candidate[2])
                    best_cand = tuple(candidate)

            mmmm_row.append()
            mmmm_table.flush()
            rtFile.Close()

        h5file.close()


if __name__ == "__main__":
    main(sys.argv[1])
