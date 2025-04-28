# -*- coding: utf-8 -*-
"""
Created on Thu Apr 24 20:24:33 2025

@author: Jorn
"""

import argparse
import QuickPlotAbs.functions.load_data as LoadData
import QuickPlotAbs.functions.plot as Plot

def main():
    parser = argparse.ArgumentParser(description='Overlay spectra plots with color gradient and Abs at a chosen wavelength.')
    parser.add_argument('folder', help='Path to folder containing ASCII files')
    parser.add_argument('--wavelength', type=float, default=Plot.default_wl, help=f'Wavelength at which to plot Abs (default: {Plot.default_wl})')
    parser.add_argument('--legend', type=str, default='off', help='Legend for UV-Vis spectra (default: off)')
    args = parser.parse_args()

    data_dict = LoadData.read_ascii_files_as_dict(args.folder)
    Plot.plot_overlay_spectra(data_dict, args.wavelength, args.folder, args.legend)

if __name__ == '__main__':
    main()
