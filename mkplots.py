from plotters.plotter import Plotter
import sys

def four_l():
    plotter = Plotter("DblH", "(mass > 0)", "./ntuples", "./plots/4l",
                      channels=["dblh4l"], lumi=19.7)

    plotter.add_group("hpp", r"$\Phi^{++}(500)$", "HPlus*500*",
                      facecolor='mediumorchid', edgecolor='indigo')
    plotter.add_group("dyjets", "Z+Jets", "DYJets*",
                      facecolor="orange", edgecolor="darkorange")
    plotter.add_group("top", "Top", "T*",
                      facecolor="mediumseagreen", edgecolor="darkgreen")
    plotter.add_group("zz", "ZZ", "ZZTo*",
                      facecolor="lightskyblue", edgecolor="darkblue")
    plotter.add_group("wwv", "WWV", "WW[WZ]*",
                      facecolor="tomato", edgecolor="red")
    plotter.add_group("ttv", "TTV", "TT[WZ]*",
                      facecolor="springgreen", edgecolor="seagreen")

    #plotter.stack_order("wwv", "ttv", "top", "dyjets", "zz", "hpp")
    plotter.stack_order("top", "dyjets", "zz", "hpp")

    plotter.plot_stack('h1mass.pdf', 'h1mass', 25, 0, 600,
            title=r'CMS Preliminary $\sqrt{s}=$ 8 TeV, $\mathcal{L}_{int}=$ 19.7 $\textsf{fb}^{-1}$',
            xlab=r'$M_{l^+l^+}$ [GeV]',
            label_bin_width=True, log=True)

    plotter.plot_stack('st1.pdf', 'sT1', 25, 0, 600,
            title=r'CMS Preliminary $\sqrt{s}=$ 8 TeV, $\mathcal{L}_{int}=$ 19.7 $\textrm{fb}^{-1}$',
            xlab=r'$s_T(\Phi^{++})$ [GeV]',
            label_bin_width=True, log=True)

    plotter.plot_stack('st2.pdf', 'sT2', 25, 0, 600,
            title=r'CMS Preliminary $\sqrt{s}=$ 8 TeV, $\mathcal{L}_{int}=$ 19.7 $\textrm{fb}^{-1}$',
            xlab=r'$s_T(\Phi^{--})$ [GeV]',
            label_bin_width=True, log=True)

    plotter.plot_stack('st.pdf', 'sT', 25, 0, 600,
            title=r'CMS Preliminary $\sqrt{s}=$ 8 TeV, $\mathcal{L}_{int}=$ 19.7 $\textrm{fb}^{-1}$',
            xlab=r'$s_T$ [GeV]',
            label_bin_width=True, log=True)

def cut_flow():
    plotter = Plotter("DblH", "(mass > 0)", "./ntuples", "./plots/4l",
                      channels=["dblh4l"], lumi=19.7)

    plotter.add_group("hpp", "HPP (500)", "HPlus*500*",
                      facecolor='mediumorchid', edgecolor='indigo')
    plotter.add_group("dyjets", "Z+Jets", "DYJets*",
                      facecolor="orange", edgecolor="darkorange")
    plotter.add_group("top", "Top", "T*",
                      facecolor="mediumseagreen", edgecolor="darkgreen")
    plotter.add_group("zz", "ZZ", "ZZTo*",
                      facecolor="lightskyblue", edgecolor="darkblue")
    plotter.add_group("wwv", "WWV", "WW[WZ]*",
                      facecolor="tomato", edgecolor="red")
    plotter.add_group("ttv", "TTV", "TT[WZ]*",
                      facecolor="springgreen", edgecolor="seagreen")

    plotter.stack_order("ttv", "wwv", "top", "dyjets", "zz", "hpp")

    cuts = ["(True)",
            "(%f < sT)" % (0.6*500 + 130.),
            "(%f < sT) & (%f < h1mass) & (h1mass < %f)" % ((0.6*500 + 130.), 0.9*500, 1.1*500)]

    labels = ["Preselection",
              "sT",
              "Mass Window"]

    plotter.cut_flow("cut_flow.pdf", cuts, labels, log=True, title="19.7 fb-1 (8 TeV)")


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

    plotter.stack_order("ttv", "wz", "top", "tt", "dyjets")

    plotter.plot_stack('h1mass.pdf', 'h1mass', 10, 0, 400,
            title=r'CMS Preliminary $\sqrt{s}=$ 8 TeV, $\mathcal{L}_{int}=$ 19.7 $\textrm{fb}^{-1}$',
            xlab=r'$M_{l^+l^+}$ [GeV]',
            label_bin_width=True, log=True)

    plotter.plot_stack('met.pdf', 'met', 10, 0, 400,
            title=r'CMS Preliminary $\sqrt{s}=$ 8 TeV, $\mathcal{L}_{int}=$ 19.7 $\textrm{fb}^{-1}$',
            xlab=r'$E_T^{miss}$ [GeV]',
            label_bin_width=True, log=True)

    plotter.plot_stack('st1.pdf', 'sT1', 10, 0, 400,
            title=r'CMS Preliminary $\sqrt{s}=$ 8 TeV, $\mathcal{L}_{int}=$ 19.7 $\textrm{fb}^{-1}$',
            xlab=r'$s_T(\Phi^{++})$ [GeV]',
            label_bin_width=True, log=True)

    plotter.plot_stack('st2.pdf', 'sT2', 10, 0, 400,
            title=r'CMS Preliminary $\sqrt{s}=$ 8 TeV, $\mathcal{L}_{int}=$ 19.7 $\textrm{fb}^{-1}$',
            xlab=r'$s_T(\Phi^{--})$ [GeV]',
            label_bin_width=True, log=True)

    plotter.plot_stack('st.pdf', 'sT', 10, 0, 400,
            title=r'CMS Preliminary $\sqrt{s}=$ 8 TeV, $\mathcal{L}_{int}=$ 19.7 $\textrm{fb}^{-1}$',
            xlab=r'$s_T$ [GeV]',
            label_bin_width=True, log=True)

def z_control():
    cut = '(sT > 150)'
    plotter = Plotter("DblH", cut, "./ntuples", "./plots/z_ctrl",
                      channels=["dblh4l_z_control"], lumi=19.7)

    plotter.add_group("dyjets", r"Z+Jets", "Z[1234]jets*",
                      facecolor='orange', edgecolor='darkorange')

    plotter.add_group("top", "Top", "TTJets*", "T_*", "Tbar_*",
                      facecolor='mediumseagreen', edgecolor='darkgreen')

    plotter.add_group("zz", "ZZ", "ZZTo*",
                      facecolor='lightskyblue', edgecolor='darkblue')

    plotter.add_group("wz", "$WZ$", "WZJets*",
                      facecolor='mediumpurple', edgecolor='midnightblue')

    plotter.add_group("data", "Observed", "data_*", isdata=True)

    plotter.stack_order("wz", "top", "dyjets", "zz")

    plotter.plot_stack('h1mass.pdf', 'h1mass', 20, 0, 500,
            title=r'CMS Preliminary $\sqrt{s}=$ 8 TeV, $\mathcal{L}_{int}=$ 19.7 $\textrm{fb}^{-1}$',
            xlab=r'$M_{l^+l^+}$ [GeV]',
            label_bin_width=True, log=True)

    plotter.plot_stack('met.pdf', 'met', 20, 0, 500,
            title=r'CMS Preliminary $\sqrt{s}=$ 8 TeV, $\mathcal{L}_{int}=$ 19.7 $\textrm{fb}^{-1}$',
            xlab=r'$E_T^{miss}$ [GeV]',
            label_bin_width=True, log=True)

    plotter.plot_stack('st1.pdf', 'sT1', 20, 0, 500,
            title=r'CMS Preliminary $\sqrt{s}=$ 8 TeV, $\mathcal{L}_{int}=$ 19.7 $\textrm{fb}^{-1}$',
            xlab=r'$s_T(\Phi^{++})$ [GeV]',
            label_bin_width=True, log=True)

    plotter.plot_stack('st2.pdf', 'sT2', 20, 0, 500,
            title=r'CMS Preliminary $\sqrt{s}=$ 8 TeV, $\mathcal{L}_{int}=$ 19.7 $\textrm{fb}^{-1}$',
            xlab=r'$s_T(\Phi^{--})$ [GeV]',
            label_bin_width=True, log=True)

    plotter.plot_stack('st.pdf', 'sT', 20, 0, 500,
            title=r'CMS Preliminary $\sqrt{s}=$ 8 TeV, $\mathcal{L}_{int}=$ 19.7 $\textrm{fb}^{-1}$',
            xlab=r'$s_T$ [GeV]',
            label_bin_width=True, log=True)

def zz():
    channels = ["mmmm"]
    tmp = ["channel == '%s'" % c for c in channels]
    cut = "(mass > 0) & (40 < z1mass) & (z1mass < 120) & (12 < z2mass) & (z2mass < 120) & (%s)" % (") | (".join(tmp))

    plotter = Plotter("ZZ4l", cut, "./ntuples", "./plots/zz",
                      channels=["zz4l"], lumi=19.7)

    plotter.add_group("zz", "ZZ", "ZZTo*",
                      facecolor='lightskyblue', edgecolor='darkblue')
    plotter.add_group("dyjets", "Z+Jets", "Z[1234]jets*",
                      facecolor='orange', edgecolor='darkorange')

    plotter.add_group("data", "Observed", "data_*", isdata=True)

    plotter.stack_order("zz")

    plotter.plot_stack('m4l.pdf', 'mass', 50, 0, 500,
            title=r'$\sqrt{s}=$ 8 TeV, $\mathcal{L}_{int}=$ 19.7 $\text{fb}^{-1}$',
            xlab=r'$M_{4l}$ [GeV]',
            label_bin_width=True, log=False)

    plotter.plot_stack('mz1.pdf', 'z1mass', 30, 60, 120,
            title=r'$\sqrt{s}=$ 8 TeV, $\mathcal{L}_{int}=$ 19.7 $\text{fb}^{-1}$',
            xlab=r'$M_{Z_1}$ [GeV]',
            label_bin_width=True, log=False)

    plotter.plot_stack('mz2.pdf', 'z2mass', 30, 60, 120,
            title=r'$\sqrt{s}=$ 8 TeV, $\mathcal{L}_{int}=$ 19.7 $\text{fb}^{-1}$',
            xlab=r'$M_{Z_2}$ [GeV]',
            label_bin_width=True, log=False)

def main():

    if sys.argv[1] == "zz":
        zz()
    elif sys.argv[1] == "ctrl":
        control()
    elif sys.argv[1] == "tt":
        tt_control()
    elif sys.argv[1] == "z":
        z_control()
    elif sys.argv[1] == "4l":
        four_l()
    elif sys.argv[1] == "flow":
        cut_flow()
    else:
        raise ValueError("Incorrect option given: %s" % sys.argv[1])


if __name__ == "__main__":
    main()
