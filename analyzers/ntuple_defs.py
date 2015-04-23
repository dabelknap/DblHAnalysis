import tables as tb


class EventBase(tb.IsDescription):
    evt            = tb.Int32Col()
    run            = tb.Int32Col()
    lumi           = tb.Int32Col()

    nvtx           = tb.Int32Col()

    channel        = tb.StringCol(4)

    lep_scale      = tb.Float32Col()
    lep_scale_e_up = tb.Float32Col()
    lep_scale_m_up = tb.Float32Col()
    pu_weight      = tb.Float32Col()


class Event4l(EventBase):
    mass    = tb.Float32Col()

    sT      = tb.Float32Col()

    met     = tb.Float32Col()
    metPhi  = tb.Float32Col()

    jetVeto = tb.Int32Col()

    h1mass  = tb.Float32Col()
    sT1     = tb.Float32Col()
    dPhi1   = tb.Float32Col()

    h2mass  = tb.Float32Col()
    sT2     = tb.Float32Col()
    dPhi2   = tb.Float32Col()

    l1Pt    = tb.Float32Col()
    l1Eta   = tb.Float32Col()
    l1Phi   = tb.Float32Col()
    l1Chg   = tb.Int8Col()
    l1Flv   = tb.StringCol(1)
    l1Iso   = tb.Float32Col()

    l2Pt    = tb.Float32Col()
    l2Eta   = tb.Float32Col()
    l2Phi   = tb.Float32Col()
    l2Chg   = tb.Int8Col()
    l2Flv   = tb.StringCol(1)
    l2Iso   = tb.Float32Col()

    l3Pt    = tb.Float32Col()
    l3Eta   = tb.Float32Col()
    l3Phi   = tb.Float32Col()
    l3Chg   = tb.Int8Col()
    l3Flv   = tb.StringCol(1)
    l3Iso   = tb.Float32Col()

    l4Pt    = tb.Float32Col()
    l4Eta   = tb.Float32Col()
    l4Phi   = tb.Float32Col()
    l4Chg   = tb.Int8Col()
    l4Flv   = tb.StringCol(1)
    l4Iso   = tb.Float32Col()


class EventZZ(EventBase):
    mass    = tb.Float32Col()
    z1mass  = tb.Float32Col()
    z2mass  = tb.Float32Col()
    sT      = tb.Float32Col()

    l1Pt    = tb.Float32Col()
    l1Eta   = tb.Float32Col()
    l1Phi   = tb.Float32Col()
    l1Chg   = tb.Int16Col()
    l1Iso   = tb.Float32Col()

    l2Pt    = tb.Float32Col()
    l2Eta   = tb.Float32Col()
    l2Phi   = tb.Float32Col()
    l2Chg   = tb.Int16Col()
    l2Iso   = tb.Float32Col()

    l3Pt    = tb.Float32Col()
    l3Eta   = tb.Float32Col()
    l3Phi   = tb.Float32Col()
    l3Chg   = tb.Int16Col()
    l3Iso   = tb.Float32Col()

    l4Pt    = tb.Float32Col()
    l4Eta   = tb.Float32Col()
    l4Phi   = tb.Float32Col()
    l4Chg   = tb.Int16Col()
    l4Iso   = tb.Float32Col()
