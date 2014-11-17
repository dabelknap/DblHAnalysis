from limits import Limits
from plotters.limits import plot_limits
import logging
import sys
import numpy as np

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

_4L_MASSES = [110, 130, 150, 170, 200, 250, 300,
              350, 400, 450, 500, 600, 700]

_3L_MASSES = [170, 200, 250, 300, 350, 400, 450,
              500, 600, 700]


class Scales(object):

    def __init__(self, br_ee, br_em, br_et, br_mm, br_mt, br_tt):
        x = np.array([br_ee, br_em, br_et, br_mm, br_mt, br_tt], dtype=float)
        self.m = np.outer(x, x) * 36.0
        self.index = {"ee": 0, "em": 1, "et": 2, "mm": 3, "mt": 4, "tt": 5}

    def scale(hpp, hmm):
        i = self.index[hpp]
        j = self.index[hmm]
        return self.m[i,j]


def four_lepton(name, channels, directory, scale=1.0):
    for mass in _4L_MASSES:
        cuts = '(%f < h1mass) & (h1mass < %f)' % (0.9*mass, 1.1*mass)
        cuts += '& (%f < sT)' % (0.6*mass + 130.0)
        cuts += '& (%s)' % ' | '.join(['channel == "%s"' % channel for channel in channels])

        limits = Limits("DblH", cuts, "./ntuples", "%s/%i" % (directory, mass),
                channels=["dblh4l"], lumi=19.7, blinded=True)

        limits.add_group("hpp%i" % mass, "HPlus*%i*" % mass, isSignal=True, scale=scale)
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

        limits.gen_card("%s.txt" % name)


def fourl_100():
    four_lepton("card", ["mmmm"], "./datacards/mmmm_100", scale=36.0)
    four_lepton("card", ["eeee"], "./datacards/eeee_100", scale=36.0)
    four_lepton("card", ["emem","emme", "meem", "meme"], "./datacards/emem_100", scale=36.0)


def BP1():
    s = Scales(0, 0.1, 0.1, 0.3, 0.38, 0.3)
    four_lepton("emem", ["emem", "emme", "meme", "meem"], "./datacards/BP1", scale=s.scale("em","em"))
    four_lepton("emmm", ["emmm", "memm"], "./datacards/BP1", scale=s.scale("em","mm"))
    four_lepton("mmem", ["mmem", "mmme"], "./datacards/BP1", scale=s.scale("mm","em"))
    four_lepton("mmmm", ["mmmm"], "./datacards/BP1", scale=s.scale("mm","mm"))


def BP2():
    s = Scales(0.5, 0, 0, 0.125, 0.25, 0.125)
    four_lepton("eemm", ["eemm"], "./datacards/BP2", scale=s.scale("ee","mm"))
    four_lepton("mmee", ["mmee"], "./datacards/BP2", scale=s.scale("mm","ee"))
    four_lepton("eeee", ["eeee"], "./datacards/BP2", scale=s.scale("ee","ee"))
    four_lepton("mmmm", ["mmmm"], "./datacards/BP2", scale=s.scale("mm","mm"))


def BP3():
    s = Scales(0.34, 0, 0, 0.33, 0, 0.33)
    four_lepton("eemm", ["eemm"], "./datacards/BP3", scale=s.scale("ee","mm"))
    four_lepton("mmee", ["mmee"], "./datacards/BP3", scale=s.scale("mm","ee"))
    four_lepton("eeee", ["eeee"], "./datacards/BP3", scale=s.scale("ee","ee"))
    four_lepton("mmmm", ["mmmm"], "./datacards/BP3", scale=s.scale("mm","mm"))


def BP4():
    s = Scales(1./6., 1./6., 1./6., 1./6., 1./6., 1./6.)
    four_lepton("emem", ["emem", "emme", "meme", "meem"], "./datacards/BP4", scale=s.scale("em","em"))
    four_lepton("emmm", ["emmm", "memm"], "./datacards/BP4", scale=s.scale("em","mm"))
    four_lepton("mmem", ["mmem", "mmme"], "./datacards/BP4", scale=s.scale("mm","em"))
    four_lepton("mmmm", ["mmmm"], "./datacards/BP4", scale=s.scale("mm","mm"))
    four_lepton("eeee", ["eeee"], "./datacards/BP4", scale=s.scale("ee","ee"))
    four_lepton("eemm", ["eemm"], "./datacards/BP4", scale=s.scale("ee","mm"))
    four_lepton("mmee", ["mmee"], "./datacards/BP4", scale=s.scale("mm","ee"))


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
