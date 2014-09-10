from limits import Limits
import logging
import sys

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

_4L_MASSES = [110, 130, 150, 170, 200, 250, 300,
              350, 400, 450, 500, 600, 700]

def four_l(mass):
    logger.info("Process mass-point %i" % mass)

    limits = Limits("DblH", "(mass > 0)", "./ntuples", "./datacards/4l",
            channels=["dblh4l"], lumi=19.7, blinded=True)

    limits.add_group("hpp%i" % mass, "HPlus*%i*" % mass, isSignal=True)
    limits.add_group("dyjets", "DYJets*")
    limits.add_group("zz", "ZZTo*")
    limits.add_group("top", "T*")
    limits.add_group("data", "data_*", isData=True)

    lumi = {'hpp450': 0.026,
            'dyjets': 0.026,
            'zz':     0.026,
            'top':    0.026}

    limits.add_systematics("lumi", "lnN", **lumi)

    limits.gen_card("%i.txt" % mass)


def main():

    for mass in _4L_MASSES:
        four_l(mass)


if __name__ == "__main__":
    main()
