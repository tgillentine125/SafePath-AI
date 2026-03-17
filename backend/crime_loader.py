import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

def load_crime_data(path: str = "data/raw/sample_crime_data.csv"):
    """Load crime data CSV into a GeoDataFrame.

    Columns expected: timestamp, latitude, longitude, offense, severity
    """
    df = pd.read_csv(path)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["severity"] = df["severity"].astype(float)

    geometry = [Point(xy) for xy in zip(df["longitude"], df["latitude"])]
    gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")
    return gdf
