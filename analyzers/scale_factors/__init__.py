import sys
import os
import logging

sys.argv.append('-b')
import ROOT as rt
sys.argv.pop()


class LeptonScaleFactors(object):

    def __init__(self):
        path = os.path.join(os.path.dirname(__file__),
                            'CombinedMethod_ScaleFactors_RecoIdIsoSip.root')
        self.e_rtfile = rt.TFile(path, 'READ')
        self.e_hist = self.e_rtfile.Get("h_electronScaleFactor_RecoIdIsoSip")

        path = os.path.join(os.path.dirname(__file__),
                            'MuonScaleFactors_2011_2012.root')
        self.m_rtfile = rt.TFile(path, 'READ')
        self.m_hist = self.m_rtfile.Get("TH2D_ALL_2012")

        self.logger = logging.getLogger(__name__)
        logging.basicConfig(
                level=logging.DEBUG,
                filename='analyzers/scale_factors/scalefactors.log',
                filemode='w')

    def scale_factor(self, row, *lep_list):
        scl = 1.0
        mup = 1.0
        eup = 1.0

        log_mssg = ""

        for l in lep_list:
            lep_type = l[0]

            if lep_type == 'm':
                mscale = self.m_scale(row, l)
                scl *= mscale[0]
                mup *= mscale[0] + mscale[1]
                eup *= mscale[0]

                log_mssg += " m: {scale: %f, sigma: %f}, " % \
                    (mscale[0], mscale[1])

            elif lep_type == 'e':
                escale = self.e_scale(row, l)
                scl *= escale[0]
                mup *= escale[0]
                eup *= escale[0] + escale[1]

                log_mssg += " e: {scale: %f, sigma: %f}, " % \
                    (escale[0], escale[1])

            else:
                raise TypeError("Lepton type %s not recognized" % lep_type)

        log_mssg += " scale: %f, scale_mu_up: %f, scale_e_up: %f" % \
            (scl, mup, eup)

        self.logger.debug(log_mssg)

        return (scl, mup, eup)

    def e_scale(self, row, l):
        pt = getattr(row, "%sPt" % l)
        eta = getattr(row, "%sEta" % l)
        global_bin = self.e_hist.FindBin(pt, eta)
        scl = self.e_hist.GetBinContent(global_bin)
        err = self.e_hist.GetBinError(global_bin)

        if scl < 0.1:
            scl = 1.0
            err = 0.0

        return (scl, err)

    def m_scale(self, row, l):
        pt = getattr(row, "%sPt" % l)
        eta = getattr(row, "%sEta" % l)
        global_bin = self.m_hist.FindBin(pt, eta)
        scl = self.m_hist.GetBinContent(global_bin)
        err = self.m_hist.GetBinError(global_bin)

        if scl < 0.1:
            scl = 1.0
            err = 0.0

        return (scl, err)

    def close(self):
        self.e_rtfile.Close()
        self.m_rtfile.Close()
