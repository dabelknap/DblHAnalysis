import tables as tb


class EventBase(tb.IsDescription):
    evt     = tb.Int32Col()
    run     = tb.Int32Col()
    lumi    = tb.Int32Col()

    channel = tb.StringCol(4)

    weight  = tb.Float32Col()


class Event4l(EventBase):
    mass    = tb.Float32Col()
    h1mass  = tb.Float32Col()
    h2mass  = tb.Float32Col()

    l1Pt    = tb.Float32Col()
    l1Eta   = tb.Float32Col()
    l1Phi   = tb.Float32Col()
    l1Chg   = tb.Int8Col()
    l1Flv   = tb.EnumCol(['t','e','m'], 'e', base='uint8')
    l1Iso   = tb.Float32Col()

    l2Pt    = tb.Float32Col()
    l2Eta   = tb.Float32Col()
    l2Phi   = tb.Float32Col()
    l2Chg   = tb.Int8Col()
    l2Flv   = tb.EnumCol(['t','e','m'], 'e', base='uint8')
    l2Iso   = tb.Float32Col()

    l3Pt    = tb.Float32Col()
    l3Eta   = tb.Float32Col()
    l3Phi   = tb.Float32Col()
    l3Chg   = tb.Int8Col()
    l3Flv   = tb.EnumCol(['t','e','m'], 'e', base='uint8')
    l3Iso   = tb.Float32Col()

    l4Pt    = tb.Float32Col()
    l4Eta   = tb.Float32Col()
    l4Phi   = tb.Float32Col()
    l4Chg   = tb.Int8Col()
    l4Flv   = tb.EnumCol(['t','e','m'], 'e', base='uint8')
    l4Iso   = tb.Float32Col()


class EventZZ(EventBase):
    mass    = tb.Float32Col()
    z1mass  = tb.Float32Col()
    z2mass  = tb.Float32Col()

    l1Pt    = tb.Float32Col()
    l1Eta   = tb.Float32Col()
    l1Phi   = tb.Float32Col()
    l1Chg   = tb.Int16Col()
    l1Iso   = tb.Float32Col()
    l1Id    = tb.Float32Col()

    l2Pt    = tb.Float32Col()
    l2Eta   = tb.Float32Col()
    l2Phi   = tb.Float32Col()
    l2Chg   = tb.Int16Col()
    l2Iso   = tb.Float32Col()
    l2Id    = tb.Float32Col()

    l3Pt    = tb.Float32Col()
    l3Eta   = tb.Float32Col()
    l3Phi   = tb.Float32Col()
    l3Chg   = tb.Int16Col()
    l3Iso   = tb.Float32Col()
    l3Id    = tb.Float32Col()

    l4Pt    = tb.Float32Col()
    l4Eta   = tb.Float32Col()
    l4Phi   = tb.Float32Col()
    l4Chg   = tb.Int16Col()
    l4Iso   = tb.Float32Col()
    l4Id    = tb.Float32Col()
