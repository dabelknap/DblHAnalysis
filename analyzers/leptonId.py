import sys

sys.argv.append('b')
import ROOT as rt
sys.argv.pop()


def muon_id(rtrow, *lep):
    dz = [getattr(rtrow, "m%iPVDZ" % l) < 1.0 for l in lep]
    dxy = [getattr(rtrow, "m%iPVDXY" % l) < 0.5 for l in lep]
    sip = [getattr(rtrow, "m%iIP3DS" % l) < 4.0 for l in lep]

    mu_type = [getattr(rtrow, "m%iIsTracker" % l) or getattr(rtrow, "m%iIsGlobal" % l) for l in lep]

    return all(dz + dxy + sip + mu_type)


def elec_id(rtrow, *lep):
    dz = [getattr(rtrow, "e%iPVDZ" % l) < 1.0 for l in lep]
    dxy = [getattr(rtrow, "e%iPVDXY" % l) < 0.5 for l in lep]
    sip = [getattr(rtrow, "e%iIP3DS" % l) < 4.0 for l in lep]

    nhit = [getattr(rtrow, "e%iMissingHits" % l) <= 1 for l in lep]

    mva = [_ele_mva(rtrow, l) for l in lep]

    return all(dz + dxy + sip + nhit + mva)


def _ele_mva(rtrow, l):
    pt = getattr(rtrow, "e%iPt" % l)
    eta = getattr(rtrow, "e%iSCEta" % l)
    mva = getattr(rtrow, "e%iMVANonTrig" % l)

    if 5.0 < pt < 10.0:
        return (eta < 0.8 and mva > 0.47) or (0.8 < eta < 1.479 and mva > 0.004) or (1.479 < eta and mva > 0.295)

    elif 10.0 < pt:
        return (eta < 0.8 and mva > -0.34) or (0.8 < eta < 1.479 and mva > -0.65) or (1.479 < eta and mva > 0.6)

    else:
        return False
