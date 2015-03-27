from yields import Yields
from uncertainties import ufloat
from numpy import sqrt
from tabulate import tabulate
import numpy as np
import logging


_4L_MASSES = [110, 130, 150, 170, 200, 250, 300,
              350, 400, 450, 500, 600, 700]

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

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

    inner.add_group("zz", "ZZTo*")
    inner.add_group("top", "T*")
    inner.add_group("dyjets", "Z[1234]jets*M50")

    sig = ufloat(*inner.yields("zz")) + ufloat(*inner.yields("top")) + \
        ufloat(*inner.yields("dyjets"))

    bounds = '(12 < h1mass) & (h1mass < 700) & (12 < h2mass) & (h2mass < 700)'
    outer = Yields("DblH", "~(%s) & (%s) & (%s)" % (cuts, bounds, channel),
                   "./ntuples", channels=["dblh4l"], lumi=19.7)

    outer.add_group("zz", "ZZTo*")
    outer.add_group("top", "T*")
    outer.add_group("dyjets", "Z[1234]jets*M50")

    bkg = ufloat(*outer.yields("zz")) + ufloat(*outer.yields("top")) + \
        ufloat(*outer.yields("dyjets"))

    if bkg.nominal_value == 0:
        return sig.nominal_value
    if sig.nominal_value < sig.std_dev:
        return sig.std_dev
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
    Nsb = data_sideband(mass, channel, cuts=cuts)
    Nbgsr = alpha(mass, channel) * (Nsb + 1.0)
    Err = alpha(mass, channel) * sqrt(Nsb + 1.0)

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


def lepscale(channels):
    """
    Print a table of the %-change in the signal yields (for each mass point)
    for the provided channel.
    """

    print "mass, diff_e, diff_mu"

    for mass in (_4L_MASSES):
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
        diff_e = (e_up - nominal)/nominal * 100.0
        diff_mu = (mu_up - nominal)/nominal * 100.0

        print mass, diff_e, diff_mu


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
    #table2latex(mktable())
    #out = mktable(["emem", "meme", "emme", "meem"])
    #out = mktable(["mmmm"])
    #out = mktable(["eeee"])
    #print "mass mc_sig sigma(mc_sig) mc_bkg sigma(mc_bkg) sb_bkg sigma(sb_bkg)"
    #for i, mass in enumerate(_4L_MASSES):
    #    print mass, out[i,0], out[i,1], out[i,2], out[i,3], out[i,4], out[i,5]

    #lepscale(["mmmm"])
    lepscale_ZZ()
