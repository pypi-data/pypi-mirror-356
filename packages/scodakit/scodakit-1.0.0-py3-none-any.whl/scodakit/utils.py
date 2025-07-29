# -*- coding: utf-8 -*-
"""
utils.py

This module provides utility functions and classes for seismic data processing.
It includes functions for filtering seismic data using Butterworth IIR filters

Filters utility class for seismic data processing.

This module provides a class for applying Butterworth IIR filters to seismic or signal data.
It supports highpass, lowpass, and bandpass filtering using second-order sections (sos).
The filters are designed to be used with 1D numpy arrays representing the signal data.
The class includes methods for:
- highpass_filter: Apply a highpass Butterworth filter.
- lowpass_filter: Apply a lowpass Butterworth filter.
- bandpass_filter: Apply a bandpass Butterworth filter.
- filter_for_phase_distinction: Filter a seismic trace to enhance either P or S arrival clarity.
"""

from scipy import signal
import numpy as np

class Filters:
    """
    A utility class for applying Butterworth IIR filters to seismic or signal data.
    Supports highpass, lowpass, and bandpass filtering using second-order sections (sos).
    """

    @staticmethod
    def highpass_filter(signal_data: np.ndarray, sample_rate: float, filter_order: int, cutoff_freq: float):
        """
        Apply a highpass Butterworth filter.
        
        Parameters:
        - signal_data: Input signal as 1D numpy array.
        - sample_rate: Sampling rate in Hz.
        - filter_order: Filter order (higher = sharper cutoff).
        - cutoff_freq: Highpass cutoff frequency in Hz.

        Returns:
        - Filtered signal as 1D numpy array.
        """
        nyquist = sample_rate / 2
        if cutoff_freq >= nyquist:
            raise ValueError(f"Highpass frequency {cutoff_freq} must be < Nyquist {nyquist}.")
        sos = signal.butter(filter_order, cutoff_freq, 'highpass', fs=sample_rate, output='sos')
        return signal.sosfilt(sos, signal_data)

    @staticmethod
    def lowpass_filter(signal_data: np.ndarray, sample_rate: float, filter_order: int, cutoff_freq: float):
        """
        Apply a lowpass Butterworth filter.

        Parameters:
        - signal_data: Input signal as 1D numpy array.
        - sample_rate: Sampling rate in Hz.
        - filter_order: Filter order.
        - cutoff_freq: Lowpass cutoff frequency in Hz.

        Returns:
        - Filtered signal as 1D numpy array.
        """
        nyquist = sample_rate / 2
        if cutoff_freq >= nyquist:
            raise ValueError(f"Lowpass frequency {cutoff_freq} must be < Nyquist {nyquist}.")
        sos = signal.butter(filter_order, cutoff_freq, 'lowpass', fs=sample_rate, output='sos')
        return signal.sosfilt(sos, signal_data)

    @staticmethod
    def bandpass_filter(signal_data: np.ndarray, sample_rate: float, filter_order: int, freqmin: float, freqmax: float):
        """
        Apply a bandpass Butterworth filter.

        Parameters:
        - signal_data: Input signal as 1D numpy array.
        - sample_rate: Sampling rate in Hz.
        - filter_order: Filter order.
        - freqmin: Lower cutoff frequency.
        - freqmax: Upper cutoff frequency.

        Returns:
        - Filtered signal as 1D numpy array.
        """
        nyquist = sample_rate / 2
        if freqmax >= nyquist:
            raise ValueError(f"Bandpass max frequency {freqmax} must be < Nyquist {nyquist}.")
        if freqmin >= freqmax:
            raise ValueError(f"Minimum frequency {freqmin} must be < maximum frequency {freqmax}.")
        sos = signal.butter(filter_order, [freqmin, freqmax], 'bandpass', fs=sample_rate, output='sos')
        return signal.sosfilt(sos, signal_data)

    @staticmethod
    def filter_for_phase_distinction(signal_data: np.ndarray, sample_rate: float, phase: str, filter_order: int):
        """
        Filter a seismic trace to enhance either P or S arrival clarity.

        Parameters:
        - signal_data: Input signal as 1D numpy array.
        - phase: 'P' or 'S'
        - filter_order: IIR filter order
        - sample_rate: Sampling rate in Hz.

        Returns:
        - Filtered data as numpy array
        """
        fs = sample_rate

        if phase.upper() == 'P':
            return Filters.bandpass_filter(signal_data, fs, filter_order, freqmin=5.0, freqmax=15.0)
        elif phase.upper() == 'S':
            return Filters.bandpass_filter(signal_data, fs, filter_order, freqmin=2.0, freqmax=10.0)
        else:
            raise ValueError("Seismic phase must be either 'P' or 'S'")
