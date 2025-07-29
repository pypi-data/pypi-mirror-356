# -*- coding: utf-8 -*-
"""
plots.py

This script provides functionality to:
- Plot full 3-component seismic waveforms with annotated origin, P, and S arrival times.
- Plot the corresponding spectrogram or wavelet transform.
- Do the same for extracted S-coda waveforms.
- Save figures to designated output directories.

Inputs:
- Excel with arrival times (origin, P, S)
- Folder with validated waveform files (.mseed)
- Folder with extracted coda windows (.mseed)

Output:
- PNG plots for full traces and codas with annotations and time-frequency analysis.
"""

import os
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from obspy import read, UTCDateTime
from scipy.signal import spectrogram


def plot_trace_with_annotations(tr, p_time, s_time, origin_time, tc , coda_endtime, ax, label_color):
    times = tr.times(reftime=origin_time)
    ax.plot(times, tr.data, linewidth=0.3, label=f"{tr.stats.channel}", color=label_color)
    ax.axvline((p_time - origin_time), linestyle="--", color="r", label='P')
    ax.axvline((s_time - origin_time), linestyle="--", color="b", label='S')
    ax.axvline((tc - origin_time), linestyle="--", color="k", label='Coda start')
    ax.axvline((coda_endtime - origin_time), linestyle="--", color="g", label='Coda end')
    #ax.axvline(0, linestyle="--", color="k", label='Origin')
    ax.set_ylabel("Amplitude (m/s)")
    ax.legend(loc='upper right', fontsize=8)
    ax.grid(True)

def trace_spectrogram(trace, fs, window_duration=0.1, overlap=0.5, scaling='density', log_scale=False):
    """
    Compute the spectrogram of a seismic trace using short-time Fourier transform (STFT).
    
    Parameters:
        trace (ndarray): The seismic trace to analyze.
        fs (float): The sampling frequency of the trace.
        window_duration (float): Duration of the STFT window in seconds (default: 0.1).
        overlap (float): Fraction of overlap between windows (default: 0.5).
        scaling (str): Scaling of the spectrogram ('density' or 'spectrum').
        log_scale (bool): Whether to return the spectrogram in log scale (default: False).
    
    Returns:
        tuple:
            - f (ndarray): Array of sample frequencies [Hz].
            - t (ndarray): Array of time segments [s].
            - Sxx (ndarray): Spectrogram of the trace.
    """
    # Define the window length and overlap
    window_length = int(window_duration * fs)
    window = np.hanning(window_length)
    noverlap = int(window_length * overlap)
    nfft = max(256, 2 ** int(np.ceil(np.log2(window_length))))  # Power of 2 for FFT length

    # Compute the spectrogram
    f, t, Sxx = spectrogram(trace, fs, window=window, noverlap=noverlap, nfft=nfft, scaling=scaling)

    # Optionally convert to logarithmic scale
    if log_scale:
        Sxx = 10 * np.log10(Sxx + 1e-12)  # Add small value to avoid log(0)

    return f, t, Sxx

def plot_spectrogram(tr, ax):
    tr.spectrogram(log=False, axes=ax, wlen=int(0.1 * tr.stats.sampling_rate), cmap='nipy_spectral', show=False, samp_rate =tr.stats.sampling_rate, dbscale = True)
    fs = tr.stats.sampling_rate
    #f, t, Sxx = trace_spectrogram(tr.data, fs, window_duration=0.1, overlap=0.5, scaling='density', log_scale=False)
    #ax.pcolormesh(t, f, 10 * np.log10(Sxx), shading='gouraud', cmap='jet')
    ax.set_ylabel("Frequency (Hz)")
    ax.set_xlabel("Time (s)")
    ax.grid(True)

def plot_waveform_and_spectrogram(
    mseed_file, origin_time, p_time, s_time, tc, coda_endtime,
    out_dir
):
    """Plot 3-component waveform and spectrogram"""
    st = read(mseed_file)
    fig, axs = plt.subplots(4, 1, figsize=(10, 8), sharex=True)
    plot_trace_with_annotations(st[0], p_time, s_time, origin_time, tc, coda_endtime, axs[0], 'm')
    plot_trace_with_annotations(st[1], p_time, s_time, origin_time, tc, coda_endtime, axs[1], 'g')
    plot_trace_with_annotations(st[2], p_time, s_time, origin_time, tc, coda_endtime, axs[2], 'c')
    axs[0].set_title(f"Waveform: {st[0].stats.station} | {origin_time.date}")
    plot_spectrogram(st[0], axs[3])
    axs[3].set_title("Spectrogram (Vertical Component)")
    plt.tight_layout()
    fname = f"{origin_time.strftime('%Y%m%dT%H%M%S')}_{st[0].stats.station}_full.png"
    fig.savefig(Path(out_dir) / fname, dpi=200)
    plt.close(fig)

def plot_coda_with_spectrogram(mseed_file, origin_time, out_dir):
    """Plot 3-component coda waveform and spectrogram"""
    st = read(mseed_file)
    fig, axs = plt.subplots(3, 1, figsize=(10, 8), sharex=True)
    axs[0].plot(st[0].times(), st[0].data, linewidth=0.3, color='m', label=st[0].stats.channel)
    axs[1].plot(st[1].times(), st[1].data, linewidth=0.3, color='g', label=st[1].stats.channel)
    axs[2].plot(st[2].times(), st[2].data, linewidth=0.3, color='c', label=st[2].stats.channel)
    axs[0].set_ylabel("Amplitude (m/s)")
    axs[1].set_ylabel("Amplitude (m/s)")
    axs[2].set_ylabel("Amplitude (m/s)")
    axs[2].set_xlabel("Time (s)")
    axs[0].legend(loc='upper right', fontsize=8)
    axs[1].legend(loc='upper right', fontsize=8)
    axs[2].legend(loc='upper right', fontsize=8)
    axs[0].set_title(f"Coda: {st[0].stats.station} | {origin_time.date}")
    for ax in axs[:3]:
        ax.grid(True)
    #plot_spectrogram(st[0], axs[3])
    #axs[3].set_title("Spectrogram (Vertical Component)")
    plt.tight_layout()
    fname = f"{origin_time.strftime('%Y%m%dT%H%M%S')}_{st[0].stats.station}_coda.png"
    fig.savefig(Path(out_dir) / fname, dpi=200)
    plt.close(fig)

def plot_all(
    arrival_excel, validated_waveforms_dir, coda_waveforms_dir,
    output_full_dir, output_coda_dir
):
    """
    Plot all full and coda waveforms with spectrograms.

    Parameters
    ----------
    arrival_excel : str
        Path to Excel file with arrival times.
    validated_waveforms_dir : str
        Folder containing full waveforms.
    coda_waveforms_dir : str
        Folder containing coda waveforms.
    output_full_dir : str
        Folder to save full waveform plots.
    output_coda_dir : str
        Folder to save coda waveform plots.
    """
    df = pd.read_excel(arrival_excel)
    Path(output_full_dir).mkdir(parents=True, exist_ok=True)
    Path(output_coda_dir).mkdir(parents=True, exist_ok=True)

    print("Generating Plots...")
    for i, row in df.iterrows():
        origin = UTCDateTime(row['Origin time'])
        p_arr = UTCDateTime(row['P arrival time'])
        s_arr = UTCDateTime(row['S arrival time'])
       
        base_name = f"{origin.strftime('%Y-%m-%d-%H-%M-%S')}_{row['Network']}_{row['Station']}.mseed"
        full_path = Path(validated_waveforms_dir) / base_name
        coda_path = Path(coda_waveforms_dir) / base_name
        # read the coda file to extract the tc and coda_endtime
        if coda_path.exists():
            st = read(coda_path)
            tc = st[0].stats.starttime
            if len(st) > 0:
                coda_endtime = st[0].stats.endtime
            else:
                print(f"No data in {coda_path}, skipping.")
                continue
        else:
            print(f"Coda file {coda_path} does not exist, skipping.")
            continue
        
        if full_path.exists():
            plot_waveform_and_spectrogram(full_path, origin, p_arr, s_arr, tc, coda_endtime, output_full_dir)
        if coda_path.exists():
            plot_coda_with_spectrogram(coda_path, origin, output_coda_dir)
    
    