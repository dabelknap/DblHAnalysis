import sys

sys.argv.append('-b')
import ROOT as rt
sys.argv.pop()


class LeptonScaleFactors(object):

    def __init__(self):
        self.e_rtfile = rt.TFile('./lepton_scales/CombinedMethod_ScaleFactors_RecoIdIsoSip.root', 'READ')
        self.e_hist = self.e_rtfile.Get("h_electronScaleFactor_RecoIdIsoSip")

        self.m_rtfile = rt.TFile('./lepton_scales/MuonScaleFactors_2011_2012.root', 'READ')
        self.m_hist = self.m_rtfile.Get("TH2D_ALL_2012")


    def scale_factor(self, row, *lep_list):
        out = 1.0
        for l in lep_list:
            lep_type = l[0]

            if lep_type == 'm':
                out *= self.m_scale(row, l)

            if lep_type == 'e':
                out *= self.e_scale(row, l)

            else:
                raise TypeError("Lepton type %s not recognized" % lep_type)

        return out


    def e_scale(self, row, l):
        pt = getattr(row, "%sPt" % l)
        eta = getattr(row, "%sEta" % l)
        global_bin = self.e_hist.FindBin(pt, eta)
        scl = self.e_hist.GetBinContent(global_bin)

        if scl < 0.1:
            scl = 1.0

        return scl


    def m_scale(self, row, l):
        pt = getattr(row, "%sPt" % l)
        eta = getattr(row, "%sEta" % l)
        global_bin = self.m_hist.FindBin(pt, eta)
        scl = self.m_hist.GetBinContent(global_bin)

        if scl < 0.1:
            scl = 1.0

        return scl


    def close(self):
        self.e_rtfile.Close()
        self.m_rtfile.Close()
