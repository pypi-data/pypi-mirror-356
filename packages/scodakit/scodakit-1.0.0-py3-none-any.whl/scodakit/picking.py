# -*- coding: utf-8 -*-
"""
picking.py

This script allows for manual picking of P and S phases from seismic waveforms.
It reads .mseed files from a specified folder, applies a bandpass filter,
and displays the waveforms for manual picking. The picked arrival times
are saved to an Excel file, and the validated waveforms are saved to a specified folder.
The script uses the ObsPy library for seismic data handling and Matplotlib for plotting.

Author: Marios Karagiorgas  
"""

import os
import logging
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import SpanSelector
from obspy import read
from scodakit.utils import Filters

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def pick_phases_from_folder(
    input_folder: str, 
    output_excel: str,
    output_waveform_folder: str,
):
    """
    Allows manual P and S phase picking from seismic waveforms.

    Parameters
    ----------
    input_folder : str
        Directory containing input .mseed files.
    output_excel : str
        Path to save the picked arrival times.
    output_waveform_folder : str
        Directory to save validated waveform files.
    """
    Path(output_waveform_folder).mkdir(parents=True, exist_ok=True)

    logging.info(f"Starting phase picking from folder: {input_folder}")
    if not os.path.exists(input_folder):
        logging.error(f"Input folder {input_folder} does not exist.")
        return
    
    seismic_files = []
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.endswith('.mseed'):
                seismic_files.append(os.path.join(root, file))

    data_dict = {'Origin time': [], 'P arrival time': [], 'S arrival time': [], 'Network': [], 'Station': []}

    for fname in seismic_files:
        stream_path = os.path.join(input_folder, fname)
        format = os.path.splitext(fname)[-1].upper()
        st = read(stream_path, format).copy()
        trE, trN, trZ = st[0], st[1], st[2]

        trE_data = trE.data
        trE_filt = Filters.filter_for_phase_distinction(trE_data, trE.stats.sampling_rate, 'S', 4) 
        trZ_data = trZ.data
        trZ_filt = Filters.filter_for_phase_distinction(trZ_data, trZ.stats.sampling_rate, 'P', 4)

        logging.info(f"Opening interactive waveform plot of {fname} file...")
        logging.info("Use red bar for P, blue for S. Press [Q] to quit each window.")
        fig, ax = plt.subplots(2, 1, sharex=True)
        ax[0].plot(trZ.times(), trZ_filt, 'k-', linewidth=0.5)
        ax[0].set_title(f"{trZ.stats.network}.{trZ.stats.station}.{trZ.stats.channel} | {trZ.stats.starttime}")
        ax[0].set_ylabel("Amplitude")
        trZ.spectrogram(log=False, axes=ax[1], wlen=int(0.1 * trZ.stats.sampling_rate), cmap='nipy_spectral', show=False, samp_rate =trZ.stats.sampling_rate, dbscale = True)
        ax[1].set_xlabel("Time (s)")
        ax[1].set_ylabel("Frequency (Hz)")
        ax[1].set_title("Spectrogram")
        plt.tight_layout()
        p_pick, s_pick = [], []

        def onselect_p(xmin, xmax):
            p_pick.append(trZ.stats.starttime + xmin)

        def onselect_s(xmin, xmax):
            s_pick.append(trE.stats.starttime + xmin)

        span1 = SpanSelector(ax[0], onselect_p, 'horizontal', useblit=True, props=dict(alpha=0.5, facecolor='red'))
        plt.show()

        fig, ax = plt.subplots(2, 1, sharex=True)
        ax[0].plot(trE.times(), trE_filt, 'b-', linewidth=0.5)
        ax[0].set_title(f"{trE.stats.network}.{trE.stats.station}.{trE.stats.channel} | {trE.stats.starttime}")
        ax[0].set_ylabel("Amplitude")
        trE.spectrogram(log=False, axes=ax[1], wlen=int(0.1 * trE.stats.sampling_rate), cmap='nipy_spectral', show=False, samp_rate =trE.stats.sampling_rate, dbscale = True)
        ax[1].set_xlabel("Time (s)")
        ax[1].set_ylabel("Frequency (Hz)")
        ax[1].set_title("Spectrogram")
        plt.tight_layout()
        span2 = SpanSelector(ax[0], onselect_s, 'horizontal', useblit=True, props=dict(alpha=0.5, facecolor='blue'))
        plt.show()

        if p_pick and s_pick:
            data_dict['Origin time'].append(trZ.stats.starttime)
            data_dict['P arrival time'].append(p_pick[0])
            data_dict['S arrival time'].append(s_pick[0])
            data_dict['Network'].append(trZ.stats.network)
            data_dict['Station'].append(trZ.stats.station)


            output_name = f"{trZ.stats.starttime.strftime('%Y-%m-%d-%H-%M-%S')}_{trZ.stats.network}_{trZ.stats.station}.mseed"
            
            # Apply bandpass filter to the three components and save the validated waveform
            fs = trE.stats.sampling_rate
            trE.filter("bandpass", freqmin=1, freqmax=30, corners=4, zerophase=True)
            trN.filter("bandpass", freqmin=1, freqmax=30, corners=4, zerophase=True)
            trZ.filter("bandpass", freqmin=1, freqmax=30, corners=4, zerophase=True)
            st.write(os.path.join(output_waveform_folder, output_name), format='MSEED')
            logging.info(f"Saved validated waveform: {output_name}")
        else:
            logging.warning(f"No picks made for {fname}. Skipping...")
        
        plt.close('all')
    
    logging.info(f"All files processed. Saving results to {output_excel}...")

    df = pd.DataFrame(data_dict)
    df.to_excel(output_excel, index=False)
    logging.info(f"Arrival times saved to {output_excel}")