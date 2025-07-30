"""
Miscellaneous functions. Copyright (C) 2025 Ylan A. CLODINE-FLORENT, Tissue Engineering Group - HEPIA

This file is part of the NeuralSpikeClassifierCNN package.
NeuralSpikeClassifierCNN is a free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or any later version.
NeuralSpikeClassifierCNN is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with NeuralSpikeClassifierCNN. If not, see <https://www.gnu.org/licenses/>
"""

import os
import datetime
import numpy as np
from ast import literal_eval

def str_to_array(dataframe_column=list[list[int]] | list[list[float]]):

    converted = []
    for cutout_string in dataframe_column:
        cutout_array = np.array(literal_eval(cutout_string)) # converts string cutout to list
        converted.append(cutout_array)
    print('shape:', np.shape(converted), 'first element:', converted[0])
    return converted

def reshape_cutouts(cutouts=list, cutout_length=int):
    reshaped = []
    print("before reshape:",np.shape(cutouts))
    for cutout in cutouts:        
        reshaped.append(np.reshape(cutout, (cutout_length, 1))) # reshape the array to fit the model input
    print("after reshape:",np.shape(reshaped))
    return reshaped

    
def get_timestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %Hh%M")

    
def create_folder(path=str):
    if os.path.isdir(path): # if path exist
        print(f"folder already exist : {path}")
        pass
    else :
        os.mkdir(path)
        print(f"new folder created : {path}")


def standard(array=list):
    """
    converts array values from scientific to standard notation.
    takes a 1D or 2D array as input.
    """

    dim = len(np.shape(array))

    formatted = []

    if dim == 1:
        for value in array:

            if isinstance(value, float):
                # np.format_float_positional remove the scientific notation and returns a string
                formatted.append(float(np.format_float_positional(value)))
            else:
                formatted.append(value)
    
    else:
        for subarray in array:
            
            f_array = []
            for value in subarray:
           
                if isinstance(value, float):
                    f_array.append(float(np.format_float_positional(value)))
                else:
                    f_array.append(value)         

            formatted.append(f_array)
        
    return formatted

  
def split_by_phase(cutouts=list):
    pos = []
    neg = []
    for cutout in cutouts:
        if cutout[24] > 0: pos.append(cutout)
        else: neg.append(cutout)
    return pos, neg

def split_by_labels(cutouts, labels):
    noise = []
    signals = []

    for i, label in enumerate(labels):
        if label[0] == 1: noise.append(cutouts[i])
        if label[1] == 1: signals.append(cutouts[i])

    return noise, signals