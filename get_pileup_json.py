#!/usr/bin/env python
"""
Generate a JSON file containing PU weighting values

Author: D. Austin Belknap, UW-Madison
"""

import sys
import argparse
import json

ARGV = sys.argv[1:]

# Runs ROOT in batch mode
sys.argv.append('-b')
import ROOT as rt


def compute_pu_weights(data_file_name, mc_file_name):
    data_file = rt.TFile(data_file_name, "READ")
    mc_file = rt.TFile(mc_file_name, "READ")

    data_dist = data_file.Get("pileup")
    mc_dist = mc_file.Get("pileup")

    data_dist.Scale(1.0/data_dist.Integral())
    mc_dist.Scale(1.0/mc_dist.Integral())

    if data_dist.GetNbinsX() != mc_dist.GetNbinsX():
        raise ValueError("Bin numbers do not match")

    out = {}

    for i in xrange(1, data_dist.GetNbinsX()+1):
        if mc_dist[i] == 0:
            out[i-1] = 1.0
        else:
            out[i-1] = data_dist[i] / mc_dist[i]

    data_file.Close()
    mc_file.Close()

    return out


def parse_command_line(argv):
    parser = argparse.ArgumentParser(description='Create a JSON w/ PU weights')
    parser.add_argument('outfile', type=str,
                        help='Output JSON file')
    parser.add_argument('data', type=str,
                        help='ROOT file containing PU computed from data.')
    parser.add_argument('MC', type=str,
                        help='ROOT file containing PU computed from MC')
    args = parser.parse_args(argv)

    return args
    


def main(argv=None):
    if argv is None:
        argv = ARGV

    args = parse_command_line(argv)

    pu_dict = compute_pu_weights(args.data, args.MC)

    with open(args.outfile, 'w') as outfile:
        outfile.write(json.dumps(pu_dict, indent=4, sort_keys=True))

    return 0


if __name__ == "__main__":
    status = main()
    sys.exit(status)
