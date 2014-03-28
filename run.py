import analyze4l as an
import analyzeZZ as zzan
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
            with an.analyzer4lmmmm("%s/%s" % (root_dir, name), "%s/%s.h5" % (ntup_dir, name)) as muanalyzer:
                print "4mu analyzer"
                muanalyzer.analyze()

            with an.analyzer4leeee("%s/%s" % (root_dir, name), "%s/%s.h5" % (ntup_dir, name)) as eleanalyzer:
                print "4ele analyzer"
                eleanalyzer.analyze()

    elif sys.argv[1] == "zz":
        for name in sample_names:
            print "processing %s" % name
            with zzan.ZZAnalyzerMMMM("%s/%s" % (root_dir, name), "%s/%s.h5" % (ntup_dir, name)) as muanalyzer:
                print "4mu analyzer"
                muanalyzer.analyze()

            with zzan.ZZAnalyzerEEEE("%s/%s" % (root_dir, name), "%s/%s.h5" % (ntup_dir, name)) as eleanalyzer:
                print "4ele analyzer"
                eleanalyzer.analyze()

    else:
        raise ValueError("%s is invalid option" % sys.argv[1])

    return 0


if __name__ == "__main__":
    main()
