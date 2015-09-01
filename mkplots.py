from plotters.plotter import Plotter
import sys
from numpy import linspace

_4L_MASSES = [110, 130, 150, 170, 200, 250, 300,
              350, 400, 450, 500, 600, 700]


#_TITLE=r'\textbf{CMS} \emph{Preliminary} \hspace{1.9in} 19.7 fb$^{-1}$ (8 TeV)'
_TITLE=r'\textbf{Belknap PhD Thesis} \hspace{1.5in} 19.7 fb$^{-1}$ (8 TeV)'


def signal_shapes():
    plotter = Plotter("DblH", "(mass > 0)", "./ntuples", "./plots/thesis/4l",
                      channels=["dblh4l"], lumi=19.7)

    masses = _4L_MASSES

    colors = [(i,0,0) for i in linspace(0,1,len(_4L_MASSES))]

    for i, mass in enumerate(masses):
        plotter.add_group("hpp%i" % mass, r"$\Phi^{++}(%i)$" % mass,
                "HPlus*%i*" % mass, edgecolor=colors[i])

    order = ["hpp%i" % mass for mass in masses]
    plotter.stack_order(*order)

    plotter.plot_compare('h1masses.pdf', 'h1mass', 200, 0, 1000,
            title=_TITLE,
            xlab=r'$M_{\ell^+\ell^+}$ (GeV)',
            ylab=r'A.U.', log=False, legend_size=10)

    plotter2 = Plotter("DblH", "(mass > 0)", "./ntuples", "./plots/4l",
                      channels=["dblh4l"], lumi=19.7)

    plotter2.add_group("hpp500", r"$\Phi^{++}(500)$",
                "HPlus*500*", edgecolor=(1,0,0))

    plotter2.stack_order("hpp500")

    plotter2.plot_compare('h1500.pdf', 'h1mass', 200, 300, 700,
            title=_TITLE,
            xlab=r'$M_{\ell^+\ell^+}$ (GeV)',
            ylab=r'A.U.', log=False,
            shade=[(450.0, 550.0, 'r')])

def two_D():
    plotter = Plotter("DblH", "(mass > 0)", "./ntuples", "./plots/4l",
                      channels=["dblh4l"], lumi=19.7, partial_blind=False)

    plotter.add_group("hpp", r"$\Phi^{++}(500)$", "HPlus*500*",
                      facecolor='mediumorchid', edgecolor='indigo')

    plotter.add_group("zz", "$ZZ$", "ZZTo*", "ggZZ*",
                      facecolor="lightskyblue", edgecolor="darkblue")

    plotter.stack_order("hpp")

    plotter.plot_2D("h1h2.pdf", "h1mass", "h2mass", 50, 50, 300, 700, 300, 700,
            title=_TITLE,
            xlab=r"$M(\ell^+\ell^+)$ (GeV)",
            ylab=r"$M(\ell^-\ell^-)$ (GeV)")


def four_l():
    MASS = 500
    plotter = Plotter("DblH", "(mass > 0)", "./ntuples", "./plots/thesis/4l",
                      channels=["dblh4l"], lumi=19.7, partial_blind=False)

    plotter.add_group("hpp", r"$\Phi^{++}(%s)$" % MASS, "HPlus*%s*" % MASS,
                      facecolor='mediumorchid', edgecolor='indigo')

    plotter.add_group("dyjets", "Z+Jets", "DYJets*",
                      facecolor="orange", edgecolor="darkorange")

    plotter.add_group("top", r"$t/t\bar{t}$", "T*",
                      facecolor="mediumseagreen", edgecolor="darkgreen")

    plotter.add_group("zz", "$ZZ$", "ZZTo*", "ggZZ*",
                      facecolor="lightskyblue", edgecolor="darkblue")

    plotter.add_group("wwv", "$WWV$", "WW[WZ]*",
                      facecolor="tomato", edgecolor="red")

    plotter.add_group("ttv", r"$t\bar{t}V$", "TT[WZ]*",
                      facecolor="springgreen", edgecolor="seagreen")

    plotter.add_group("data", "Observed", "data_*", isdata=True)

    plotter.stack_order("ttv", "wwv", "dyjets", "top", "zz", "hpp")
    #plotter.stack_order("hpp","zz","top")

    plotter.plot_stack('h1mass.pdf', 'h1mass', 25, 0, 625,
            title=_TITLE,
            xlab=r'$M_{\ell^+\ell^+}$ (GeV)',
            label_bin_width=True, log=True)

    #plotter.plot_stack('z_sep_%i.png' % MASS, 'z_sep', 25, 0, 500,
    #        title=_TITLE,
    #        xlab=r'$\min(M(\ell^+\ell^-)- M_Z)$ (GeV)',
    #        label_bin_width=True, log=True,
    #        shade=[(0.0, 80.0, 'k')])

    #st_cut = '(%f < sT)' % (0.6*MASS + 130.0)

    #plotter.plot_stack('z_sep_st_%i.png' % MASS, 'z_sep', 25, 0, 500,
    #        cuts= st_cut,
    #        title=_TITLE,
    #        xlab=r'$\min(M(\ell^+\ell^-)- M_Z)$ (GeV)',
    #        label_bin_width=True, log=True,
    #        shade=[(0.0, 80.0, 'k')])

    #mass_cut = '(%f < h1mass) & (h1mass < %f) & (%f < h2mass) & (h2mass < %f)' % (0.9*MASS, 1.1*MASS, 0.9*MASS, 1.1*MASS)

    #plotter.plot_stack('z_sep_st_mass_%i.png' % MASS, 'z_sep', 25, 0, 500,
    #        cuts='%s & %s' % (st_cut, mass_cut),
    #        title=_TITLE,
    #        xlab=r'$\min(M(\ell^+\ell^-)- M_Z)$ (GeV)',
    #        label_bin_width=True, log=False,
    #        shade=[(0.0, 80.0, 'k')])

    #plotter.plot_stack('dphi1.pdf', 'dPhi1', 25, -4, 4,
    #        title=_TITLE,
    #        xlab=r'$\Delta\phi_1$',
    #        label_bin_width=True, log=False)

    #plotter.plot_stack('dphi2.pdf', 'dPhi2', 25, -4, 4,
    #        title=_TITLE,
    #        xlab=r'$\Delta\phi_2$',
    #        label_bin_width=True, log=False)

    #plotter.plot_stack('st1.pdf', 'sT1', 25, 0, 600,
    #        title=_TITLE,
    #        xlab=r'$s_T(\Phi^{++})$ (GeV)',
    #        label_bin_width=True, log=True)

    #plotter.plot_stack('st2.pdf', 'sT2', 25, 0, 600,
    #        title=_TITLE,
    #        xlab=r'$s_T(\Phi^{--})$ (GeV)',
    #        label_bin_width=True, log=True)

    plotter.plot_stack('st.pdf', 'sT', 25, 0, 2000,
            title=_TITLE,
            xlab=r'$s_T$ (GeV)',
            label_bin_width=True, log=True)

    plotter.plot_stack('sideband.pdf', 'h1mass', 24, 0, 600,
            title=_TITLE,
            xlab=r'$M_{\ell^+\ell^+}$ (GeV)',
            label_bin_width=True, log=True, legend_loc='upper right', legend_size=12,
            shade=[(450.0, 550.0, 'r'),(12.0,450.0,'k'),(550.0,700.,'k')])

def four_l_em():
    channels = ["emem"]
    tmp = ["(channel == '%s')" % c for c in channels]
    cut = "((%s))" % (" | ".join(tmp))

    plotter = Plotter("DblH", cut, "./ntuples", "./plots/4l_em",
                      channels=["dblh4l"], lumi=19.7, partial_blind=True)

    plotter.add_group("hpp", r"$\Phi^{++}(450)$", "HPlus*450*",
                      facecolor='mediumorchid', edgecolor='indigo')

    plotter.add_group("dyjets", "Z+Jets", "DYJets*",
                      facecolor="orange", edgecolor="darkorange")

    plotter.add_group("top", "Top", "T*",
                      facecolor="mediumseagreen", edgecolor="darkgreen")

    plotter.add_group("zz", "ZZ", "ZZTo*", "ggZZ*",
                      facecolor="lightskyblue", edgecolor="darkblue")

    plotter.add_group("wwv", "WWV", "WW[WZ]*",
                      facecolor="tomato", edgecolor="red")

    plotter.add_group("ttv", "TTV", "TT[WZ]*",
                      facecolor="springgreen", edgecolor="seagreen")

    #plotter.add_group("data", "Observed", "data_*", isdata=True)

    plotter.stack_order("zz", "hpp")

    plotter.plot_stack('h1mass_emem.pdf', 'h1mass', 25, 0, 500,
            title=_TITLE,
            xlab=r'$M_{\ell^+\ell^+}$ (GeV)',
            label_bin_width=True, log=True)

def cut_flow():
    MASS =500
    plotter = Plotter("DblH", "(mass > 0)", "./ntuples", "./plots/thesis/4l",
                      channels=["dblh4l"], lumi=19.7)

    plotter.add_group("hpp", r"$\Phi^{++}(%s)$" % MASS, "HPlus*%s*" % MASS,
                      facecolor='mediumorchid', edgecolor='indigo')
    plotter.add_group("dyjets", "Z+Jets", "DYJets*",
                      facecolor="orange", edgecolor="darkorange")
    plotter.add_group("top", "Top", "T*",
                      facecolor="mediumseagreen", edgecolor="darkgreen")
    plotter.add_group("zz", "$ZZ$", "ZZTo*", "ggZZ*",
                      facecolor="lightskyblue", edgecolor="darkblue")
    plotter.add_group("wwv", "$WWV$", "WW[WZ]*",
                      facecolor="tomato", edgecolor="red")
    plotter.add_group("ttv", r"$t\bar{t}V$", "TT[WZ]*",
                      facecolor="springgreen", edgecolor="seagreen")

    plotter.add_group("data", "Observed", "data_*", isdata=True)

    plotter.stack_order("ttv", "wwv", "top", "dyjets", "zz", "hpp")
    #plotter.stack_order("zz", "hpp")
    #plotter.stack_order("top", "dyjets", "zz", "hpp")

    cuts = ["(True)",
            "(%f < sT)" % (0.6*MASS + 130.),
            "(%f < sT) & (%f < h1mass) & (h1mass < %f) & (%f < h2mass) & (h2mass < %f)" % ((0.6*MASS + 130.), 0.9*MASS, 1.1*MASS, 0.9*MASS, 1.1*MASS)]

    labels = ["Preselection",
              "sT",
              "Mass Window"]

    plotter.cut_flow("cut_flow.pdf", cuts, labels, log=True,
            title=_TITLE, legend_loc='lower left')


def control():
    plotter = Plotter("DblH", "(mass > 0)", "./ntuples", "./plots/ctrl",
                      channels=["dblh4l_control"], lumi=19.7)

    #plotter.add_group("hpp", "HPP", "HPlus*450*",
    #                  facecolor='mediumorchid', edgecolor='indigo')
    #plotter.add_group("zz", "ZZ", "ZZTo*",
    #                  facecolor='lightskyblue', edgecolor='darkblue')
    plotter.add_group("dyjets", r"Z+Jets", "Z[1234]jets*",
                      facecolor='orange', edgecolor='darkorange')
    plotter.add_group("top", "Top", "TTJets*",
                      facecolor='mediumseagreen', edgecolor='darkgreen')

    plotter.add_group("data", "Observed", "data_*", isdata=True)

    plotter.stack_order("top","dyjets")

    plotter.plot_stack('h1mass.pdf', 'h1mass', 25, 0, 500,
            #title=_TITLE,
            #xlab=r'$M_{\ell^+\ell^+}$ (GeV)',
            title='sqrt(s)= 8 TeV, L = 19.7 fb-1',
            xlab='M(++) (GeV)',
            label_bin_width=True, log=True)

    #plotter.plot_stack('st1.pdf', 'sT1', 25, 0, 500,
    #        title=_TITLE,
    #        xlab=r'$s_T(\Phi^{++})$ (GeV)',
    #        label_bin_width=True, log=True)

    #plotter.plot_stack('st2.pdf', 'sT2', 25, 0, 500,
    #        title=_TITLE,
    #        xlab=r'$s_T(\Phi^{--})$ (GeV)',
    #        label_bin_width=True, log=True)

    plotter.plot_stack('st.pdf', 'sT', 25, 0, 500,
            #title=_TITLE,
            #xlab=r'$s_T$ (GeV)',
            title='sqrt(s)= 8 TeV, L = 19.7 fb-1',
            xlab='sT (GeV)',
            label_bin_width=True, log=True)

def tt_control():
    cut = '(sT > 150) & (met > 30)'
    plotter = Plotter("DblH", cut, "./ntuples", "./plots/thesis/tt_ctrl",
                      channels=["dblh4l_tt_control"], lumi=19.7)

    plotter.add_group("dyjets", r"Z+Jets", "Z[1234]jets*",
                      facecolor='orange', edgecolor='darkorange')

    plotter.add_group("tt", r"$t\bar{t}$", "TTJets*",
                      facecolor='mediumseagreen', edgecolor='darkgreen')

    plotter.add_group("top", "$t$", "T_*", "Tbar_*",
                      facecolor='lightseagreen', edgecolor='seagreen')

    plotter.add_group("wz", "$WZ$", "WZJets*",
                      facecolor='mediumpurple', edgecolor='midnightblue')

    plotter.add_group("wwv", "$WWV$", "WW[WZ]*",
                      facecolor="tomato", edgecolor="red")

    plotter.add_group("ttv", r"$t\bar{t}V$", "TT[WZ]*",
                      facecolor="springgreen", edgecolor="seagreen")

    plotter.add_group("data", "Observed", "data_*", isdata=True)

    plotter.stack_order("ttv", "wwv", "wz", "top", "tt", "dyjets")

    plotter.plot_stack('h1mass.pdf', 'h1mass', 10, 0, 800,
            title=_TITLE,
            xlab=r'$M_{\ell^+\ell^+}$ (GeV)',
            label_bin_width=True, log=False, mc_bands=0.3)

    plotter.plot_stack('st.pdf', 'sT', 10, 0, 800,
            title=_TITLE,
            xlab=r'$s_T$ (GeV)',
            label_bin_width=True, log=False, mc_bands=0.3)

    #plotter.plot_stack('met.pdf', 'met', 10, 0, 400,
    #        title=_TITLE,
    #        xlab=r'$E_T^{miss}$ (GeV)',
    #        label_bin_width=True, log=True)

    #plotter.plot_stack('st1.pdf', 'sT1', 10, 0, 400,
    #        title=_TITLE,
    #        xlab=r'$s_T(\Phi^{++})$ (GeV)',
    #        label_bin_width=True, log=True)

    #plotter.plot_stack('st2.pdf', 'sT2', 10, 0, 400,
    #        title=_TITLE,
    #        xlab=r'$s_T(\Phi^{--})$ (GeV)',
    #        label_bin_width=True, log=True)

def z_control():
    channels = ["eemm","mmee","emme","meem","emem","meme","mmmm","eeee"]
    tmp = ["channel == '%s'" % c for c in channels]
    #cut = '(sT > 150) & ((%s))' % (") | (".join(tmp))
    cut = '(sT > 50) & ((%s))' % (") | (".join(tmp))
    #cut += '& (l1Pt > 15)'
    #cut += '& (l2Pt > 15)'
    #cut += '& (l3Pt > 15)'
    #cut += '& (l4Pt > 15)'

    plotter = Plotter("DblH", cut, "./ntuples", "./plots/thesis/z_ctrl",
                      channels=["dblh4l_z_control"], lumi=19.7)

    plotter.add_group("dyjets", r"Z+Jets", "Z[1234]jets*",
                      facecolor='orange', edgecolor='darkorange')

    plotter.add_group("ggH", "$H(125)$", "GluGlu*125*",
                      facecolor='lightcoral', edgecolor='maroon')

    plotter.add_group("top", r"$t/t\bar{t}$", "TTJets*", "T_*", "Tbar_*",
                      facecolor='mediumseagreen', edgecolor='darkgreen')

    plotter.add_group("zz", "$ZZ$", "ZZTo*", #"ggZZ*",
                      facecolor='lightskyblue', edgecolor='darkblue')

    plotter.add_group("ggzz", "$ZZ(gg)$", "ggZZ*",
                      facecolor='deepskyblue', edgecolor='navy')

    plotter.add_group("wz", "$WZ$", "WZJets*",
                      facecolor='mediumpurple', edgecolor='midnightblue')

    plotter.add_group("wwv", "$WWV$", "WW[WZ]*",
                      facecolor="tomato", edgecolor="red")

    plotter.add_group("ttv", r"$t\bar{t}V$", "TT[WZ]*",
                      facecolor="springgreen", edgecolor="seagreen")

    plotter.add_group("data", "Observed", "data_*", isdata=True)

    plotter.stack_order("ttv", "wwv", "wz", "top", "dyjets", "ggH", "zz", "ggzz")

    plotter.plot_stack('h1mass.pdf', 'h1mass', 20, 0, 500,
            title=_TITLE,
            xlab=r'$M_{\ell^+\ell^+}$ (GeV)',
            mc_bands=0.1, cuts="(sT > 150)",
            label_bin_width=True, log=False)#, legend_size=10)

    #plotter.plot_stack('h1mass_binned.pdf', 'h1mass', 25, 0, 500,
    #        title=_TITLE,
    #        xlab=r'$M_{\ell^+\ell^+}$ (GeV)',
    #        label_bin_width=True, log=False)

    plotter.plot_stack('st.pdf', 'sT', 20, 0, 500,
            title=_TITLE,
            xlab=r'$s_T$ (GeV)',
            mc_bands=0.1,
            label_bin_width=True, log=False,#legend_size=10,
            shade=[(0, 150.0, 'b')])

    #plotter.plot_stack('met.pdf', 'met', 20, 0, 500,
    #        title=_TITLE,
    #        xlab=r'$E_T^{miss}$ (GeV)',
    #        label_bin_width=True, log=False)

    #plotter.plot_stack('st1.pdf', 'sT1', 20, 0, 500,
    #        title=_TITLE,
    #        xlab=r'$s_T(\Phi^{++})$ (GeV)',
    #        label_bin_width=True, log=False)

    #plotter.plot_stack('st2.pdf', 'sT2', 20, 0, 500,
    #        title=_TITLE,
    #        xlab=r'$s_T(\Phi^{--})$ (GeV)',
    #        label_bin_width=True, log=False)

    #plotter.plot_stack('l1pt.pdf', 'l1Pt', 20, 0, 100,
    #        title=_TITLE,
    #        xlab=r'$p_T(\ell_1)$ (GeV)',
    #        label_bin_width=True, log=False)

    #plotter.plot_stack('l2pt.pdf', 'l2Pt', 20, 0, 100,
    #        title=_TITLE,
    #        xlab=r'$p_T(\ell_2)$ (GeV)',
    #        label_bin_width=True, log=False)

    #plotter.plot_stack('l3pt.pdf', 'l3Pt', 20, 0, 100,
    #        title=_TITLE,
    #        xlab=r'$p_T(\ell_3)$ (GeV)',
    #        label_bin_width=True, log=False)

    #plotter.plot_stack('l4pt.pdf', 'l4Pt', 20, 0, 100,
    #        title=_TITLE,
    #        xlab=r'$p_T(\ell_4)$ (GeV)',
    #        label_bin_width=True, log=False)

    #plotter.plot_stack('l1eta.pdf', 'l1Eta', 20, -2.5, 2.5,
    #        title=_TITLE,
    #        xlab=r'$\eta(\ell_1)$ (GeV)',
    #        label_bin_width=True, log=False)

    #plotter.plot_stack('l2eta.pdf', 'l2Eta', 20, -2.5, 2.5,
    #        title=_TITLE,
    #        xlab=r'$\eta(\ell_2)$ (GeV)',
    #        label_bin_width=True, log=False)

    #plotter.plot_stack('l3eta.pdf', 'l3Eta', 20, -2.5, 2.5,
    #        title=_TITLE,
    #        xlab=r'$\eta(\ell_3)$ (GeV)',
    #        label_bin_width=True, log=False)

    #plotter.plot_stack('l4eta.pdf', 'l4Eta', 20, -2.5, 2.5,
    #        title=_TITLE,
    #        xlab=r'$\eta(\ell_4)$ (GeV)',
    #        label_bin_width=True, log=False)

def zz_smp_m4l():
    channels = ["eeee", "mmmm", "eemm", "mmee"]
    #channels = ["eeee"]
    #channels = ["mmmm"]
    #channels = ["eemm", "mmee"]
    cuts = "(100 < mass)"
    cuts += "& (60 < z1mass) & (z1mass < 120)"
    cuts += "& (60 < z2mass) & (z2mass < 120)"
    cuts += "& (%s)" % ' | '.join(['(channel == "%s")' % c for c in channels])

    plotter = Plotter("ZZ4l", cuts, "./ntuples", "./plots/zz/smp",
                      channels=["zz4l"], lumi=19.7)

    plotter.add_group("zz", "ZZ", "ZZTo*",
                      facecolor='lightskyblue', edgecolor='darkblue')
    plotter.add_group("ggzz", "ZZ(gg)", "ggZZ*",
                      facecolor='deepskyblue', edgecolor='navy')

    plotter.add_group("data", "Observed", "data_*", isdata=True)

    plotter.stack_order("zz", "ggzz")

    plotter.plot_stack('m4l.pdf', 'mass', 36, 100, 1000,
            title=_TITLE,
            xlab=r'm(4l) (GeV)',
            label_bin_width=True, log=False)


def zz_4mu():
    channels = ["mmmm"]
    tmp = ["channel == '%s'" % c for c in channels]
    cut = "(mass > 0) & (40 < z1mass) & (z1mass < 120) & (12 < z2mass) & (z2mass < 120) & ((%s))" % (") | (".join(tmp))

    plotter = Plotter("ZZ4l", cut, "./ntuples", "./plots/thesis/zz/4mu",
                      channels=["zz4l"], lumi=19.7)

    plotter.add_group("zz", r"$ZZ$", "ZZTo*", "ggZZ*",
                      facecolor='lightskyblue', edgecolor='darkblue')
    #plotter.add_group("dyjets", "Z+Jets", "Z[1234]jets*",
    #                  facecolor='orange', edgecolor='darkorange')
    plotter.add_group("ggH", r"$H(125)$", "GluGlu*125*",
                      facecolor='lightcoral', edgecolor='maroon')

    plotter.add_group("data", "Observed", "data_*", isdata=True)

    plotter.stack_order("zz", "ggH")

    #plotter.add_group("top", "Top", "TTJets*", "T_*", "Tbar_*",
    #                  facecolor='mediumseagreen', edgecolor='darkgreen')
    #plotter.add_group("zz", "ZZ", "ZZTo*",
    #                  facecolor='lightskyblue', edgecolor='darkblue')
    #plotter.add_group("wz", "WZ", "WZJets*",
    #                  facecolor='mediumpurple', edgecolor='midnightblue')
    #plotter.add_group("wwv", "WWV", "WW[WZ]*",
    #                  facecolor="tomato", edgecolor="red")
    #plotter.add_group("ttv", "TTV", "TT[WZ]*",
    #                  facecolor="springgreen", edgecolor="seagreen")
    #plotter.add_group("dyjets", "Z+Jets", "Z[1234]jets*",
    #                  facecolor='orange', edgecolor='darkorange')
    #plotter.add_group("ggH", "H(125)", "GluGlu*125*",
    #                  facecolor='lightcoral', edgecolor='maroon')

    #plotter.add_group("data", "Observed", "data_*", isdata=True)

    #plotter.stack_order("top","wz","wwv","ttv","dyjets","zz","ggH")

    plotter.plot_stack('st.pdf', 'sT', 50, 0, 500,
            title=_TITLE,
            xlab=r'$s_T$ (GeV)',
            label_bin_width=True, log=False)

    plotter.plot_stack('m4l.pdf', 'mass', 50, 0, 500,
            title=_TITLE,
            xlab=r'$M_{4\ell}$ (GeV)',
            label_bin_width=True, log=False)

    plotter.plot_stack('mz1.pdf', 'z1mass', 30, 60, 120,
            title=_TITLE,
            xlab=r'$M_{Z_1}$ (GeV)',
            label_bin_width=True, log=False)

    plotter.plot_stack('mz2.pdf', 'z2mass', 30, 60, 120,
            title=_TITLE,
            xlab=r'$M_{Z_2}$ (GeV)',
            label_bin_width=True, log=False)

    plotter.plot_stack('l1pt.pdf', 'l1Pt', 20, 0, 100,
            title=_TITLE,
            xlab=r'$p_T(\ell_1)$ (GeV)',
            label_bin_width=True, log=False)

    plotter.plot_stack('l2pt.pdf', 'l2Pt', 20, 0, 100,
            title=_TITLE,
            xlab=r'$p_T(\ell_2)$ (GeV)',
            label_bin_width=True, log=False)

    plotter.plot_stack('l3pt.pdf', 'l3Pt', 20, 0, 100,
            title=_TITLE,
            xlab=r'$p_T(\ell_3)$ (GeV)',
            label_bin_width=True, log=False)

    plotter.plot_stack('l4pt.pdf', 'l4Pt', 20, 0, 100,
            title=_TITLE,
            xlab=r'$p_T(\ell_4)$ (GeV)',
            label_bin_width=True, log=False)

    plotter.plot_stack('l1eta.pdf', 'l1Eta', 20, -2.5, 2.5,
            title=_TITLE,
            xlab=r'$\eta(\ell_1)$ (GeV)',
            label_bin_width=True, log=False)

    plotter.plot_stack('l2eta.pdf', 'l2Eta', 20, -2.5, 2.5,
            title=_TITLE,
            xlab=r'$\eta(\ell_2)$ (GeV)',
            label_bin_width=True, log=False)

    plotter.plot_stack('l3eta.pdf', 'l3Eta', 20, -2.5, 2.5,
            title=_TITLE,
            xlab=r'$\eta(\ell_3)$ (GeV)',
            label_bin_width=True, log=False)

    plotter.plot_stack('l4eta.pdf', 'l4Eta', 20, -2.5, 2.5,
            title=_TITLE,
            xlab=r'$\eta(\ell_4)$ (GeV)',
            label_bin_width=True, log=False)

def zz_4e():
    channels = ["eeee"]
    tmp = ["channel == '%s'" % c for c in channels]
    cut = "(mass > 0) & (40 < z1mass) & (z1mass < 120) & (12 < z2mass) & (z2mass < 120) & ((%s))" % (") | (".join(tmp))
    print cut

    plotter = Plotter("ZZ4l", cut, "./ntuples", "./plots/thesis/zz/4e",
                      channels=["zz4l"], lumi=19.7)

    plotter.add_group("zz", r"$ZZ$", "ZZTo*", "ggZZ*",
                      facecolor='lightskyblue', edgecolor='darkblue')
    plotter.add_group("dyjets", "Z+Jets", "Z[1234]jets*",
                      facecolor='orange', edgecolor='darkorange')
    plotter.add_group("ggH", r"$H(125)$", "GluGlu*125*",
                      facecolor='lightcoral', edgecolor='maroon')

    plotter.add_group("data", "Observed", "data_*", isdata=True)

    plotter.stack_order("zz", "ggH")
    #plotter.add_group("top", "Top", "TTJets*", "T_*", "Tbar_*",
    #                  facecolor='mediumseagreen', edgecolor='darkgreen')
    #plotter.add_group("zz", "ZZ", "ZZTo*",
    #                  facecolor='lightskyblue', edgecolor='darkblue')
    #plotter.add_group("wz", "WZ", "WZJets*",
    #                  facecolor='mediumpurple', edgecolor='midnightblue')
    #plotter.add_group("wwv", "WWV", "WW[WZ]*",
    #                  facecolor="tomato", edgecolor="red")
    #plotter.add_group("ttv", "TTV", "TT[WZ]*",
    #                  facecolor="springgreen", edgecolor="seagreen")
    #plotter.add_group("dyjets", "Z+Jets", "Z[1234]jets*",
    #                  facecolor='orange', edgecolor='darkorange')
    #plotter.add_group("ggH", "H(125)", "GluGlu*125*",
    #                  facecolor='lightcoral', edgecolor='maroon')

    #plotter.add_group("data", "Observed", "data_*", isdata=True)

    #plotter.stack_order("top","wz","wwv","ttv","dyjets","zz","ggH")

    plotter.plot_stack('st.pdf', 'sT', 50, 0, 500,
            title=_TITLE,
            xlab=r'$s_T$ (GeV)',
            label_bin_width=True, log=False)

    plotter.plot_stack('m4l.pdf', 'mass', 50, 0, 500,
            title=_TITLE,
            xlab=r'$M_{4\ell}$ (GeV)',
            label_bin_width=True, log=False)

    plotter.plot_stack('mz1.pdf', 'z1mass', 30, 60, 120,
            title=_TITLE,
            xlab=r'$M_{Z_1}$ (GeV)',
            label_bin_width=True, log=False)

    plotter.plot_stack('mz2.pdf', 'z2mass', 30, 60, 120,
            title=_TITLE,
            xlab=r'$M_{Z_2}$ (GeV)',
            label_bin_width=True, log=False)

    plotter.plot_stack('l1pt.pdf', 'l1Pt', 20, 0, 100,
            title=_TITLE,
            xlab=r'$p_T(\ell_1)$ (GeV)',
            label_bin_width=True, log=False)

    plotter.plot_stack('l2pt.pdf', 'l2Pt', 20, 0, 100,
            title=_TITLE,
            xlab=r'$p_T(\ell_2)$ (GeV)',
            label_bin_width=True, log=False)

    plotter.plot_stack('l3pt.pdf', 'l3Pt', 20, 0, 100,
            title=_TITLE,
            xlab=r'$p_T(\ell_3)$ (GeV)',
            label_bin_width=True, log=False)

    plotter.plot_stack('l4pt.pdf', 'l4Pt', 20, 0, 100,
            title=_TITLE,
            xlab=r'$p_T(\ell_4)$ (GeV)',
            label_bin_width=True, log=False)

    plotter.plot_stack('l1eta.pdf', 'l1Eta', 20, -2.5, 2.5,
            title=_TITLE,
            xlab=r'$\eta(\ell_1)$ (GeV)',
            label_bin_width=True, log=False)

    plotter.plot_stack('l2eta.pdf', 'l2Eta', 20, -2.5, 2.5,
            title=_TITLE,
            xlab=r'$\eta(\ell_2)$ (GeV)',
            label_bin_width=True, log=False)

    plotter.plot_stack('l3eta.pdf', 'l3Eta', 20, -2.5, 2.5,
            title=_TITLE,
            xlab=r'$\eta(\ell_3)$ (GeV)',
            label_bin_width=True, log=False)

    plotter.plot_stack('l4eta.pdf', 'l4Eta', 20, -2.5, 2.5,
            title=_TITLE,
            xlab=r'$\eta(\ell_4)$ (GeV)',
            label_bin_width=True, log=False)


def zz_2e2mu():
    channels = ["eemm", "mmee"]
    tmp = ["channel == '%s'" % c for c in channels]
    cut = "(mass > 0) & (40 < z1mass) & (z1mass < 120) & (12 < z2mass) & (z2mass < 120) & ((%s))" % (") | (".join(tmp))

    plotter = Plotter("ZZ4l", cut, "./ntuples", "./plots/thesis/zz/2e2mu",
                      channels=["zz4l"], lumi=19.7)

    plotter.add_group("zz", r"$ZZ$", "ZZTo*", "ggZZ*",
                      facecolor='lightskyblue', edgecolor='darkblue')

    plotter.add_group("ggH", r"$H(125)$", "GluGlu*125*",
                      facecolor='lightcoral', edgecolor='maroon')

    plotter.add_group("data", "Observed", "data_*", isdata=True)

    plotter.stack_order("zz", "ggH")

    plotter.plot_stack('m4l.pdf', 'mass', 50, 0, 500,
            title=_TITLE,
            xlab=r'$M_{4l}$ (GeV)',
            label_bin_width=True, log=False)


def zz_all():
    channels = ["eeee", "mmmm", "eemm", "mmee"]
    tmp = ["channel == '%s'" % c for c in channels]
    cut = "(0 < mass) & (40 < z1mass) & (z1mass < 120) & (12 < z2mass) & (z2mass < 120) & ((%s))" % (") | (".join(tmp))

    plotter = Plotter("ZZ4l", cut, "./ntuples", "./plots/thesis/zz/all",
                      channels=["zz4l"], lumi=19.7)

    plotter.add_group("top", "Top", "TTJets*", "T_*", "Tbar_*",
                      facecolor='mediumseagreen', edgecolor='darkgreen')
    plotter.add_group("zz", r"$ZZ$", "ZZTo*", "ggZZ*",
                      facecolor='lightskyblue', edgecolor='darkblue')
    plotter.add_group("wz", "WZ", "WZJets*",
                      facecolor='mediumpurple', edgecolor='midnightblue')
    plotter.add_group("wwv", "WWV", "WW[WZ]*",
                      facecolor="tomato", edgecolor="red")
    plotter.add_group("ttv", "TTV", "TT[WZ]*",
                      facecolor="springgreen", edgecolor="seagreen")
    plotter.add_group("dyjets", "Z+Jets", "Z[1234]jets*",
                      facecolor='orange', edgecolor='darkorange')
    plotter.add_group("ggH", r"$H(125)$", "GluGlu*125*",
                      facecolor='lightcoral', edgecolor='maroon')

    plotter.add_group("data", "Observed", "data_*", isdata=True)

    plotter.stack_order("zz","ggH")

    plotter.plot_stack('m4l.pdf', 'mass', 50, 0, 500,
            title=_TITLE,
            xlab=r'$M_{4\ell}$ (GeV)',
            label_bin_width=True, log=False)

    plotter.plot_stack('st.pdf', 'sT', 50, 0, 500,
            title=_TITLE,
            xlab=r'$s_T$ (GeV)',
            label_bin_width=True, log=False)

    plotter.plot_stack('mz1.pdf', 'z1mass', 30, 60, 120,
            title=_TITLE,
            xlab=r'$M_{Z_1}$ (GeV)',
            label_bin_width=True, log=False)

    plotter.plot_stack('mz2.pdf', 'z2mass', 30, 60, 120,
            title=_TITLE,
            xlab=r'$M_{Z_2}$ (GeV)',
            label_bin_width=True, log=False)

    plotter.plot_stack('l1pt.pdf', 'l1Pt', 20, 0, 100,
            title=_TITLE,
            xlab=r'$p_T(\ell_1)$ (GeV)',
            label_bin_width=True, log=False)

    plotter.plot_stack('l2pt.pdf', 'l2Pt', 20, 0, 100,
            title=_TITLE,
            xlab=r'$p_T(\ell_2)$ (GeV)',
            label_bin_width=True, log=False)

    plotter.plot_stack('l3pt.pdf', 'l3Pt', 20, 0, 100,
            title=_TITLE,
            xlab=r'$p_T(\ell_3)$ (GeV)',
            label_bin_width=True, log=False)

    plotter.plot_stack('l4pt.pdf', 'l4Pt', 20, 0, 100,
            title=_TITLE,
            xlab=r'$p_T(\ell_4)$ (GeV)',
            label_bin_width=True, log=False)

    plotter.plot_stack('l1eta.pdf', 'l1Eta', 20, -2.5, 2.5,
            title=_TITLE,
            xlab=r'$\eta(\ell_1)$ (GeV)',
            label_bin_width=True, log=False)

    plotter.plot_stack('l2eta.pdf', 'l2Eta', 20, -2.5, 2.5,
            title=_TITLE,
            xlab=r'$\eta(\ell_2)$ (GeV)',
            label_bin_width=True, log=False)

    plotter.plot_stack('l3eta.pdf', 'l3Eta', 20, -2.5, 2.5,
            title=_TITLE,
            xlab=r'$\eta(\ell_3)$ (GeV)',
            label_bin_width=True, log=False)

    plotter.plot_stack('l4eta.pdf', 'l4Eta', 20, -2.5, 2.5,
            title=_TITLE,
            xlab=r'$\eta(\ell_4)$ (GeV)',
            label_bin_width=True, log=False)


def zz_powheg_breakdown():
    channels = ["eeee", "mmmm", "eemm", "mmee"]
    tmp = ["channel == '%s'" % c for c in channels]
    cut = "(0 < mass) & (60 < z1mass) & (z1mass < 120) & (60 < z2mass) & (z2mass < 120) & ((%s))" % (") | (".join(tmp))
    #cut = "(0 < mass) & (60 < z1mass) & (z1mass < 120) & (60 < z2mass) & (z2mass < 120)"

    plotter = Plotter("ZZ4l", cut, "./ntuples", "./plots/zz/powheg",
                      channels=["zz4l"], lumi=19.7)

    plotter.add_group("4e", "ZZ to 4e", "ZZTo4e*",
                      facecolor='lightskyblue', edgecolor='darkblue')

    plotter.add_group("4mu", "ZZ to 4mu", "ZZTo4mu*",
                      facecolor='lightskyblue', edgecolor='darkblue')

    plotter.add_group("4tau", "ZZ to 4tau", "ZZTo4tau*",
                      facecolor='lightskyblue', edgecolor='darkblue')

    plotter.add_group("2e2mu", "ZZ to 2e2mu", "ZZTo2e2mu*",
                      facecolor='lightskyblue', edgecolor='darkblue')

    plotter.add_group("2e2tau", "ZZ to 2e2tau", "ZZTo2e2tau*",
                      facecolor='lightskyblue', edgecolor='darkblue')

    plotter.add_group("2mu2tau", "ZZ to 2mu2tau", "ZZTo2mu2tau*",
                      facecolor='lightskyblue', edgecolor='darkblue')

    plotter.stack_order("4e")
    plotter.plot_stack('m4l_4e.pdf', 'mass', 50, 0, 500,
            title=_TITLE,
            xlab=r'$M_{4l}$ (GeV)',
            label_bin_width=True, log=False)

    plotter.stack_order("4mu")
    plotter.plot_stack('m4l_4mu.pdf', 'mass', 50, 0, 500,
            title=_TITLE,
            xlab=r'$M_{4l}$ (GeV)',
            label_bin_width=True, log=False)

    #plotter.stack_order("4tau")
    #plotter.plot_stack('m4l_4tau.pdf', 'mass', 50, 0, 500,
    #        title=_TITLE,
    #        xlab=r'$M_{4l}$ (GeV)',
    #        label_bin_width=True, log=False)

    plotter.stack_order("2e2mu")
    plotter.plot_stack('m4l_2e2mu.pdf', 'mass', 50, 0, 500,
            title=_TITLE,
            xlab=r'$M_{4l}$ (GeV)',
            label_bin_width=True, log=False)

    plotter.stack_order("2e2tau")
    plotter.plot_stack('m4l_2e2tau.pdf', 'mass', 50, 0, 500,
            title=_TITLE,
            xlab=r'$M_{4l}$ (GeV)',
            label_bin_width=True, log=False)

    plotter.stack_order("2mu2tau")
    plotter.plot_stack('m4l_2mu2tau.pdf', 'mass', 50, 0, 500,
            title=_TITLE,
            xlab=r'$M_{4l}$ (GeV)',
            label_bin_width=True, log=False)


def zz_breakdown():
    channels = ["eeee", "mmmm", "eemm", "mmee"]
    tmp = ["channel == '%s'" % c for c in channels]
    #cut = "(0 < mass) & (60 < z1mass) & (z1mass < 120) & (60 < z2mass) & (z2mass < 120) & ((%s))" % (") | (".join(tmp))
    cut = "(0 < mass) & (l1Pt > 20) & (l2Pt > 10) & (l3Pt > 10) & (l4Pt < 10) & ((%s))" % (") | (".join(tmp))
    #cut = "(0 < mass) & (60 < z1mass) & (z1mass < 120) & (60 < z2mass) & (z2mass < 120)"

    plotter = Plotter("ZZ4l", cut, "./ntuples", "./plots/zz/powheg",
                      channels=["zz4l"], lumi=19.7)

    plotter.add_group("4e", "ZZ to 4e", "ZZTo4e*",
                      facecolor='mediumseagreen', edgecolor='darkgreen')

    plotter.add_group("4mu", "ZZ to 4mu", "ZZTo4mu*",
                      facecolor='lightskyblue', edgecolor='darkblue')

    plotter.add_group("4tau", "ZZ to 4tau", "ZZTo4tau*",
                      facecolor='mediumpurple', edgecolor='midnightblue')

    plotter.add_group("2e2mu", "ZZ to 2e2mu", "ZZTo2e2mu*",
                      facecolor='tomato', edgecolor='red')

    plotter.add_group("2e2tau", "ZZ to 2e2tau", "ZZTo2e2tau*",
                      facecolor='springgreen', edgecolor='seagreen')

    plotter.add_group("2mu2tau", "ZZ to 2mu2tau", "ZZTo2mu2tau*",
                      facecolor='orange', edgecolor='darkorange')

    plotter.add_group("data", "Observed", "data_*", isdata=True)

    plotter.stack_order("4tau","2e2tau","2mu2tau", "2e2mu", "4e", "4mu")

    plotter.plot_stack('m4l.pdf', 'mass', 50, 0, 500,
            title=_TITLE,
            xlab=r'$M_{4l}$ (GeV)',
            label_bin_width=True, log=False, legend_size=10)

    plotter.plot_stack('mz1.pdf', 'z1mass', 36, 0, 120,
            title=_TITLE,
            xlab=r'$M_{Z_1}$ (GeV)',
            label_bin_width=True, log=False)

    plotter.plot_stack('mz2.pdf', 'z2mass', 36, 0, 120,
            title=_TITLE,
            xlab=r'$M_{Z_2}$ (GeV)',
            label_bin_width=True, log=False)


def main():

    if sys.argv[1] == "zz4mu":
        zz_4mu()
    elif sys.argv[1] == "zz4e":
        zz_4e()
    elif sys.argv[1] == "zz2e2mu":
        zz_2e2mu()
    elif sys.argv[1] == "zz":
        zz_all()
    elif sys.argv[1] == "ctrl":
        control()
    elif sys.argv[1] == "smp":
        zz_smp_m4l()
    elif sys.argv[1] == "tt":
        tt_control()
    elif sys.argv[1] == "z":
        z_control()
    elif sys.argv[1] == "4l":
        four_l()
    elif sys.argv[1] == "2D":
        two_D()
    elif sys.argv[1] == "4l_em":
        four_l_em()
    elif sys.argv[1] == "sigshapes":
        signal_shapes()
    elif sys.argv[1] == "flow":
        cut_flow()
    elif sys.argv[1] == "powheg":
        zz_powheg_breakdown()
    elif sys.argv[1] == "breakdown":
        zz_breakdown()
    else:
        raise ValueError("Incorrect option given: %s" % sys.argv[1])


if __name__ == "__main__":
    main()
