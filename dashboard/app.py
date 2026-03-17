import streamlit as st
from pathlib import Path

from map_visualizer import load_crime_points, build_map

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "raw" / "sample_crime_data.csv"

st.title("SafePath AI")
st.write("Synthetic crime heatmap + map viewer")

points = load_crime_points(DATA_FILE)
m = build_map(points, map_center=(36.0999, -80.2442), zoom=13, heatmap=True)

st.components.v1.html(m._repr_html_(), height=650)
