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
import numpy as np

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

def plot_overlay_spectra(data_dict):
    plt.figure(figsize=(10, 6))
    num_files = len(data_dict)
    color_map = cm.get_cmap('viridis', num_files)

    for idx, (filename, df) in enumerate(sorted(data_dict.items())):
        color = color_map(idx)
        plt.plot(df['X'], df['Y'], label=filename, color=color, linewidth=1.5)

    plt.title("Overlayed Spectra")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend(loc='best', fontsize='small')
    plt.tight_layout()
    plt.show()

def main():
    parser = argparse.ArgumentParser(description='Overlay spectra plots with color gradient.')
    parser.add_argument('folder', help='Path to folder containing ASCII files')
    args = parser.parse_args()

    data_dict = read_ascii_files_as_dict(args.folder)
    plot_overlay_spectra(data_dict)

if __name__ == '__main__':
    main()

