# -*- coding: utf-8 -*-
"""
map_generator.py

This script reads a catalogue of seismic events and their corresponding stations,
and generates a map visualizing the events and stations. It also exports the data in
various formats (GeoJSON, CSV, Shapefile).
"""
from pathlib import Path
import logging

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature


def load_data(catalogue_path):
    catalogue = pd.read_excel(catalogue_path)

    # Check required columns
    required = ["Latitude", "Longitude", "Magnitude (ML)", "Depth (km)", "Station_Latitude", "Station_Longitude", "Station"]
    for col in required:
        if col not in catalogue.columns:
            raise ValueError(f"Missing required column: {col}")

    # Convert to GeoDataFrames and ensure they have the same index
    catalogue = catalogue.dropna(subset=["Latitude", "Longitude", "Station_Latitude", "Station_Longitude"])
    if catalogue.empty:
        raise ValueError("Catalogue is empty after dropping rows with missing coordinates.")
    logging.info(f"Loaded catalogue with {len(catalogue)} events and {len(catalogue['Station'].unique())} unique stations.")
    # Create GeoDataFrames for events and stations
    # Ensure that the coordinates are in the correct format
    if not all(catalogue[["Latitude", "Longitude", "Station_Latitude", "Station_Longitude"]].apply(pd.to_numeric, errors='coerce').notnull().all()):
        raise ValueError("Coordinates must be numeric.")
    station_cat = catalogue.drop_duplicates(subset=["Station", "Station_Latitude", "Station_Longitude"])
    if station_cat.empty:
        raise ValueError("No unique stations found in the catalogue.")
    # Create GeoDataFrames
    logging.info("Creating GeoDataFrames for events and stations.")
    events_gdf = gpd.GeoDataFrame(
        catalogue,
        geometry=gpd.points_from_xy(catalogue["Longitude"], catalogue["Latitude"]),
        crs="EPSG:4326"
    )
    
    stations_gdf = gpd.GeoDataFrame(
        station_cat,
        geometry=gpd.points_from_xy(station_cat["Station_Longitude"], station_cat["Station_Latitude"]),
        crs="EPSG:4326"
    )

    return events_gdf, stations_gdf

def plot_map(events_gdf, stations_gdf, output_dir, image_formats):
    fig, ax = plt.subplots(figsize=(12, 12), subplot_kw={"projection": ccrs.PlateCarree()})
    ax.set_title("Seismic Events and Stations")

    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS, linestyle=':')
    ax.add_feature(cfeature.LAND, facecolor='whitesmoke')
    ax.gridlines(draw_labels=True)

    stations_gdf.plot(ax=ax, marker="^", color="blue", markersize=60, label="Stations", edgecolor="black", zorder=5)
    events_gdf.plot(ax=ax, marker="o", column="Magnitude (ML)", cmap="Reds", alpha=0.7, legend=True, label="Events", zorder=4)

    # Add labels for stations
    for _, row in stations_gdf.iterrows():
        ax.text(row.geometry.x + 0.05, row.geometry.y + 0.05, row["Station"], fontsize=8, color="blue")

    ax.legend()
    for fmt in image_formats:
        out_path = Path(output_dir) / f"seismic_map.{fmt}"
        plt.savefig(out_path, dpi=300)
        logging.info(f"Saved map to {out_path}")
    plt.close()


def export_data(events_gdf, stations_gdf, output_dir, formats):
    for fmt in formats:
        if fmt == "geojson":
            events_gdf.to_file(Path(output_dir) / "events.geojson", driver="GeoJSON")
            stations_gdf.to_file(Path(output_dir) / "stations.geojson", driver="GeoJSON")
        elif fmt == "csv":
            events_gdf.drop(columns="geometry").to_csv(Path(output_dir) / "events.csv", index=False)
            stations_gdf.drop(columns="geometry").to_csv(Path(output_dir) / "stations.csv", index=False)
        elif fmt == "shp":
            events_gdf.to_file(Path(output_dir) / "events.shp")
            stations_gdf.to_file(Path(output_dir) / "stations.shp")
        logging.info(f"Exported GIS data as {fmt}")


def generate_map(catalogue_path, output_dir, image_formats, export_formats):
    
    # Create output directory if it doesn't exist
    if not Path(output_dir).exists():
        logging.info(f"Creating output directory: {output_dir}")
    else:
        logging.info(f"Output directory already exists: {output_dir}")
    
    # Create the directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    events_gdf, stations_gdf = load_data(catalogue_path)
    plot_map(events_gdf, stations_gdf, output_dir, image_formats)
    export_data(events_gdf, stations_gdf, output_dir, export_formats)