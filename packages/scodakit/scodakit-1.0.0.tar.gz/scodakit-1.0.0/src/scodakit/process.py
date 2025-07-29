# -*- coding: utf-8 -*-
"""
process.py

This module processes S-coda waveforms to estimate the mean free path using the single isotropic scattering model.
It includes:
    - Loading and slicing waveforms
    - Signal-to-noise ratio filtering
    - Coda window selection
    - RMS amplitude calculations
    - Energy decay curve generation
    - Linear regression on F(t) to estimate mean free path and coda attenuation factor

Inputs:
    - Excel file containing the data for analusis. Must include:
        - P/S arrivals
        - Origin time
        - Hypocentral distance
        - S-wave Radiated energy
    - Directory of validated waveform files (MiniSEED)
    - Output directories for coda segments, figures, and Excel summaries
"""

import os
import logging
from pathlib import Path
import pandas as pd
import numpy as np
from obspy import read, UTCDateTime
from matplotlib import pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score


# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def rms(data: np.ndarray, power: int = 2):
    """
    Compute the Root Mean Square (RMS) of a numeric array.

    Parameters
    ----------
    data : np.ndarray
        Input array containing signal data.
    power : int, optional
        The exponent used before averaging. Default is 2 (standard RMS).

    Returns
    -------
    float
        The RMS value. Returns np.nan if input is empty.
    """
    if data.size == 0:
        return np.nan
    return np.sqrt(np.mean(np.power(data, power)))


def extract_coda_window(
    stream_path, coda_dir, p_arrival, s_arrival, origin_time,
    snr_threshold=3.0, noise_window_length=3.0, debug=False
):
    """
    Extract the S-coda window from a waveform based on SNR.

    Parameters
    ----------
    stream_path : str
        Path to the miniSEED file.
    p_arrival : UTCDateTime
        P-wave arrival time.
    s_arrival : UTCDateTime
        S-wave arrival time.
    origin_time : UTCDateTime
        Event origin time.
    snr_threshold : float
        SNR threshold for coda end.
    noise_window_length : float
        Length of the noise and signal window in seconds.
    coda_dir : str
        directory to save the extracted coda window.
    debug : bool
        If True, plot the SNR curve and waveform with annotations.

    Returns
    -------
    obspy.Stream or None
        Coda window stream, or None if invalid.
    """
    try:
        st = read(stream_path)
        if len(st) < 1:
            raise ValueError("No traces in stream.")
        tr = st[0]  # Use vertical component

        fs = tr.stats.sampling_rate
        samples_per_window = int(noise_window_length * fs)
        tsp = s_arrival - p_arrival
        tc = p_arrival + 2 * tsp

        noise_data = tr.slice(
            starttime=p_arrival - noise_window_length,
            endtime=p_arrival,
            nearest_sample=False
        ).data

        if len(noise_data) < samples_per_window:
            raise ValueError("Insufficient data in noise window.")

        rms_noise = rms(noise_data)
        logging.info(f"[{stream_path}] RMS noise: {rms_noise}")

        signal_trace = tr.slice(starttime=tc, endtime=tr.stats.endtime)
        signal_data = signal_trace.data
        n_samples = len(signal_data)

        snr_values = []
        coda_end_time = tr.stats.endtime  # fallback

        # Iterate over the signal data to compute SNR after the first 10 seconds (Tc + 10s) and find the coda end time
        for i in range(int(10 * fs), n_samples - samples_per_window):
            window = signal_data[i:i + samples_per_window]
            rms_signal = rms(window)
            snr = rms_signal / rms_noise
            snr_values.append(snr)

            if snr <= snr_threshold:
                coda_end_time = tc + i / fs
                logging.info(f"[{stream_path}] Coda ends at {coda_end_time} (SNR={snr:.2f})")
                break

        coda_window = st.slice(starttime=tc, endtime=coda_end_time)

        # Save coda window to file
        coda_window.write(os.path.join(coda_dir, os.path.basename(stream_path)), format='MSEED')
        if not os.path.exists(coda_dir):
            os.makedirs(coda_dir)

        if debug:

            logging.info(f"Coda start: {tc}, end: {coda_end_time}, duration: {coda_end_time - tc} seconds")
            logging.info(f"Signal-to-noise ratio threshold: {snr_threshold}")
            logging.info(f"Number of samples in coda window: {len(coda_window)}")
            logging.info(f"Number of samples in noise window: {len(noise_data)}")
            logging.info(f"Number of samples in signal window: {len(signal_data)}")

            # Plot SNR curve
            plt.figure(figsize=(10, 5))
            time_axis = np.arange(0, len(snr_values)) / fs
            plt.plot(time_axis, snr_values)
            plt.axhline(y=snr_threshold, color='r', linestyle='--', label='SNR Threshold')
            plt.title(f"SNR Curve for {os.path.basename(stream_path)}")
            plt.xlabel("Time after Tc (s)")
            plt.ylabel("SNR")
            plt.legend()
            plt.tight_layout()
            plt.show()

            # Plot waveform with annotations
            plt.figure(figsize=(10, 5))
            plt.plot(tr.times(), tr.data, label='Waveform')
            plt.axvline(x=(p_arrival - noise_window_length - tr.stats.starttime), color='c', linestyle='--', label='Noise Start')
            plt.axvline(x=(p_arrival - tr.stats.starttime), color='g', linestyle='--', label='P Arrival')
            plt.axvline(x=(s_arrival - tr.stats.starttime), color='b', linestyle='--', label='S Arrival')
            plt.axvline(x=(tc - tr.stats.starttime), color='y', linestyle='--', label='Tc')
            plt.axvline(x=(coda_end_time - tr.stats.starttime), color='r', linestyle='--', label='Coda End')
            plt.title(f"Waveform with Arrival Times for {os.path.basename(stream_path)}")
            plt.xlabel("Time (s)")
            plt.ylabel("Amplitude")
            plt.legend()
            plt.tight_layout()
            plt.show()

        if not (coda_end_time - tc) < 1.0:
            return coda_window
        
        else:
            # If coda window is too short, log a warning 
            logging.warning(f"Coda window too short: {coda_end_time - tc} seconds, and will not be extracted.")
            return None

    except Exception as e:
        logging.error(f"Error extracting coda window from {stream_path}: {e}")
        return None

def compute_energy_decay(coda, origin_time, s_delay, r_km, w_erg):
    """
    Compute energy decay metrics from coda stream.

    Parameters
    ----------
    coda : obspy.Stream
        Stream containing coda window.
    origin_time : UTCDateTime
        Origin time.
    s_delay : float
        S arrival - origin in seconds.
    r_km : float
        Source-receiver distance in kilometers.
    w_erg : float
        S-wave Radiated energy in erg.
 
    Returns
    -------
    pd.DataFrame
        Energy decay data.
    """
    try:
        Dt = 2
        values = {'Vx^2(t)': [], 'Vy^2(t)': [], 'Vz^2(t)': [], 'lapse time t': []}
        for win in coda.slide(window_length=Dt, step=Dt):
            values['Vx^2(t)'].append(np.mean(win[0].data**2))
            values['Vy^2(t)'].append(np.mean(win[1].data**2))
            values['Vz^2(t)'].append(np.mean(win[2].data**2))
            values['lapse time t'].append(win[0].stats.endtime - origin_time)
        df = pd.DataFrame(values)
        df['Ax^2(t)'] = df['Vx^2(t)'] * 1e4
        df['Ay^2(t)'] = df['Vy^2(t)'] * 1e4
        df['Az^2(t)'] = df['Vz^2(t)'] * 1e4
        df['t/ts'] = df['lapse time t'] / s_delay
        df['K(t/ts)'] = (1 / df['t/ts']) * np.log((df['t/ts'] + 1) / (df['t/ts'] - 1))
        df['m[gr/cm^3]'] = 2.7
        df['W(M)[erg]'] = w_erg
        df['R^2[cm^2]'] = (r_km ** 2) * 1e10
        df['F(t)[cm]'] = np.log10((df['W(M)[erg]'] / (8 * np.pi * df['R^2[cm^2]'])) * df['K(t/ts)']) - \
                        np.log10(2.7 * (df['Ax^2(t)'] + df['Ay^2(t)'] + df['Az^2(t)']))
        return df
    except Exception as e:
        logging.error(f"Error computing energy decay: {e}")
        return None

def process_event_batch(
    data_catalog, waveform_dir, output_dir,

):
    """
    Process all events in the given Excel catalog.

    Parameters
    ----------
    data_catalog : str
        Excel file containing the data for analysis.
    waveform_dir : str
        Folder containing waveform files.
    coda_dir : str
        Folder to save extracted coda segments.
    output_dir : str
        Output folder to save results.
    
    """
    try:
        df_phases = pd.read_excel(data_catalog)
        logging.info(f"Loaded {len(df_phases)} events from {data_catalog}")
        logging.info(f"Processing {len([f for f in Path(waveform_dir).iterdir() if f.is_file()])} validated waveforms from {waveform_dir}")
        if not os.path.exists(waveform_dir):
            logging.error(f"Waveform directory {waveform_dir} does not exist.")
            return None
        if not os.path.exists(data_catalog):
            logging.error(f"Data catalog {data_catalog} does not exist.")
            return None
        if not os.path.exists(output_dir):
            logging.error(f"Output directory {output_dir} does not exist. Attempting to create it.")
            os.makedirs(output_dir)
        # Display the df_phases DataFrame
        logging.info(f"Data catalog:\n{df_phases.head()}")
        
        # Create coda directory if it doesn't exist
        if not os.path.exists(os.path.join(output_dir, "coda_segments")):
            os.makedirs(os.path.join(output_dir, "coda_segments"))
        coda_dir = os.path.join(output_dir, "coda_segments")
        logging.info(f"Creating coda directory: {coda_dir}")
        results = {'Origin Time': [], 'Magnitude (ML)': [], 'S-wave Radiated Energy (erg)': [],
                   'Hypocentral Distance (km)': [], 'log10l': [], 'B': [], 'R²': [], 'Mean Free Path (cm)': []}

        for i, row in df_phases.iterrows():
            origin = UTCDateTime(row['Origin time'])
            #logging.info(f"Processing event {i + 1}/{len(df_phases)}: {origin}")
            p_arr = UTCDateTime(row['P arrival time'])
            #logging.info(f"P arrival time: {p_arr}")
            s_arr = UTCDateTime(row['S arrival time'])
            #logging.info(f"S arrival time: {s_arr}")
            r = row['Hypocentral Distance R (km)']
            #logging.info(f"Hypocentral distance: {r} km")
            w = row['S Wave Radiated Energy W (erg)']
            m = row['Magnitude (ML)']
            #logging.info(f"Magnitude: {m} ML")
            #logging.info(f"S-wave radiated energy: {w} erg")
            tsp = s_arr - p_arr

            fname = f"{origin.strftime('%Y-%m-%d-%H-%M-%S')}_{row['Network']}_{row['Station']}.mseed"
            fpath = os.path.join(waveform_dir, fname)
            
            logging.info(f"Processing {i}/{len(df_phases)} waveform: {fpath}")
            if not os.path.exists(fpath):
                logging.warning(f"File {fpath} does not exist. Skipping.")
                continue
            
            # Extract coda window
            logging.info(f"Extracting coda window")
            coda = extract_coda_window(fpath, coda_dir, p_arr, s_arr, origin, snr_threshold = 3.0, noise_window_length=10.0, debug=False)
            logging.info(f"Coda window extracted and stored in: {coda}")
            if coda is None:
                logging.warning(f"No valid coda window found for {fpath}. Skipping.")
                continue

            # Compute energy decay
            logging.info(f"Computing energy decay")
            df = compute_energy_decay(coda, origin, s_arr - origin, r, w)
            if df is None or df.empty:
                logging.warning(f"Empty DataFrame for {fpath}. Skipping.")
                continue
            X = df['lapse time t'].values.reshape(-1, 1)
            Y = df['F(t)[cm]'].values.reshape(-1, 1)

            model = LinearRegression().fit(X, Y)
            Y_pred = model.predict(X)
            r2 = r2_score(Y, Y_pred)
            results['Origin Time'].append(origin)
            results['Magnitude (ML)'].append(m)
            results['S-wave Radiated Energy (erg)'].append(w)
            results['Hypocentral Distance (km)'].append(r)
            results['log10l'].append(model.intercept_[0])
            results['B'].append(model.coef_[0][0])
            results['R²'].append(r2)
            results['Mean Free Path (cm)'].append(10 ** model.intercept_[0]) 
           
            logging.info(f"Processed event {i + 1}/{len(df_phases)}: Origin Time: {origin}, "
                         f"ML: {m}, S-wave Energy: {w} erg, R: {r} km, "
                         f"log10l: {model.intercept_[0]}, B: {model.coef_[0][0]}, R²: {r2:.2f}")

            #logging.info(f"Event {i + 1}/{len(df_phases)}: log10l: {model.intercept_[0]} | B: {model.coef_[0][0]} | R²: {r2}")
           
            fig, ax = plt.subplots()
            ax.scatter(X, Y, s=10)
            ax.plot(X, Y_pred, color='red')
            ax.set_title(f"F(t) vs t | R² = {r2:.2f}")
            ax.set_xlabel("Lapse Time t (s)")
            ax.set_ylabel("F(t)")
            plt.tight_layout()
            fig_path = os.path.join(output_dir, f"{origin.strftime('%Y%m%d_%H%M%S')}_Ft_fit.png")
            fig.savefig(fig_path, dpi=200)
            plt.close()
        
        df_out = pd.DataFrame(results)
        path = os.path.join(output_dir, "scattering_par_summary.xlsx")
        df_out.to_excel(path, index=False)
        logging.info(f"Processing complete. S-coda scattering parametres summary saved to {path}")
    except Exception as e:
        logging.error(f"Error processing event batch: {e}")
        return None