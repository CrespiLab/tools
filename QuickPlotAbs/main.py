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
# import numpy as np

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

# def plot_overlay_spectra(data_dict):
#     plt.figure(figsize=(10, 6))
#     num_files = len(data_dict)
#     color_map = cm.get_cmap('viridis', num_files)

#     for idx, (filename, df) in enumerate(sorted(data_dict.items())):
#         color = color_map(idx)
#         plt.plot(df['X'], df['Y'], label=filename, color=color, linewidth=1.5)

#     plt.title("Overlayed Spectra")
#     plt.xlabel("X")
#     plt.ylabel("Y")
#     plt.grid(True, linestyle='--', alpha=0.5)
#     plt.legend(loc='best', fontsize='small')
#     plt.tight_layout()
#     plt.show()

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

    plt.tight_layout()
    plt.show()



# def main():
#     parser = argparse.ArgumentParser(description='Overlay spectra plots with color gradient.')
#     parser.add_argument('folder', help='Path to folder containing ASCII files')
#     args = parser.parse_args()

#     data_dict = read_ascii_files_as_dict(args.folder)
#     plot_overlay_spectra(data_dict)

def main():
    parser = argparse.ArgumentParser(description='Overlay spectra plots with color gradient and snapshot.')
    parser.add_argument('folder', help='Path to folder containing ASCII files')
    parser.add_argument('--snapshot_x', type=float, default=500, help='X value at which to take the snapshot (default: 500)')
    args = parser.parse_args()

    data_dict = read_ascii_files_as_dict(args.folder)
    plot_overlay_spectra(data_dict, snapshot_x=args.snapshot_x)


if __name__ == '__main__':
    main()

