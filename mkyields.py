from yields import Yields
from plotters.xsec import xsecs
from uncertainties import ufloat
from numpy import sqrt
from tabulate import tabulate
import numpy as np
import logging
import sys
import json


_4L_MASSES = [110, 130, 150, 170, 200, 250, 300,
              350, 400, 450, 500, 600, 700]

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class Scales(object):

    def __init__(self, br_ee, br_em, br_et, br_mm, br_mt, br_tt):
        x = np.array([br_ee, br_em, br_et, br_mm, br_mt, br_tt], dtype=float)
        self.m = np.outer(x, x) * 36.0
        self.index = {"ee": 0, "em": 1, "et": 2, "mm": 3, "mt": 4, "tt": 5}

    def scale(self, hpp, hmm):
        i = self.index[hpp]
        j = self.index[hmm]
        return self.m[i,j]



def data_sideband(mass, channel, cuts='(True)'):
    """
    Compute the number of data events in the sidebands.

    Parameters
    ----------
    mass : float
    channel : str
        Must be 'eeee', 'emem', or 'mmmm', etc.
    cuts : str
        Additional sideband selections

    Returns
    -------
    N : int
        Number of events in sideband from data
    """

    # Define mass window
    window = '(%f < h1mass) & (h1mass < %f)' % (0.9*mass, 1.1*mass)
    window += '& (%f < h2mass) & (h2mass < %f)' % (0.9*mass, 1.1*mass)
    bounds = '(12 < h1mass) & (h1mass < 700) & (12 < h2mass) & (h2mass < 700)'

    x = Yields("DblH", "~(%s) & (%s) & (%s) & (%s)" % (window, bounds, cuts, channel),
               "./ntuples", channels=["dblh4l"], lumi=19.7)
    x.add_group("data", "data_*", isData=True)

    return x.yields("data")[0]


def alpha(mass, channel):
    """
    Compute alpha used in sideband method background estimation

    Parameters
    ----------
    mass : float
    channel : str
        Must be 'eeee', 'emem', or 'mmmm', etc.
    cuts : str
        Additional sideband selections

    Returns
    -------
    alpha : float
        If the sideband has 0 MC statistics, return MC value in signal region
        If the error in the signal region is greater than nominal value,
            return the standard deviaiton in signal region
        Otherwise, return the ratio of the events in the signal region to
            the sidebands
    """

    cuts = '(%f < h1mass) & (h1mass < %f)' % (0.9*mass, 1.1*mass)
    cuts += '& (%f < h2mass) & (h2mass < %f)' % (0.9*mass, 1.1*mass)

    inner = Yields("DblH", "(%s) & (%s)" % (cuts, channel), "./ntuples",
                   channels=["dblh4l"], lumi=19.7)

    inner.add_group("zz", "ZZTo*", "ggZZ*")
    inner.add_group("top", "T*")
    inner.add_group("dyjets", "Z[1234]jets*M50")

    sig = ufloat(*inner.yields("zz")) + ufloat(*inner.yields("top")) + \
        ufloat(*inner.yields("dyjets"))

    bounds = '(12 < h1mass) & (h1mass < 700) & (12 < h2mass) & (h2mass < 700)'
    outer = Yields("DblH", "~(%s) & (%s) & (%s)" % (cuts, bounds, channel),
                   "./ntuples", channels=["dblh4l"], lumi=19.7)

    outer.add_group("zz", "ZZTo*", "ggZZ*")
    outer.add_group("top", "T*")
    outer.add_group("dyjets", "Z[1234]jets*M50")

    with open('plotters/mc_events.json', 'r') as jfile:
        mc_events = json.load(jfile)
        single_zz_event = xsecs['ZZTo4e_8TeV-powheg-pythia6'] * 19.7 / \
                mc_events['ZZTo4e_8TeV-powheg-pythia6']

    bkg = ufloat(*outer.yields("zz")) + ufloat(*outer.yields("top")) + \
        ufloat(*outer.yields("dyjets"))

    if bkg.nominal_value == 0.0:
        return sig.nominal_value
    if sig.nominal_value < sig.std_dev:
        return sig.std_dev
    if sig.nominal_value == 0.0:
        return single_zz_event
    else:
        return (sig/bkg).nominal_value


def bkg_estimate(mass, channel, cuts='(True)'):
    """
    Compute the background estimate using the sideband method

    Parameters
    ----------
    mass : float
    channel : str
    cuts : str

    Returns
    -------
    Nbgsr : float
        Number of background events in signal region
    Err : float
        Error on background estimate in signal region
    """
    alp = alpha(mass, channel)

    Nsb = data_sideband(mass, channel, cuts=cuts)
    Nbgsr = alp * (Nsb + 1.0)
    Err = alp * sqrt(Nsb + 1.0)

    return (Nbgsr, Err)


def test():
    mass = 300

    cuts = '(%f < h1mass) & (h1mass < %f)' % (0.9*mass, 1.1*mass)
    cuts+= '& (%f < h2mass) & (h2mass < %f)' % (0.9*mass, 1.1*mass)
    cuts += '& (channel == "mmmm")'

    sig_reg = Yields("DblH", cuts, "./ntuples", channels=["dblh4l"], lumi=19.7)
    sig_reg.add_group("zz", "ZZTo*")
    sig_reg.add_group("top", "T*")

    zz = ufloat(*sig_reg.yields("zz"))
    top = ufloat(*sig_reg.yields("top"))

    print zz + top

    cuts = '(%f > h1mass) & (h1mass > %f)' % (0.9*mass, 1.1*mass)
    cuts+= '& (%f > h2mass) & (h2mass > %f)' % (0.9*mass, 1.1*mass)
    cuts += '& (channel == "mmmm")'
    bkg_reg = Yields("DblH", cuts, "./ntuples", channels=["dblh4l"], lumi=19.7)
    bkg_reg.add_group("zz", "ZZTo*")
    bkg_reg.add_group("top", "T*")

    z = ufloat(*bkg_reg.yields("zz"))

    print z

    print (zz + top)/(z)


def mktable(channels):

    out = np.zeros((len(_4L_MASSES), 6))

    for i, mass in enumerate(_4L_MASSES):

        cuts = '(%f < h1mass) & (h1mass < %f)' % (0.9*mass, 1.1*mass)
        cuts+= '& (%f < h2mass) & (h2mass < %f)' % (0.9*mass, 1.1*mass)
        cuts += '& (%s)' % ' | '.join(['(channel == "%s")' % channel for channel
                                       in channels])

        mc_bkg = Yields("DblH", cuts, "./ntuples", channels=["dblh4l"],
                        lumi=19.7)
        mc_bkg.add_group("zz", "ZZTo*")
        mc_bkg.add_group("top", "T*")
        mc_bkg.add_group("dyjets", "Z[1234]jets*M50")

        bkg_rate = ufloat(*mc_bkg.yields("zz")) + ufloat(*mc_bkg.yields("top"))\
                   + ufloat(*mc_bkg.yields("dyjets"))


        bkg_est = bkg_estimate(mass, '(%s)' % ' | '.join(['(channel == "%s")' %
                                                          channel for channel
                                                          in channels]))

        mc_sig = Yields("DblH", cuts, "./ntuples", channels=["dblh4l"],
                        lumi=19.7)
        mc_sig.add_group("sig", "HPlus*M-%i_8TeV*" % mass)

        sig_rate = ufloat(*mc_sig.yields("sig"))*36.0


        out[i,0] = sig_rate.nominal_value
        out[i,1] = sig_rate.std_dev
        out[i,2] = bkg_rate.nominal_value
        out[i,3] = bkg_rate.std_dev
        out[i,4] = bkg_est[0]
        out[i,5] = bkg_est[1]

    return out


def bkg_compare(mass, channels, scale=36.0):

    cuts = '(%f < h1mass) & (h1mass < %f)' % (0.9*mass, 1.1*mass)
    cuts+= '& (%f < h2mass) & (h2mass < %f)' % (0.9*mass, 1.1*mass)
    cuts += '& (%s)' % ' | '.join(['(channel == "%s")' % channel for channel
                                   in channels])

    mc_bkg = Yields("DblH", cuts, "./ntuples", channels=["dblh4l"],
                    lumi=19.7)
    mc_bkg.add_group("zz", "ZZTo*")
    mc_bkg.add_group("top", "T*")
    mc_bkg.add_group("dyjets", "Z[1234]jets*M50")

    bkg_rate = ufloat(*mc_bkg.yields("zz")) + ufloat(*mc_bkg.yields("top"))\
               + ufloat(*mc_bkg.yields("dyjets"))


    bkg_est = bkg_estimate(mass, '(%s)' % ' | '.join(['(channel == "%s")' %
                                                      channel for channel
                                                      in channels]))

    mc_sig = Yields("DblH", cuts, "./ntuples", channels=["dblh4l"],
                    lumi=19.7)
    mc_sig.add_group("sig", "HPlus*M-%i_8TeV*" % mass)

    sig_rate = ufloat(*mc_sig.yields("sig")) * ufloat(1.0, 0.15) * scale

    return np.array([bkg_rate, ufloat(bkg_est[0], bkg_est[1]), ufloat(0.0,0.0), sig_rate])


def bkg_table_BP1(mass):
    s = Scales(0, 0.01, 0.01, 0.3, 0.38, 0.3)
    out =  bkg_compare(mass, ["emem", "emme", "meme", "meem"], scale=s.scale("em","em"))
    out += bkg_compare(mass, ["emmm", "memm"], scale=s.scale("em","mm"))
    out += bkg_compare(mass, ["mmem", "mmme"], scale=s.scale("mm","em"))
    out += bkg_compare(mass, ["mmmm"], scale=s.scale("mm","mm"))
    return out


def bkg_table_BP2(mass):
    s = Scales(0.5, 0, 0, 0.125, 0.25, 0.125)
    out =  bkg_compare(mass, ["eemm"], scale=s.scale("ee","mm"))
    out += bkg_compare(mass, ["mmee"], scale=s.scale("mm","ee"))
    out += bkg_compare(mass, ["eeee"], scale=s.scale("ee","ee"))
    out += bkg_compare(mass, ["mmmm"], scale=s.scale("mm","mm"))
    return out


def bkg_table_BP3(mass):
    s = Scales(0.34, 0, 0, 0.33, 0, 0.33)
    out =  bkg_compare(mass, ["eemm"], scale=s.scale("ee","mm"))
    out += bkg_compare(mass, ["mmee"], scale=s.scale("mm","ee"))
    out += bkg_compare(mass, ["eeee"], scale=s.scale("ee","ee"))
    out += bkg_compare(mass, ["mmmm"], scale=s.scale("mm","mm"))
    return out


def bkg_table_BP4(mass):
    s = Scales(1./6., 1./6., 1./6., 1./6., 1./6., 1./6.)
    out =  bkg_compare(mass, ["emem", "emme", "meme", "meem"], scale=s.scale("em","em"))
    out += bkg_compare(mass, ["emmm", "memm"], scale=s.scale("em","mm"))
    out += bkg_compare(mass, ["mmem", "mmme"], scale=s.scale("mm","em"))
    out += bkg_compare(mass, ["mmmm"], scale=s.scale("mm","mm"))
    out += bkg_compare(mass, ["eeee"], scale=s.scale("ee","ee"))
    out += bkg_compare(mass, ["eemm"], scale=s.scale("ee","mm"))
    out += bkg_compare(mass, ["mmee"], scale=s.scale("mm","ee"))
    return out


def bkg_table_mm100(mass):
    out = bkg_compare(mass, ["mmmm"], scale=36.0)
    return out


def bkg_table_ee100(mass):
    out = bkg_compare(mass, ["eeee"], scale=36.0)
    return out


def bkg_table_em100(mass):
    out = bkg_compare(mass, ["emem", "emme", "meem", "meme"], scale=36.0)
    return out


def generate_bkg_tables():
    functions = [bkg_table_ee100, bkg_table_em100, bkg_table_mm100,
                 bkg_table_BP1, bkg_table_BP2, bkg_table_BP3, bkg_table_BP4]

    with open('bkg_tables.txt', 'w') as outfile:
        for fun in functions:
            log.info("Processing BP: %s" % fun.func_name)

            header = "\n" + fun.func_name + "\n"
            header += "\\hline\n"
            header += r"Mass (GeV) & MC Estimate & Sideband Estimate & Observation & Signal \\" + "\n"
            header += "\\hline\n"

            outfile.write(header)

            for mass in _4L_MASSES:
                values = fun(mass)
                string = ("%i &"
                          " $%.2f \\pm %.2f$ &"
                          " $%.2f \\pm %.2f$ &"
                          " $%.2f \\pm %.2f$ &"
                          " $%.2f \\pm %.2f$ \\\\\n" %
                          (mass,
                           values[0].nominal_value, values[0].std_dev,
                           values[1].nominal_value, values[1].std_dev,
                           values[2].nominal_value, values[2].std_dev,
                           values[3].nominal_value, values[3].std_dev))

                outfile.write(string)


def sidebands(channels):

    out = []

    for i, mass in enumerate(_4L_MASSES):

        cuts = '(%f < h1mass) & (h1mass < %f)' % (0.9*mass, 1.1*mass)
        cuts+= '& (%f < h2mass) & (h2mass < %f)' % (0.9*mass, 1.1*mass)
        cuts += '& (%s)' % ' | '.join(['(channel == "%s")' % channel for channel
                                       in channels])

        # sideband alpha
        a = alpha(mass,
                  '(%s)' % ' | '.join(['(channel == "%s")' % channel for channel in channels]))
        sb = data_sideband(mass,
                  '(%s)' % ' | '.join(['(channel == "%s")' % channel for channel in channels]),
                  cuts='(%f < sT)' % (0.6*mass + 130.0))
        bkg = bkg_estimate(mass,
                  '(%s)' % ' | '.join(['(channel == "%s")' % channel for channel in channels]),
                  cuts='(%f < sT)' % (0.6*mass + 130.0))

        out.append([mass, "%.4f" % a, sb, r"$%.4f \pm %.4f$" % (bkg[0], bkg[1]), 0])

    print ""
    print tabulate(out, headers=["Mass (GeV)", r"\alpha",
                                 "Sideband Events (data)",
                                 "Signal Region Background Estimation",
                                 "Signal Region Events (data)"])
                   #tablefmt="latex")


def lepscale(channels):
    """
    Print a table of the %-change in the signal yields (for each mass point)
    for the provided channel.
    """

    out = []

    #for mass in (_4L_MASSES):
    for mass in ([110]):
        log.info("Processing signal mass: %s" % mass)

        # Apply 2D mass window for the given mass point
        cuts = '(%f < h1mass) & (h1mass < %f)' % (0.9*mass, 1.1*mass)
        cuts += '& (%f < h2mass) & (h2mass < %f)' % (0.9*mass, 1.1*mass)

        # Select which channels to look at
        cuts += '& (%s)' % ' | '.join(['(channel == "%s")' % channel for channel
                                       in channels])

        mc_sig = Yields("DblH", cuts, "./ntuples", channels=["dblh4l"],
                        lumi=19.7)
        mc_sig.add_group("sig", "HPlus*M-%i_8TeV*" % mass)

        # compute the nominal yields with the normal scale factors
        nominal = mc_sig.yields("sig")[0]

        # compute the yields with the scaled-up scale factors
        e_up    = mc_sig.yields("sig", scale = "lep_scale_e_up")[0]
        mu_up   = mc_sig.yields("sig", scale = "lep_scale_m_up")[0]

        # compute the %-change in the yields
        diff_e = (e_up - nominal)/nominal + 1.0
        diff_mu = (mu_up - nominal)/nominal + 1.0

        out.append([mass, nominal, e_up, mu_up, diff_e, diff_mu])

    print ""
    print channels[0]
    print tabulate(out, headers=["Mass", "Nominal Yield", "Yield e Up",
                                 "Yield mu Up", "%-Diff e", "%-Diff mu"],
                   floatfmt=".3f")


def lepscale_ZZ():
    """
    Print a table of the %-change in the signal yields (for each mass point)
    for the provided channel.
    """

    chan = [["mmmm"],["eeee"],["eemm","mmee"]]

    out = []

    for channels in chan:

        # HZZ4L phase space cuts
        cuts = ('(mass > 0) '
                '& (40 < z1mass) & (z1mass < 120) '
                '& (12 < z2mass) & (z2mass < 120)')

        # Select which channels to look at
        cuts += '& (%s)' % ' | '.join(['(channel == "%s")' % channel for channel
                                       in channels])

        mc_sig = Yields("ZZ4l", cuts, "./ntuples", channels=["zz4l"], lumi=19.7)
        mc_sig.add_group("sig", "GluGluToH*")

        # compute the nominal yields with the normal scale factors
        nominal = mc_sig.yields("sig")[0]

        # compute the yields with the scaled-up scale factors
        e_up    = mc_sig.yields("sig", scale = "lep_scale_e_up")[0]
        mu_up   = mc_sig.yields("sig", scale = "lep_scale_m_up")[0]

        # compute the %-change in the yields
        diff_e = (e_up - nominal)/nominal * 100.0
        diff_mu = (mu_up - nominal)/nominal * 100.0

        out.append([channels[0], nominal, e_up, mu_up, diff_e, diff_mu])

    print ""
    print tabulate(out, headers=["Channels", "Nominal Yield", "Yield e Up",
                                 "Yield mu Up", "%-Diff e", "%-Diff mu"])


def table2latex(table):
    nrows = table.shape[0]

    for i in range(nrows):
        row = table[i,:]
        line = ' & '.join(['%.3e' % k for k in row])
        print _4L_MASSES[i], '&', line, r'\\'


if __name__ == "__main__":
    #out = mktable(["emem", "meme", "emme", "meem"])
    #out = mktable(["mmmm"])
    #out = mktable(["eeee"])
    #print "mass mc_sig sigma(mc_sig) mc_bkg sigma(mc_bkg) sb_bkg sigma(sb_bkg)"
    #for i, mass in enumerate(_4L_MASSES):
    #    print mass, out[i,0], out[i,1], out[i,2], out[i,3], out[i,4], out[i,5]

    arg = sys.argv[1]

    if arg == "lepscale":
        arg2 = sys.argv[2]

        if arg2 == "mmmm":
            lepscale(["mmmm"])

        elif arg2 == "eeee":
            lepscale(["eeee"])

        elif arg2 == "emem":
            lepscale(["emem","emme","meem","meme"])

        elif arg2 == "eemm":
            lepscale(["eemm","mmee"])

        elif arg2 == "eeem":
            lepscale(["eeem","eeme","emee","meee"])

        elif arg2 == "emmm":
            lepscale(["mmme","mmem","memm","emmm"])

        elif arg2 == "zz":
            lepscale_ZZ()

        else:
            raise ValueError("invalid argument")

    elif arg == "sidebands":
        arg2 = sys.argv[2]

        if arg2 == "mm100":
            sidebands(["mmmm"])

        elif arg2 == "ee100":
            sidebands(["eeee"])

        elif arg2 == "em100":
            sidebands(["emem","emme","meem","meme"])

        elif arg2 == "BP1":
            sidebands(["emem","emme","meem","meme",
                       "mmmm"
                       "mmme","mmem","memm","emmm"])

        elif arg2 == "BP2":
            sidebands(["eeee","mmmm","eemm","mmee"])

        elif arg2 == "BP3":
            sidebands(["eeee","mmmm","eemm","mmee"])

        elif arg2 == "BP4":
            sidebands(["emem","emme","meem","meme",
                       "mmmm","eeee"
                       "eemm","mmee",
                       "eeem","eeme","emee","meee",
                       "mmme","mmem","memm","emmm"])
        else:
            raise ValueError("invalid argument")

    elif arg == "bkg_tables":
        generate_bkg_tables()

    else:
        raise ValueError("Unrecognized option: '%s'" % arg)
