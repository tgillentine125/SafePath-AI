# SafePath AI

SafePath AI is a safer-route prototype for Winston-Salem.
It weights walking routes by incident risk (synthetic data in this starter repo).

## Run locally
Install dependencies and start the API (requires internet to pull the OSM walk graph):

```bash
pip install -r requirements.txt
uvicorn backend.main:app --reload
```

Start the dashboard (defaults to `http://localhost:8000` for the API):

```bash
streamlit run dashboard/app.py
```

## Endpoints
- `GET /` health
- `GET /nodes` graph stats
- `GET /route` safer route using risk-weighted edges

Query parameters include start/end lat/lon and tuning knobs like `alpha` and `radius_m`.

## Next steps
Replace the synthetic dataset with real Winston-Salem incident records and validate
that safety-weighted routes reduce incident density compared to the shortest path.
