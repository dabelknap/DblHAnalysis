from analyzers import analyze4l as an4l
from analyzers import analyzeZZ as anZZ
import glob
import os
import sys

def main():
    root_dir = './root_files'
    ntup_dir = './ntuples'

    sample_names = [os.path.basename(fname)
                    for string in sys.argv[2:]
                    for fname in glob.glob("%s/%s" % (root_dir, string))]

    if sys.argv[1] == "4l":
        for name in sample_names:
            print "processing %s" % name
            with an4l.Analyzer4lMMMM("%s/%s" % (root_dir, name), "%s/%s.h5" % (ntup_dir, name)) as muanalyzer:
                print "4mu analyzer"
                muanalyzer.analyze()

            with an4l.Analyzer4lEEEE("%s/%s" % (root_dir, name), "%s/%s.h5" % (ntup_dir, name)) as eleanalyzer:
                print "4ele analyzer"
                eleanalyzer.analyze()

    elif sys.argv[1] == "zz":
        for name in sample_names:
            print "processing %s" % name
            with anZZ.ZZAnalyzerMMMM("%s/%s" % (root_dir, name), "%s/%s.h5" % (ntup_dir, name)) as muanalyzer:
                print "4mu analyzer"
                muanalyzer.analyze()

            with anZZ.ZZAnalyzerEEEE("%s/%s" % (root_dir, name), "%s/%s.h5" % (ntup_dir, name)) as eleanalyzer:
                print "4ele analyzer"
                eleanalyzer.analyze()

    elif sys.argv[1] == "ctrl":
        for name in sample_names:
            print "processing %s" % name
            with an4l.AnalyzerControlMMMM("%s/%s" % (root_dir, name), "%s/%s.h5" % (ntup_dir, name)) as muanalyzer:
                print "4mu control analyzer"
                muanalyzer.analyze()

    else:
        raise ValueError("%s is invalid option" % sys.argv[1])

    return 0


if __name__ == "__main__":
    main()
