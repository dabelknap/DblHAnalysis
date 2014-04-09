import sys

sys.argv.append('b')
import ROOT as rt
sys.argv.pop()


def lep_id(rtrow, *lep, **kwargs):
    control = kwargs.get('control', False)
    
    ids = [muon_id(rtrow, l, control) for l in lep if l[0] == 'm']
    ids += [elec_id(rtrow, l, control) for l in lep if l[0] == 'e']

    return all(ids)


def muon_id(rtrow, l, control):
    dz = getattr(rtrow, "%sPVDZ" % l) < 1.0
    dxy = getattr(rtrow, "%sPVDXY" % l) < 0.5

    if control:
        sip = getattr(rtrow, "%sIP3DS" % l) > 4.0
    else:
        sip = getattr(rtrow, "%sIP3DS" % l) < 4.0

    mu_type = getattr(rtrow, "%sIsTracker" % l) or getattr(rtrow, "%sIsGlobal" % l)

    return all([dz, dxy, sip, mu_type])


def elec_id(rtrow, l, control):
    dz = getattr(rtrow, "%sPVDZ" % l) < 1.0
    dxy = getattr(rtrow, "%sPVDXY" % l) < 0.5

    if control:
        sip = getattr(rtrow, "%sIP3DS" % l) > 4.0
    else:
        sip = getattr(rtrow, "%sIP3DS" % l) < 4.0

    nhit = getattr(rtrow, "%sMissingHits" % l) <= 1

    mva = _elec_mva(rtrow, l)

    return all([dz, dxy, sip, nhit, mva])


def _elec_mva(rtrow, l):
    pt = getattr(rtrow, "%sPt" % l)
    eta = abs(getattr(rtrow, "%sSCEta" % l))
    mva = getattr(rtrow, "%sMVANonTrig" % l)

    if 5.0 < pt < 10.0:
        return (eta < 0.8 and mva > 0.47) or (0.8 < eta < 1.479 and mva > 0.004) or (1.479 < eta and mva > 0.295)

    elif 10.0 < pt:
        return (eta < 0.8 and mva > -0.34) or (0.8 < eta < 1.479 and mva > -0.65) or (1.479 < eta and mva > 0.6)

    else:
        return False
