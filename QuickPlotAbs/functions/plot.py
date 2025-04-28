# -*- coding: utf-8 -*-
"""
Created on Thu Apr 24 20:24:33 2025

@author: Jorn
"""

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.gridspec as gridspec
from scipy.optimize import curve_fit
import numpy as np

def exp_decay(x, a, b, c):
    return a * np.exp(-b * x) + c

def plot_overlay_spectra(data_dict, wavelength, folder, legend_on):
    fig = plt.figure(figsize=(14, 6))
    gs = gridspec.GridSpec(1, 5)  # Wider spectra plot

    # First subplot: overlay spectra
    ax0 = fig.add_subplot(gs[0:3])
    ax0.set_title(f"Overlayed Spectra from: {folder}")
    
    num_files = len(data_dict)
    color_map = cm.get_cmap('viridis', num_files)

    Abs_values = []  # List of (index, Y_at_wavelength)

    for idx, (filename, df) in enumerate(sorted(data_dict.items())):
        color = color_map(idx)
        ax0.plot(df['X'], df['Y'], label=filename, color=color, linewidth=1.5)

        # Find nearest Y-value to wavelength
        nearest_idx = (df['X'] - wavelength).abs().idxmin()
        y_value = df.loc[nearest_idx, 'Y']
        Abs_values.append((idx, y_value))  # Save index and Y
    
    # dashed vertical line
    # ax0.axvline(x=wavelength, color='gray', linestyle='--', linewidth=1.5, label=f'X={wavelength}')
    ax0.axvline(x=wavelength, color='gray', linestyle='--', linewidth=1.5)
    
    ax0.set_xlabel("Wavelength (nm)")
    ax0.set_ylabel("Absorbance")
    ax0.grid(True, linestyle='--', alpha=0.5)
    
    if legend_on == "on":
        ax0.legend(loc='best', fontsize='small')
    elif legend_on == "off":
        pass

    # Second subplot: scatter plot (index vs Y-value)
    ax1 = fig.add_subplot(gs[3:5])
    ax1.set_title('Scatter Plot')
    
    indices, y_values = zip(*Abs_values)
    colors = [color_map(idx) for idx in indices]

    ax1.scatter(indices, y_values, color=colors, s=50)
    ax1.set_xlabel('Spectrum Index')
    ax1.set_ylabel(f'Y at X = {wavelength}')
    
    ax1.grid(True, linestyle='--', alpha=0.5)

    # Fit exponential decay to scatter data
    indices_array = np.array(indices)
    y_values_array = np.array(y_values)

    p0 = estimate_initial_params(indices_array, y_values_array)

    print(f"indices_array: {indices_array}")
    print(f"y_values_array: {y_values_array}")

    try:
        popt, pcov = curve_fit(exp_decay, indices_array, y_values_array, p0=p0)
        fitted_y = exp_decay(indices_array, *popt)
        ##!!! plot the fit with more points

        # Plot the fitted curve
        ax1.plot(indices_array, fitted_y, color='black', linestyle='--', label=f'Exp. Decay Fit\nFit parameters: a={popt[0]:.3f}, b={popt[1]:.3f}, c={popt[2]:.3f}')
        ax1.legend(fontsize='small')

        print(f"Fit parameters: a={popt[0]:.3f}, b={popt[1]:.3f}, c={popt[2]:.3f}")
    except RuntimeError:
        print("Warning: Exponential fit failed.")

    plt.tight_layout()
    plt.show()

def estimate_initial_params(indices_array, y_values_array):
    # Estimate a (amplitude)
    a_guess = 0-y_values_array[0]  # Starting Y-value
    
    # Estimate b (rate of decay/growth)
    # Rough guess: the change in Y per index (assuming exponential-like behavior)
    if len(indices_array) > 1:
        # b_guess = np.log(y_values_array[1] / y_values_array[0]) / (indices_array[1] - indices_array[0])
        b_guess = 2/indices_array[-1]
    else:
        b_guess = -0.1  # Default decay if only one point (just a safe guess)

    # Estimate c (offset) as the minimum value in Y (or last value in some cases)
    # c_guess = np.min(y_values_array)
    c_guess = y_values_array[-1]
    
    return (a_guess, b_guess, c_guess)
