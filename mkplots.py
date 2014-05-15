from plotters.plotter import Plotter
import sys

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
            title=r'$\sqrt{s}=$ 8 TeV, $\mathcal{L}_{int}=$ 19.7 $\text{fb}^{-1}$',
            xlab=r'$M_{l^+l^+}$ [GeV]',
            label_bin_width=True, log=True)

    plotter.plot_stack('st1.pdf', 'sT1', 25, 0, 500,
            title=r'$\sqrt{s}=$ 8 TeV, $\mathcal{L}_{int}=$ 19.7 $\text{fb}^{-1}$',
            xlab=r'$s_T(\Phi^{++})$ [GeV]',
            label_bin_width=True, log=True)

    plotter.plot_stack('st2.pdf', 'sT2', 25, 0, 500,
            title=r'$\sqrt{s}=$ 8 TeV, $\mathcal{L}_{int}=$ 19.7 $\text{fb}^{-1}$',
            xlab=r'$s_T(\Phi^{--})$ [GeV]',
            label_bin_width=True, log=True)

    plotter.plot_stack('st.pdf', 'sT', 25, 0, 500,
            title=r'$\sqrt{s}=$ 8 TeV, $\mathcal{L}_{int}=$ 19.7 $\text{fb}^{-1}$',
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
    else:
        raise ValueError("Incorrect option given: %s" % sys.argv[1])


if __name__ == "__main__":
    main()
