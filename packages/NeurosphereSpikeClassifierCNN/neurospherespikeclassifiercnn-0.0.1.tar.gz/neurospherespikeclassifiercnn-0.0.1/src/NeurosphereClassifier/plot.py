"""
Plotting functions used to display waveforms. Copyright (C) 2025 Ylan A. CLODINE-FLORENT, Tissue Engineering Group - HEPIA

This file is part of the NeuralSpikeClassifierCNN package.
NeuralSpikeClassifierCNN is a free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or any later version.
NeuralSpikeClassifierCNN is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with NeuralSpikeClassifierCNN. If not, see <https://www.gnu.org/licenses/>
"""

import matplotlib.pyplot as plt
import numpy as np


def plot_cutout_overlap(ax, cutouts=list):
    x_axis = np.linspace(start=0, stop=3000, num=75)
    
    max_aplitude = 0
    min_aplitude = 0

    if len(cutouts) > 2:
        for cutout in cutouts:
            ax.plot(x_axis, cutout, color="grey")
            if max_aplitude < max(cutout):
                max_aplitude = max(cutout)
            if min_aplitude > min(cutout):
                min_aplitude = min(cutout)
        

        ax.plot(x_axis, np.mean(cutouts, axis=0), color='red', linewidth=2, label="Mean")
        ax.grid(True)
        ax.set_xlabel('us')
        ax.set_ylabel('uV')
        ax.axvline(x=1000.0, color='r', linestyle='-')
        ax.axvline(x=500.0, color='b', linestyle='--')
        ax.axvline(x=1500.0, color='b', linestyle='--')
        ax.axhline(y=min_aplitude, color='grey', linestyle='--')
        ax.axhline(y=max_aplitude, color='grey', linestyle='--')
        ax.axhline(y=0, color='grey', linestyle='--', alpha=0.2)
        ax.fill_between(x=[500, 1500], y1=min_aplitude, y2=max_aplitude, color='b', alpha=0.1)
        ax.fill_between(x=[0, 500], y1=min_aplitude, y2=max_aplitude, color='grey', alpha=0.5)
        ax.fill_between(x=[1500, 3000], y1=min_aplitude, y2=max_aplitude, color='grey', alpha=0.5)

    else:
        ax.text(0.5, 0.5, "no cutouts.", verticalalignment='center', horizontalalignment='center', transform=ax.transAxes)


def plot_cutout(cutout, lab="Cutout", title="cutout"):
    x_axis = np.linspace(start=0, stop=3000, num=75)

    plt.plot(x_axis, cutout, color="red", label=lab)
    plt.grid(True)
    plt.xlabel('us')
    plt.ylabel('uV')
    plt.title(title)
    plt.axvline(x=1000.0, color='b', linestyle='-')
    plt.axvline(x=500.0, color='b', linestyle='--')
    plt.axvline(x=1500.0, color='b', linestyle='--')
    plt.axhline(y=0, color='grey', linestyle='--', alpha=0.2)
    plt.axhline(y=20, color='grey', linestyle='--', alpha=0.2)
    plt.axhline(y=-20, color='grey', linestyle='--', alpha=0.2)
    plt.show()



