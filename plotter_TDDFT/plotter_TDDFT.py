# -*- coding: utf-8 -*-
"""
Author: Stefano
Modified by: Jorn

Plotter for TDDFT excitations

"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator#, MultipleLocator, ScalarFormatter
# import matplotlib.gridspec as gridspec
# import pandas as pd
# import seaborn as sns

#########################
#### USER PARAMETERS ####
#########################
#### DATA ####
parentfolder = r'C:\Users\TDDFTfolder' ## folder containing subfolders that contain .out files
molecule = "molecule" ## name of subfolder that contains .out file
outfilename = "orca.out" ## name of .out file

#### ORCA or GAMESS ####
outfile = "ORCA" ## out file from ORCA calculation
# outfile = "GAMESS" ## TBA (out file from GAMESS calculation)

#### ORCA version ####
ORCAversion = 5 ## default
# ORCAversion = 6 ##
########################

#### range x-axis ####
plot_start = 200 ##
plot_end = 1000 ## this should be high enough for the Gaussian band shape to not be cut off

colours = ['black','red','blue']

########################################################################
########################################################################

########################################################################
########################################################################
##### READ FILE AND FIND DATA #####
########################################################################
########################################################################
filename = parentfolder+"\\"+molecule+"\\"+outfilename
plots = parentfolder+"\\"+r"Plots" ## folder to save plots in

#### ORCA version-dependent settings ####
#############
linesplits_ORCA5 = [3,2]
linesplits_ORCA6 = [4,5] 

if ORCAversion == 5:
    linesplit_OSC = linesplits_ORCA5[0]
    linesplit_wl = linesplits_ORCA5[1]
elif ORCAversion == 6:
    linesplit_OSC = linesplits_ORCA6[0]
    linesplit_wl = linesplits_ORCA6[1]
else:
    print("Choose correct ORCA version")
#############
########################

def gaussian(x, wl, f):
    return +40489.994 * f * np.exp(-((1/x-1/wl)/0.0003226222738)**2)

if outfile == "ORCA":
    print("Using ORCA .out file")
    lookup="ABSORPTION SPECTRUM VIA TRANSITION VELOCITY DIPOLE MOMENTS"
    init_state="Number of roots to be determined"
    
    # plot_start=200 ##
    # plot_end=1000 ## this should be high enough for the Gaussian band shape to not be cut off
    
    with open(filename) as file:
        for num, line in enumerate(file, 1):
            if init_state in line:
                roots=int(line.split()[7])
    with open(filename) as file:
        for num, line in enumerate(file, 1):
            if lookup in line:
                start=(num+3)
                end=(start+roots+1)
    osc=[]
    with open(filename) as file:
         for i, line in enumerate(file):
            if start < i < end:
                osc.append(float(line.split()[linesplit_OSC]))
    wl=[]
    with open(filename) as file:
         for i, line in enumerate(file):
            if start < i < end:
                wl.append(float(line.split()[linesplit_wl]))
    x=np.arange(plot_start, plot_end)
    dic={}
    for i in range(0, roots):
        dic[(wl[i])]=(osc[i])
    DIC={k:v for (k,v) in dic.items() if plot_start <= k <= plot_end}
    
    # print(DIC)
    
    spectrum = gaussian(x,wl[0],osc[0])
    # print(f"spectrum.shape: {spectrum.shape}")
    for i in np.arange(1,roots):
        spectrum=spectrum + gaussian(x,wl[i],osc[i])  
#############
elif outfile == "GAMESS":
    print("using GAMESS .out file")


##############################################################################
################ PLOT AND SAVE ####################
########################################################################

fig, ax1 = plt.subplots(figsize=(6,4),dpi=600,constrained_layout=True)
fig.suptitle(f'TDDFT simulated spectrum: {molecule}',fontsize=16)

ax1.plot(x, spectrum, color=colours[0])
ax1.set_xlim(200,950)
ax1.set_ylim(0,)
ax1.set_xlabel("Wavelength " + r'$(\lambda)\ [nm]$')
ax1.set_ylabel(r'$\epsilon(\lambda)\ [M^{-1}cm^{-1}]$')
ax1.xaxis.set_minor_locator(AutoMinorLocator(2))
ax1.yaxis.set_minor_locator(AutoMinorLocator(2))

ax2=ax1.twinx()
ax2.stem(*zip(*DIC.items()),'C0',linefmt=colours[1], markerfmt=colours[1])
ax2.set_ylim(0,)
ax2.set_ylabel('Oscillator strength (f)', c='C0')
ax2.yaxis.set_minor_locator(AutoMinorLocator(2))
ax2.spines['right'].set_color(colours[1])  # Spine color
ax2.tick_params(axis='y', which='major', colors=colours[1])  # Major ticks color
ax2.tick_params(axis='y', which='minor', colors=colours[1])  # Minor ticks color
ax2.yaxis.label.set_color(colours[1])  # Y-axis label color

###################

savefilename = f'{plots}\\{molecule}'
plt.savefig(savefilename+".svg",bbox_inches="tight")
plt.savefig(savefilename+".png",bbox_inches="tight")
print("Saved plot")

plt.show()
