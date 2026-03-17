from __future__ import annotations

from pathlib import Path
from typing import Sequence

import folium
import pandas as pd
from folium.plugins import HeatMap


DEFAULT_CENTER = [36.0999, -80.2442]
DEFAULT_ZOOM = 13


def load_crime_points(csv_path: str | Path) -> list[list[float]]:
    df = pd.read_csv(csv_path)

    required = {"latitude", "longitude"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"CSV missing required columns: {sorted(missing)}")

    df["severity"] = df.get("severity", 1).astype(float).fillna(1.0)

    points: list[list[float]] = []
    for _, row in df.iterrows():
        points.append([float(row["latitude"]), float(row["longitude"]), float(row["severity"])])

    return points


def build_map(
    center: Sequence[float] = DEFAULT_CENTER,
    zoom_start: int = DEFAULT_ZOOM,
    crime_points: Sequence[Sequence[float]] | None = None,
) -> folium.Map:
    m = folium.Map(location=list(center), zoom_start=zoom_start)

    if crime_points:
        HeatMap(crime_points, radius=15, blur=18, max_zoom=1).add_to(m)

    return m
