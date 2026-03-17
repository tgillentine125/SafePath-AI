from fastapi import FastAPI, HTTPException
import osmnx as ox

from graph_builder import build_graph
from router import safe_route


app = FastAPI(title="SafePath AI", version="0.2.0")
G = build_graph()


def _nearest_node(lat: float, lon: float) -> int:
    """Nearest graph node for a lat/lon point."""
    try:
        # osmnx expects lon/x then lat/y
        return int(ox.distance.nearest_nodes(G, X=lon, Y=lat))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Could not find nearest node: {e}")


@app.get("/")
def home():
    return {"project": "SafePath AI", "status": "running"}


@app.get("/nodes")
def nodes():
    return {"nodes": len(G.nodes), "edges": len(G.edges)}


@app.get("/route")
def route(
    start_lat: float,
    start_lon: float,
    end_lat: float,
    end_lon: float,
    alpha: float = 0.2,
    radius_m: float = 150.0,
):
    """Return safety-weighted route between two coordinate points."""
    start_node = _nearest_node(start_lat, start_lon)
    end_node = _nearest_node(end_lat, end_lon)

    route_info = safe_route(G, start_node, end_node, alpha=alpha, radius_m=radius_m)

    return {
        "start": {"lat": start_lat, "lon": start_lon, "node": start_node},
        "end": {"lat": end_lat, "lon": end_lon, "node": end_node},
        **route_info,
    }
