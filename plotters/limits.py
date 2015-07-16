import sys
import os

import numpy as np
import scipy as sp
import scipy.interpolate as spi
import scipy.optimize as spo

import matplotlib as mpl
from matplotlib.patches import Patch

# Use PFG/Tikz backend to generate plots
# Enables Latex, with better performance
#mpl.use("pgf")
#pgf_with_pdflatex = {
#        "pgf.texsystem": "pdflatex",
#        "pgf.preamble": [
#            r"\usepackage[utf8x]{inputenc}",
#            r"\usepackage[T1]{fontenc}",
#            r"\usepackage{libertine}",
#            r"\usepackage[libertine,cmintegrals,cmbraces]{newtxmath}"
#            ]
#        }
#mpl.rcParams.update(pgf_with_pdflatex)

import matplotlib.pyplot as plt


plt.rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
plt.rc('text', usetex=True)
plt.rcParams['text.latex.preamble']=[r'\usepackage[helvet]{sfmath}']


sys.argv.append('-b')
import ROOT as rt
sys.argv.pop() # remove '-b' from cmd-line args


def plot_limits(out_fname, masses, datacard_base_dir, blinded=True, title="", x_label="", y_label=""):
    masses = np.asarray(masses, dtype=int)

    q = np.empty((6, masses.size), dtype=float)

    for j, mass in enumerate(masses):
        fname = os.path.join(datacard_base_dir, str(mass), "higgsCombineTest.Asymptotic.mH%i.root" % mass)
        rtfile = rt.TFile(fname, "READ")
        tree = rtfile.Get("limit")

        for i, row in enumerate(tree):
            q[i,j] = row.limit

    legend_handles = []
    legend_labels = []

    if not blinded:
        obs_hdl, = plt.plot(masses, q[5], 'k-', lw=2)
        legend_handles.append(obs_hdl)
        legend_labels.append("Observed")

    exp_hdl, = plt.plot(masses, q[2], 'k--')
    legend_handles.append(exp_hdl)
    legend_labels.append("Expected")

    plt.fill_between(masses, q[0], q[4], facecolor='yellow', edgecolor='yellow')
    plt.fill_between(masses, q[1], q[3], facecolor='limegreen', edgecolor='limegreen')

    ylw_hdl = Patch(color='yellow')
    grn_hdl = Patch(color='limegreen')

    legend_handles += [ylw_hdl, grn_hdl]
    legend_labels += [r"Expected $2\sigma$", r"Expected $1\sigma$"]

    plt.plot(masses, np.ones(masses.shape), 'k', lw=1)

    plt.legend(legend_handles, legend_labels, loc='upper left')

    ax = plt.gca()
    ax.grid(True, which="both", axis='y')
    ax.grid(True, which="major", axis='x')

    plt.yscale('log')
    plt.xlim(xmin=np.min(masses), xmax=np.max(masses))

    plt.xlabel(x_label, fontsize=18, ha='right', position=(1,0))
    plt.ylabel(y_label, fontsize=18, ha='right', position=(0,1))
    plt.title(title, fontsize=18)

    plt.savefig(out_fname)

    plt.clf()


def exclusion(masses, datacard_base_dir, blinded=True):
    masses = np.asarray(masses, dtype=int)

    q = np.empty((6, masses.size), dtype=float)

    for j, mass in enumerate(masses):
        fname = os.path.join(datacard_base_dir, str(mass),
                             "higgsCombineTest.Asymptotic.mH%i.root" % mass)
        rtfile = rt.TFile(fname, "READ")
        tree = rtfile.Get("limit")

        for i, row in enumerate(tree):
            q[i,j] = row.limit

    fun_exp = spi.interp1d(masses, q[2]-1) # expected
    fun_obs = spi.interp1d(masses, q[5]-1) # observed

    ecl_exp = spo.newton(fun_exp, 600)
    ecl_obs = spo.newton(fun_obs, 600)

    if blinded:
        return (ecl_exp, None)
    else:
        return (ecl_exp, ecl_obs)
