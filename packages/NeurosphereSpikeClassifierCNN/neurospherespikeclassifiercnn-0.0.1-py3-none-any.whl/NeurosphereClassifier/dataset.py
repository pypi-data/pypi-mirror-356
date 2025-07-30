"""
Methods allowing dataset loading and saving. Copyright (C) 2025 Ylan A. CLODINE-FLORENT, Tissue Engineering Group - HEPIA

This file is part of the NeuralSpikeClassifierCNN package.
NeuralSpikeClassifierCNN is a free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or any later version.
NeuralSpikeClassifierCNN is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with NeuralSpikeClassifierCNN. If not, see <https://www.gnu.org/licenses/>
"""

import os 
from sklearn.utils import shuffle
import pandas as pd

from NeurosphereClassifier.utils import standard, str_to_array

def load_dataset(filepath):
    csv = pd.read_csv(filepath, sep=";")
    df = pd.DataFrame(csv)                  # convert to dataframe
    df = shuffle(df)                        # shuffle rows
    df.reset_index(inplace=True, drop=True) # reset index column 
    print("dataset size:", len(df.index))   

    df_arrays = []
    for column in df.columns:
        df_arrays.append(str_to_array(df[column]))

    return df_arrays


def save_as_csv(arrays=list, colnames=list[str], path=str, filename=str):

    # CHECK FOR EXISTING FILE
    filepath = os.path.join(path, f'{filename}.csv')
    if os.path.isfile(filepath):
        new_name = input(f"{filename} already exists, choose another filename.")
        filepath = os.path.join(path, f'{new_name}.csv')

    # CREATING DATAFRAME
    d = {}
    for array, name in zip(arrays, colnames):
        d.update({name : standard(array)})
    df = pd.DataFrame(d)

    # SAVING DF AS CSV
    df.to_csv(filepath, index=False, columns=colnames, sep=";")
    print("file saved :", filepath)


