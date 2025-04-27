# -*- coding: utf-8 -*-
"""
Created on Thu Apr 24 20:24:33 2025

@author: Jorn
"""

import pandas as pd
import glob
import os
import argparse
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.gridspec as gridspec
from scipy.optimize import curve_fit
import numpy as np

def exp_decay(x, a, b, c):
    return a * np.exp(b * x) + c

def read_ascii_files_as_dict(folder_path):
    file_pattern = os.path.join(folder_path, '*.txt')
    data_dict = {}

    for file in glob.glob(file_pattern):
        df = pd.read_csv(
            file,
            sep=';',
            skiprows=8,
            usecols=[0, 4],
            header=None,
            names=['X', 'Y']
        )
        filename = os.path.basename(file)
        data_dict[filename] = df

    return data_dict

def plot_overlay_spectra(data_dict, snapshot_x):
    fig = plt.figure(figsize=(14, 6))
    gs = gridspec.GridSpec(1, 2, width_ratios=[3, 1])  # Wider spectra plot

    # First subplot: overlay spectra
    ax0 = fig.add_subplot(gs[0])
    num_files = len(data_dict)
    color_map = cm.get_cmap('viridis', num_files)

    snapshot_values = []  # List of (index, Y_at_snapshot_x)

    for idx, (filename, df) in enumerate(sorted(data_dict.items())):
        color = color_map(idx)
        ax0.plot(df['X'], df['Y'], label=filename, color=color, linewidth=1.5)

        # Find nearest Y-value to snapshot_x
        nearest_idx = (df['X'] - snapshot_x).abs().idxmin()
        y_value = df.loc[nearest_idx, 'Y']
        snapshot_values.append((idx, y_value))  # Save index and Y
    
    # dashed vertical line
    ax0.axvline(x=snapshot_x, color='gray', linestyle='--', linewidth=1.5, label=f'Snapshot X={snapshot_x}')

    ax0.set_title("Overlayed Spectra")
    ax0.set_xlabel("X")
    ax0.set_ylabel("Y")
    ax0.grid(True, linestyle='--', alpha=0.5)
    ax0.legend(loc='best', fontsize='small')

    # Second subplot: scatter plot (index vs Y-value)
    ax1 = fig.add_subplot(gs[1])
    indices, y_values = zip(*snapshot_values)
    colors = [color_map(idx) for idx in indices]

    ax1.scatter(indices, y_values, color=colors, s=50)
    ax1.set_xlabel('Spectrum Index')
    ax1.set_ylabel(f'Y at X = {snapshot_x}')
    ax1.set_title('Snapshot Scatter')
    ax1.grid(True, linestyle='--', alpha=0.5)

    # Fit exponential decay to snapshot scatter data
    indices_array = np.array(indices)
    y_values_array = np.array(y_values)

    p0 = estimate_initial_params(indices_array, y_values_array)

    print(f"indices_array: {indices_array}")
    print(f"y_values_array: {y_values_array}")

    try:
        popt, pcov = curve_fit(exp_decay, indices_array, y_values_array, p0=p0)
        fitted_y = exp_decay(indices_array, *popt)

        # Plot the fitted curve
        ax1.plot(indices_array, fitted_y, color='black', linestyle='--', label='Exp. Decay Fit')
        ax1.legend(fontsize='small')

        print(f"Fit parameters: a={popt[0]:.3f}, b={popt[1]:.3f}, c={popt[2]:.3f}")
    except RuntimeError:
        print("Warning: Exponential fit failed.")

    plt.tight_layout()
    plt.show()

def estimate_initial_params(indices_array, y_values_array):
    # Estimate a (amplitude)
    a_guess = y_values_array[0]  # Starting Y-value
    
    # Estimate b (rate of decay/growth)
    # Rough guess: the change in Y per index (assuming exponential-like behavior)
    if len(indices_array) > 1:
        b_guess = np.log(y_values_array[1] / y_values_array[0]) / (indices_array[1] - indices_array[0])
    else:
        b_guess = -0.1  # Default decay if only one point (just a safe guess)

    # Estimate c (offset) as the minimum value in Y (or last value in some cases)
    c_guess = np.min(y_values_array)
    
    return (a_guess, b_guess, c_guess)


def main():
    parser = argparse.ArgumentParser(description='Overlay spectra plots with color gradient and snapshot.')
    parser.add_argument('folder', help='Path to folder containing ASCII files')
    parser.add_argument('--snapshot_x', type=float, default=500, help='X value at which to take the snapshot (default: 500)')
    args = parser.parse_args()

    data_dict = read_ascii_files_as_dict(args.folder)
    plot_overlay_spectra(data_dict, snapshot_x=args.snapshot_x)


if __name__ == '__main__':
    main()
