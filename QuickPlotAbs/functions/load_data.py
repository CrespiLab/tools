# -*- coding: utf-8 -*-
"""
Created on Thu Apr 24 20:24:33 2025

@author: Jorn
"""

import pandas as pd
import glob
import os

def read_ascii_files_as_dict(folder_path):
    file_pattern = os.path.join(folder_path, '*.txt')
    # file_pattern = os.path.join(folder_path, '*.Abs.txt') ## add if necessary
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

