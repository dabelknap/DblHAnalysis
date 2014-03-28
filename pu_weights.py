import sys
import json

sys.argv.append('-b')
import ROOT as rt
sys.pop()


class PileupWeights(object):

    def __init__(self):
        with open('./pile_up/pu_weights.json', 'r') as pu_file:
            self.pu_weights = json.load(pu_file)


    def weight(rtrow):
        if row.nTruePU < 0:
            return 1
        else:
            return self.pu_weights[str(int(floor(row.nTruePU)))]
