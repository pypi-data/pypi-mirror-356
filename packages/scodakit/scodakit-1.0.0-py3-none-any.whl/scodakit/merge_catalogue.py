# -*- coding: utf-8 -*-
"""
merge_catalogue.py

This script reads arrival picks from an Excel file and a seismic catalogue (in various formats),
merges them based on origin time, fetches station coordinates from a specified FDSN client,
and computes epicentral and hypocentral distances, as well as S-wave radiated energy.
It then saves the merged data to an Excel file.

"""

import pandas as pd
import numpy as np
import logging
from obspy import read_events, UTCDateTime
from obspy.clients.fdsn import Client
from obspy.geodetics import locations2degrees, degrees2kilometers
from scodakit.download import detect_delimiter

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def prepare_catalog_for_mfp(picks_excel: str, seismic_catalog: str, output_excel: str, client: str = "NOA"):
    """
    Merges arrival picks with catalog metadata and computes distances and energy.

    Parameters:
    - picks_excel: Excel file with P/S picks and Origin time.
    - seismic_catalog: Catalog file (.xml, .csv, .xlsx, etc.).
    - output_excel: Where to save the merged and enhanced dataframe.
    - client: FDSN client to fetch station coordinates. Default is "NOA".
    """
    logging.info(f'Merging arrival times with catalog: {picks_excel} and {seismic_catalog}. Matching by origin time (UTC-agnostic merge)')
    # Load arrival picks
    logging.info(f"Reading arrival picks from {picks_excel}")
    df = pd.read_excel(picks_excel)
    # Ensure required columns exist
    required_columns = ['Origin time','P arrival time', 'S arrival time', 'Network', 'Station']
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        logging.error(f"Missing columns in arrival data: {missing}")
        return

    df['Origin time'] = pd.to_datetime(df['Origin time'])

    # Load seismic catalog
    logging.info(f"Reading seismic catalog from {seismic_catalog}")

    if seismic_catalog.endswith(".xml"):
        events = read_events(seismic_catalog)
        catalog_df = pd.DataFrame([
            {
                'Origin time': e.preferred_origin().time.datetime,
                'Latitude': e.preferred_origin().latitude,
                'Longitude': e.preferred_origin().longitude,
                'Magnitude (ML)': e.preferred_magnitude().mag,
                'Depth (km)': e.preferred_origin().depth / 1000
            } for e in events
        ])
    else:
        if seismic_catalog.endswith((".csv", ".txt")):
            catalog_df = pd.read_csv(seismic_catalog, delimiter=detect_delimiter(seismic_catalog))
        else:
            catalog_df = pd.read_excel(seismic_catalog, engine='openpyxl')

        required = ["Origin Time (GMT)", "Latitude", "Longitude", "Magnitude (ML)", "Depth (km)"]
        for col in required:
            if col not in catalog_df.columns:
                raise ValueError(f"Missing required column: {col}")
        catalog_df['Origin time'] = pd.to_datetime(catalog_df['Origin Time (GMT)'])

    # Normalize datetime format
    df["Origin time"] = pd.to_datetime(df["Origin time"]).dt.tz_localize(None)
    catalog_df["Origin time"] = pd.to_datetime(catalog_df["Origin time"]).dt.tz_localize(None)

    # Sort for merge_asof
    df = df.sort_values("Origin time")
    catalog_df = catalog_df.sort_values("Origin time")

    # Merge using fuzzy timestamp match (±60s tolerance)
    merged = pd.merge_asof(
        df,
        catalog_df,
        on="Origin time",
        tolerance=pd.Timedelta(seconds=60),
        direction="nearest",
        suffixes=('_arrival', '_catalog')
    )
    # print all the dataframes
    logging.info(f"Arrival DataFrame:\n{df.head()}")
    logging.info(f"Catalog DataFrame:\n{catalog_df.head()}")
    logging.info(f"Merged DataFrame:\n{merged.head()}")

    # Fetch station coordinates
    client = Client(client)
    station_coords = {}
    for net, sta in merged[['Network', 'Station']].values: 
        try:
            inv = client.get_stations(network=net, station=sta, level="station", starttime=UTCDateTime(merged['Origin time'].min()))
            station = inv.select(network=net, station=sta)[0][0]
            print(f'station inventory: {inv}')
            station_coords[(net, sta)] = (station.latitude, station.longitude)
            logging.info(f"Fetched coordinates for {net}.{sta}: {station.latitude}, {station.longitude}")
        except Exception as e:
            logging.warning(f"Could not fetch coordinates for {net}.{sta}: {e}")
            station_coords[(net, sta)] = (None, None)
    
    logging.info(f"Station coordinates fetched for {len(station_coords)} stations.")
    logging.info(f"Station coordinates: {station_coords}")     
    
    ## Assign coordinates to merged dataframe
    merged['Station_Latitude'] = merged.apply(
        lambda row: station_coords.get((row['Network'], row['Station']), (None, None))[0],
        axis=1
    )
    merged['Station_Longitude'] = merged.apply(
        lambda row: station_coords.get((row['Network'], row['Station']), (None, None))[1],
        axis=1
    )

    # Epicentral distance (in km)
    merged['Epicentral Distance E (km)'] = merged.apply(
        lambda x: degrees2kilometers(locations2degrees(x['Latitude'], x['Longitude'], x['Station_Latitude'], x['Station_Longitude']))
        if pd.notnull(x['Station_Latitude']) else np.nan,
        axis=1
    )

    # Hypocentral distance
    merged['Hypocentral Distance R (km)'] = np.sqrt(
        merged['Epicentral Distance E (km)']**2 + merged['Depth (km)']**2
    )

    # S-wave Radiated Energy (ergs)
    merged['S Wave Radiated Energy W (erg)'] = 10**(11.8 + 1.5 * merged['Magnitude (ML)'])

    # Save
    merged.to_excel(output_excel, index=False)

    logging.info("{} matched events ({} skipped)".format(len(merged), len(df) - len(merged)))
    logging.info(f"Saved merged catalog to {output_excel}")
