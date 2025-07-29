"""
download.py

Downloads seismic waveforms from a catalog using ObsPy, with flexible station selection
(either by station codes list or radius) and multiple waveform output formats (MSEED, SAC, WAV).

Author: Marios Karagiorgas
"""

from obspy import UTCDateTime, read_events
from obspy.clients.fdsn import Client
from obspy.clients.fdsn.header import URL_MAPPINGS
from obspy.geodetics.base import kilometer2degrees
from pathlib import Path
import logging
import pandas as pd
from typing import List, Union

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def detect_delimiter(filepath):
    """
    Detects the delimiter of a CSV or TXT file by reading the first few lines.
    Args:
        filepath (str): Path to the file.
    Returns:
        str: Detected delimiter (comma or tab).
    """
    try:
        with open(filepath, 'r') as file:
            lines = [file.readline() for _ in range(5)]
        comma_count = sum(line.count(',') for line in lines)
        tab_count = sum(line.count('\t') for line in lines)
        return ',' if comma_count > tab_count else '\t'
    except Exception as e:
        logging.error(f"Error detecting delimiter: {e}")
        return ','

def get_inventory_stations(inv):
    """
    Extracts station codes from an ObsPy inventory object.
    Args:
        inv (obspy.core.inventory.Inventory): ObsPy inventory object.
    Returns:
        List[str]: List of station codes in the format 'NET.STA.CHA'.
    """
    code_list = []
    for net in inv:
        for sta in net:
            for cha in sta:
                code_list.append(f"{net.code}.{sta.code}.{cha.code}")
    return sorted(code_list)

def make_event_folders(events, destination):
    """
    Creates a directory structure for each event based on its date.
    Args:
        events (list): List of event times (UTCDateTime).
        destination (str): Base directory for event folders.
    Returns:
        dict: Dictionary mapping event times to their respective directory paths.
    """
    destination = Path(destination)
    path_dict = {}
    for event in events:
        event_dir = destination / str(event.year)
        event_dir.mkdir(parents=True, exist_ok=True)
        path_dict[str(event)] = event_dir
    return path_dict

def write_waveform(wf, out_path, output_format):
    """
    Writes the waveform to a file in the specified format.
    Args:
        wf (obspy.core.stream.Stream): ObsPy Stream object.
        out_path (str): Output file path.
        output_format (str): Desired output format (MSEED, SAC, WAV).
    """
    try:
        if output_format in ["SAC", "WAV"]:
            wf.remove_response(output="VEL", water_level=60, zero_mean=True, taper=True, taper_fraction=0.05)
            wf.merge()
        else:
            wf.remove_response(output="VEL", water_level=60, zero_mean=True, taper=True, taper_fraction=0.05)
        wf.write(str(out_path), format=output_format)
        logging.info(f"Saved waveform to {out_path}")
    except Exception as e:
        logging.warning(f"Failed to save waveform {out_path.name}: {e}")

def download_waveforms(
    catalogue_path: Union[str, Path], # Path to the catalogue file. Can be XML, CSV, TXT, XLSX. 
    station_list: Union[str, List[str], None], # List of station codes in the format 'NET.STA.CHA' or None. If None, stations will be selected based on radius. If a string provided, it will be treated as a single station code.
    destination: Union[str, Path], # Directory to save the downloaded waveforms.
    radius: float = None, # Radius in kilometers to search for stations. If None, station_list will be used.
    channels: str = "*", # Channel codes to download. Default is all channels.
    start_offset: int = -30, # Start time offset in seconds before the event time.
    end_offset: int = 150, # End time offset in seconds after the event time.
    output_format: str = "MSEED", # Output format for the waveforms. Can be 'MSEED', 'SAC', or 'WAV'.
    node: str = "NOA", # FDSN node to use for downloading waveforms. Available nodes can be found in obspy.clients.fdsn.header.URL_MAPPINGS.
    network_filter: List[str] = ["HL"] # List of network codes to filter the stations. Default is ['HL']. 
):
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=True)
    client = Client(node)

    if not Path(catalogue_path).exists():
        raise FileNotFoundError(f"Catalogue path does not exist: {catalogue_path}")

    valid_formats = ["MSEED", "SAC", "WAV"]
    if output_format not in valid_formats:
        raise ValueError(f"Invalid output format: {output_format}")

    if node not in sorted(URL_MAPPINGS.keys()):
        raise ValueError(f"Invalid node: {node}")

    logging.info(f"Reading seismic events from catalogue: {catalogue_path}")

    if str(catalogue_path).endswith(".xml"):
        evs = read_events(str(catalogue_path))
        events = [e.preferred_origin().time for e in evs]
        lat_list = [e.preferred_origin().latitude for e in evs]
        lon_list = [e.preferred_origin().longitude for e in evs]

    elif str(catalogue_path).endswith((".csv", ".txt", ".xls", ".xlsx")):
        if str(catalogue_path).endswith((".csv", ".txt")):
            df = pd.read_csv(catalogue_path, delimiter=detect_delimiter(catalogue_path))
        else:
            df = pd.read_excel(catalogue_path, engine='openpyxl')

        required_columns = ["Origin Time (GMT)", "Latitude", "Longitude"]
        for col in required_columns:
            if col not in df.columns:
                raise ValueError(f"Missing required column: {col}")

        df["Origin Time (GMT)"] = pd.to_datetime(df["Origin Time (GMT)"])
        df["Origin Time (GMT)"] = df["Origin Time (GMT)"].apply(lambda x: UTCDateTime(x))
        events = df["Origin Time (GMT)"].tolist()
        lat_list = df["Latitude"].tolist()
        lon_list = df["Longitude"].tolist()
    else:
        raise ValueError("Unsupported catalogue format.")

    path_dict = make_event_folders(events, destination)

    logging.info(f'Number of seismic events: {len(events)}')
    logging.info(f'Station list: {station_list if station_list else "Dynamic based on radius"}')
    
    
    for i, event in enumerate(events):
        logging.info(f"Processing event {i}/{len(events)}: {event}")

        if station_list is not None and radius is None:
            station_codes = station_list if isinstance(station_list, list) else [station_list]
        elif station_list is None and radius is not None:
            try:
                inv = client.get_stations(
                    network= network_filter, latitude=lat_list[i], longitude=lon_list[i],
                    maxradius=kilometer2degrees(radius),  # Convert km to degrees
                    level='response', starttime=event - 1, endtime=event
                )
                station_codes = get_inventory_stations(inv)
            except Exception as e:
                logging.warning(f"Failed to retrieve stations: {e}")
                continue
        else:
            raise ValueError("Specify either station_list or radius, not both or neither.")

        for code in station_codes:
            try:
                if "." in code:
                    net, sta = code.split(".")[:2]
                else:
                    sta = code
                    # Attempt to fetch the network dynamically (try all available if needed)
                    try:
                        inv = client.get_stations(station=sta, level="station", starttime=event - 1, endtime=event)
                        net = inv[0].code
                    except Exception as e:
                        logging.warning(f"Could not fetch network for station {sta}: {e}")
                        continue
                
                logging.info(f"Downloading waveform for {code} at {event}")
                wf = client.get_waveforms(
                    network=net, station=sta, channel=channels, location="*",
                    starttime=event + start_offset, endtime=event + end_offset,
                    attach_response=True
                )
                wf.detrend("linear")
                wf.detrend("demean")
                out_file = path_dict[str(event)] / f"{event.strftime('%Y%m%dT%H%M%S')}_{net}_{sta}.{output_format.lower()}"
                write_waveform(wf, out_file, output_format)
                logging.info(f"Waveform saved to {out_file}")
            except Exception as e:
                logging.warning(f"Failed to download for {code} at {event}: {e}")