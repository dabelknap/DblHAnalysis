from plotters.plotter import Plotter
import sys
from numpy import linspace

_4L_MASSES = [110, 130, 150, 170, 200, 250, 300,
              350, 400, 450, 500, 600, 700]


def signal_shapes():
    plotter = Plotter("DblH", "(mass > 0)", "./ntuples", "./plots/4l",
                      channels=["dblh4l"], lumi=19.7)

    masses = _4L_MASSES

    colors = [(i,0,0) for i in linspace(0,1,len(_4L_MASSES))]

    for i, mass in enumerate(masses):
        plotter.add_group("hpp%i" % mass, r"$\Phi^{++}(%i)$" % mass,
                "HPlus*%i*" % mass, edgecolor=colors[i])

    order = ["hpp%i" % mass for mass in masses]
    plotter.stack_order(*order)

    plotter.plot_compare('h1masses.png', 'h1mass', 200, 0, 1000,
            title=r'CMS Preliminary $\sqrt{s}=$ 8 TeV, $\mathcal{L}_{int}=$ 19.7 fb$^{-1}$',
            xlab=r'$M_{l^+l^+}$ [GeV]',
            ylab=r'A.U.', log=False)

    plotter2 = Plotter("DblH", "(mass > 0)", "./ntuples", "./plots/4l",
                      channels=["dblh4l"], lumi=19.7)

    plotter2.add_group("hpp500", r"$\Phi^{++}(500)$",
                "HPlus*500*", edgecolor=(1,0,0))

    plotter2.stack_order("hpp500")

    plotter2.plot_compare('h1500.png', 'h1mass', 200, 300, 700,
            title=r'CMS Preliminary $\sqrt{s}=$ 8 TeV, $\mathcal{L}_{int}=$ 19.7 fb$^{-1}$',
            xlab=r'$M_{l^+l^+}$ [GeV]',
            ylab=r'A.U.', log=False,
            shade=[(450.0, 550.0, 'r')])


def four_l():
    plotter = Plotter("DblH", "(mass > 0)", "./ntuples", "./plots/4l",
                      channels=["dblh4l"], lumi=19.7, partial_blind=True)

    plotter.add_group("hpp", r"$\Phi^{++}(250)$", "HPlus*250*",
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

    plotter.add_group("data", "Observed", "data_*", isdata=True)

    plotter.stack_order("ttv", "wwv", "top", "dyjets", "zz", "hpp")

    plotter.plot_stack('h1mass.pdf', 'h1mass', 25, 0, 500,
            title=r'CMS Preliminary $\sqrt{s}=$ 8 TeV, $\mathcal{L}_{int}=$ 19.7 fb$^{-1}$',
            xlab=r'$M_{l^+l^+}$ [GeV]',
            label_bin_width=True, log=False)

    plotter.plot_stack('st1.pdf', 'sT1', 25, 0, 600,
            title=r'CMS Preliminary $\sqrt{s}=$ 8 TeV, $\mathcal{L}_{int}=$ 19.7 fb$^{-1}$',
            xlab=r'$s_T(\Phi^{++})$ [GeV]',
            label_bin_width=True, log=True)

    plotter.plot_stack('st2.pdf', 'sT2', 25, 0, 600,
            title=r'CMS Preliminary $\sqrt{s}=$ 8 TeV, $\mathcal{L}_{int}=$ 19.7 fb$^{-1}$',
            xlab=r'$s_T(\Phi^{--})$ [GeV]',
            label_bin_width=True, log=True)

    plotter.plot_stack('st.pdf', 'sT', 25, 0, 800,
            title=r'CMS Preliminary $\sqrt{s}=$ 8 TeV, $\mathcal{L}_{int}=$ 19.7 fb$^{-1}$',
            xlab=r'$s_T$ [GeV]',
            label_bin_width=True, log=True)

    plotter.plot_stack('sideband.pdf', 'h1mass', 24, 0, 600,
            title=r'CMS Preliminary $\sqrt{s}=$ 8 TeV, $\mathcal{L}_{int}=$ 19.7 fb$^{-1}$',
            xlab=r'$M_{l^+l^+}$ [GeV]',
            label_bin_width=True, log=True,
            shade=[(225.0, 275.0, 'r'),(12.0,225.0,'k'),(275.0,700.,'k')])

def cut_flow():
    plotter = Plotter("DblH", "(mass > 0)", "./ntuples", "./plots/4l",
                      channels=["dblh4l"], lumi=19.7)

    plotter.add_group("hpp", "HPP (500)", "HPlus*500*",
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

    plotter.stack_order("ttv", "wwv", "top", "dyjets", "zz", "hpp")
    #plotter.stack_order("top", "dyjets", "zz", "hpp")

    cuts = ["(True)",
            "(%f < sT)" % (0.6*500 + 130.),
            "(%f < sT) & (%f < h1mass) & (h1mass < %f)" % ((0.6*500 + 130.), 0.9*500, 1.1*500)]

    labels = ["Preselection",
              "sT",
              "Mass Window"]

    plotter.cut_flow("cut_flow.pdf", cuts, labels, log=True,
            title=r'CMS Preliminary $\sqrt{s}=$ 8 TeV, $\mathcal{L}_{int}=$ 19.7 fb$^{-1}$')


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
            #title=r'$\sqrt{s}=$ 8 TeV, $\mathcal{L}_{int}=$ 19.7 $\text{fb}^{-1}$',
            #xlab=r'$M_{l^+l^+}$ [GeV]',
            title='sqrt(s)= 8 TeV, L = 19.7 fb-1',
            xlab='M(++) [GeV]',
            label_bin_width=True, log=True)

    #plotter.plot_stack('st1.pdf', 'sT1', 25, 0, 500,
    #        title=r'$\sqrt{s}=$ 8 TeV, $\mathcal{L}_{int}=$ 19.7 $\text{fb}^{-1}$',
    #        xlab=r'$s_T(\Phi^{++})$ [GeV]',
    #        label_bin_width=True, log=True)

    #plotter.plot_stack('st2.pdf', 'sT2', 25, 0, 500,
    #        title=r'$\sqrt{s}=$ 8 TeV, $\mathcal{L}_{int}=$ 19.7 $\text{fb}^{-1}$',
    #        xlab=r'$s_T(\Phi^{--})$ [GeV]',
    #        label_bin_width=True, log=True)

    plotter.plot_stack('st.pdf', 'sT', 25, 0, 500,
            #title=r'$\sqrt{s}=$ 8 TeV, $\mathcal{L}_{int}=$ 19.7 $\text{fb}^{-1}$',
            #xlab=r'$s_T$ [GeV]',
            title='sqrt(s)= 8 TeV, L = 19.7 fb-1',
            xlab='sT [GeV]',
            label_bin_width=True, log=True)

def tt_control():
    cut = '(sT > 150) & (met > 30)'
    plotter = Plotter("DblH", cut, "./ntuples", "./plots/tt_ctrl",
                      channels=["dblh4l_tt_control"], lumi=19.7)

    plotter.add_group("dyjets", r"Z+Jets", "Z[1234]jets*",
                      facecolor='orange', edgecolor='darkorange')

    plotter.add_group("tt", r"$t\bar{t}$", "TTJets*",
                      facecolor='mediumseagreen', edgecolor='darkgreen')

    plotter.add_group("top", "$t$", "T_*", "Tbar_*",
                      facecolor='lightseagreen', edgecolor='seagreen')

    plotter.add_group("wz", "$WZ$", "WZJets*",
                      facecolor='mediumpurple', edgecolor='midnightblue')

    plotter.add_group("wwv", "WWV", "WW[WZ]*",
                      facecolor="tomato", edgecolor="red")

    plotter.add_group("ttv", "TTV", "TT[WZ]*",
                      facecolor="springgreen", edgecolor="seagreen")

    plotter.add_group("data", "Observed", "data_*", isdata=True)

    plotter.stack_order("ttv", "wwv", "wz", "top", "tt", "dyjets")

    plotter.plot_stack('h1mass.pdf', 'h1mass', 10, 0, 800,
            title=r'CMS Preliminary $\sqrt{s}=$ 8 TeV, $\mathcal{L}_{int}=$ 19.7 fb$^{-1}$',
            xlab=r'$M_{l^+l^+}$ [GeV]',
            label_bin_width=True, log=True)

    plotter.plot_stack('st.pdf', 'sT', 10, 0, 800,
            title=r'CMS Preliminary $\sqrt{s}=$ 8 TeV, $\mathcal{L}_{int}=$ 19.7 fb$^{-1}$',
            xlab=r'$s_T$ [GeV]',
            label_bin_width=True, log=True)

    plotter.plot_stack('met.pdf', 'met', 10, 0, 400,
            title=r'CMS Preliminary $\sqrt{s}=$ 8 TeV, $\mathcal{L}_{int}=$ 19.7 fb$^{-1}$',
            xlab=r'$E_T^{miss}$ [GeV]',
            label_bin_width=True, log=True)

    plotter.plot_stack('st1.pdf', 'sT1', 10, 0, 400,
            title=r'CMS Preliminary $\sqrt{s}=$ 8 TeV, $\mathcal{L}_{int}=$ 19.7 fb$^{-1}$',
            xlab=r'$s_T(\Phi^{++})$ [GeV]',
            label_bin_width=True, log=True)

    plotter.plot_stack('st2.pdf', 'sT2', 10, 0, 400,
            title=r'CMS Preliminary $\sqrt{s}=$ 8 TeV, $\mathcal{L}_{int}=$ 19.7 fb$^{-1}$',
            xlab=r'$s_T(\Phi^{--})$ [GeV]',
            label_bin_width=True, log=True)

def z_control():
    channels = ["eemm","mmee","emme","meem","emem","meme","mmmm","eeee"]
    tmp = ["channel == '%s'" % c for c in channels]
    #cut = '(sT > 150) & ((%s))' % (") | (".join(tmp))
    cut = '(sT > 50) & ((%s))' % (") | (".join(tmp))
    #cut += '& (l1Pt > 15)'
    #cut += '& (l2Pt > 15)'
    #cut += '& (l3Pt > 15)'
    #cut += '& (l4Pt > 15)'

    plotter = Plotter("DblH", cut, "./ntuples", "./plots/z_ctrl",
                      channels=["dblh4l_z_control"], lumi=19.7)

    plotter.add_group("dyjets", r"Z+Jets", "Z[1234]jets*",
                      facecolor='orange', edgecolor='darkorange')

    plotter.add_group("ggH", "H(125)", "GluGlu*125*",
                      facecolor='lightcoral', edgecolor='maroon')

    plotter.add_group("top", "Top", "TTJets*", "T_*", "Tbar_*",
                      facecolor='mediumseagreen', edgecolor='darkgreen')

    plotter.add_group("zz", "ZZ", "ZZTo*", "ggZZ*",
                      facecolor='lightskyblue', edgecolor='darkblue')

#    plotter.add_group("ggzz", "ZZ(gg)", "ggZZ*",
#                      facecolor='deepskyblue', edgecolor='navy')

    plotter.add_group("wz", "WZ", "WZJets*",
                      facecolor='mediumpurple', edgecolor='midnightblue')

    plotter.add_group("wwv", "WWV", "WW[WZ]*",
                      facecolor="tomato", edgecolor="red")

    plotter.add_group("ttv", "TTV", "TT[WZ]*",
                      facecolor="springgreen", edgecolor="seagreen")

    plotter.add_group("data", "Observed", "data_*", isdata=True)

    plotter.stack_order("ttv", "wwv", "wz", "top", "dyjets", "ggH", "zz")

    plotter.plot_stack('h1mass.pdf', 'h1mass', 20, 0, 500,
            title=r'CMS Preliminary $\sqrt{s}=$ 8 TeV, $\mathcal{L}_{int}=$ 19.7 fb$^{-1}$',
            xlab=r'$M_{l^+l^+}$ [GeV]',
            label_bin_width=True, log=False, legend_size=10)

    plotter.plot_stack('h1mass_binned.pdf', 'h1mass', 25, 0, 500,
            title=r'CMS Preliminary $\sqrt{s}=$ 8 TeV, $\mathcal{L}_{int}=$ 19.7 fb$^{-1}$',
            xlab=r'$M_{l^+l^+}$ [GeV]',
            label_bin_width=True, log=False)

    plotter.plot_stack('st.pdf', 'sT', 20, 0, 500,
            title=r'CMS Preliminary $\sqrt{s}=$ 8 TeV, $\mathcal{L}_{int}=$ 19.7 fb$^{-1}$',
            xlab=r'$s_T$ [GeV]',
            label_bin_width=True, log=False, legend_size=10,
            shade=[(0, 150.0, 'k')])

    plotter.plot_stack('met.pdf', 'met', 20, 0, 500,
            title=r'CMS Preliminary $\sqrt{s}=$ 8 TeV, $\mathcal{L}_{int}=$ 19.7 fb$^{-1}$',
            xlab=r'$E_T^{miss}$ [GeV]',
            label_bin_width=True, log=False)

    plotter.plot_stack('st1.pdf', 'sT1', 20, 0, 500,
            title=r'CMS Preliminary $\sqrt{s}=$ 8 TeV, $\mathcal{L}_{int}=$ 19.7 fb$^{-1}$',
            xlab=r'$s_T(\Phi^{++})$ [GeV]',
            label_bin_width=True, log=False)

    plotter.plot_stack('st2.pdf', 'sT2', 20, 0, 500,
            title=r'CMS Preliminary $\sqrt{s}=$ 8 TeV, $\mathcal{L}_{int}=$ 19.7 fb$^{-1}$',
            xlab=r'$s_T(\Phi^{--})$ [GeV]',
            label_bin_width=True, log=False)

    plotter.plot_stack('l1pt.pdf', 'l1Pt', 20, 0, 100,
            title=r'$\sqrt{s}=$ 8 TeV, $\mathcal{L}_{int}=$ 19.7 fb$^{-1}$',
            xlab=r'$p_T(l_1)$ [GeV]',
            label_bin_width=True, log=False)

    plotter.plot_stack('l2pt.pdf', 'l2Pt', 20, 0, 100,
            title=r'$\sqrt{s}=$ 8 TeV, $\mathcal{L}_{int}=$ 19.7 fb$^{-1}$',
            xlab=r'$p_T(l_2)$ [GeV]',
            label_bin_width=True, log=False)

    plotter.plot_stack('l3pt.pdf', 'l3Pt', 20, 0, 100,
            title=r'$\sqrt{s}=$ 8 TeV, $\mathcal{L}_{int}=$ 19.7 fb$^{-1}$',
            xlab=r'$p_T(l_3)$ [GeV]',
            label_bin_width=True, log=False)

    plotter.plot_stack('l4pt.pdf', 'l4Pt', 20, 0, 100,
            title=r'$\sqrt{s}=$ 8 TeV, $\mathcal{L}_{int}=$ 19.7 fb$^{-1}$',
            xlab=r'$p_T(l_4)$ [GeV]',
            label_bin_width=True, log=False)

    plotter.plot_stack('l1eta.pdf', 'l1Eta', 20, -2.5, 2.5,
            title=r'$\sqrt{s}=$ 8 TeV, $\mathcal{L}_{int}=$ 19.7 fb$^{-1}$',
            xlab=r'$\eta(l_1)$ [GeV]',
            label_bin_width=True, log=False)

    plotter.plot_stack('l2eta.pdf', 'l2Eta', 20, -2.5, 2.5,
            title=r'$\sqrt{s}=$ 8 TeV, $\mathcal{L}_{int}=$ 19.7 fb$^{-1}$',
            xlab=r'$\eta(l_2)$ [GeV]',
            label_bin_width=True, log=False)

    plotter.plot_stack('l3eta.pdf', 'l3Eta', 20, -2.5, 2.5,
            title=r'$\sqrt{s}=$ 8 TeV, $\mathcal{L}_{int}=$ 19.7 fb$^{-1}$',
            xlab=r'$\eta(l_3)$ [GeV]',
            label_bin_width=True, log=False)

    plotter.plot_stack('l4eta.pdf', 'l4Eta', 20, -2.5, 2.5,
            title=r'$\sqrt{s}=$ 8 TeV, $\mathcal{L}_{int}=$ 19.7 fb$^{-1}$',
            xlab=r'$\eta(l_4)$ [GeV]',
            label_bin_width=True, log=False)

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
            title=r'$\sqrt{s}=$ 8 TeV, $\mathcal{L}_{int}=$ 19.7 fb$^{-1}$',
            xlab=r'm(4l) [GeV]',
            label_bin_width=True, log=False)


def zz_4mu():
    channels = ["mmmm"]
    tmp = ["channel == '%s'" % c for c in channels]
    cut = "(mass > 0) & (40 < z1mass) & (z1mass < 120) & (12 < z2mass) & (z2mass < 120) & ((%s))" % (") | (".join(tmp))

    plotter = Plotter("ZZ4l", cut, "./ntuples", "./plots/zz/4mu",
                      channels=["zz4l"], lumi=19.7)

    plotter.add_group("zz", "ZZ", "ZZTo*", "ggZZ*",
                      facecolor='lightskyblue', edgecolor='darkblue')
    #plotter.add_group("dyjets", "Z+Jets", "Z[1234]jets*",
    #                  facecolor='orange', edgecolor='darkorange')
    plotter.add_group("ggH", "H(125)", "GluGlu*125*",
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
            title=r'$\sqrt{s}=$ 8 TeV, $\mathcal{L}_{int}=$ 19.7 fb$^{-1}$',
            xlab=r'$s_T$ [GeV]',
            label_bin_width=True, log=False)

    plotter.plot_stack('m4l.pdf', 'mass', 50, 0, 500,
            title=r'$\sqrt{s}=$ 8 TeV, $\mathcal{L}_{int}=$ 19.7 fb$^{-1}$',
            xlab=r'$M_{4l}$ [GeV]',
            label_bin_width=True, log=False)

    plotter.plot_stack('mz1.pdf', 'z1mass', 30, 60, 120,
            title=r'$\sqrt{s}=$ 8 TeV, $\mathcal{L}_{int}=$ 19.7 fb$^{-1}$',
            xlab=r'$M_{Z_1}$ [GeV]',
            label_bin_width=True, log=False)

    plotter.plot_stack('mz2.pdf', 'z2mass', 30, 60, 120,
            title=r'$\sqrt{s}=$ 8 TeV, $\mathcal{L}_{int}=$ 19.7 fb$^{-1}$',
            xlab=r'$M_{Z_2}$ [GeV]',
            label_bin_width=True, log=False)

    plotter.plot_stack('l1pt.pdf', 'l1Pt', 20, 0, 100,
            title=r'$\sqrt{s}=$ 8 TeV, $\mathcal{L}_{int}=$ 19.7 fb$^{-1}$',
            xlab=r'$p_T(l_1)$ [GeV]',
            label_bin_width=True, log=False)

    plotter.plot_stack('l2pt.pdf', 'l2Pt', 20, 0, 100,
            title=r'$\sqrt{s}=$ 8 TeV, $\mathcal{L}_{int}=$ 19.7 fb$^{-1}$',
            xlab=r'$p_T(l_2)$ [GeV]',
            label_bin_width=True, log=False)

    plotter.plot_stack('l3pt.pdf', 'l3Pt', 20, 0, 100,
            title=r'$\sqrt{s}=$ 8 TeV, $\mathcal{L}_{int}=$ 19.7 fb$^{-1}$',
            xlab=r'$p_T(l_3)$ [GeV]',
            label_bin_width=True, log=False)

    plotter.plot_stack('l4pt.pdf', 'l4Pt', 20, 0, 100,
            title=r'$\sqrt{s}=$ 8 TeV, $\mathcal{L}_{int}=$ 19.7 fb$^{-1}$',
            xlab=r'$p_T(l_4)$ [GeV]',
            label_bin_width=True, log=False)

    plotter.plot_stack('l1eta.pdf', 'l1Eta', 20, -2.5, 2.5,
            title=r'$\sqrt{s}=$ 8 TeV, $\mathcal{L}_{int}=$ 19.7 fb$^{-1}$',
            xlab=r'$\eta(l_1)$ [GeV]',
            label_bin_width=True, log=False)

    plotter.plot_stack('l2eta.pdf', 'l2Eta', 20, -2.5, 2.5,
            title=r'$\sqrt{s}=$ 8 TeV, $\mathcal{L}_{int}=$ 19.7 fb$^{-1}$',
            xlab=r'$\eta(l_2)$ [GeV]',
            label_bin_width=True, log=False)

    plotter.plot_stack('l3eta.pdf', 'l3Eta', 20, -2.5, 2.5,
            title=r'$\sqrt{s}=$ 8 TeV, $\mathcal{L}_{int}=$ 19.7 fb$^{-1}$',
            xlab=r'$\eta(l_3)$ [GeV]',
            label_bin_width=True, log=False)

    plotter.plot_stack('l4eta.pdf', 'l4Eta', 20, -2.5, 2.5,
            title=r'$\sqrt{s}=$ 8 TeV, $\mathcal{L}_{int}=$ 19.7 fb$^{-1}$',
            xlab=r'$\eta(l_4)$ [GeV]',
            label_bin_width=True, log=False)

def zz_4e():
    channels = ["eeee"]
    tmp = ["channel == '%s'" % c for c in channels]
    cut = "(mass > 0) & (40 < z1mass) & (z1mass < 120) & (12 < z2mass) & (z2mass < 120) & ((%s))" % (") | (".join(tmp))
    print cut

    plotter = Plotter("ZZ4l", cut, "./ntuples", "./plots/zz/4e",
                      channels=["zz4l"], lumi=19.7)

    plotter.add_group("zz", "ZZ", "ZZTo*", "ggZZ*",
                      facecolor='lightskyblue', edgecolor='darkblue')
    plotter.add_group("dyjets", "Z+Jets", "Z[1234]jets*",
                      facecolor='orange', edgecolor='darkorange')
    plotter.add_group("ggH", "H(125)", "GluGlu*125*",
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
            title=r'$\sqrt{s}=$ 8 TeV, $\mathcal{L}_{int}=$ 19.7 fb$^{-1}$',
            xlab=r'$s_T$ [GeV]',
            label_bin_width=True, log=False)

    plotter.plot_stack('m4l.pdf', 'mass', 50, 0, 500,
            title=r'$\sqrt{s}=$ 8 TeV, $\mathcal{L}_{int}=$ 19.7 fb$^{-1}$',
            xlab=r'$M_{4l}$ [GeV]',
            label_bin_width=True, log=False)

    plotter.plot_stack('mz1.pdf', 'z1mass', 30, 60, 120,
            title=r'$\sqrt{s}=$ 8 TeV, $\mathcal{L}_{int}=$ 19.7 fb$^{-1}$',
            xlab=r'$M_{Z_1}$ [GeV]',
            label_bin_width=True, log=False)

    plotter.plot_stack('mz2.pdf', 'z2mass', 30, 60, 120,
            title=r'$\sqrt{s}=$ 8 TeV, $\mathcal{L}_{int}=$ 19.7 fb$^{-1}$',
            xlab=r'$M_{Z_2}$ [GeV]',
            label_bin_width=True, log=False)

    plotter.plot_stack('l1pt.pdf', 'l1Pt', 20, 0, 100,
            title=r'$\sqrt{s}=$ 8 TeV, $\mathcal{L}_{int}=$ 19.7 fb$^{-1}$',
            xlab=r'$p_T(l_1)$ [GeV]',
            label_bin_width=True, log=False)

    plotter.plot_stack('l2pt.pdf', 'l2Pt', 20, 0, 100,
            title=r'$\sqrt{s}=$ 8 TeV, $\mathcal{L}_{int}=$ 19.7 fb$^{-1}$',
            xlab=r'$p_T(l_2)$ [GeV]',
            label_bin_width=True, log=False)

    plotter.plot_stack('l3pt.pdf', 'l3Pt', 20, 0, 100,
            title=r'$\sqrt{s}=$ 8 TeV, $\mathcal{L}_{int}=$ 19.7 fb$^{-1}$',
            xlab=r'$p_T(l_3)$ [GeV]',
            label_bin_width=True, log=False)

    plotter.plot_stack('l4pt.pdf', 'l4Pt', 20, 0, 100,
            title=r'$\sqrt{s}=$ 8 TeV, $\mathcal{L}_{int}=$ 19.7 fb$^{-1}$',
            xlab=r'$p_T(l_4)$ [GeV]',
            label_bin_width=True, log=False)

    plotter.plot_stack('l1eta.pdf', 'l1Eta', 20, -2.5, 2.5,
            title=r'$\sqrt{s}=$ 8 TeV, $\mathcal{L}_{int}=$ 19.7 fb$^{-1}$',
            xlab=r'$\eta(l_1)$ [GeV]',
            label_bin_width=True, log=False)

    plotter.plot_stack('l2eta.pdf', 'l2Eta', 20, -2.5, 2.5,
            title=r'$\sqrt{s}=$ 8 TeV, $\mathcal{L}_{int}=$ 19.7 fb$^{-1}$',
            xlab=r'$\eta(l_2)$ [GeV]',
            label_bin_width=True, log=False)

    plotter.plot_stack('l3eta.pdf', 'l3Eta', 20, -2.5, 2.5,
            title=r'$\sqrt{s}=$ 8 TeV, $\mathcal{L}_{int}=$ 19.7 fb$^{-1}$',
            xlab=r'$\eta(l_3)$ [GeV]',
            label_bin_width=True, log=False)

    plotter.plot_stack('l4eta.pdf', 'l4Eta', 20, -2.5, 2.5,
            title=r'$\sqrt{s}=$ 8 TeV, $\mathcal{L}_{int}=$ 19.7 fb$^{-1}$',
            xlab=r'$\eta(l_4)$ [GeV]',
            label_bin_width=True, log=False)

def zz_all():
    channels = ["eeee", "mmmm", "eemm", "mmee"]
    tmp = ["channel == '%s'" % c for c in channels]
    cut = "(0 < mass) & (40 < z1mass) & (z1mass < 120) & (12 < z2mass) & (z2mass < 120) & ((%s))" % (") | (".join(tmp))

    plotter = Plotter("ZZ4l", cut, "./ntuples", "./plots/zz/all",
                      channels=["zz4l"], lumi=19.7)

    plotter.add_group("top", "Top", "TTJets*", "T_*", "Tbar_*",
                      facecolor='mediumseagreen', edgecolor='darkgreen')
    plotter.add_group("zz", "ZZ", "ZZTo*", "ggZZ*",
                      facecolor='lightskyblue', edgecolor='darkblue')
    plotter.add_group("wz", "WZ", "WZJets*",
                      facecolor='mediumpurple', edgecolor='midnightblue')
    plotter.add_group("wwv", "WWV", "WW[WZ]*",
                      facecolor="tomato", edgecolor="red")
    plotter.add_group("ttv", "TTV", "TT[WZ]*",
                      facecolor="springgreen", edgecolor="seagreen")
    plotter.add_group("dyjets", "Z+Jets", "Z[1234]jets*",
                      facecolor='orange', edgecolor='darkorange')
    plotter.add_group("ggH", "H(125)", "GluGlu*125*",
                      facecolor='lightcoral', edgecolor='maroon')

    plotter.add_group("data", "Observed", "data_*", isdata=True)

    plotter.stack_order("zz","ggH")

    plotter.plot_stack('m4l.pdf', 'mass', 50, 0, 500,
            title=r'$\sqrt{s}=$ 8 TeV, $\mathcal{L}_{int}=$ 19.7 fb$^{-1}$',
            xlab=r'$M_{4l}$ [GeV]',
            label_bin_width=True, log=False)

    plotter.plot_stack('st.pdf', 'sT', 50, 0, 500,
            title=r'$\sqrt{s}=$ 8 TeV, $\mathcal{L}_{int}=$ 19.7 fb$^{-1}$',
            xlab=r'$s_T$ [GeV]',
            label_bin_width=True, log=False)

    plotter.plot_stack('mz1.pdf', 'z1mass', 30, 60, 120,
            title=r'$\sqrt{s}=$ 8 TeV, $\mathcal{L}_{int}=$ 19.7 fb$^{-1}$',
            xlab=r'$M_{Z_1}$ [GeV]',
            label_bin_width=True, log=False)

    plotter.plot_stack('mz2.pdf', 'z2mass', 30, 60, 120,
            title=r'$\sqrt{s}=$ 8 TeV, $\mathcal{L}_{int}=$ 19.7 fb$^{-1}$',
            xlab=r'$M_{Z_2}$ [GeV]',
            label_bin_width=True, log=False)

    plotter.plot_stack('l1pt.pdf', 'l1Pt', 20, 0, 100,
            title=r'$\sqrt{s}=$ 8 TeV, $\mathcal{L}_{int}=$ 19.7 fb$^{-1}$',
            xlab=r'$p_T(l_1)$ [GeV]',
            label_bin_width=True, log=False)

    plotter.plot_stack('l2pt.pdf', 'l2Pt', 20, 0, 100,
            title=r'$\sqrt{s}=$ 8 TeV, $\mathcal{L}_{int}=$ 19.7 fb$^{-1}$',
            xlab=r'$p_T(l_2)$ [GeV]',
            label_bin_width=True, log=False)

    plotter.plot_stack('l3pt.pdf', 'l3Pt', 20, 0, 100,
            title=r'$\sqrt{s}=$ 8 TeV, $\mathcal{L}_{int}=$ 19.7 fb$^{-1}$',
            xlab=r'$p_T(l_3)$ [GeV]',
            label_bin_width=True, log=False)

    plotter.plot_stack('l4pt.pdf', 'l4Pt', 20, 0, 100,
            title=r'$\sqrt{s}=$ 8 TeV, $\mathcal{L}_{int}=$ 19.7 fb$^{-1}$',
            xlab=r'$p_T(l_4)$ [GeV]',
            label_bin_width=True, log=False)

    plotter.plot_stack('l1eta.pdf', 'l1Eta', 20, -2.5, 2.5,
            title=r'$\sqrt{s}=$ 8 TeV, $\mathcal{L}_{int}=$ 19.7 fb$^{-1}$',
            xlab=r'$\eta(l_1)$ [GeV]',
            label_bin_width=True, log=False)

    plotter.plot_stack('l2eta.pdf', 'l2Eta', 20, -2.5, 2.5,
            title=r'$\sqrt{s}=$ 8 TeV, $\mathcal{L}_{int}=$ 19.7 fb$^{-1}$',
            xlab=r'$\eta(l_2)$ [GeV]',
            label_bin_width=True, log=False)

    plotter.plot_stack('l3eta.pdf', 'l3Eta', 20, -2.5, 2.5,
            title=r'$\sqrt{s}=$ 8 TeV, $\mathcal{L}_{int}=$ 19.7 fb$^{-1}$',
            xlab=r'$\eta(l_3)$ [GeV]',
            label_bin_width=True, log=False)

    plotter.plot_stack('l4eta.pdf', 'l4Eta', 20, -2.5, 2.5,
            title=r'$\sqrt{s}=$ 8 TeV, $\mathcal{L}_{int}=$ 19.7 fb$^{-1}$',
            xlab=r'$\eta(l_4)$ [GeV]',
            label_bin_width=True, log=False)

def main():

    if sys.argv[1] == "zz4mu":
        zz_4mu()
    elif sys.argv[1] == "zz4e":
        zz_4e()
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
    elif sys.argv[1] == "sigshapes":
        signal_shapes()
    elif sys.argv[1] == "flow":
        cut_flow()
    else:
        raise ValueError("Incorrect option given: %s" % sys.argv[1])


if __name__ == "__main__":
    main()
