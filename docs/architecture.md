# Architecture

## Repository layout
- `backend/`: FastAPI service (graph building, routing, risk scoring)
- `dashboard/`: Streamlit UI and map rendering
- `data/raw/`: raw crime dataset (synthetic) + other inputs
- `data/processed/`: generated artifacts (not committed; kept via `.gitkeep`)
- `docs/`: architecture/system flow/API docs
- `notebooks/`: exploratory analysis and sanity checks
- `analytics/`: ML model exploration (clustering/prediction)

## Backend components
- `graph_builder.py`: builds an OSMnx walkable graph for Winston-Salem
- `crime_loader.py`: loads crime records into a GeoDataFrame
- `risk_model.py`: computes node risk and assigns safety weights to edges
- `router.py`: computes a safety-weighted path (NetworkX shortest path)
- `main.py`: FastAPI endpoints (`/`, `/nodes`, `/route`)

## Data pipeline
1. Load raw incident records
2. Attach incidents to nearby graph nodes (radius search)
3. Compute node risk and edge safety weights
4. Route using `safety_weight`
5. Return route nodes and stats (future: route polyline)

## Dashboard
Streamlit renders a Folium map using `map_visualizer.py`.
Current default view is a heatmap; next step is calling the API and overlaying the computed route.
