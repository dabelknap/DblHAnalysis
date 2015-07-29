from limits import Limits
from plotters.limits import plot_limits, exclusion
import mkyields as mky
import logging
import sys
import os
import numpy as np
import argparse
from tabulate import tabulate


logger = logging.getLogger("mklimits")
logging.basicConfig(level=logging.INFO)

_4L_MASSES = [130, 150, 170, 200, 250, 300,
              350, 400, 450, 500, 600, 700]

_3L_MASSES = [170, 200, 250, 300, 350, 400, 450,
              500, 600, 700]

_EFFICIENCY_SYST = {"mmmm": {"m": 1.010},
                    "eeee": {"e": 1.066},
                    "eemm": {"m": 1.005, "e": 1.032},
                    "eeem": {"m": 1.002, "e": 1.047},
                    "emmm": {"m": 1.007, "e": 1.016}}

_TITLE=r'\textbf{CMS} \emph{Preliminary} \hspace{1.9in} 19.7 fb$^{-1}$ (8 TeV)'


def efficiency_systematic(channel):
    # sort the characters so e's come before m's
    # normalize the channel format so it works with the dictionary
    chan = ''.join(sorted(channel))
    try:
        m_syst = _EFFICIENCY_SYST[chan]['m']
    except KeyError:
        m_syst = None

    try:
        e_syst = _EFFICIENCY_SYST[chan]['e']
    except KeyError:
        e_syst = None

    return (m_syst, e_syst)


class Scales(object):

    def __init__(self, br_ee, br_em, br_et, br_mm, br_mt, br_tt):
        x = np.array([br_ee, br_em, br_et, br_mm, br_mt, br_tt], dtype=float)
        self.m = np.outer(x, x) * 36.0
        self.index = {"ee": 0, "em": 1, "et": 2, "mm": 3, "mt": 4, "tt": 5}

    def scale(self, hpp, hmm):
        i = self.index[hpp]
        j = self.index[hmm]
        return self.m[i,j]


def four_lepton(name, channels, directory, scale=1.0):
    for mass in _4L_MASSES:
        cuts = '(%f < h1mass) & (h1mass < %f)' % (0.9*mass, 1.1*mass)
        cuts += '& (%f < h2mass) & (h2mass < %f)' % (0.9*mass, 1.1*mass)
        cuts += '& (%f < sT)' % (0.6*mass + 130.0)
        cuts += '& (%s)' % ' | '.join(['(channel == "%s")' % channel for channel in channels])

        limits = Limits("DblH", cuts, "./ntuples", "%s/%i" % (directory, mass),
                channels=["dblh4l"], lumi=19.7, blinded=True)

        limits.add_group("hpp%i" % mass, "HPlus*%i*" % mass, isSignal=True, scale=scale)
        limits.add_group("data", "data_*", isData=True)

        lumi = {'hpp%i' % mass: 1.026}
        limits.add_systematics("lumi", "lnN", **lumi)

        hpp_sys = {'hpp%i' % mass: 1.15}
        limits.add_systematics("sig_mc_err", "lnN", **hpp_sys)

        #mu_eff = {'hpp%i' % mass: 1.043}
        #limits.add_systematics("mu_eff", "lnN", **mu_eff)

        eff_syst = efficiency_systematic(name)

        # Add the muon efficiency systematic if it exists for this channel
        if eff_syst[0]:
            mu_eff = {'hpp%i' % mass: eff_syst[0]}
            limits.add_systematics("mu_eff", "lnN", **mu_eff)

        # Add the electron efficiency systematic if it exists for this channel
        if eff_syst[1]:
            e_eff = {'hpp%i' % mass: eff_syst[1]}
            limits.add_systematics("e_eff", "lnN", **e_eff)

        N_db_data = mky.data_sideband(
            mass,
            '(%s)' % ' | '.join(['(channel == "%s")' % channel for channel in channels]),
            cuts='(%f < sT)' % (0.6*mass + 130.0))

        alpha = mky.alpha(
            mass,
            '(%s)' % ' | '.join(['(channel == "%s")' % channel for channel in channels]))

        limits.add_bkg_rate("bkg_sb_%s" % channels[0], float(N_db_data) * alpha)
        kwargs = {"bkg_sb_%s" % channels[0]: alpha}
        limits.add_systematics("bkg_err_%s" % channels[0], "gmN %i" % N_db_data, **kwargs)

        kwargs = {"bkg_sb_%s" % channels[0]: 1.10}
        limits.add_systematics("alpha_err", "lnN", **kwargs)

        limits.gen_card("%s.txt" % name)


def four_lepton_mc(name, channels, directory, scale=1.0):
    for mass in _4L_MASSES:
        cuts = '(%f < h1mass) & (h1mass < %f)' % (0.9*mass, 1.1*mass)
        cuts += '& (%f < h2mass) & (h2mass < %f)' % (0.9*mass, 1.1*mass)
        cuts += '& (%f < sT)' % (0.6*mass + 130.0)
        cuts += '& (%s)' % ' | '.join(['(channel == "%s")' % channel for channel in channels])

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

        hpp_sys = {'hpp%i' % mass: 1.15}
        limits.add_systematics("sig_mc_err", "lnN", **hpp_sys)

        eff_syst = efficiency_systematic(name)

        if eff_syst[0]:
            mu_eff = {'hpp%i' % mass: eff_syst[0],
                      'dyjets':       eff_syst[0],
                      'zz':           eff_syst[0],
                      'top':          eff_syst[0]}
            limits.add_systematics("mu_eff", "lnN", **mu_eff)

        if eff_syst[1]:
            e_eff = {'hpp%i' % mass: eff_syst[1],
                     'dyjets':       eff_syst[1],
                     'zz':           eff_syst[1],
                     'top':          eff_syst[1]}
            limits.add_systematics("e_eff", "lnN", **e_eff)

        limits.gen_card("%s.txt" % name)


def fourl_100():
    four_lepton("card", ["mmmm"], "./datacards/mmmm_100", scale=36.0)
    four_lepton("card", ["eeee"], "./datacards/eeee_100", scale=36.0)
    four_lepton("card", ["emem","emme", "meem", "meme"], "./datacards/emem_100", scale=36.0)


def BP1(directory):
    s = Scales(0, 0.01, 0.01, 0.3, 0.38, 0.3)
    four_lepton("emem", ["emem", "emme", "meme", "meem"], os.path.join(directory, "BP1"), scale=s.scale("em","em"))
    four_lepton("emmm", ["emmm", "memm"], os.path.join(directory, "BP1"), scale=s.scale("em","mm"))
    four_lepton("mmem", ["mmem", "mmme"], os.path.join(directory, "BP1"), scale=s.scale("mm","em"))
    four_lepton("mmmm", ["mmmm"], os.path.join(directory, "BP1"), scale=s.scale("mm","mm"))


def BP2(directory):
    s = Scales(0.5, 0, 0, 0.125, 0.25, 0.125)
    four_lepton("eemm", ["eemm"], os.path.join(directory, "BP2"), scale=s.scale("ee","mm"))
    four_lepton("mmee", ["mmee"], os.path.join(directory, "BP2"), scale=s.scale("mm","ee"))
    four_lepton("eeee", ["eeee"], os.path.join(directory, "BP2"), scale=s.scale("ee","ee"))
    four_lepton("mmmm", ["mmmm"], os.path.join(directory, "BP2"), scale=s.scale("mm","mm"))


def BP3(directory):
    s = Scales(0.34, 0, 0, 0.33, 0, 0.33)
    four_lepton("eemm", ["eemm"], os.path.join(directory, "BP3"), scale=s.scale("ee","mm"))
    four_lepton("mmee", ["mmee"], os.path.join(directory, "BP3"), scale=s.scale("mm","ee"))
    four_lepton("eeee", ["eeee"], os.path.join(directory, "BP3"), scale=s.scale("ee","ee"))
    four_lepton("mmmm", ["mmmm"], os.path.join(directory, "BP3"), scale=s.scale("mm","mm"))


def BP4(directory):
    s = Scales(1./6., 1./6., 1./6., 1./6., 1./6., 1./6.)
    four_lepton("emem", ["emem", "emme", "meme", "meem"], os.path.join(directory, "BP4"), scale=s.scale("em","em"))
    four_lepton("emmm", ["emmm", "memm"], os.path.join(directory, "BP4"), scale=s.scale("em","mm"))
    four_lepton("mmem", ["mmem", "mmme"], os.path.join(directory, "BP4"), scale=s.scale("mm","em"))
    four_lepton("mmmm", ["mmmm"], os.path.join(directory, "BP4"), scale=s.scale("mm","mm"))
    four_lepton("eeee", ["eeee"], os.path.join(directory, "BP4"), scale=s.scale("ee","ee"))
    four_lepton("eemm", ["eemm"], os.path.join(directory, "BP4"), scale=s.scale("ee","mm"))
    four_lepton("mmee", ["mmee"], os.path.join(directory, "BP4"), scale=s.scale("mm","ee"))


def mm100(directory):
    four_lepton("mmmm", ["mmmm"], os.path.join(directory, "mm100"), scale=36.0)


def ee100(directory):
    four_lepton("eeee", ["eeee"], os.path.join(directory, "ee100"), scale=36.0)


def em100(directory):
    four_lepton("emem", ["emem"],
            os.path.join(directory, "em100"),
            scale=36.0)


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

    limits.gen_card("test.txt")


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
    plot_limits("test.pdf", _4L_MASSES, "datacards/mmmm100", blinded=True,
                x_label=r"$\Phi^{++}$ Mass [GeV]",
                y_label=r"95% CL Upper Limit on $\sigma/\sigma_{SM}$")


def plot(BP, directory="datacards", out=""):
    logger.info("Plotting %s" % BP)
    plot_limits("./plots/limits/%s/%s.pdf" % (out,BP), _4L_MASSES, "%s/%s" % (directory, BP), blinded=True,
                title=_TITLE,
                x_label=r"$\Phi^{++}$ Mass (GeV)",
                y_label=r"95\% CLs Upper Limit on $\sigma/\sigma_{SM+\Phi^{\pm\pm}}$")


def exclude(BP, directory="datacards"):
     return exclusion(_4L_MASSES, "%s/%s" % (directory, BP), blinded=True)


def plot_3l():
    plot_limits("test_3l.pdf", _3L_MASSES, "datacards/3l", blinded=True,
                x_label=r"$\Phi^{++}$ Mass [GeV]",
                y_label=r"95\% CLs Upper Limit on $\sigma/\sigma_{SM}$")


def parse_command_line(argv):
    parser = argparse.ArgumentParser(description="")

    parser.add_argument('operation', type=str, nargs="+")

    args = parser.parse_args(argv)

    return args


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    BPS = ["ee100", "em100", "mm100", "BP1", "BP2", "BP3", "BP4"]

    args = parse_command_line(argv)

    if args.operation[0] == "plot":
        if args.operation[1] == "all":
            for i in BPS:
                globals()["plot"](i)
        else:
            globals()["plot"](args.operation[1], directory="datacards/4l_8tev")

    elif args.operation[0] == "plotcomb":
        if args.operation[1] == "all":
            for i in BPS:
                globals()["plot"](i, directory="combination", out="comb")
        else:
            globals()["plot"](args.operation[1], directory="datacards/comb_8tev", out="comb")

    elif args.operation[0] == "exclude":
        if args.operation[1] == "all":
            out = []
            for i in BPS:
                exp, obs = globals()["exclude"](i, directory="datacards/4l_8tev")
                out.append([i,exp,obs])
            print tabulate(out,
                           headers=["BP", "Expected", "Observed"],
                           floatfmt=".0f")
        else:
            print globals()["exclude"](args.operation[1], directory="datacards/4l_8tev")

    elif args.operation[0] == "excludecomb":
        if args.operation[1] == "all":
            out = []
            for i in BPS:
                exp, obs = globals()["exclude"](i, directory="datacards/comb_8tev")
                out.append([i,exp,obs])
            print tabulate(out,
                           headers=["BP", "Expected", "Observed"],
                           floatfmt=".0f")
        else:
            print globals()["exclude"](args.operation[1], directory="datacards/comb_8tev")

    elif args.operation[0] == "all":
        for i in BPS:
            globals()[i]("./datacards/4l_8tev")

    else:
        globals()[args.operation[0]]("./datacards/4l_8tev")

    return 0


if __name__ == "__main__":
    status = main()
    sys.exit(status)
