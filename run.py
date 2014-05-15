#!/usr/bin/env python
"""
This is a run script for running the H++/H-- analysis on FSA n-tuples.

Author: D. Austin Belknap, UW-Madison
"""

import os
import sys
import glob
import argparse

from analyzers import analyzeZZ as anZZ
from analyzers import Analyzer4l
from analyzers import Control4l
from analyzers import TTControl4l


def run_ntuples(analyzer_type, samples):
    root_dir = './root_files'
    ntup_dir = './ntuples'

    sample_names = [os.path.basename(fname)
                    for string in samples
                    for fname in glob.glob("%s/%s" % (root_dir, string))]

    if analyzer_type == "4l":
        for name in sample_names:
            print "Processing %s" % name
            with Analyzer4l("%s/%s" % (root_dir, name),
                            "%s/%s.h5" % (ntup_dir, name)) as analyzer:
                analyzer.analyze()

    elif analyzer_type == "ctrl":
        for name in sample_names:
            print "Processing %s" % name
            with Control4l("%s/%s" % (root_dir, name),
                           "%s/%s.h5" % (ntup_dir, name)) as analyzer:
                analyzer.analyze()

    elif analyzer_type == "tt":
        for name in sample_names:
            print "Processing %s" % name
            with TTControl4l("%s/%s" % (root_dir, name),
                           "%s/%s.h5" % (ntup_dir, name)) as analyzer:
                analyzer.analyze()

    elif analyzer_type == "zz":
        for name in sample_names:
            print "processing %s" % name
            with anZZ.ZZAnalyzer4l("%s/%s" % (root_dir, name),
                                     "%s/%s.h5" % (ntup_dir, name)) as Anlyzr:
                Anlyzr.analyze()

    else:
        raise ValueError("%s is invalid option" % analyzer_type)

    return 0



def parse_command_line(argv):
    parser = argparse.ArgumentParser(description="Run the desired analyzer on "
                                                 "FSA n-tuples")

    parser.add_argument('analyzer', type=str, help='4l, ctrl, or zz')
    parser.add_argument('sample_names', nargs='+',
                        help='Sample names w/ UNIX wildcards')
    args = parser.parse_args(argv)

    return args


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    args = parse_command_line(argv)

    run_ntuples(args.analyzer, args.sample_names)

    return 0


if __name__ == "__main__":
    status = main()
    sys.exit(status)
