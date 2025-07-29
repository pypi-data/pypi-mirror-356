# ScodaKit: A scientific Python-based command line toolkit for S-coda seismic wave analysis and scattering parameters estimation

**ScodaKit** is an open-source command-line pipeline for estimating the **scattering parameters of S-coda waves** from seismic waveform data. It combines waveform downloading, manual seismic phase picking, catalog metadata merging, coda window extraction, energy decay analysis and visualization — all within a modular and extensible architecture.

> Designed for researchers, seismologists, and geophysicists working on seismic attenuation, crustal scattering, or seismic coda-based energy models.

---

## 🛠️ Features

This command-line pipeline allows you to:

- 📡 Download waveform data from FDSN-compliant data centers (e.g., NOA, IRIS)
- ⌛ Manual picking of **P and S seismic wave arrivals** using interactive seismic waveform viewers
- 🗃️ Merge waveform arrival data with seismic event metadata
- 🌍 Generate interactive or GIS-compatible **maps of events and stations**
- 🧠 Extract **S-coda waveforms** from the seismic traces using signal to noise ratio (SNR) method
- 📉 Analyze S-coda energy decay to estimate **mean free path (ℓ)** and **Coda attenuation factor (B)** using the Single Isotropic Scattering Model
- 📊 Visualize full waveforms, spectrograms and coda windows 
- 📉Analyze and visualize results statistically
- 🧪 Modular stages via CLI for reproducible research

---

For more information please visit https://github.com/marioskaragiorgas/ScodaKit

**Copyright:** Marios Karagiorgas <karagiorgasmarios@gmail.com>

**license:** https://www.apache.org/licenses/LICENSE-2.0