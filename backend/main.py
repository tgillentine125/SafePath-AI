from fastapi import FastAPI, HTTPException
import networkx as nx
import osmnx as ox

from graph_builder import build_graph
from router import safe_route

app = FastAPI()

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
    return {"SafePath AI": "running"}


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
    """Return safe route between two coordinate points."""
    start_node = _nearest_node(start_lat, start_lon)
    end_node = _nearest_node(end_lat, end_lon)

    path = safe_route(G, start_node, end_node, alpha=alpha, radius_m=radius_m)

    total_weight = 0.0
    for u, v in zip(path[:-1], path[1:]):
        edge_data = G.get_edge_data(u, v, 0) or {}
        total_weight += float(edge_data.get("safety_weight", edge_data.get("length", 0.0)))

    return {
        "start_node": start_node,
        "end_node": end_node,
        "path": path,
        "total_safety_weight": total_weight,
        "alpha": alpha,
        "radius_m": radius_m,
    }
