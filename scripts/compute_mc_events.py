import os
import sys
import argparse
import json
import glob
import logging

sys.argv.append('-b')
import ROOT as rt
sys.argv.pop()


def count_events(rtfile_name):
    rtfile = rt.TFile(rtfile_name, "READ")

    tree = rtfile.Get("mmmm/metaInfo")

    if not tree:
        raise SystemExit(1)

    total_events = 0

    for entry in xrange(tree.GetEntries()):
        tree.GetEntry(entry)
        total_events += tree.nevents

    rtfile.Close()

    return total_events


def sample_counts(sample_location):
    filenames = os.listdir(sample_location)

    counts = 0
    for f in filenames:
        counts += count_events("%s/%s" % (sample_location, f))

    return counts


def main(argv=None):
    filename = './plotters/mc_events.json'

    try:
        with open(filename, 'r') as infile:
            out = json.load(infile)
    except IOError:
        out = {}

    log = logging.getLogger(__name__)

    logging.basicConfig(level=logging.INFO)

    root_dir = "./root_files"

    sample_names = [os.path.basename(fname)
                    for string in sys.argv[1:]
                    for fname in glob.glob("%s/%s" % (root_dir, string))]

    for name in sample_names:
        out[name] = sample_counts("%s/%s" % (root_dir, name))
        log.info("Processing %s: %i" % (name, out[name]))

    with open('./plotters/mc_events.json', 'w') as outfile:
        outfile.write(json.dumps(out, indent=4, sort_keys=True))


if __name__ == "__main__":
    main()
