from yields import Yields
from uncertainties import ufloat
from numpy import sqrt
import numpy as np


def data_sideband(mass):
    cuts = '(%f < h1mass) & (h1mass < %f)' % (0.9*mass, 1.1*mass)
    cuts+= '& (%f < h2mass) & (h2mass < %f)' % (0.9*mass, 1.1*mass)

def data_sideband(mass, cuts='(True)'):
    # Define mass window
    window = '(%f < h1mass) & (h1mass < %f)' % (0.9*mass, 1.1*mass)
    window += '& (%f < h2mass) & (h2mass < %f)' % (0.9*mass, 1.1*mass)
    bounds = '(12 < h1mass) & (h1mass < 700) & (12 < h2mass) & (h2mass < 700)'

    x = Yields("DblH", "~(%s) & (%s) & (%s)" % (window, bounds, cuts),
               "./ntuples", channels=["dblh4l"], lumi=19.7)
    x.add_group("data", "data_*", isData=True)

    return ufloat(*x.yields("data"))


def alpha(mass):
    cuts = '(%f < h1mass) & (h1mass < %f)' % (0.9*mass, 1.1*mass)
    cuts += '& (%f < h2mass) & (h2mass < %f)' % (0.9*mass, 1.1*mass)
    channel = '(channel == "mmmm")'

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

    return sig/bkg


def bkg_estimate(mass, cuts='(True)'):
    Nbgsr = alpha(mass) * (data_sideband(mass, cuts=cuts) + 1)

    return (Nbgsr.nominal_value, Nbgsr.std_dev,
            Nbgsr.nominal_value/sqrt(Nbgsr.nominal_value + 1))


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


if __name__ == "__main__":
    print bkg_estimate(300)
