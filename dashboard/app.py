from __future__ import annotations

import os
from typing import Any

import requests
import streamlit as st

from map_visualizer import build_map

DEFAULT_START = {"lat": 36.0999, "lon": -80.2442}
DEFAULT_END = {"lat": 36.1060, "lon": -80.2400}

API_URL = os.getenv("SAFEPATH_API", "http://localhost:8000")

st.set_page_config(page_title="SafePath AI", layout="wide")
st.title("SafePath AI")
st.write("Safer-route demo using synthetic incident data.")

with st.sidebar:
    st.subheader("Route inputs")

    start_lat = st.number_input("Start lat", value=DEFAULT_START["lat"], format="%.6f")
    start_lon = st.number_input("Start lon", value=DEFAULT_START["lon"], format="%.6f")
    end_lat = st.number_input("End lat", value=DEFAULT_END["lat"], format="%.6f")
    end_lon = st.number_input("End lon", value=DEFAULT_END["lon"], format="%.6f")

    st.subheader("Safety tuning")
    alpha = st.slider("alpha (risk weight)", 0.0, 2.0, 0.2, 0.05)
    radius_m = st.slider("risk radius (meters)", 25, 500, 150, 25)

    compute = st.button("Compute safer route", use_container_width=True)

route_coords: list[dict[str, float]] | None = None
summary: dict[str, Any] | None = None

if compute:
    try:
        resp = requests.get(
            f"{API_URL}/route",
            params={
                "start_lat": start_lat,
                "start_lon": start_lon,
                "end_lat": end_lat,
                "end_lon": end_lon,
                "alpha": alpha,
                "radius_m": radius_m,
            },
            timeout=30,
        )
        resp.raise_for_status()
        payload = resp.json()
        route_coords = payload.get("coords")
        summary = payload.get("summary")

    except Exception as exc:
        st.error(f"Route computation failed: {exc}")

m = build_map(route_coords=route_coords)
st.components.v1.html(m._repr_html_(), height=720)

if summary:
    st.subheader("Route summary")
    st.json(summary)
