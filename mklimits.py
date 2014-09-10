from limits import Limits
import logging
import sys

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

_4L_MASSES = [110, 130, 150, 170, 200, 250, 300,
              350, 400, 450, 500, 600, 700]

def four_l(mass):
    logger.info("Processing mass-point %i" % mass)

    cuts = '(%f < h1mass) & (h1mass < %f)' % (0.9*mass, 1.1*mass)
    cuts += '& (%f < sT)' % (0.6*mass + 130.0)
    cuts += '& (channel == "mmmm")'

    limits = Limits("DblH", cuts, "./ntuples", "./datacards/4l",
            channels=["dblh4l"], lumi=19.7, blinded=True)

    limits.add_group("hpp%i" % mass, "HPlus*%i*" % mass, isSignal=True)
    limits.add_group("dyjets", "DYJets*")
    limits.add_group("zz", "ZZTo*")
    limits.add_group("top", "T*")
    limits.add_group("data", "data_*", isData=True)

    lumi = {'hpp%i' % mass: 0.026,
            'dyjets':       0.026,
            'zz':           0.026,
            'top':          0.026}
    limits.add_systematics("lumi", "lnN", **lumi)

    mu_eff = {'hpp%i' % mass: 0.043,
              'dyjets':       0.043,
              'zz':           0.043,
              'top':          0.043}
    limits.add_systematics("mu_eff", "lnN", **mu_eff)

    limits.gen_card("%i.txt" % mass)


def main():

    for mass in _4L_MASSES:
        four_l(mass)


if __name__ == "__main__":
    main()
