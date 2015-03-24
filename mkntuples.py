#!/usr/bin/env python
"""
This is a run script for running the H++/H-- analysis on FSA n-tuples.

Author: D. Austin Belknap, UW-Madison
"""

import os
import sys
import glob
import argparse

from multiprocessing import Pool

from analyzers import analyzeZZ as anZZ
from analyzers import Analyzer4l
from analyzers import Control4l
from analyzers import TTControl4l
from analyzers import ZControl4l

def run_qcd_ctrl_4l(args):
    location, outfile = args
    print "Processing %s" % location
    with Control4l(location, outfile) as analyzer:
        analyzer.analyze()


def run_z_ctrl_4l(args):
    location, outfile = args
    print "Processing %s" % location
    with ZControl4l(location, outfile) as analyzer:
        analyzer.analyze()


def run_tt_ctrl_4l(args):
    location, outfile = args
    print "Processing %s" % location
    with TTControl4l(location, outfile) as analyzer:
        analyzer.analyze()


def run_4l(args):
    location, outfile = args
    print "Processing %s" % location
    with Analyzer4l(location, outfile) as analyzer:
        analyzer.analyze()


def run_zz_4l(args):
    location, outfile = args
    print "processing %s" % location
    with anZZ.ZZAnalyzer4l(location, outfile) as Anlyzr:
        Anlyzr.analyze()



def run_ntuples(analyzer_type, samples, njobs=1):

    root_dir = './root_files'
    ntup_dir = './ntuples'

    p = Pool(njobs)

    sample_names = [os.path.basename(fname)
                    for string in samples
                    for fname in glob.glob("%s/%s" % (root_dir, string))]

    if analyzer_type == "4l":
        p.map(run_4l, [("%s/%s" % (root_dir, name), "%s/%s.h5" % (ntup_dir, name)) for name in sample_names])

    elif analyzer_type == "ctrl":
        p.map(run_qcd_ctrl_4l, [("%s/%s" % (root_dir, name), "%s/%s.h5" % (ntup_dir, name)) for name in sample_names])

    elif analyzer_type == "tt":
        p.map(run_tt_ctrl_4l, [("%s/%s" % (root_dir, name), "%s/%s.h5" % (ntup_dir, name)) for name in sample_names])

    elif analyzer_type == "z":
        p.map(run_z_ctrl_4l, [("%s/%s" % (root_dir, name), "%s/%s.h5" % (ntup_dir, name)) for name in sample_names])

    elif analyzer_type == "zz":
        p.map(run_zz_4l, [("%s/%s" % (root_dir, name), "%s/%s.h5" % (ntup_dir, name)) for name in sample_names])
        #for name in sample_names:
        #    print "processing %s" % name
        #    with anZZ.ZZAnalyzer4l("%s/%s" % (root_dir, name),
        #                             "%s/%s.h5" % (ntup_dir, name)) as Anlyzr:
        #        Anlyzr.analyze()

    else:
        raise ValueError("%s is invalid option" % analyzer_type)

    return 0



def parse_command_line(argv):
    parser = argparse.ArgumentParser(description="Run the desired analyzer on "
                                                 "FSA n-tuples")

    parser.add_argument('analyzer', type=str, help='4l, ctrl, or zz')
    parser.add_argument('sample_names', nargs='+',
                        help='Sample names w/ UNIX wildcards')
    parser.add_argument('-n', '--n-jobs', type=int, default=1,
                        help='Number of instances to run at one time. '
                             'Default is 1.')

    args = parser.parse_args(argv)

    return args


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    args = parse_command_line(argv)

    run_ntuples(args.analyzer, args.sample_names, njobs=args.n_jobs)

    return 0


if __name__ == "__main__":
    status = main()
    sys.exit(status)
