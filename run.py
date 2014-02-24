import analyze4l as an
import glob
import os
import sys

def main():
    root_dir = './root_files'
    ntup_dir = './ntuples'

    sample_names = [os.path.basename(fname)
                    for string in sys.argv[1:]
                    for fname in glob.glob("%s/%s" % (root_dir, string))]

    for name in sample_names:
        print "Processing %s" % name
        with an.Analyzer4lMMMM("%s/%s" % (root_dir, name), "%s/%s.h5" % (ntup_dir, name)) as MuAnalyzer:
            print "4Mu Analyzer"
            MuAnalyzer.analyze()

        with an.Analyzer4lEEEE("%s/%s" % (root_dir, name), "%s/%s.h5" % (ntup_dir, name)) as EleAnalyzer:
            print "4Ele Analyzer"
            EleAnalyzer.analyze()

    return 0


if __name__ == "__main__":
    main()
