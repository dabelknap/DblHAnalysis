from limits import Limits
import sys

def four_l():
    limits = Limits("DblH", "(mass > 0)", "./ntuples", "./datacards/4l",
            channels=["dblh4l"], lumi=19.7, blinded=True)

    limits.add_group("hpp450", "HPlus*450*", isSignal=True)
    limits.add_group("dyjets", "DYJets*")
    limits.add_group("zz", "ZZTo*")
    limits.add_group("top", "T*")
    limits.add_group("data", "data_*", isData=True)

    lumi = {'hpp450': 0.026,
            'dyjets': 0.026,
            'zz':     0.026,
            'top':    0.026}

    limits.add_systematics("lumi", "lnN", **lumi)

    limits.gen_card("test.txt")


def main():
     four_l()


if __name__ == "__main__":
    main()
