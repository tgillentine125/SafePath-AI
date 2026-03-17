# System Flow

## Runtime flow (route request)
1. **Build/load graph**: `graph_builder.build_graph()` creates an OSMnx walkable graph for Winston-Salem.
2. **Load incidents**: `crime_loader.load_crime_data()` reads raw incident records (CSV -> GeoDataFrame).
3. **Risk scoring**:
   - `risk_model.compute_node_risk()` aggregates incident severity within `radius_m` meters of each node.
   - `risk_model.add_safety_weights()` writes `safety_weight` onto each edge: `length + alpha * edge_risk`.
4. **Route computation**:
   - `router.safe_route()` runs NetworkX shortest path using `weight="safety_weight"`.
   - API returns route node sequence and request parameters.

## Deployment flow (local dev)
1. Install dependencies: `pip install -r requirements.txt`
2. Start API: `uvicorn backend.main:app --reload`
3. Start dashboard: `streamlit run dashboard/app.py`
4. Dashboard calls API, renders heatmap + route overlay (future).

## Error handling checklist
- Missing graph build: OSMnx network download may fail due to network restrictions.
- Empty incident file: risk scores default to near zero, making routing close to shortest path.
- Coordinate input: start/end lat/lon must be within the graph bounding box.
