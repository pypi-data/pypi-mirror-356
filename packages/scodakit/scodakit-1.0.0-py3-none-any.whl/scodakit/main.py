# -*- coding: utf-8 -*-
"""
main.py

ScodaKit: A scientific Python-based command line toolkit for S-coda seismic wave analysis and scattering parameters estimation

This script orchestrates the complete S-coda wave analysis and scattering parameters estimation process,
including:
    1. Downloading waveform data
    2. Manual picking of P/S phases
    3. Merging picks with event metadata
    4. Generating maps of events and stations
    5. Extracting and analyzing S-coda waveforms
    6. Visualizing results

Usage:
    scodakit --download --pick --merge_catalog --map --process --plot 

Author: Marios Karagiorgas
"""

import argparse
import logging
import sys
import time
from pathlib import Path


from scodakit.download import download_waveforms
from scodakit.picking import pick_phases_from_folder
from scodakit.merge_catalogue import prepare_catalog_for_mfp
from scodakit.map_generator import generate_map
from scodakit.process import process_event_batch
from scodakit.plots import plot_all

# Check python version compatibility
if sys.version_info.major < 3 or sys.version_info.minor < 8:
    print("Python version 3.7 or higher is required.")
    print(f"Current version: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    print("Please update your Python version.")
    print("Exiting...")
    sys.exit(1)

# Redirects print statements and stdout to both console and a log file.
class DualLogger:
    """Redirect print and stdout to both console and file."""
    def __init__(self, logfile_path):
        self.terminal = sys.stdout
        self.log = open(logfile_path, "w", encoding="utf-8")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        self.terminal.flush()
        self.log.flush()

# Sets up logging to both console and file. If log_to_file is True, it will also redirect stdout to a file
def setup_logging(output_dir: Path, log_to_file: bool = True):
    """Sets up console and optional file logging."""
    
    output_dir.mkdir(parents=True, exist_ok=True)
    log_file = output_dir / "pipeline.log"
    
    # Console formatter: just the message
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter('%(levelname)s- %(message)s'))

    logging.basicConfig(
        level=logging.INFO,
        handlers=[console_handler]
    )

    # If file logging enabled, redirect stdout (print) and also attach a file handler to logging
    if log_to_file:
        # Redirect print() to file
        sys.stdout = DualLogger(log_file)

        # Add file handler to logging module
        file_handler = logging.FileHandler(log_file, mode='a', encoding="utf-8")
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logging.getLogger().addHandler(file_handler)

        logging.info("Logging to file enabled.")

# Check for required dependencies
def check_dependencies():
    try:
        import obspy
        import pandas as pd
        import numpy as np
        import matplotlib.pyplot as plt
        import sklearn
        import geopandas as gpd
        import cartopy
        import cartopy.crs as ccrs
        import cartopy.feature as cfeature
    except ImportError as e:
        logging.error(f"Missing dependency: {e.name}. Install it using pip.")
        return False
    return True

def log_stage(name):
    print(f"\n{'='*50}\n Starting Stage: {name}\n{'='*50}")
    return time.time()

def log_stage_complete(start_time, stage_name):
    duration = time.time() - start_time
    logging.info(f"{stage_name} completed in {duration:.1f} seconds.")

def main():
    pipeline_start = time.time()
    parser = argparse.ArgumentParser(
        description="Scodakit" \
        "A scientific Python-based command line toolkit for S-coda seismic wave analysis and scattering parameters estimation",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )


    # Pipeline stages
    parser.add_argument('--download', action='store_true', help="Download waveforms from FDSN")
    parser.add_argument('--pick', action='store_true', help="Manually pick P and S arrivals")
    parser.add_argument('--merge_catalog', action='store_true', help="Merge picks with seismic metadata")
    parser.add_argument('--map', action='store_true', help="Create GIS-compatible maps and export event/station data")
    parser.add_argument('--process', action='store_true', help="Extract S-coda and compute mean free path")
    parser.add_argument('--plot', action='store_true', help="Plot waveforms")
    parser.add_argument('--analyze', action='store_true', help="Run post-analysis")

    # Downloading options
    parser.add_argument('--catalog', type=str, help="Seismic event catalog file (.xml, .csv, .xlsx)")
    parser.add_argument('--stations', nargs='+', default=None, help="Station codes (e.g., ['ATH'], ['KAL', 'KAL2']) or a single station code as a string (e.g., 'ATH')")
    parser.add_argument('--radius', type=float, default=None, help="Search radius in km")
    parser.add_argument('--channels', type=str, default="HH?", help="SEED channel pattern (e.g., HH?)")
    parser.add_argument('--start_offset', type=int, default=-30, help="Seconds before origin")
    parser.add_argument('--end_offset', type=int, default=150, help="Seconds after origin")
    parser.add_argument('--output_format', type=str, default="MSEED", help="Waveform format")
    parser.add_argument('--node', type=str, default="NOA", help="FDSN data node")
    parser.add_argument('--network_filter', nargs='+', default=["HL"], help="Allowed network codes")

    # Map Generation options
    parser.add_argument('--map_output_dir', type=str, default="maps", help="Output directory for maps. Will be created if it doesn't exist.")
    parser.add_argument('--image_formats', nargs='+', default=["png", "pdf"], help="Image formats for map output")
    parser.add_argument('--export_formats', nargs='+', default=["geojson", "csv"], help="Export formats for map data (e.g., geojson, csv, shapefile)")

    # General
    parser.add_argument('--output_dir', type=str, default=None, help="Base output directory containing the results specified by the user. Will be created if it doesn't exist.")
    parser.add_argument('--log_to_file', action='store_true', help="Also write logs to pipeline.log")

    args = parser.parse_args()

    # Validate and process output directory
    if not args.output_dir:
        logging.error("Output directory must be specified using --output_dir")
        sys.exit(1)
     
    output_dir = Path(args.output_dir / 'results')
    if not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)

    setup_logging(output_dir, args.log_to_file)

    logging.info("S-coda Mean Free Path Pipeline started.")
    logging.info(f"Working directory: {output_dir}")
    logging.info(f"User arguments: {args}")

    if not check_dependencies():
        sys.exit(1)

    if (args.download or args.merge_catalog) and not Path(args.catalog).exists():
        logging.error(f"Catalog file not found: {args.catalog}")
        sys.exit(1)

    # STAGE 1: Download
    if args.download:
        start = log_stage("Downloading Waveforms")
        download_waveforms(
            catalogue_path=args.catalog,
            station_list=args.stations, #if not (len(args.stations) == 1 and args.stations[0].isdigit()) else None,
            radius=args.radius,
            channels=args.channels,
            start_offset=args.start_offset,
            end_offset=args.end_offset,
            output_format=args.output_format,
            node=args.node,
            network_filter=args.network_filter,
            destination=output_dir / "waveforms"
        )
        log_stage_complete(start, "Download")
    else:
        logging.info("Skipping download stage (--download not set)")

    # STAGE 2: Pick Phases
    if args.pick:
        start = log_stage("Manual P/S Phase Picking")
        pick_phases_from_folder(
            input_folder=str(output_dir / "waveforms"),
            output_excel=str(output_dir / "arrival_times.xlsx"),
            output_waveform_folder=str(output_dir / "validated_waveforms")
        )
        log_stage_complete(start, "Picking")
    else:
        logging.info("Skipping picking stage (--pick not set)")

    # STAGE 3: Merge Catalog
    if args.merge_catalog:
        start = log_stage("Merging Picks with Catalog")
        prepare_catalog_for_mfp(
            picks_excel=str(output_dir / "arrival_times.xlsx"),
            seismic_catalog=args.catalog,
            output_excel=str(output_dir / "merged_catalog.xlsx"),
            client=args.node
        )
        log_stage_complete(start, "Merge Catalog")
    else:
        logging.info("Skipping merge_catalog stage (--merge_catalog not set)")

    # STAGE 4: Generate Map
    if args.map:
        start = log_stage("Generating Map")
        generate_map(
            catalogue_path=str(output_dir / "merged_catalog.xlsx"),
            output_dir=str(output_dir / args.map_output_dir),
            image_formats=args.image_formats,
            export_formats=args.export_formats
        )
        log_stage_complete(start, "Map Generation")
    else:
        logging.info("Skipping map generation stage (--map not set)")

    # STAGE 5: Process
    if args.process:
        start = log_stage("S-Coda Mean Free Path Estimation")
        process_event_batch(
            data_catalog=str(output_dir / "merged_catalog.xlsx"),
            waveform_dir=str(output_dir / "validated_waveforms"),
            output_dir=str(output_dir / "processed_output")
        )
        log_stage_complete(start, "Processing")
    else:
        logging.info("Skipping processing stage (--process not set)")

    # STAGE 6: Plot
    if args.plot:
        start = log_stage("Plotting")
        plot_all(
            arrival_excel=str(output_dir / "arrival_times.xlsx"),
            validated_waveforms_dir=str(output_dir / "validated_waveforms"),
            coda_waveforms_dir=str(output_dir / "processed_output" / "coda_segments"),
            output_full_dir=str(output_dir / "plots/full_waveforms"),
            output_coda_dir=str(output_dir / "plots/coda_waveforms")
        )
        log_stage_complete(start, "Plotting")
    else:
        logging.info("Skipping plotting stage (--plot not set)")

    logging.info("Pipeline execution complete. All selected stages finished.")
    logging.info(f"Total execution time: {time.time() - pipeline_start:.1f} seconds.")
    logging.info("Exiting pipeline.")

if __name__ == "__main__":
    main()