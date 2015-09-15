import sys

sys.argv.append('b')
import ROOT as rt
sys.argv.pop()


def lep_id(rtrow, *lep, **kwargs):
    control = kwargs.get('control', False)
    
    ids = [muon_id_tight(rtrow, l) for l in lep if l[0] == 'm']
    ids += [elec_id_tight(rtrow, l) for l in lep if l[0] == 'e']

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


def muon_id_tight(rtrow, l):
    pt = getattr(rtrow, "%sPt" % l) > 10
    eta = abs(getattr(rtrow, "%sEta" % l)) < 2.4
    tightid = getattr(rtrow, "%sPFIDTight" % l)

    return all([pt, eta, tightid])


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


def elec_id_loose(rtrow, l):
    pt = getattr(rtrow, "%sPt" % l)
    eta = abs(getattr(rtrow, "%sEta" % l))
    sceta = abs(getattr(rtrow, "%sSCEta" % l))
    sieie = getattr(rtrow, "%sSigmaIEtaIEta" % l)
    dphi = getattr(rtrow, "%sdeltaPhiSuperClusterTrackAtVtx" %l)
    deta = getattr(rtrow, "%sdeltaEtaSuperClusterTrackAtVtx" %l)
    hoe = getattr(rtrow, "%sHadronicOverEM" %l)
    eiso = getattr(rtrow, "%sEcalIsoDR03" %l)
    hiso = getattr(rtrow, "%sHcalIsoDR03" %l)
    tiso = getattr(rtrow, "%sTrkIsoDR03" %l)
    conv = getattr(rtrow, "%sHasConversion" %l)
    misshits = getattr(rtrow, "%sMissingHits" %l)

    passid = True
    if pt < 10: passid = False
    if eta > 2.5: passid = False
    if sceta < 1.479:
        if sieie > 0.01: passid = False
        if dphi > 0.15: passid = False
        if deta > 0.007: passid = False
        if hoe > 0.12: passid = False
        if max(eiso-1,0)/pt > 0.2: passid = False
    if sceta >= 1.479:
        if sieie > 0.03: passid = False
        if dphi > 0.1: passid = False
        if deta > 0.009: passid = False
        if hoe > 0.1: passid = False
        if eiso/pt > 0.2: passid = False
    if tiso/pt > 0.2: passid = False
    if hiso/pt > 0.2: passid = False
    if conv: passid = False
    if misshits: passid = False

    return passid


def elec_id_tight(rtrow, l):
    dz = getattr(rtrow, "%sPVDZ" % l) < 0.1
    dxy = getattr(rtrow, "%sPVDXY" % l) < 0.02
    chgId = getattr(rtrow, "%sChargeIdTight" % l)

    mva = _elec_trig_mva(rtrow, l)
    elec_loose = elec_id_loose(rtrow, l)

    return all([dz, dxy, mva, elec_loose, chgId])


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


def _elec_trig_mva(rtrow, l):
    pt = getattr(rtrow, "%sPt" % l)
    eta = abs(getattr(rtrow, "%sSCEta" % l))
    mva = getattr(rtrow, "%sMVATrig" % l)

    if 10.0 < pt < 20.0:
        return (abs < 0.8 and mva > 0.00) or \
                (0.8 < eta < 1.479 and mva > 0.10) or \
                (1.479 < eta and mva > 0.62)

    elif 20.0 < pt:
        return (abs < 0.8 and mva > 0.94) or \
                (0.8 < eta < 1.479 and mva > 0.85) or \
                (1.479 < eta and mva > 0.92)

    else:
        return False
