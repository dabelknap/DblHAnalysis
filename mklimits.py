from limits import Limits
from plotters.limits import plot_limits
import logging
import sys

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

_4L_MASSES = [110, 130, 150, 170, 200, 250, 300,
              350, 400, 450, 500, 600, 700]

_3L_MASSES = [170, 200, 250, 300, 350, 400, 450,
              500, 600, 700]

def mmmm_100(mass):
    logger.info("Processing mass-point %i" % mass)

    cuts = '(%f < h1mass) & (h1mass < %f)' % (0.9*mass, 1.1*mass)
    cuts += '& (%f < sT)' % (0.6*mass + 130.0)
    cuts += '& (channel == "mmmm")'

    limits = Limits("DblH", cuts, "./ntuples", "./datacards/mmmm100/%i" % mass,
            channels=["dblh4l"], lumi=19.7, blinded=True)

    limits.add_group("hpp%i" % mass, "HPlus*%i*" % mass, isSignal=True, scale=36.0)
    limits.add_group("dyjets", "DYJets*")
    limits.add_group("zz", "ZZTo*")
    limits.add_group("top", "T*")
    limits.add_group("data", "data_*", isData=True)

    lumi = {'hpp%i' % mass: 1.026,
            'dyjets':       1.026,
            'zz':           1.026,
            'top':          1.026}
    limits.add_systematics("lumi", "lnN", **lumi)

    mu_eff = {'hpp%i' % mass: 1.043,
              'dyjets':       1.043,
              'zz':           1.043,
              'top':          1.043}
    limits.add_systematics("mu_eff", "lnN", **mu_eff)

    limits.gen_card("mmmm.txt")


def fourl(mass):
    logger.info("Processing mass-point %i" % mass)

    cuts = '(%f < h1mass) & (h1mass < %f)' % (0.9*mass, 1.1*mass)
    cuts += '& (%f < sT)' % (0.6*mass + 130.0)
    cuts += ('& ((channel == "mmmm") | (channel == "eeee") | (channel == "eemm") |'
             '(channel == "mmee") | (channel == "meme") | (channel == "emem") |'
             '(channel == "emme") | (channel == "meem") |'
             '(channel == "eeem") | (channel == "eeme") | (channel == "emee") | (channel == "meee") |'
             '(channel == "emmm") | (channel == "memm") | (channel == "mmem") | (channel == "mmme"))')

    limits = Limits("DblH", cuts, "./ntuples", "./datacards/light_lep_all/%i" % mass,
            channels=["dblh4l"], lumi=19.7, blinded=True)

    limits.add_group("hpp%i" % mass, "HPlus*%i*" % mass, isSignal=True)
    limits.add_group("dyjets", "DYJets*")
    limits.add_group("zz", "ZZTo*")
    limits.add_group("top", "T*")
    limits.add_group("data", "data_*", isData=True)

    lumi = {'hpp%i' % mass: 1.026,
            'dyjets':       1.026,
            'zz':           1.026,
            'top':          1.026}
    limits.add_systematics("lumi", "lnN", **lumi)

    mu_eff = {'hpp%i' % mass: 1.043,
              'dyjets':       1.043,
              'zz':           1.043,
              'top':          1.043}

    e_eff = {'hpp%i' % mass: 1.101,
             'dyjets':       1.101,
             'zz':           1.101,
             'top':          1.101}

    limits.add_systematics("mu_eff", "lnN", **mu_eff)
    limits.add_systematics("e_eff", "lnN", **e_eff)

    hpp_sys = {'hpp%i' % mass: 1.15}

    limits.add_systematics("mc_err", "lnN", **hpp_sys)

    limits.gen_card("4l.txt")


def plot_mmmm():
    plot_limits("test.pdf", _4L_MASSES, "datacards/4l", blinded=True,
                x_label=r"$\Phi^{++}$ Mass [GeV]",
                y_label=r"95% CL Upper Limit on $\sigma/\sigma_{SM}$")


def plot_4l():
    plot_limits("test_4l_all.pdf", _4L_MASSES, "datacards/light_lep_all", blinded=True,
                x_label=r"$\Phi^{++}$ Mass [GeV]",
                y_label=r"95% CLs Upper Limit on $\sigma/\sigma_{SM}$")

def plot_3l():
    plot_limits("test_3l.pdf", _3L_MASSES, "datacards/3l", blinded=True,
                x_label=r"$\Phi^{++}$ Mass [GeV]",
                y_label=r"95% CLs Upper Limit on $\sigma/\sigma_{SM}$")

def main():

    #plot_mmmm()
    plot_3l()

    #for mass in _4L_MASSES:
    #    fourl(mass)


if __name__ == "__main__":
    main()
