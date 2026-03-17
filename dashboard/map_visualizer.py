from __future__ import annotations

from pathlib import Path
from typing import Any, Sequence

import folium
import pandas as pd
from folium.plugins import HeatMap

DEFAULT_CENTER = [36.0999, -80.2442]
DEFAULT_ZOOM = 13

DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "raw" / "sample_crime_data.csv"


def load_crime_points(csv_path: str | Path = DATA_FILE) -> list[list[float]]:
    df = pd.read_csv(csv_path)

    required = {"latitude", "longitude"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"CSV missing required columns: {sorted(missing)}")

    df["severity"] = df.get("severity", 1).astype(float).fillna(1.0)
    points = df[["latitude", "longitude", "severity"]].astype(float).values.tolist()
    return points


def _coords_to_polyline(coords: Sequence[dict[str, float]]) -> list[tuple[float, float]]:
    return [(float(c["lat"]), float(c["lon"])) for c in coords]


def build_map(
    *,
    center: Sequence[float] | None = None,
    zoom_start: int = DEFAULT_ZOOM,
    crime_points: Sequence[Sequence[float]] | None = None,
    route_coords: Sequence[dict[str, float]] | None = None,
) -> folium.Map:
    if crime_points is None:
        crime_points = load_crime_points(DATA_FILE)

    if center is None:
        if route_coords:
            center = [float(route_coords[0]["lat"]), float(route_coords[0]["lon"])]
        else:
            center = DEFAULT_CENTER

    m = folium.Map(location=list(center), zoom_start=zoom_start)

    if crime_points:
        HeatMap(crime_points, min_opacity=0.2, radius=25, blur=15, max_zoom=1).add_to(m)

    if route_coords:
        line = _coords_to_polyline(route_coords)
        folium.PolyLine(line, weight=6, opacity=0.85).add_to(m)
        folium.Marker(line[0], tooltip="Start", icon=folium.Icon(color="green")).add_to(m)
        folium.Marker(line[-1], tooltip="End", icon=folium.Icon(color="red")).add_to(m)

    return m
