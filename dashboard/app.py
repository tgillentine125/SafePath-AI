import streamlit as st
import folium

st.title("SafePath AI")

m = folium.Map(location=[36.0999,-80.2442], zoom_start=13)

st.components.v1.html(m._repr_html_(), height=600)
